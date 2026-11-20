# Validação do Cold-Start, bloco a bloco e do módulo inteiro

Este guia diz como testar cada bloco do `esquematico_blocos.png` no Virtuoso, o que plotar e qual resultado esperar. Os gráficos desta pasta são o "gabarito": foram simulados em ngspice com o PDK SKY130, testando cada bloco sozinho e com as mesmas fontes ideais descritas abaixo.

> **Atenção: os números vêm do SKY130.** No PDK do Virtuoso, as tensões de limiar e as correntes de fuga são outras, então os valores absolutos vão mudar, principalmente as correntes em nA, que dependem exponencialmente do Vth.
>
> O que deve se manter é o **comportamento**: a forma das curvas, quem conduz em cada estado e as relações (por exemplo, VDD = VG − Vgs). A coluna "aceitável" das tabelas dá uma faixa razoável. Se o seu resultado sair dela, ajuste W/L (dicas no fim) antes de seguir para o próximo bloco.

## Ordem recomendada

Teste na ordem **C → D → E → A → B → F → G**, depois o módulo:

1. **C, D e E** formam o regulador (corrente de nA → pilha → seguidor). Se eles funcionarem, VDD já existe.
2. **A e B** escolhem de onde vem VS.
3. **F e G** só desligam o regulador.

## Como montar cada testbench

- Crie uma célula `tb_<bloco>` (por exemplo `tb_cs_bias_na`) com um símbolo do bloco. Ligue cada pino a uma fonte da `analogLib`:
  - `vdc`: fonte de tensão;
  - `idc`: fonte de corrente;
  - `vcvs`: fonte controlada (usada no bloco B);
  - `vpwl`: fonte por trechos, para os transitórios;
  - `res` e `cap`: cargas.
- **GND:** use o `gnd` da `analogLib`. Todo NMOS tem o corpo em GND e todo PMOS tem o corpo em VS, exceto quando o bloco diz o contrário.
- **Varreduras:**
  - DC: varre o parâmetro `dc` de uma fonte. Ponha uma variável de projeto (ex.: `VS`) no campo da fonte e varra a variável na análise DC.
  - Temperatura: análise DC com *Sweep Variable = Temperature*.
  - Várias curvas: *Parametric Analysis*, ou uma variável com lista de valores no ADE Explorer.
- **Correntes:** no *Direct Plot*, clique no terminal da fonte. No Spectre, a corrente é positiva **entrando** no terminal +, então a corrente que uma fonte *fornece* aparece com sinal negativo. Os gráficos daqui mostram o módulo.
- **Eixo em escala log:** nos gráficos de nA, use eixo Y em log (*Axis → Log*).

---

## A. `cs_inv_ctrl`: inversores de controle → `A_inversores.png`

| Pino | Fonte |
|---|---|
| VS | `vdc` = 3,7 V (paramétrico: 2,0 / 3,3 / 3,7 / 4,3 V) |
| CTRL_LOW e CTRL_HIGH | a mesma `vdc`, varrida de 0 a VS |
| nlow, nhigh | abertos (só observar) |

**Análise:** DC sweep da entrada. Plotar `nlow`, `nhigh` e a corrente de VS (em log).

| Medida | Esperado (SKY130) | Aceitável |
|---|---|---|
| nlow com entrada = 0 / = VS | VS / 0 V | erro < 10 mV |
| Ponto de chaveamento Vm (VS = 3,7 V) | 1,53 V (≈ 0,4·VS) | 1,2–2,2 V |
| Corrente de VS com entrada em 0 ou VS | ~8 pA | < 1 nA |
| Pico de corrente na transição (VS = 3,7 V) | ~52 µA | qualquer, desde que seja só na transição |
| nlow e nhigh | idênticas | idênticas |

## B. `cs_sel_fonte`: seleção de fonte → `B_selecao_de_fonte.png`

Aqui `nlow` viria do bloco A. No teste isolado, ela é imposta:
- `nlow = 0` nos casos em que CTRL_LOW está alto;
- `nlow = VS`, com uma `vcvs` de ganho 1 ligada entre VS e GND, nos casos com CTRL_LOW = 0.

