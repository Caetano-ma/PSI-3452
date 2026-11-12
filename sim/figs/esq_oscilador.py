"""Esquematico: oscilador em anel current-starved + gerador de pulso + buffers."""
from util import *
from schemdraw import logic

d = desenho()
rot(d, (-1.5, 3.4), 'Oscilador (v2): anel current-starved + detector de borda (pulso t_on) + buffers', halign='left', fs=12)
rot(d, (-1.5, 2.8), 'Tudo alimentado por VDD (≈ 1,8 V, do Cold-Start), transistores de 5 V.  Sem VDD, todos os nós ficam em 0 V → CLK = 0.',
    halign='left', fs=8, cor='#555')

AZ = '#1f5fa8'


def inv(x, y, s=False, nome=None):
    g = Inversor(d, x, y)
    if s:
        rot(d, ((g.in1.x + g.out.x) / 2 - 0.1, y + 0.75), 'S', fs=8, cor='#c0392b')
    if nome:
        rot(d, ((g.in1.x + g.out.x) / 2 - 0.1, y - 0.75), nome, fs=7, cor='#555')
    return g


def cap(p, txt):
    d.add(elm.Capacitor().at(p).down().to((p[0], p[1] - 1.3)))
    gnd(d, (p[0], p[1] - 1.3))
    rot(d, (p[0] + 0.25, p[1] - 0.65), txt, fs=7, cor='#555', halign='left')


# ---------------- anel de 5 inversores ----------------
x, y = 0.0, 0.0
w(d, (-0.8, 0.0), (0.0, 0.0))
nos = []
for i in range(5):
    g = inv(x, y, s=True, nome=f'X{i+1}')
    xo = g.out.x
    w(d, (xo, y), (xo + 1.4, y))
    dot(d, (xo + 0.7, y))
    rot(d, (xo + 0.7, y + 0.35), f'r{i+1}', fs=8, cor=AZ)
    cap((xo + 0.7, y), 'Cr')
    nos.append(xo + 0.7)
    x = xo + 1.4
x_r5 = nos[-1]
# realimentacao r5 -> entrada
w(d, (x, 0.0), (x + 0.4, 0.0), (x + 0.4, 1.6), (-0.8, 1.6), (-0.8, 0.0))
rot(d, (x / 2, 1.85), 'realimentação (anel)', fs=7, cor='#777')

# ---------------- gerador de pulso ----------------
y2 = -4.5
w(d, (x + 0.4, 0.0), (x + 0.4, -2.6), (-0.8, -2.6), (-0.8, y2), (0.0, y2))
dot(d, (x + 0.4, 0.0))
g = inv(0.0, y2, s=True, nome='XS1')
w(d, (g.out.x, y2), (g.out.x + 0.8, y2))
g = inv(g.out.x + 0.8, y2, nome='XS2')
xs2 = g.out.x + 0.6
w(d, (g.out.x, y2), (xs2 + 0.6, y2))
dot(d, (xs2, y2)); rot(d, (xs2, y2 + 0.35), 's2', fs=8, cor=AZ)
xx = xs2 + 0.6
for i in range(3):
    g = inv(xx, y2, s=True, nome=f'XD{i+1}')
    xo = g.out.x
    w(d, (xo, y2), (xo + 1.4, y2))
    dot(d, (xo + 0.7, y2))
    cap((xo + 0.7, y2), 'Cd')
    if i == 2:
        rot(d, (xo + 0.7, y2 + 0.35), 'd3', fs=8, cor=AZ)
    xx = xo + 1.4
