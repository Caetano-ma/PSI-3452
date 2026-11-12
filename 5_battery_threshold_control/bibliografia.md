# Bibliografia: Battery Threshold Control

TEXAS INSTRUMENTS. *BQ25504 Ultra Low-Power Boost Converter With Battery Management for Energy Harvester Applications*. Datasheet SLUSAH0G, rev. G, ago. 2023.

- Arquivo: `bibliografia/TI_BQ25504_datasheet_SLUSAH0G.pdf`. O PDF não está no repositório público (direitos autorais do editor); baixe pelo link da fonte abaixo.
- Fonte: <https://www.ti.com/lit/ds/symlink/bq25504.pdf>
- **Diagrama:** **Fig. 9-1 "Typical Solar Application Circuit" (p. 20)**: limites da bateria programados por divisores resistivos externos (R_OV, R_UV) e a cadeia R_OK1–R_OK3 com o pino OK_HYST para a histerese.
- **Relação com o circuito:** É o modelo direto dos seus pinos T_R/T_U/T_UH/T_D/T_DH: divisor externo + resistor de histerese chaveado por dentro do CI. A seção 8.2 (p. 12) mostra o bloco "Battery Threshold Control" com os comparadores OV/UV/OK.
- **Diferenças:** No bq25504 cada limite tem o seu divisor; no seu projeto um único divisor serve aos dois comparadores.
