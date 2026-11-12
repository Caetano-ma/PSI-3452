# Bibliografia: Comparador contínuo de ~12 nA

HASLER, J. *Comparators*. Notas de aula, ECE 4430 (Analog Integrated Circuits), Georgia Institute of Technology.

- Arquivo: `bibliografia/Hasler_GaTech_ECE4430_Comparators.pdf`. O PDF não está no repositório público (direitos autorais do editor); baixe pelo link da fonte abaixo.
- Fonte: <https://hasler.ece.gatech.edu/Courses/ECE4430/Proj4/Comparators.pdf>
- **Diagrama:** **Slide 9 ("2-stage Comparator")**: par diferencial com espelho de corrente seguido de um 2º estágio fonte-comum, sem compensação.
- **Relação com o circuito:** É a estrutura do núcleo do seu comparador: OTA (M1–M4 + cauda MPT) seguido do 2º estágio MC1/MC2. Os slides 16–17 mostram ainda a histerese por realimentação externa, usada no Battery Threshold Control.
- **Diferenças:** O seu comparador usa par PMOS (entrada perto do GND) em vez de NMOS e termina num Schmitt trigger; a figura mostra a versão com par NMOS.
