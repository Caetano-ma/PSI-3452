# Bibliografia: Cold-Start (seleção de fonte + regulador)

LEE, I.; SYLVESTER, D.; BLAAUW, D. A Subthreshold Voltage Reference With Scalable Output Voltage for Low-Power IoT Systems. *IEEE Journal of Solid-State Circuits*, v. 52, n. 5, p. 1443–1449, 2017. DOI: 10.1109/JSSC.2017.2654326.

- Arquivo: `bibliografia/Lee_Sylvester_Blaauw_2017_JSSC_subthreshold_voltage_reference.pdf`. O PDF não está no repositório público (direitos autorais do editor); baixe pelo link da fonte abaixo.
- Fonte: <https://blaauw.engin.umich.edu/wp-content/uploads/sites/342/2017/11/LeeA-Subthreshold-voltage-reference.pdf>
- **Diagrama:** **Fig. 1 (p. 1444)**: NMOS nativos ("Zero-V_th") usados como fonte de corrente de pA/nA alimentando uma pilha de transistores ligados como diodo.
- **Relação com o circuito:** É o mesmo princípio do núcleo do regulador: XMB (nativo, fonte de nA) alimenta a pilha XD1–XD3, que fixa VG ≈ 2,4 V; o seguidor nativo XMF copia VG para VDD.
- **Diferenças:** A seleção de fonte (XSB, XST, DTR) e o desligamento (XK1–XK4) não aparecem nessa figura; são chaves e portas simples, descritas no esquemático.
