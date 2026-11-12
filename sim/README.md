# Ambiente de simulação (gratuito)

| Ferramenta | Versão | Local |
|---|---|---|
| ngspice (simulador SPICE) | 47 | `C:\Users\caean\EDA\Spice64\bin\` (`ngspice.exe` com GUI, `ngspice_con.exe` para modo batch) |
| PDK SkyWater SKY130 (130 nm) | volare c6d73a3 | `C:\Users\caean\EDA\pdk\sky130A\` (`PDK_ROOT` aponta para `C:\Users\caean\EDA\pdk`) |
| Qucs-S (esquemático gráfico → ngspice) | 26.1.1 | `C:\Users\caean\EDA\qucs-s\bin\qucs-s.exe` |
| Manual do ngspice | 47 | `C:\Users\caean\EDA\downloads\ngspice-47-manual.pdf` |

## Como usar o PDK num netlist

```spice
.lib "C:/Users/caean/EDA/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice" tt
```

Corners disponíveis: `tt ss ff sf fs` (e `ll hh hl lh`). Os dispositivos são subcircuitos (instância `X...`), com W e L em µm:

```spice
XN1 d g s b sky130_fd_pr__nfet_g5v0d10v5 W=10 L=1 nf=1   * NMOS 5 V (óxido espesso), para nós em VBAT/VSTOR
XP1 d g s b sky130_fd_pr__pfet_g5v0d10v5 W=10 L=1 nf=1   * PMOS 5 V
XN2 d g s b sky130_fd_pr__nfet_01v8      W=1  L=0.15     * NMOS 1,8 V (núcleo)
XP2 d g s b sky130_fd_pr__pfet_01v8      W=1  L=0.15     * PMOS 1,8 V
```

Outros úteis: `nfet_01v8_lvt`, `pfet_01v8_hvt`, `nfet_05v0_nvt` (nativo, Vth ≈ 0), diodos `diode_pw2nd_05v5`, resistores `res_xhigh_po_*`, capacitores `cap_mim_m3_1`.

Cada pasta de simulação precisa de um `.spiceinit` (copie o desta pasta), que ativa a compatibilidade com os modelos SKY130.

## Rodar

```
cd sim\teste_pdk
ngspice_con -b teste_mos.spice     (batch, imprime os .meas)
ngspice teste_mos.spice            (interativo, permite plot)
```

A primeira execução leva cerca de 20 s, porque o PDK é grande.

## Qucs-S

Em *File → Application settings / Simulators*, aponte o ngspice para `C:\Users\caean\EDA\Spice64\bin\ngspice_con.exe`. Para usar os transistores SKY130, coloque um bloco *SPICE library* (`.LIB`) com o caminho acima e use componentes *SPICE subcircuit* com os nomes dos dispositivos.

---

# Prova de conceito das arquiteturas (SKY130, tt, 27 °C)

Os subcircuitos ficam em `blocos/`, e cada pasta numerada tem o testbench do seu bloco. Para os nós em VBAT/VSTOR/VDD foram usados só os dispositivos de 5 V (`g5v0d10v5`) e o NMOS nativo `nfet_05v0_nvt`.

Premissas provisórias: VDD ≈ 2,2 V, f ≈ 100 kHz, limiares 4,2/4,1 V e 3,0/3,1 V, célula com Voc = 0,8 V e Isc = 50 µA (MPP de 0,675 V e 29,7 µW), L = 220 µH, TRIGGER = 3,3 V.

| Bloco | Arquitetura | Resultado |
|---|---|---|
| Referência (`referencia.spice`) | 2 transistores (Seok 2012): nativo com Vgs = 0 alimentando um NMOS ligado como diodo | VREF = 133 mV, ±1 mV de 0 a 60 °C, 0,4 mV/V, ~14 pA |
| Comparador (`comparador.spice`) | Bias por nativo com Vgs = 0 (~12 nA, sem referência), OTA com par PMOS (n-well na cauda), 2º estágio fonte-comum e Schmitt trigger com corrente limitada | Offset ~1 mV, saída de 0 a VBAT |
| Threshold Control (`threshold_ctrl.spice`) | Ref. + 2 comparadores + 2 NMOS de histerese entre pinos | Disparos em 4,24/4,11 V e 2,96/3,12 V; 160 nA com o divisor de 20 MΩ |
| Cold-Start (`coldstart.spice`) | PMOS do TRIGGER (gate = CTRL_LOW) com diodo série, PMOS do VBAT, pilha de 3 diodos NMOS alimentada por nA espelhada, seguidor nativo, 2 pares NMOS de desligamento | VDD = 2,2 V (±20 mV de 2,9 a 4,4 V); os 4 estados da tabela conferidos; ~20 nA próprios |
| Oscilador (`oscilador.spice`) | Anel de 5 inversores com corrente limitada por nativo (Vgs = 0), detector de borda (atraso + NAND) e buffers | 101 kHz, pulso t_on = 534 ns, 1,2 µW com a chave de carga |
| Boost (`boost.spice`) | Chave NMOS de 200 µm + diodo p+/n-well, em DCM com f e t_on fixos → R_in = 2L/(t_on²·f)·(1 − V_in/V_out) ≈ 13 kΩ ≈ R_mpp | 94 a 99% do MPP extraído, η ≈ 72% (67% incluindo o oscilador) |
| Sistema (`chip.spice`, `05_sistema/`) | Tudo interligado, com a bateria trocada por 0,1 µF | A: carrega até 4,22 V e para (VDD e CLK a 0). B: parte do TRIGGER a 2,9 V e passa para o VBAT em 3,1 V |

## Divisor externo (pendência 1)

```
T_R(VBAT) ─R1─ T_DH ─Rhd─ T_D ─R2─ T_U ─Rhu─ T_UH ─R3─ GND
                 └─NMOS_L─┘          └─NMOS_H─┘
