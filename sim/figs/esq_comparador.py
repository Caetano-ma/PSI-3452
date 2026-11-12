"""Esquematico: comparador continuo de ~10 nA (OTA + 2o estagio + Schmitt)."""
from util import *

d = desenho()
rot(d, (-2.5, 2.3), 'Comparador contínuo de baixo consumo (~12 nA por ramo)', halign='left', fs=12)
rot(d, (-2.5, 1.7), 'out = 0 V quando inp < inn   •   tudo alimentado por VBAT, transistores de 5 V',
    halign='left', fs=8, cor='#555')

# trilho VBAT
vdd(d, (0, 0))
w(d, (0, 0), (15, 0))

# ---------------- polarizacao ----------------
P(d, 0, 0, gate='right', nome='MPB', lado='left')
w(d, (0, -1.5), (0, -2.5))
w(d, (0, -1.9), (2.0, -1.9), (2.0, -0.75))
dot(d, (0, -1.9)); dot(d, (2.0, -0.75))
rot(d, (2.0, -0.45), 'nb', fs=8, cor='#1f5fa8')
N(d, 0, -2.5, gate='left', nome='MB', nativo=True)
w(d, (-1.37, -3.25), (-1.37, -4.0), (0, -4.0))
gnd(d, (0, -4.0))

# ---------------- OTA ----------------
w(d, (13, 0), (15, 0))
P(d, 6.0, 0, gate='left', nome='MPT')
w(d, (1.37, -0.75), (4.63, -0.75))
w(d, (6.0, -1.5), (6.0, -2.2))
w(d, (4.5, -2.2), (7.5, -2.2))
w(d, (4.5, -2.2), (4.5, -2.7)); w(d, (7.5, -2.2), (7.5, -2.7))
dot(d, (6.0, -2.2))
rot(d, (6.15, -1.95), 'tail', fs=8, cor='#1f5fa8', halign='left')
P(d, 4.5, -2.7, gate='left', lado='none')
P(d, 7.5, -2.7, gate='right', lado='none')
rot(d, (4.75, -3.2), 'M1', fs=8, halign='left')
rot(d, (7.25, -3.2), 'M2', fs=8, halign='right')
w(d, (3.13, -3.45), (2.6, -3.45)); dot(d, (2.6, -3.45), 'inp', loc='left')
w(d, (8.87, -3.45), (9.25, -3.45)); dot(d, (9.25, -3.45), 'inn', loc='bottom')
rot(d, (6.0, -4.3), 'n-well de M1/M2 = tail', fs=7, cor='#c0392b')
w(d, (4.5, -4.2), (4.5, -5.2)); w(d, (7.5, -4.2), (7.5, -5.2))
N(d, 4.5, -5.2, gate='right', nome='M3', lado='left')
N(d, 7.5, -5.2, gate='left', nome='M4', lado='right')
w(d, (5.87, -5.95), (6.13, -5.95))
w(d, (4.5, -4.75), (6.0, -4.75), (6.0, -5.95))
dot(d, (4.5, -4.75)); dot(d, (6.0, -5.95))
rot(d, (4.35, -4.75), 'd1', fs=8, cor='#1f5fa8', halign='right')
gnd(d, (4.5, -6.7)); gnd(d, (7.5, -6.7))

# ---------------- 2o estagio (fonte comum) ----------------
dot(d, (7.5, -4.75))
w(d, (7.5, -4.75), (9.0, -4.75), (9.0, -5.95), (9.63, -5.95))
rot(d, (8.2, -4.55), 'o1', fs=8, cor='#1f5fa8')
P(d, 11.0, 0, gate='left', nome='MC2')
rot(d, (9.75, -0.5), 'nb', fs=8, cor='#1f5fa8', halign='center')
w(d, (11.0, -1.5), (11.0, -5.2))
N(d, 11.0, -5.2, gate='left', nome='MC1')
gnd(d, (11.0, -6.7))
dot(d, (11.0, -3.4))
w(d, (11.0, -3.4), (13.1, -3.4))
rot(d, (11.2, -3.2), 'o2', fs=8, cor='#1f5fa8', halign='left')