Carga: `res` de 15 MΩ de VS a GND, que equivale ao consumo do chip.

| Caso | TRIGGER | VBAT | CTRL_LOW | nlow | Varre |
|---|---|---|---|---|---|
| B1 normal | 0 V | varre 0–4,5 V | = VBAT | 0 | VBAT |
| B2 LOW ativo | 3,3 V | varre 0–4,5 V | 0 | `vcvs` = VS | VBAT |
| B3 bateria morta | varre 0–4,5 V | 0 V | 0 | `vcvs` = VS | TRIGGER |

**Plotar:** VS, I(VBAT) e I(TRIGGER).

| Medida | Esperado | Aceitável |
|---|---|---|
| B1: VS − VBAT (VBAT de 2,9 a 4,3 V) | ~0 V | queda < 10 mV |
| B1: I(TRIGGER) | 0 | < 1 nA: o diodo DTR impede o retorno |
| B2: VS com VBAT < 3 V | 2,74 V (= 3,3 − Vdiodo) | 2,5–2,9 V |
| B2: I(VBAT) com VBAT < 3 V | 0 | < 1 nA |
| B2: VBAT > ~3,3 V | VS = VBAT − 0,57 V (diodo de corpo do XSB) | é esperado, não é defeito |
| B3: VS | TRIGGER − 0,56 V | queda 0,4–0,7 V |

## C. `cs_bias_na`: fonte de nA + espelho → `C_fonte_nA_espelho.png`

| Pino | Fonte |
|---|---|
| VS | `vdc` 3,7 V (varrida no 1º teste) |
| VG | `vdc` 1,0 V no 1º teste; varrida de 0 a 3,7 V no 2º |
| dk | `vdc` 0,3 V no 1º teste; varrida de 0 a 3,7 V no 2º |

> Por que VG = 1 V e não 2,28 V no teste ×VS? Se VG ficar acima de VS, o diodo dreno–poço do XPM conduz e a fonte ideal injeta mA no circuito. É um artefato do teste, e no circuito real isso não acontece.

**Análises:**
- DC de VS (0–4,5 V);
- DC de VG e de dk (compliance);
- DC de temperatura (−20 a 85 °C).

**Plotar:** a corrente que entra nas fontes de VG e dk e a corrente de VS.

| Medida (VS = 3,7 V, 27 °C) | Esperado | Aceitável |
|---|---|---|
| I(XPM) → VG | 10,5 nA (com VG = 2,28 V) | 3–40 nA |
| I(XPD) → dk | 5,8 nA (dk = 0,3 V) | 0,3 a 0,8 × I(XPM) |
| I(VS) total (ramo XMB + XPM + XPD) | ~27 nA | < 100 nA |
| Variação de I(XPM) com VS de 2,5 a 4,5 V | +12 % | < 30 % |
| Compliance: I(XPM) de VG = 0 a 3,3 V | 11,5 → 9,9 nA | variação < 15 % |
| I × temperatura | ~1 nA (−20 °C) → ~70 nA (85 °C), exponencial | só a forma importa |

> **Correção:** a versão anterior do `esquematico_blocos.png` dizia "~4 nA para a pilha" e "~1 nA para o detector". Os valores simulados são **~10 nA** e **~6 nA**, e a figura já foi corrigida.

## D. `cs_ref_pilha`: pilha de 3 diodos → `D_pilha_de_diodos.png`

**Teste 1, curva I–V:** `vdc` em VG varrida de 0 a 3,2 V. Plotar a corrente da fonte em log.

**Teste 2:** `idc` injetando 3, 10 e 30 nA em VG (paramétrico) + DC de temperatura. Plotar V(VG).

| Medida | Esperado | Aceitável |
|---|---|---|
| VG com 10,5 nA | 2,28 V | 1,9–2,7 V |
| Inclinação em sublimiar | ~0,48 V por década (3 diodos, com efeito de corpo nos dois de cima) | 0,3–0,6 V/déc |
| VG × T com corrente fixa | ≈ −8 mV/°C | negativo, de −5 a −10 mV/°C |