```

Cada NMOS conduz com a saída inativa (gate ligado direto em CTRL_x) e abre quando o comparador dispara, inserindo o resistor de histerese. Os valores estão em `03_comparador/tb_threshold.spice`: S = 20 MΩ, R3 ≈ 636 kΩ, R2 ≈ 254 kΩ, Rhd ≈ 667 kΩ, Rhu ≈ 16 kΩ.

## Problemas encontrados e corrigidos (vale lembrar no Virtuoso)

1. **Efeito de corpo no par PMOS do comparador:** com o n-well em VBAT, o comparador só funcionava perto de 3,5 V. O n-well foi ligado na cauda.
2. **Saída do OTA vai só até cerca de 1 V:** não aciona um inversor alimentado por VBAT. Foi incluído um 2º estágio fonte-comum.
3. **Nativo com fonte fora do terra:** com o efeito de corpo, a corrente cai de nA para pA. Fontes de bias nativas ficam sempre com a fonte no GND, com espelho PMOS quando necessário.
4. **Inversor do Cold-Start alimentado por VBAT:** com a bateria morta, o TRIGGER injetava 22 mA nela. Os inversores passaram a ser alimentados por VS e o n-well da chave foi ligado em VS.
5. **TRIGGER ausente (0 V) com LOW ativo na partida:** a bateria descarregava para o pino. Foi incluído um diodo série no TRIGGER.
6. **VDD flutuando em ~0,7 V quando desligado:** foi incluído um par NMOS de pull-down.
7. **Crowbar no estágio de saída perto do limiar:** empatava com a corrente de carga e o sistema "estacionava" no limiar. A solução foi o Schmitt trigger com corrente limitada a nA.
8. **Partida do VREF:** como só pA carregam o capacitor, ele leva alguns ms para estabilizar. Por isso Cref ficou pequeno (0,1 pF), e nesse intervalo o estado é seguro (não carrega).

## Ainda em aberto

- **Diodo p+/n-well:** cai cerca de 0,77 V, o que custa uns 15% de eficiência. O modelo SPICE também não inclui o PNP parasita para o substrato. Um Schottky externo é a alternativa simples.
- Corners (ss/ff), temperatura e Monte Carlo no PDK definitivo.
- Com luz fraca, o R_in fixo se afasta do MPP (η ≈ 55% com metade da luz).
- **Fuga no estado 0-1 (VDD desligado):** o seguidor nativo XMF conduz ~0,9 µA com Vgs = 0 através do pull-down XK3/XK4. São ~4 µW perdidos enquanto a carga está parada. Opções: XMF com L maior, um NMOS comum no lugar do nativo, ou uma chave em série no dreno de XMF.
- **CLK flutua em ~0,4 V depois que VDD é cortado:** fica abaixo do Vth da chave, que permanece aberta, mas o requisito pede 0 V. Um pull-down fraco no CLK (por exemplo, um nativo com Vgs = 0 ou um resistor alto) resolve.
- A referência de 2 transistores consome ~14 pA (não ~5 pA como eu tinha anotado; esse valor era da geometria inicial).

Os esquemáticos e gráficos de cada módulo estão nas pastas `1_cold_start` … `6_boost` e `integração`, na raiz do projeto. Para gerá-los de novo: `sim/figs/tb/*.spice` (simulações) → `python graficos.py` e `python esq_*.py` (em `sim/figs`).
