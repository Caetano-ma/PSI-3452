# Cold-Start (seleção de fonte + regulador)

- `esquematico.png`: circuito em nível de transistor. Chaves do TRIGGER e do VBAT, referência de nA espelhada, pilha de 3 diodos, seguidor de fonte nativo e pull-downs do estado 0-1.
- `regulacao_linha_carga_temperatura.png`: VDD em função de VBAT, da corrente de carga e da temperatura (≈ 2,2 V).
- `estados_de_controle.png`: os 4 estados de CTRL_LOW/CTRL_HIGH em sequência, com VS, VDD e as correntes puxadas de VBAT e do TRIGGER.
  No estado 0-1 aparece uma fuga de ~0,9 µA pelo seguidor nativo, que é um ponto a melhorar.

- `bibliografia.md`: a referência cujo diagrama embasa este circuito (PDF em `bibliografia/`).