> No módulo, a corrente do bloco C sobe com T e compensa a queda da pilha: VG fica plano em 2,27–2,28 V de −20 a 85 °C (veja `modulo_1_dc.png`).

## E. `cs_seguidor`: seguidor nativo → `E_seguidor.png`

| Pino | Fonte |
|---|---|
| VS | `vdc` 3,7 V |
| VG | `vdc`, varrida de 0 a 3,2 V (ou fixa em 2,25 V) |
| VDD | `idc` de carga para GND: 10 nA / 0,15 µA / 2 µA |

**Testes:**
1. DC de VG com as 3 cargas.
2. DC da carga de 10 nA a 20 µA, com VG = 2,25 V.
3. Fuga: VG = 0 e VDD = 0 (duas `vdc`). Varrer VS e a temperatura e medir a corrente de VS.

| Medida | Esperado | Aceitável |
|---|---|---|
| VDD com VG = 2,28 V e 0,15 µA | 1,84 V | VG − (0,2 a 0,7 V) |
| Inclinação dVDD/dVG | ~0,87 | 0,8–1,0 |
| Regulação de carga | ~70 mV/década; 1,82 → 1,68 V de 0,15 a 5 µA | VDD > 1,6 V até 5 µA |
| Fuga com Vgs = 0 (27 °C) | ~10 nA | < 50 nA |
| Fuga a 85 °C | ~70 nA | só a forma importa |

> Se o seu PDK **não tiver NMOS nativo**, o seguidor com NMOS comum perde ~0,5–0,7 V a mais. Nesse caso, aumente a pilha D para 4 diodos ou use diodos menores.

## F. `cs_desliga`: desligamento no estado 0-1 → `F_desligamento.png`

| Pino | Fonte |
|---|---|
| VG | `vdc` 2,25 V |
| VDD | `vdc` 1,8 V |
| CTRL_LOW | `vdc` 0 ou 3,7 V (paramétrico) |
| nhigh | `vdc`, varrida de 0 a 3,7 V |

**Plotar:** a corrente puxada das fontes de VG e VDD (em log).

| CTRL_LOW | nhigh | Esperado | Aceitável |
|---|---|---|---|
| 0 | 0 | ~3 pA | < 1 nA |
| 0 | 3,7 V | ~5 pA | < 1 nA |
| 3,7 V | 0 | ~10 pA | < 1 nA |
| 3,7 V | 3,7 V | **~270 µA** | > 10 µA, várias décadas acima dos ~10 nA do bloco C |

> A curva × nhigh cruza os 10,5 nA do bloco C perto de nhigh ≈ 0,5 V. Acima disso, o desligamento vence o espelho.

## G. `cs_det_escuro`: detector de escuro → `G_detector_de_escuro.png`

**Teste isolado:**

| Pino | Fonte |
|---|---|
| dk | `vdc` 0,5 V |
| VG | `vdc` 2,25 V |
| VDD | `vdc` 1,8 V |
| VIN_DC | `vdc`, varrida de 0 a 0,8 V |

1. Plotar a corrente da fonte de dk, que é I(XLD), × VIN_DC.
2. Com VIN_DC = 0, varrer dk de 0 a 3,7 V e plotar as correntes puxadas de VG e VDD (XKD1 e XKD2).

**Teste C + G:** instancie `cs_bias_na` e `cs_det_escuro` juntos, ligados por dk (VS = 3,7 V, VG = 2,25 V, VDD = 1,8 V). Varrer VIN_DC a −20, 27 e 85 °C e plotar V(dk).

