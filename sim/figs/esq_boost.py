"""Esquematico: estagio de potencia do Boost (DCM, f e t_on fixos)."""
from util import *

d = desenho()
rot(d, (-1.0, 3.6), 'Boost Charge Controller: chave NMOS + diodo, em modo descontínuo (DCM)', halign='left', fs=12)
rot(d, (-1.0, 3.0), 'Sem enable: o boost para quando o CLK some.  f e t_on fixos vêm do Oscilador.',
    halign='left', fs=8, cor='#555')

# ---------------- celula FV (modelo) ----------------
d.add(elm.SourceI().at((0, -3)).up().to((0, 0)).label('Iph\n50 µA', loc='bottom', fontsize=FS - 1))
d.add(elm.Diode().at((1.6, 0)).down().to((1.6, -3)).label('Dcel', loc='bottom', fontsize=FS - 1))
d.add(elm.Resistor().at((3.2, 0)).down().to((3.2, -3)).label('Rsh\n200 kΩ', loc='bottom', fontsize=FS - 1))
w(d, (0, 0), (3.2, 0)); w(d, (0, -3), (6.2, -3))
dot(d, (1.6, 0)); dot(d, (3.2, 0)); dot(d, (1.6, -3)); dot(d, (3.2, -3))
d.add(elm.Resistor().at((3.2, 0)).right().to((5.2, 0)).label('Rs 50 Ω', loc='top', fontsize=FS - 1))
caixa(d, -1.0, 1.4, 4.3, -3.6, cor='#2a9d5c')
rot(d, (1.65, 1.75), 'célula a-Si (modelo): Voc 0,8 V, MPP 0,675 V / 29,7 µW', fs=7, cor='#2a9d5c')
gnd(d, (3.2, -3))

# ---------------- Cin e indutor externos ----------------
w(d, (5.2, 0), (6.2, 0))
dot(d, (6.2, 0), 'VIN_DC', loc='top')
d.add(elm.Capacitor().at((6.2, 0)).down().to((6.2, -3)).label('Cin\n100 nF', loc='bottom', fontsize=FS - 1))
d.add(elm.Inductor2(loops=4).at((6.2, 0)).right().to((9.2, 0))
      .label('L = 220 µH\n(DCR 5 Ω)', loc='top', fontsize=FS - 1))
w(d, (9.2, 0), (10.0, 0))
d.add(elm.Dot(radius=0.11, open=True).theta(0).at((10.0, 0)))
rot(d, (9.6, 0.45), 'LBST', fs=9, cor='#d1495b')

# ---------------- dentro do CI ----------------
caixa(d, 10.0, 1.6, 16.0, -4.0, cor='#444', ls='-', lw=1.2)
rot(d, (13.0, 1.3), 'dentro do CI', fs=8, cor='#777')
w(d, (10.0, 0), (11.5, 0), (11.5, -1.0))
dot(d, (11.5, 0))
N(d, 11.5, -1.0, gate='left', nome='SW', wl='W/L = 200/0,5 µm', lado='right')
gnd(d, (11.5, -2.5))
w(d, (10.13, -1.75), (10.13, -3.2))
rot(d, (10.2, -3.5), 'CLK (do Oscilador)', fs=8, cor='#d1495b', halign='left')
d.add(elm.Diode().at((11.5, 0)).right().to((14.5, 0))
      .label('DR  p+/n-well', loc='top', fontsize=FS - 1))
w(d, (14.5, 0), (16.0, 0))
d.add(elm.Dot(radius=0.11, open=True).theta(0).at((16.0, 0)))
rot(d, (16.5, 0.45), 'VSTOR', fs=9, cor='#d1495b')

# ---------------- saida: Cout + bateria ----------------
w(d, (16.0, 0), (19.5, 0))
dot(d, (17.4, 0))
d.add(elm.Capacitor().at((17.4, 0)).down().to((17.4, -3)).label('Cout\n1 µF', loc='bottom', fontsize=FS - 1))
d.add(elm.Battery().at((19.5, -3)).up().to((19.5, 0)).label('Li-ion\n3,0–4,2 V', loc='bottom', fontsize=FS - 1))
w(d, (17.4, -3), (19.5, -3)); gnd(d, (17.4, -3))
rot(d, (18.6, 0.85), 'VSTOR = VBAT', fs=8, cor='#555')

notas = [
    'Cada ciclo (DCM): CLK alto por t_on → a corrente no indutor sobe até I_pk = V_in·t_on / L.',
    'CLK baixo → o indutor descarrega a energia ½·L·I_pk² na bateria pelo diodo, e zera antes do próximo ciclo.',
    'A célula também alimenta a saída durante a descarga, então a potência retirada é  P = (V_in²·t_on²·f / 2L) · V_out/(V_out − V_in)',
    '   → a célula “vê” um resistor fixo:  R_in = 2L/(t_on²·f) · (1 − V_in/V_out)   (V_out = VBAT + V_diodo ≈ 4,5 V)',
    '        ≈ 15,3 kΩ · 0,87 ≈ 13 kΩ  ≈  R_mpp da célula (~15 kΩ)  → MPPT “de graça”, sem malha  [Martins et al., arXiv:1704.08910, eq. 2]',
    'I_pk ≈ 0,6 V · 534 ns / 220 µH ≈ 1,5 mA  =  a “corrente de referência fixa” do boost.',
    'Sem CLK a chave fica aberta e o diodo bloqueia o retorno da bateria para a célula.',
    'O diodo integrado cai ~0,77 V (≈15% de perda) e tem PNP parasita para o substrato; um Schottky externo é a alternativa simples.',
]
for i, t in enumerate(notas):
    rot(d, (-1.0, -5.0 - 0.45 * i), t, halign='left', fs=8, cor='#333')
salvar_esq(d, 'boost')
