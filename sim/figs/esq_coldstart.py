"""Esquematico: Cold-Start (selecao de fonte + regulador seguidor de fonte)."""
from util import *
from schemdraw import logic

d = desenho()
rot(d, (-6.0, 4.4), 'Cold-Start (v2): seleção de fonte + regulador + detector de escuro', halign='left', fs=12)
rot(d, (-6.0, 3.8), 'VDD ≈ 1,8 V para o Oscilador  •  transistores de 5 V  •  traço vermelho = NMOS nativo  •  em azul: novidades da v2',
    halign='left', fs=8, cor='#555')

def pino(p, txt, loc):
    d.add(elm.Dot(radius=0.11, open=True).theta(0).at(p).label(txt, loc=loc, fontsize=FS, color='#d1495b'))

# ---------------- selecao de fonte ----------------
# TRIGGER -> diodo -> XST -> VS
pino((-3, 2.6), 'TRIGGER', 'top')
d.add(elm.Diode().at((-3, 2.6)).down().to((-3, 0)).label('DTR', loc='bottom', fontsize=FS - 1))
P(d, -3, 0, gate='left', nome='XST')
rot(d, (-4.45, -0.75), 'CTRL_LOW', fs=8, cor='#d1495b', halign='right')
w(d, (-3, -1.5), (-3, -2.0))
# VBAT -> XSB -> VS
pino((1.5, 0.6), 'VBAT', 'top')
w(d, (1.5, 0.6), (1.5, 0))
P(d, 1.5, 0, gate='right', nome='XSB', lado='left')
rot(d, (3.0, -0.75), 'nlow', fs=8, cor='#1f5fa8', halign='left')
rot(d, (1.25, -1.25), 'n-well = VS', fs=7, cor='#c0392b', halign='right')
w(d, (1.5, -1.5), (1.5, -2.0))
# trilho VS
w(d, (-3, -2.0), (11.0, -2.0))
rot(d, (-3.3, -2.0), 'VS', fs=9, cor='#1f5fa8', halign='right')
dot(d, (1.5, -2.0)); dot(d, (4.0, -2.0)); dot(d, (8.0, -2.0))

# ---------------- corrente de referencia (nA) ----------------
P(d, 4.0, -2.0, gate='right', nome='XPB', lado='left')
w(d, (5.37, -2.75), (6.63, -2.75))
w(d, (4.0, -3.5), (4.0, -4.5))
w(d, (4.0, -3.9), (5.8, -3.9), (5.8, -2.75)); dot(d, (4.0, -3.9)); dot(d, (5.8, -2.75))
P(d, 8.0, -2.0, gate='left', nome='XPM', lado='none')
rot(d, (8.25, -2.4), 'XPM', fs=8, halign='left')
N(d, 4.0, -4.5, gate='left', nome='XMB', nativo=True, lado='none')
rot(d, (4.25, -6.35), 'XMB', fs=8, halign='left')
w(d, (2.63, -5.25), (2.63, -6.0), (4.0, -6.0)); gnd(d, (4.0, -6.0))

# ---------------- pilha de 3 diodos -> VG ----------------
w(d, (8.0, -3.5), (8.0, -4.5))
dot(d, (8.0, -4.0))
rot(d, (7.85, -3.8), 'VG', fs=8, cor='#1f5fa8', halign='right')
for i, y in enumerate((-4.5, -6.5, -8.5)):
    N(d, 8.0, y, gate='left', nome=f'XD{i+1}', lado='right')
    w(d, (6.63, y - 0.75), (6.63, y + 0.25), (8.0, y + 0.25)) if i else \
        w(d, (6.63, y - 0.75), (6.63, y + 0.25), (8.0, y + 0.25))
    dot(d, (8.0, y + 0.25))
w(d, (8.0, -6.0), (8.0, -6.5)); w(d, (8.0, -8.0), (8.0, -8.5))
gnd(d, (8.0, -10.0))

# ---------------- seguidor de fonte nativo ----------------
w(d, (8.0, -4.0), (9.3, -4.0), (9.3, -2.75), (9.63, -2.75))
N(d, 11.0, -2.0, gate='left', nome='XMF', nativo=True)
w(d, (11.0, -3.5), (11.0, -4.0), (18.0, -4.0))
pino((18.0, -4.0), 'VDD', 'right')
dot(d, (16.6, -4.0))
d.add(elm.Capacitor().at((16.6, -4.0)).down().to((16.6, -5.6)).label('Cvdd\n10 pF', loc='bottom', fontsize=FS - 1))
gnd(d, (16.6, -5.6))

# ---------------- desligamento (estado 0-1) ----------------
dot(d, (9.3, -4.0))
w(d, (9.3, -4.0), (9.3, -4.8))
N(d, 9.3, -4.8, gate='right', lado='none')
N(d, 9.3, -6.3, gate='right', lado='none')
rot(d, (10.8, -5.55), 'CTRL_LOW', fs=8, cor='#d1495b', halign='left')
rot(d, (10.8, -7.05), 'nhigh', fs=8, cor='#1f5fa8', halign='left')
rot(d, (10.8, -5.15), 'XK1', fs=7, halign='left', cor='#555')
rot(d, (10.8, -6.65), 'XK2', fs=7, halign='left', cor='#555')
gnd(d, (9.3, -7.8))
dot(d, (13.4, -4.0))
N(d, 13.4, -4.0, gate='right', lado='none')
N(d, 13.4, -5.5, gate='right', lado='none')
rot(d, (14.9, -4.75), 'CTRL_LOW', fs=8, cor='#d1495b', halign='left')
rot(d, (14.9, -6.25), 'nhigh', fs=8, cor='#1f5fa8', halign='left')
rot(d, (14.9, -4.35), 'XK3', fs=7, halign='left', cor='#555')
rot(d, (14.9, -5.85), 'XK4', fs=7, halign='left', cor='#555')
gnd(d, (13.4, -7.0))

