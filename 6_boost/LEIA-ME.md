# Boost Charge Controller (DCM, f e t_on fixos)

- `esquematico.png`: modelo da célula, Cin e L externos, chave NMOS + diodo no CI, Cout e bateria.
- `formas_de_onda_4_ciclos.png` e `formas_de_onda_1_ciclo.png`: CLK, V(LBST), corrente no indutor e no diodo, e V_in.
- `celula_e_ponto_de_operacao.png`: curvas I-V e P-V da célula, a reta R_in = 2L/(t_on²f)·(1 − V_in/V_out) ≈ 13 kΩ e os pontos de operação simulados.
- `eficiencia.png`: potência extraída, entregue e gasta pelo oscilador em 4 casos.

- `bibliografia.md`: a referência cujo diagrama embasa este circuito (PDF em `bibliografia/`).
