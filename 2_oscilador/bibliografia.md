# Bibliografia: Oscilador (anel current-starved + pulso t_on)

DASH, S. K.; MISHRA, S. N.; ROUT, N. K. Design of Efficient Delay Block for Low Frequency Application. *Facta Universitatis, Series: Electronics and Energetics*, v. 33, n. 3, p. 489–498, 2020. DOI: 10.2298/FUEE2003489D. (Acesso aberto, CC BY-NC-ND.)

- Arquivo: [`bibliografia/Dash_Mishra_Rout_2020_FUEE_current_starved_delay_block.pdf`](bibliografia/Dash_Mishra_Rout_2020_FUEE_current_starved_delay_block.pdf)
- Fonte: <https://casopisi.junis.ni.ac.rs/index.php/FUElectEnerg/article/view/6162>
- **Diagrama:** **Fig. 1 (p. 490)**: inversor *current-starved* usado como célula de atraso; **Fig. 2 (p. 491)**: oscilador em anel montado com essas células.
- **Relação com o circuito:** Mesma ideia dos inversores "S" do anel e da cadeia de atraso que define t_on: limitar a corrente do inversor para obter atraso grande (baixa frequência) com pouco consumo.
- **Diferenças:** No seu circuito, a limitação é feita por um NMOS nativo com Vgs = 0 em série; o artigo usa outra forma de limitar a corrente, mas o princípio é o mesmo.
