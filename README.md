# PSI-3452: Carregador de célula fotovoltaica (CI CMOS 130 nm)

CI de *energy harvesting* que carrega uma bateria Li-ion de 1 célula a partir de uma única célula fotovoltaica de silício amorfo (luz interna, 0,4–0,8 V). O projeto se inspira no TI bq25504, com blocos simplificados para serem projetados à mão em nível de transistor.

Este repositório contém a **prova de conceito em SPICE** de cada bloco, feita com ferramentas livres (ngspice + PDK SkyWater SKY130). O projeto final será feito no Cadence Virtuoso.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `1_cold_start/` | Seleção de fonte (VBAT/TRIGGER) e regulador de VDD ≈ 2,2 V |
| `2_oscilador/` | Anel *current-starved* + gerador de pulso (f ≈ 100 kHz, t_on ≈ 530 ns) |
| `3_referencia_de_tensao/` | Referência de 2 transistores (VREF ≈ 133 mV, ~14 pA) |
| `4_comparador/` | Comparador contínuo de ~12 nA (OTA + 2º estágio + Schmitt trigger) |
| `5_battery_threshold_control/` | Limites de 4,2/4,1 V e 3,0/3,1 V com divisor externo e histerese |
| `6_boost/` | Boost em DCM com f e t_on fixos (emulação de resistor ≈ MPPT) |
| `integração/` | Os 4 blocos interligados e as simulações do sistema completo |
| `sim/` | Netlists (`sim/blocos/`), testbenches e scripts que geram as figuras (`sim/figs/`) |

Cada pasta de módulo tem o esquemático (`esquematico.png`), os gráficos dos sinais relevantes, um `LEIA-ME.md` e um `bibliografia.md` com a referência cujo diagrama embasa o circuito.

O resumo das arquiteturas, os resultados e os problemas encontrados estão em [`sim/README.md`](sim/README.md).

## Como reproduzir

1. Instale o ngspice (testado com a versão 47) e o PDK SKY130 (`sky130A`, bibliotecas `sky130_fd_pr`).
2. Nos netlists, a linha `.lib` aponta para o caminho local do PDK; ajuste para o seu caminho.
3. Rode os testbenches de `sim/figs/tb/` (cada pasta precisa do `.spiceinit`) para gerar os dados em `sim/figs/dados/`.
4. Em `sim/figs/`, rode `python graficos.py` e `python esq_<módulo>.py` (requer `numpy`, `matplotlib` e `schemdraw`).

Os dados brutos das simulações (`*.txt`, ~150 MB) não estão no repositório, porque são regerados no passo 3.

## Observação sobre a bibliografia

Por direitos autorais, só está no repositório o PDF de licença aberta (Dash et al., CC BY-NC-ND). Para os demais, os `bibliografia.md` trazem o link oficial.
