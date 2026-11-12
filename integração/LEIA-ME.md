# Integração (v2)

- `esquematico.png`: os 4 blocos interligados como no diagrama de blocos, com a célula, o indutor, o **Schottky externo**, a bateria, o TRIGGER e o divisor externos. Na v2, VIN_DC também entra no Cold-Start (detector de escuro).
- `balanco_de_energia_v1_v2.png`: **comparação v1 × v2** da corrente líquida na bateria em 4 condições de luz, e o saldo diário (+23 → +46 µAh/dia com 8 h de luz cheia).
- `pouca_luz_v1_v2.png`: com pouca luz, a v2 liga o oscilador em pulsos (*burst*) e mantém saldo positivo; a v1 gastava a bateria.
- `caso_C_luz_escuro_luz.png`: luz → escuro → luz com bateria de 3,7 V. No escuro, VDD e o oscilador desligam e a bateria perde só ~0,14 µA.
- `caso_A_limite_superior.png`: carga até ~4,25 V, desligamento (VDD e CLK a 0, VIN volta à Voc) e religamento em ~4,1 V. A bateria foi trocada por um capacitor de 47 nF com uma carga de 2 MΩ (o "sensor"), para a tensão variar em ms.
- `caso_A_zoom_disparo.png` e `caso_A_zoom_religamento.png`: detalhe dos dois eventos.
- `caso_B_trigger_para_vbat.png`: com VBAT a 2,9 V o sistema roda pelo TRIGGER (3,3 V) e passa sozinho para o VBAT em 3,1 V. Depois da troca a inclinação de VBAT diminui, porque a bateria passa a alimentar o chip.
- `caso_B_zoom_troca_de_fonte.png`: detalhe da troca.

- `bibliografia.md`: a referência cujo diagrama embasa este circuito (PDF em `bibliografia/`).