| Medida | Esperado | Aceitável |
|---|---|---|
| I(XLD) × VIN_DC | reta em log, ~125 mV/década | — |
| Cruzamento de I(XLD) com I(XPD) ≈ 5,8 nA | VIN_DC ≈ 0,37 V | 0,30–0,45 V |
| XKD1/XKD2 com dk ≈ 0 (luz) | ~5 pA | < 0,1 nA |
| XKD1/XKD2 com dk = 3,7 V (escuro) | ~400 µA | > 10 µA |
| C + G: dk no escuro / com luz | 3,7 V / ~1 mV | VS / < 50 mV |
| C + G: limiar (dk = 1 V) a −20 / 27 / 85 °C | 0,39 / 0,35 / 0,28 V | 0,25–0,45 V |

---

## Módulo inteiro: `cold_start` com os 7 blocos

Crie `tb_cold_start` com o símbolo do topo. A carga do oscilador é uma `idc` de 0,15 µA em VDD (testes DC), ou 15 MΩ ∥ 10 pF (transitórios).

> **Teste de sanidade:** o netlist hierárquico desta validação (`sim/blocos/coldstart_blocos.spice`) dá o mesmo VDD que o netlist plano original. A diferença máxima é de 4·10⁻¹¹ V. Se o seu módulo divergir dos blocos testados um a um, procure um fio trocado entre blocos, não um problema de dimensionamento.

### M1. DC (`modulo_1_dc.png`)

| Teste | Condição | Esperado | Aceitável |
|---|---|---|---|
| Linha | estado 0-0 (CTRL_LOW = CTRL_HIGH = VBAT), VIN_DC = 0,6 V, varre VBAT 0–4,5 V | VDD = 1,83–1,85 V de 2,9 a 4,3 V | variação < 50 mV |
| Consumo próprio | idem, VBAT = 3,7 V | I(VBAT) = 177 nA (150 da carga + 27 próprios) | próprio < 100 nA |
| Partida a frio DC | VBAT = 0, CTRL_LOW = CTRL_HIGH = 0, varre TRIGGER | VDD > 1,6 V a partir de TRIGGER = 2,57 V; 1,83 V com 3,3 V | VDD > 1,6 V com TRIGGER = 3,3 V |
| Carga | VBAT = 3,7 V, varre a carga de 10 nA a 20 µA | 1,84 V com 0,13 µA; > 1,65 V até ~10 µA | > 1,6 V com 1 µA |
| Temperatura | VBAT = 3,7 V, −20 a 85 °C | VDD de 1,78 a 1,88 V; VG quase plano | VDD entre 1,6 e 2,0 V |

### M2. Luz/escuro (`modulo_2_luz_escuro.png`)

Estado 0-0, VBAT = 3,7 V, varrer VIN_DC de 0 a 0,8 V. Plotar VDD, V(dk) (nó interno: no Virtuoso, desça na hierarquia ou ponha um *wire label* visível) e I(VBAT).

- **Limiar** (VDD > 0,9 V): **0,37 V**; aceitável 0,30–0,45 V. O limiar daqui é um pouco maior que o do teste C + G (0,35 V), porque lá o critério era dk = 1 V.
- **I(VBAT):** ~32 nA no escuro e ~177 nA com luz.

### M3. Os 4 estados + escuro, em transitório (`modulo_3_estados.png`)

TRIGGER = 3,3 V. Fontes `vpwl` para VBAT, CTRL_LOW, CTRL_HIGH e VIN_DC, um trecho de 1 ms para cada estado (as mesmas do `sim/figs/tb/csv_M_estados.spice`).

| Trecho | VBAT | CTRL_LOW | CTRL_HIGH | VIN_DC | VS | VDD | I(VBAT) | I(TRIGGER) |
|---|---|---|---|---|---|---|---|---|
| 0-0 normal | 3,7 | 3,7 | 3,7 | 0,6 | 3,70 | 1,85 | 150 nA | 0 |
| 1-0 VBAT < T_D | 2,8 | 0 | 2,8 | 0,6 | 2,75 | 1,84 | 0 | 148 nA |
| 0-1 VBAT > T_U | 4,3 | 4,3 | 0 | 0,6 | 4,30 | **0** | 39 nA | 0 |
| 1-1 power-on | 0 | 0 | 0 | 0,6 | 2,75 | 1,84 | 0 | 148 nA |
| 0-0 no escuro | 3,7 | 3,7 | 3,7 | 0 | 3,70 | **0** | 32 nA | 0 |

