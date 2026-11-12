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

# Versão 2: melhorias de saldo de energia (atual)

A v1 está congelada em `blocos_v1/` (os testbenches de `01_coldstart/` … `05_sistema/` usam a v1). A versão atual fica em `blocos/`, e todas as figuras das pastas de módulo são da v2.

| # | Mudança | Onde |
|---|---|---|
| A | **Detector de escuro**: sem luz (VIN_DC < ~0,37 V), VDD desliga e o oscilador para | `coldstart.spice` (XPD, XLD, XKD1, XKD2; novo pino VIN_DC) |
| B | **Diodo Schottky externo** (~0,37 V) no lugar do p+/n-well integrado (~0,77 V) | `boost.spice` (`schottky_ext`), fora do chip |
| C | **Divisor de 100 MΩ** (era 20 MΩ), com 10 pF externos em T_U e T_D | só nos testbenches (componentes externos) |
| D | **VDD 2,2 → 1,8 V** (diodos da pilha com W = 6 µm) e seguidor nativo com L = 4 µm | `coldstart.spice` |
| E | **Metade da frequência** (101 → 52,7 kHz), com t_on = 751 ns para manter R_in | `oscilador.spice` (nativo do anel com L = 2 µm, Cr e Cd) |

### Resultado: corrente líquida na bateria (3,7 V), sistema completo

Medida com a carga integrada pelo próprio simulador (`sim/figs/tb/balanco_*.spice`); valor positivo = carregando.

| Condição | v1 | v2 |
|---|---|---|
| Luz cheia (Iph 50 µA) | +4,80 µA | **+6,03 µA** |
| Meia luz (25 µA) | −0,06 µA | **+0,62 µA** |
| Pouca luz (10 µA) | −0,94 µA | **+0,13 µA** (modo burst) |
| Escuro | −0,94 µA | **−0,14 µA** |
| **Dia: 8 h de luz cheia + 16 h de escuro** | **+23 µAh** | **+46 µAh (2×)** |
| Dia: 8 h de meia luz + 16 h de escuro | −15 µAh | +3 µAh |

Outros números da v2:
- **Boost:** η 72 → 81% (79% descontando o oscilador já referido à bateria).
- **Oscilador:** 0,54 → 0,13 µA.
- **Cold-Start:** consumo com bateria cheia (0-1) de 0,9 µA → 39 nA; no escuro, 32 nA.

### Achados durante a v2
1. **Aumentar só o capacitor do anel quase não reduz o consumo do oscilador:** as bordas ficam mais lentas e o crowbar por ciclo aumenta na mesma proporção. O que funcionou foi reduzir a corrente dos nativos que limitam os inversores (L = 2 µm), o que baixa f e o crowbar juntos.
2. **A primeira versão do detector de escuro** (um NMOS em série com o bias) deixava VDD em ~0,7 V no escuro. A pilha de diodos segura tensão por fuga, então foi preciso puxar VG e VDD a 0 explicitamente.
3. **O pull-down de VDD no escuro drenava ~0,7 µA** pelo seguidor nativo com Vgs = 0. Resolvido com L = 4 µm no XMF, o que também corrigiu a fuga do estado 0-1.
4. **Com o divisor de 100 MΩ, a saída do comparador se acopla nos taps** (impedância de MΩ) e o disparo trepida por ~30 µs. A correção são 10 pF externos em T_U e T_D (na prática a capacitância da placa já ajuda).
5. **Medição do balanço:** médias de corrente pulsada **não** podem ser feitas sobre a saída interpolada (`.option interp`). Isso subestimava a carga em ~2×. A medição correta usa a integral da corrente calculada pelo simulador.

### Ainda em aberto (v2)
- **Detector de escuro sem histerese:** com pouca luz ele funciona em *burst*, mas VDD só chega a ~1,15 V nos pulsos. Uma histerese pequena (por exemplo, realimentação de VDD para `dk`) deixaria os pulsos limpos.
- **R_in com meia luz:** o ponto de operação fica preso no limiar do detector (~0,36 V). Um R_in um pouco maior (t_on menor) favorece meia luz, com perda pequena em luz cheia.
- **Fuga do Schottky real:** confira a fuga a 4,2 V no componente escolhido; ela descarrega a bateria a noite toda.
- Corners (ss/ff), temperatura e Monte Carlo; calibração do limiar de 4,2 V (pelos resistores externos).

---

# Versão 1: prova de conceito das arquiteturas (SKY130, tt, 27 °C)

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

- **Diodo p+/n-well:** cai cerca de 0,77 V, o que custa uns 15% de eficiência. O modelo SPICE também não inclui o PNP parasita para o substrato. *(Resolvido na v2: Schottky externo.)*
- Corners (ss/ff), temperatura e Monte Carlo no PDK definitivo.
- Com luz fraca, o R_in fixo se afasta do MPP (η ≈ 55% com metade da luz).
- **Fuga no estado 0-1 (VDD desligado):** o seguidor nativo XMF conduz ~0,9 µA com Vgs = 0 através do pull-down XK3/XK4. São ~4 µW perdidos enquanto a carga está parada. *(Resolvido na v2: XMF com L = 4 µm; agora 39 nA.)*
- **CLK flutua em ~0,4 V depois que VDD é cortado:** fica abaixo do Vth da chave, que permanece aberta, mas o requisito pede 0 V. Um pull-down fraco no CLK (por exemplo, um nativo com Vgs = 0 ou um resistor alto) resolve.
- A referência de 2 transistores consome ~14 pA (não ~5 pA como eu tinha anotado; esse valor era da geometria inicial).

Os esquemáticos e gráficos de cada módulo estão nas pastas `1_cold_start` … `6_boost` e `integração`, na raiz do projeto. Para gerá-los de novo: `sim/figs/tb/*.spice` (simulações) → `python graficos.py` e `python esq_*.py` (em `sim/figs`).
