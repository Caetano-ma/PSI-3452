# Oscilador (v2: anel current-starved + pulso de t_on)

- `esquematico.png`: anel de 5 inversores com corrente limitada por nativos, detector de borda (atraso + NAND) e buffers. Inclui o detalhe do inversor "S".
- `formas_de_onda.png`: nós do anel, s2/d3, CLK e a corrente de VDD.
- `pulso_clk_zoom.png`: como o pulso de ~750 ns é formado.
- `corte_de_vdd.png`: com VDD = 0, o CLK fica em 0 V e a chave fica aberta.
- `f_ton_consumo_vs_vdd.png`: frequência, t_on e consumo para VDD de 1,5 a 2,1 V.

Mudanças da v2: VDD de 1,8 V; no anel, o nativo passou para L = 2 µm. A frequência caiu de 101 para ~53 kHz **e** a corrente de curto-circuito caiu junto: ~0,12 µA contra ~0,54 µA. Aumentar só o capacitor do anel quase não economizava, porque as bordas ficam mais lentas. t_on passou para ~750 ns, mantendo t_on²·f (e portanto R_in) igual ao da v1.

- `bibliografia.md`: a referência cujo diagrama embasa este circuito (PDF em `bibliografia/`).
