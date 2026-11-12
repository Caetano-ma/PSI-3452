# Integração

- `esquematico.png`: os 4 blocos interligados como no diagrama de blocos, com a célula, o indutor, a bateria, o TRIGGER e o divisor externos.
- `caso_A_limite_superior.png`: carga até ~4,23 V, desligamento (VDD e CLK a 0, VIN volta à Voc) e religamento em ~4,11 V. A bateria foi trocada por um capacitor de 47 nF para acelerar a simulação.
- `caso_A_zoom_disparo.png` e `caso_A_zoom_religamento.png`: detalhe dos dois eventos.
- `caso_B_trigger_para_vbat.png`: com VBAT a 2,9 V o sistema roda pelo TRIGGER (3,3 V) e passa sozinho para o VBAT em 3,1 V. Depois da troca a inclinação de VBAT diminui, porque a bateria passa a alimentar o chip.
- `caso_B_zoom_troca_de_fonte.png`: detalhe da troca.

- `bibliografia.md`: a referência cujo diagrama embasa este circuito (PDF em `bibliografia/`).
