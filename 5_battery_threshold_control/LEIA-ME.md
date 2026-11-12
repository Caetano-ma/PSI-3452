# Battery Threshold Control

- `esquematico.png`: referência, 2 comparadores, 2 NMOS de histerese e o divisor externo, com os valores dos resistores.
Mudança da v2: o divisor externo passou de 20 para 100 MΩ (os mesmos limiares; consumo do divisor ~5× menor).

- `rampa_de_vbat.png`: VBAT em rampa, com CTRL_LOW/CTRL_HIGH, os taps do divisor comparados a VREF e o consumo.
- `lacos_de_histerese.png`: limiares simulados de 4,26/4,10 V (HIGH) e 3,14/2,96 V (LOW); com 10 pF externos em T_U e T_D, sem trepidação.

- `bibliografia.md`: a referência cujo diagrama embasa este circuito (PDF em `bibliografia/`).
