# Bibliografia: Integração do carregador

TEXAS INSTRUMENTS. *BQ25504 Ultra Low-Power Boost Converter With Battery Management for Energy Harvester Applications*. Datasheet SLUSAH0G, rev. G, ago. 2023.

- Arquivo: `bibliografia/TI_BQ25504_datasheet_SLUSAH0G.pdf`. O PDF não está no repositório público (direitos autorais do editor); baixe pelo link da fonte abaixo.
- Fonte: <https://www.ti.com/lit/ds/symlink/bq25504.pdf>
- **Diagrama:** **Seção 8.2 "Functional Block Diagram" (p. 12)**: os blocos "Cold-Start Unit", "Boost Charge Controller", "Battery Threshold Control" e "Bias Reference and Oscillator" ligados entre LBST, VSTOR, VBAT e os pinos de programação.
- **Relação com o circuito:** É o sistema que o seu projeto simplifica, com os mesmos nomes de bloco do seu diagrama. A Fig. 9-1 (p. 20) mostra a ligação externa completa: célula, L, capacitores, bateria e divisores.
- **Diferenças:** O seu projeto tira o MPPT por amostragem (fica a emulação de resistor no boost) e troca o *enable* do boost pela parada do CLK.
