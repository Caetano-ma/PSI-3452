"""Esquematico: referencia de tensao de 2 transistores."""
from util import *

d = desenho()
rot(d, (-3.0, 1.6), 'Referência de tensão de 2 transistores', halign='left', fs=12)
rot(d, (-3.0, 1.0), '(Seok/Blaauw, 2012) — dentro do Battery Threshold Control',
    halign='left', fs=8, cor='#555')

vdd(d, (0, 0))
N(d, 0, 0, gate='left', nome='M1 (nativo)', wl='W/L = 1/4 µm', nativo=True)
w(d, (-1.37, -0.75), (-2.2, -0.75), (-2.2, -4.0))
gnd(d, (-2.2, -4.0))
w(d, (0, -1.5), (0, -2.5))
N(d, 0, -2.5, gate='left', nome='M2', wl='W/L = 10/1 µm')
w(d, (-1.37, -3.25), (-1.37, -2.0), (0, -2.0))
dot(d, (-1.37, -2.0))
dot(d, (0, -2.0))
gnd(d, (0, -4.0))
# saida + capacitor
w(d, (0, -2.0), (4.6, -2.0))
dot(d, (3.4, -2.0))
d.add(elm.Capacitor().at((3.4, -2.0)).down().to((3.4, -3.5))
      .label('Cref 0,1 pF', loc='bottom', fontsize=FS - 1))
gnd(d, (3.4, -3.5))
dot(d, (4.6, -2.0), 'VREF ≈ 133 mV', loc='right')

notas = [
    'M1: NMOS nativo (Vth ≈ 0), gate no GND → Vgs1 = −VREF.',
    '    Fonte de corrente de pA, saturada → quase não depende de VBAT.',
    'M2: NMOS 5 V ligado como diodo, em sublimiar.',
    'Mesma corrente nos dois:  VREF ≈ (Vth2 − Vth1)/2 + termo PTAT',
    '    (o termo PTAT ∝ ln[(W/L)₁/(W/L)₂] → a razão W/L ajusta o coef. de temperatura).',
    'Sem circuito de partida; consumo ≈ 14 pA.',
]
for i, t in enumerate(notas):
    rot(d, (-3.0, -5.2 - 0.42 * i), t, halign='left', fs=8, cor='#333')
rot(d, (-3.0, -5.2 - 0.42 * len(notas) - 0.2), 'Traço vermelho no canal = NMOS nativo (nfet_05v0_nvt).', halign='left', fs=8, cor='#c0392b')
salvar_esq(d, 'ref')