# ---------------- inversores de controle (alimentados por VS) ----------------
pino((-5.5, -4.5), 'CTRL_LOW', 'left')
pino((-5.5, -6.5), 'CTRL_HIGH', 'left')
g1 = logic.Not().theta(0).anchor('in1').at((-3.5, -4.5)); d.add(g1)
g2 = logic.Not().theta(0).anchor('in1').at((-3.5, -6.5)); d.add(g2)
w(d, (-5.5, -4.5), (-3.5, -4.5)); w(d, (-5.5, -6.5), (-3.5, -6.5))
w(d, (g1.out.x, g1.out.y), (g1.out.x + 0.6, g1.out.y))
w(d, (g2.out.x, g2.out.y), (g2.out.x + 0.6, g2.out.y))
rot(d, (g1.out.x + 0.7, g1.out.y), 'nlow', fs=8, cor='#1f5fa8', halign='left')
rot(d, (g2.out.x + 0.7, g2.out.y), 'nhigh', fs=8, cor='#1f5fa8', halign='left')
rot(d, (-2.6, -7.6), 'inversores alimentados por VS', fs=7, cor='#555')


# ---------------- detector de escuro (v2) ----------------
AZ2 = '#1f5fa8'
caixa(d, 9.9, -7.55, 19.0, -12.3, cor=AZ2)
rot(d, (18.9, -12.05), 'detector de escuro (v2)', fs=8, cor=AZ2, halign='right')
rot(d, (11.85, -8.0), 'VS', fs=8, cor=AZ2)
P(d, 11.5, -8.2, gate='right', nome='XPD', lado='left')
rot(d, (13.0, -8.95), 'nb', fs=8, cor=AZ2, halign='left')
w(d, (11.5, -9.7), (11.5, -10.2))
dot(d, (11.5, -9.95))
rot(d, (11.3, -9.95), 'dk', fs=8, cor=AZ2, halign='right')
N(d, 11.5, -10.2, gate='left', nome='XLD', lado='right')
gnd(d, (11.5, -11.7))
w(d, (10.13, -10.95), (9.5, -10.95))
pino((9.5, -10.95), 'VIN_DC', 'left')
w(d, (11.5, -9.95), (13.13, -9.95))
N(d, 14.5, -9.2, gate='left', nome='XKD1', lado='right')
w(d, (14.5, -9.2), (14.5, -8.9)); rot(d, (14.5, -8.7), 'VG', fs=8, cor=AZ2)
gnd(d, (14.5, -10.7))
dot(d, (12.6, -9.95))
w(d, (12.6, -9.95), (12.6, -11.95), (16.23, -11.95), (16.23, -9.95))
N(d, 17.6, -9.2, gate='left', nome='XKD2', lado='right')
w(d, (17.6, -9.2), (17.6, -8.9)); rot(d, (17.6, -8.7), 'VDD', fs=8, cor=AZ2)
gnd(d, (17.6, -10.7))

notas = [
    'Estados (sinais ativos em nível baixo):',
    '  0-0  CTRL_LOW = VBAT, CTRL_HIGH = VBAT → XSB liga, XST desliga  → regula a partir de VBAT',
    '  1-0  CTRL_LOW = 0                         → XST liga, XSB desliga  → regula a partir do TRIGGER',
    '  0-1  CTRL_LOW = VBAT, CTRL_HIGH = 0     → XK1–XK4 conduzem → VG = 0 e VDD = 0 (oscilador parado)',
    '  1-1  tudo em 0 V (power-on)               → XST liga → regula a partir do TRIGGER',
    '  e, em qualquer estado: VIN_DC < ~0,36 V (sem luz) → dk alto → XKD1/XKD2 zeram VG e VDD (oscilador parado à noite)',
    'Regulador: XMB (nativo, Vgs = 0) gera ~4 nA → espelho XPB/XPM → pilha XD1–XD3 (VG ≈ 2,0 V) → seguidor nativo XMF (VDD ≈ VG − Vgs ≈ 1,8 V).',
    'Detector de escuro: XPD copia ~1 nA de nb e puxa dk para cima; XLD (gate = VIN_DC) vence essa corrente quando há luz.',
    'DTR impede que um TRIGGER ausente (0 V) puxe VS — e a bateria, pelo diodo de corpo de XSB — para baixo.',
    'Dimensões (W/L µm): XST, XSB 10/0,5 • XPB, XPM 2/4 • XMB nativo 10/4 • XD1–3 6/1 • XMF nativo 10/4 • XK1–4, XKD1–2 1/0,5 • XPD 1/8 • XLD 40/0,5 • inversores 1/1',
]
for i, t in enumerate(notas):
    rot(d, (-6.0, -13.0 - 0.45 * i), t, halign='left', fs=8, cor='#333')
salvar_esq(d, 'cs')