**Critério:**
- VDD liga e desliga exatamente nesses trechos.
- A bateria nunca fornece corrente nos estados 1-0 e 1-1.
- O TRIGGER nunca fornece corrente nos estados com CTRL_LOW alto.

Os picos nas bordas são a carga dos capacitores e o crowbar dos inversores, e são normais.

### M4. Transitórios de partida (`modulo_4_partida.png`)

1. **Partida a frio:** VBAT = 0, CTRL_LOW = CTRL_HIGH = 0, VIN_DC = 0,6 V, TRIGGER em `vpwl` de 0 a 3,3 V entre 0,1 e 0,2 ms.
   - **Esperado:** VDD acompanha VS e chega a 90 % (1,65 V) em t ≈ 0,18 ms. Ou seja, segue a rampa sem atraso extra visível.
2. **Escuro → luz → escuro:** estado 0-0, VBAT = 3,7 V, VIN_DC = 0 → 0,6 V em 1 ms e de volta a 0 em 3 ms.
   - **Esperado:** VDD sobe ~4 µs depois da luz e cai em ~9 µs no escuro; dk faz o oposto de VIN_DC.
   - **Aceitável:** < 100 µs nos dois sentidos.

### M5. Cantos de processo (`modulo_5_cantos.png`)

São os mesmos testes M1/M2 nos cantos tt, ff, ss, fs e sf do SKY130. Servem para ter uma ideia da faixa de variação que é normal:

| Canto | VDD (3,7 V) | Limiar do escuro | I(VBAT) no escuro | Consumo próprio com luz |
|---|---|---|---|---|
| tt | 1,84 V | 0,37 V | 32 nA | 27 nA |
| ff | 1,86 V | 0,36 V | 68 nA | 55 nA |
| ss | 1,82 V | 0,37 V | 16 nA | 13 nA |
| fs | 1,81 V | 0,38 V | 12 nA | 10 nA |
| sf | 1,87 V | 0,35 V | 92 nA | 73 nA |

VDD e o limiar mudam pouco. As correntes de nA variam ~8× entre os cantos, porque dependem do Vth do nativo. Isso é esperado no seu PDK também.

---

## Se algo sair da faixa

| Sintoma | Bloco | Ajuste |
|---|---|---|
| Corrente do espelho muito alta/baixa | C | L do XMB (maior L → menos corrente); se não houver nativo, use um NMOS com gate em GND e L longo, ou uma fonte de corrente *β-multiplier* |
| VG muito alto/baixo | D | W dos diodos (maior W → menor VG) ou o número de diodos |
| VDD longe de 1,8 V com VG certo | E | o Vth do seguidor; com NMOS comum, tire 1 diodo da pilha |
| Fuga do seguidor alta (> 50 nA) | E | aumente L do XMF |
| Limiar do escuro fora de 0,3–0,45 V | C/G | razão I(XPD)/I(XLD): L do XPD (maior → limiar menor) ou W do XLD (maior → limiar menor) |
| VDD não desliga no estado 0-1 | F | ligação de CTRL_LOW e nhigh (é um AND: CTRL_LOW alto **e** CTRL_HIGH baixo) |
| Bateria fornece corrente no estado 1-0 | B | n-well das chaves PMOS deve ser VS, não VBAT; DTR em série com o TRIGGER |

## Arquivos

- **Netlist hierárquico** (um subcircuito por bloco, com os nomes sugeridos para as células): `sim/blocos/coldstart_blocos.spice`.
- **Testbenches:** `sim/figs/tb/csv_*.spice`.
  - Blocos: `csv_A` … `csv_G`, `csv_CG`, `csv_D2`, `csv_E2`.
  - Módulo: `csv_M_dc_<canto>`, `csv_M_estados`, `csv_M_partida`, `csv_M_eq`.
- **Gráficos:** `python sim/figs/graficos_cs_validacao.py`, depois de rodar os testbenches com `ngspice -b` dentro de `sim/figs/tb/`.
