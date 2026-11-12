"""Esquematico: Battery Threshold Control + divisor externo com histerese."""
from util import *

d = desenho()
rot(d, (-3.5, 3.4), 'Battery Threshold Control (com divisor resistivo externo)', halign='left', fs=12)
rot(d, (-3.5, 2.8), 'Referência + 2 comparadores contínuos + 2 NMOS de histerese.  Saídas ativas em nível baixo.',
    halign='left', fs=8, cor='#555')

# ---------------- divisor externo ----------------
ys = {'T_R': 0, 'T_DH': -3, 'T_D': -6, 'T_U': -9, 'T_UH': -12}
vals = [('R1', '19,11 MΩ'), ('Rhd', '667 kΩ'), ('R2', '254 kΩ'), ('Rhu', '16,0 kΩ'), ('R3', '636 kΩ')]
nos = list(ys.values()) + [-15]
for (nome, v), y0, y1 in zip(vals, nos[:-1], nos[1:]):
    d.add(elm.Resistor().at((0, y0)).down().to((0, y1)).label(f'{nome}\n{v}', loc='top', fontsize=FS - 1))
gnd(d, (0, -15))
for nome, y in ys.items():
    dot(d, (0, y))
    w(d, (0, y), (2.5, y))
    d.add(elm.Dot(radius=0.11, open=True).theta(0).at((2.5, y)))
    rot(d, (1.25, y + 0.3), nome, fs=8, cor='#1f5fa8')
rot(d, (0, 1.2), 'externo', fs=8, cor='#777')

# ---------------- interno ----------------
caixa(d, 2.5, 1.6, 16.3, -13.4, cor='#444', ls='-', lw=1.2)
rot(d, (9.4, 1.25), 'dentro do CI', fs=8, cor='#777')
w(d, (2.5, 0), (4.0, 0))
vdd(d, (4.0, 0), 'VBAT')
rot(d, (4.3, -0.45), 'T_R = VBAT (interno)', fs=7, cor='#555', halign='left')

# NMOS de histerese do limite inferior (entre T_DH e T_D)
w(d, (2.5, -3), (4.0, -3), (4.0, -3.75))
N(d, 4.0, -3.75, gate='right', nome='MHL', lado='left')
w(d, (4.0, -5.25), (4.0, -6.0))
rot(d, (5.55, -4.5), 'CTRL_LOW', fs=8, cor='#d1495b', halign='left')
# NMOS de histerese do limite superior (entre T_U e T_UH)
w(d, (2.5, -9), (4.0, -9), (4.0, -9.75))
N(d, 4.0, -9.75, gate='right', nome='MHH', lado='left')
w(d, (4.0, -11.25), (4.0, -12.0), (2.5, -12.0))
rot(d, (5.55, -10.5), 'CTRL_HIGH', fs=8, cor='#d1495b', halign='left')

# referencia
caixa(d, 6.6, -7.3, 9.3, -8.7, cor='#1f5fa8', ls='-', lw=1.2)
rot(d, (7.95, -7.75), 'Ref. 2T', fs=9, cor='#1f5fa8')
rot(d, (7.95, -8.25), '(VBAT → 133 mV)', fs=7, cor='#1f5fa8')
w(d, (9.3, -8.0), (10.3, -8.0)); dot(d, (10.3, -8.0))
rot(d, (9.8, -7.75), 'VREF', fs=7, cor='#1f5fa8')

# comparador L: + = T_D , - = VREF
cl = elm.Opamp(sign=True).flip().theta(0).anchor('in2').at((11, -6.0)); d.add(cl)
w(d, (2.5, -6.0), (11, -6.0)); dot(d, (4.0, -6.0))
w(d, (10.3, -7.25), (11, -7.25))
# comparador H: + = VREF , - = T_U
ch = elm.Opamp(sign=True).flip().theta(0).anchor('in2').at((11, -8.75)); d.add(ch)
w(d, (10.3, -8.75), (11, -8.75))
w(d, (10.3, -7.25), (10.3, -8.75))
w(d, (4.0, -9.0), (9.6, -9.0), (9.6, -10.0), (11, -10.0)); dot(d, (4.0, -9.0))
rot(d, (12.0, -5.2), 'comp. LOW', fs=8, cor='#555')
rot(d, (12.0, -11.1), 'comp. HIGH', fs=8, cor='#555')
# saidas
w(d, (cl.out.x, cl.out.y), (16.3, cl.out.y))
w(d, (ch.out.x, ch.out.y), (16.3, ch.out.y))
for o, nome in ((cl, 'CTRL_LOW'), (ch, 'CTRL_HIGH')):
    d.add(elm.Dot(radius=0.11, open=True).theta(0).at((16.3, o.out.y)))
    rot(d, (16.6, o.out.y), nome, fs=9, cor='#d1495b', halign='left')

notas = [
    'Funcionamento:',
    '  • CTRL_LOW = 0 V quando V(T_D) < VREF  (VBAT abaixo do limite inferior → usar TRIGGER)',
    '  • CTRL_HIGH = 0 V quando V(T_U) > VREF (VBAT acima do limite superior → parar a carga)',
    '  • Histerese: cada NMOS conduz com a saída INATIVA (gate = CTRL em nível alto) e curto-circuita',
    '    seu resistor. Quando o comparador dispara, o NMOS abre, o resistor entra no divisor e o limiar se desloca.',
    '    MHL abre → Rhd entra ACIMA de T_D → é preciso VBAT maior para liberar (3,0 V → 3,1 V).',
    '    MHH abre → Rhu entra ABAIXO de T_U → é preciso VBAT menor para liberar (4,2 V → 4,1 V).',
    '  • T_U fica ABAIXO de T_D no divisor, porque o limite superior (4,2 V) precisa de uma fração menor de VBAT.',
    '  • Divisor total ≈ 20 MΩ (~210 nA em 4,2 V).  Comparadores: ver 4_comparador.  Referência: ver 3_referencia_de_tensao.',
]
for i, t in enumerate(notas):
    rot(d, (-3.5, -16.2 - 0.45 * i), t, halign='left', fs=8, cor='#333')
salvar_esq(d, 'thr')