nd = logic.Nand().theta(0).anchor('in2').at((xx + 0.6, y2)); d.add(nd)
w(d, (xx, y2), (xx + 0.6, y2))
# s2 -> in1 do NAND por cima
w(d, (xs2, y2), (xs2, y2 + 1.4), (nd.in1.x - 0.4, y2 + 1.4), (nd.in1.x - 0.4, nd.in1.y), (nd.in1.x, nd.in1.y))
rot(d, (nd.in1.x - 0.2, y2 + 1.65), 's2', fs=8, cor=AZ)
rot(d, ((nd.in1.x + nd.out.x) / 2, y2 - 1.0), 'NAND', fs=7, cor='#555')
xp = nd.out.x
w(d, (xp, nd.out.y), (xp + 0.7, nd.out.y))
rot(d, (xp + 0.35, nd.out.y + 0.35), 'pn', fs=8, cor=AZ)
yb = nd.out.y
g = inv(xp + 0.7, yb, nome='XB1')
for nome in ('XB2', 'XB3'):
    w(d, (g.out.x, yb), (g.out.x + 0.6, yb))
    g = inv(g.out.x + 0.6, yb, nome=nome)
w(d, (g.out.x, yb), (g.out.x + 1.0, yb))
d.add(elm.Dot(radius=0.11, open=True).theta(0).at((g.out.x + 1.0, yb))
      .label('CLK → gate da chave do Boost', loc='right', fontsize=FS, color='#d1495b'))

caixa(d, -1.2, 2.3, x + 0.8, -2.2)
rot(d, (-1.0, -2.0), 'anel: define f ≈ 53 kHz', fs=8, cor='#777', halign='left')
caixa(d, -1.2, -2.35, xx + 0.3, -7.3)
rot(d, (xx + 0.1, -7.05), 'atraso: define t_on ≈ 750 ns', fs=8, cor='#777', halign='right')

# ---------------- detalhe: inversor current-starved ----------------
yi = -9.0
x0 = 1.5
rot(d, (-1.2, yi + 0.6), 'Detalhe: inversor “S” (current-starved)', halign='left', fs=9)
rot(d, (x0, yi + 0.1), 'VDD', fs=8)
P(d, x0, yi - 0.2, gate='left', nome='P 1/1', lado='right')
w(d, (x0, yi - 1.7), (x0, yi - 2.2))
N(d, x0, yi - 2.2, gate='left', nome='N 1/1', lado='right')
N(d, x0, yi - 3.7, gate='left', nome='nativo 10/2 (anel) ou 10/0,9 (atraso)', nativo=True, lado='right')
w(d, (x0 - 1.37, yi - 4.45), (x0 - 1.37, yi - 5.2), (x0, yi - 5.2)); gnd(d, (x0, yi - 5.2))
w(d, (x0 - 1.37, yi - 0.95), (x0 - 1.8, yi - 0.95), (x0 - 1.8, yi - 2.95), (x0 - 1.37, yi - 2.95))
dot(d, (x0 - 1.8, yi - 1.95), 'a', loc='left')
dot(d, (x0, yi - 1.95))
w(d, (x0, yi - 1.95), (x0 + 2.2, yi - 1.95)); dot(d, (x0 + 2.2, yi - 1.95), 'y', loc='right')
notas = [
    'O NMOS nativo com Vgs = 0 limita a corrente de descida a ~160 nA, sem precisar de circuito de bias.',
    'Isso fixa o atraso de cada estágio (t ≈ C·VDD / 2I) e, principalmente, limita a corrente de',
    'curto-circuito (crowbar) — que domina o consumo quando as bordas são lentas (µs).',
    'Resultado (com o gate da chave): 8 µW com inversores comuns → 1,2 µW (v1: VDD 2,2 V, 101 kHz)',
    '   → 0,22 µW (v2: VDD 1,8 V e nativo do anel com L = 2 µm: f cai à metade e o crowbar também).',
    '',
    'Pulso: CLK = s2 AND (s2 atrasado e invertido) → um pulso de largura t_on a cada ciclo do anel.',
    'Cr = 0,08 pF (5×)   Cd = 0,042 pF (3×)   nativo do anel 10/2 µm, da cadeia de atraso 10/0,9 µm',
    'NAND 2/0,5   buffers XB1–XB3: 2/4, 6/12, 20/40 µm (N/P), L = 0,5 µm',
]
for i, t in enumerate(notas):
    rot(d, (6.5, yi - 0.3 - 0.45 * i), t, halign='left', fs=8, cor='#333')
salvar_esq(d, 'osc')
