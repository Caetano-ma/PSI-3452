# Oscilador (anel current-starved + pulso de t_on)

- `esquematico.png`: anel de 5 inversores com corrente limitada por nativos, detector de borda (atraso + NAND) e buffers. Inclui o detalhe do inversor "S".
- `formas_de_onda.png`: nós do anel, s2/d3, CLK e a corrente de VDD.
- `pulso_clk_zoom.png`: como o pulso de ~535 ns é formado.
- `corte_de_vdd.png`: com VDD = 0 o CLK fica abaixo do Vth e a chave fica aberta. Ele flutua em ~0,4 V; um pull-down fraco no CLK resolveria.
- `f_ton_consumo_vs_vdd.png`: frequência, t_on e consumo para VDD de 1,8 a 2,6 V.

- `bibliografia.md`: a referência cujo diagrama embasa este circuito (PDF em `bibliografia/`).
