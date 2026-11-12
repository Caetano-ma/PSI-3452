# Boost Charge Controller (v2: DCM, f e t_on fixos, Schottky externo)

- `esquematico.png`: modelo da célula, Cin e L externos, chave NMOS no CI, **diodo Schottky externo** (v2), Cout e bateria.
- `formas_de_onda_4_ciclos.png` e `formas_de_onda_1_ciclo.png`: CLK, V(LBST), corrente no indutor e no diodo, e V_in.
- `celula_e_ponto_de_operacao.png`: curvas I-V e P-V da célula, a reta R_in = 2L/(t_on²f)·(1 − V_in/V_out) ≈ 13 kΩ e os pontos de operação simulados.
- `eficiencia.png`: potência extraída, entregue e gasta pelo oscilador (já referida à bateria) em 4 casos.

Mudanças da v2: diodo integrado p+/n-well (~0,77 V) trocado por Schottky externo (~0,37 V; o modelo tem ~2 nA de fuga, e no componente real é preciso conferir a fuga a 4,2 V). Clock de 52,7 kHz com t_on de 751 ns (I_pk ≈ 2 mA).

- `bibliografia.md`: a referência cujo diagrama embasa este circuito (PDF em `bibliografia/`).
