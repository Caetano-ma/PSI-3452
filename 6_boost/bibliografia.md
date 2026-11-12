# Bibliografia: Boost Charge Controller (DCM, f e t_on fixos)

HAUKE, B. *Basic Calculation of a Boost Converter's Power Stage*. Texas Instruments, Application Note SLVA372D, 2022.

- Arquivo: `bibliografia/TI_SLVA372D_Boost_power_stage_calculation.pdf`. O PDF não está no repositório público (direitos autorais do editor); baixe pelo link da fonte abaixo.
- Fonte: <https://www.ti.com/lit/pdf/slva372>
- **Diagrama:** **Fig. 1-1 "Boost Converter Power Stage" (p. 2)**: indutor L, chave SW, diodo D e capacitores C_IN/C_OUT.
- **Relação com o circuito:** É exatamente a topologia do seu boost: L externo em LBST, chave NMOS SW, diodo DR até VSTOR e Cin/Cout.
- **Diferenças:** A nota trata do modo contínuo (CCM). O seu boost opera em modo descontínuo (DCM); a fórmula de R_in usada (R_in = 2L/(t_on²·f)·(1 − V_in/V_out)) vem de MARTINS, G. C. et al., arXiv:1704.08910, 2017, eq. (2).