# ---------------- Schmitt trigger com corrente limitada ----------------
X = 15.0
P(d, X, 0, gate='left', nome='XTS')
rot(d, (X - 1.2, -0.5), 'nb', fs=8, cor='#1f5fa8')
P(d, X, -1.5, gate='left', nome='XT1')
P(d, X, -3.0, gate='left', nome='XT2')
N(d, X, -4.5, gate='left', nome='XT5')
N(d, X, -6.0, gate='left', nome='XT4')
N(d, X, -7.5, gate='left', nome='XTB', nativo=True)
w(d, (X - 1.37, -8.25), (X - 1.37, -9.0), (X, -9.0)); gnd(d, (X, -9.0))
for y in (-2.25, -3.75, -5.25, -6.75):
    w(d, (13.1, y), (X - 1.37, y))
w(d, (13.1, -2.25), (13.1, -6.75))
for y in (-3.4, -3.75, -5.25):
    dot(d, (13.1, y))
rot(d, (X + 0.6, -3.0), 'px', fs=8, cor='#1f5fa8', halign='left')
rot(d, (X + 0.6, -6.0), 'nx', fs=8, cor='#1f5fa8', halign='left')
dot(d, (X, -3.0)); dot(d, (X, -6.0)); dot(d, (X, -4.5))
# XT3: px -> GND ; XT6: VBAT -> nx ; gates em out
w(d, (X, -3.0), (16.4, -3.0), (16.4, -1.9), (17.4, -1.9))
P(d, 17.4, -1.9, gate='right', lado='none')
rot(d, (17.7, -1.45), 'XT3', fs=8, halign='left')
gnd(d, (17.4, -3.4))
w(d, (X, -6.0), (16.4, -6.0), (16.4, -7.1), (19.2, -7.1))
w(d, (19.2, -5.3), (19.2, -5.6))
rot(d, (19.2, -5.1), 'VBAT', fs=8)
N(d, 19.2, -5.6, gate='right', nome='XT6', lado='left')
w(d, (18.77, -2.65), (21.0, -2.65))
w(d, (20.57, -6.35), (21.0, -6.35))
w(d, (21.0, -2.65), (21.0, -6.35))
w(d, (X, -4.5), (22.2, -4.5))
dot(d, (21.0, -4.5))
dot(d, (22.2, -4.5), 'out', loc='right')

# caixas de funcao
caixa(d, -2.0, 0.8, 2.9, -4.9); rot(d, (0.45, -5.2), 'polarização ~12 nA', fs=8, cor='#777')
caixa(d, 2.95, 0.8, 9.5, -7.6); rot(d, (6.2, -7.9), 'OTA: par PMOS + espelho', fs=8, cor='#777')
caixa(d, 9.55, 0.8, 12.4, -7.6); rot(d, (11.0, -7.9), '2º estágio', fs=8, cor='#777')
caixa(d, 12.6, 0.8, 21.6, -9.9); rot(d, (18.5, -9.6), 'Schmitt trigger (corrente limitada)', fs=8, cor='#777')

notas = [
    'Dimensões (W/L em µm, todos de 5 V):',
    '  MB: nativo 10/4 (Vgs = 0 → ~12 nA, independe de VBAT)     MPB, MPT, MC2, XTS: PMOS 2/4 (espelhos de nb)',
    '  M1, M2: PMOS 4/2     M3, M4: NMOS 2/4     MC1: NMOS 2/1',
    '  XT1–XT6: 1/1     XTB: nativo 10/4 (limita a corrente do Schmitt junto com XTS)',
    'Por quê:',
    '  • VREF ≈ 133 mV → entrada perto do GND → par PMOS. O n-well de M1/M2 vai na cauda (sem efeito de corpo).',
    '  • o1 só sobe até ≈ 1 V → o 2º estágio (MC1 + carga MC2) leva o sinal de 0 a VBAT.',
    '  • Schmitt: comuta de uma vez; com corrente limitada a nA, o crowbar perto do limiar não “segura” a carga.',
]
for i, t in enumerate(notas):
    rot(d, (-2.0, -10.6 - 0.45 * i), t, halign='left', fs=8, cor='#333')
rot(d, (-2.0, -10.6 - 0.45 * len(notas) - 0.15), 'Traço vermelho no canal = NMOS nativo.',
    halign='left', fs=8, cor='#c0392b')
salvar_esq(d, 'comp')
