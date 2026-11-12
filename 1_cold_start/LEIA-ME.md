# Cold-Start (v2: seleção de fonte + regulador + detector de escuro)

- `esquematico.png`: circuito em nível de transistor. Chaves do TRIGGER e do VBAT, referência de nA espelhada, pilha de 3 diodos, seguidor de fonte nativo, pull-downs do estado 0-1 e, novo na v2, o **detector de escuro** (XPD, XLD, XKD1, XKD2), destacado em azul.
- `regulacao_linha_carga_temperatura.png`: VDD em função de VBAT, da corrente de carga e da temperatura (≈ 1,8 V na v2; era 2,2 V).
- `estados_de_controle.png`: os 4 estados de CTRL_LOW/CTRL_HIGH em sequência, mais um 5º trecho no escuro, com VS, VDD e as correntes puxadas de VBAT e do TRIGGER.
- `detector_de_escuro.png`: VDD e o nó `dk` em função de VIN_DC. Sem luz (VIN_DC < ~0,36 V), VDD desliga e o consumo cai para dezenas de nA.

Mudanças da v2: detector de escuro; pilha com diodos de W = 6 µm (VDD 2,2 → 1,8 V); seguidor nativo com L = 4 µm (a fuga com Vgs = 0 caiu de ~0,7 µA para ~30 nA).

- `bibliografia.md`: a referência cujo diagrama embasa este circuito (PDF em `bibliografia/`).
