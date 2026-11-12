"""Esquematico de integracao: os 4 blocos, as ligacoes entre eles e os externos."""
from util import *

d = desenho()
rot(d, (-4.0, 6.2), 'Integração (v2): carregador fotovoltaico completo', halign='left', fs=13)
rot(d, (-4.0, 5.6), 'Ligações elétricas entre os blocos (conforme o diagrama de blocos) e componentes externos',
    halign='left', fs=8, cor='#555')

VERM = '#d1495b'
AZ = '#1f5fa8'


def bloco(x0, y0, x1, y1, titulo, sub, cor, ty=0.45):
    caixa(d, x0, y0, x1, y1, cor=cor, ls='-', lw=1.8)
    rot(d, ((x0 + x1) / 2, y0 - ty), titulo, fs=10, cor=cor)
    rot(d, ((x0 + x1) / 2, y0 - ty - 0.5), sub, fs=7, cor='#555')


def pin(p, txt, ha='left', dy=0.0, dx=0.15):
    dot(d, p)
    rot(d, (p[0] + (dx if ha == 'left' else -dx), p[1] + dy), txt, fs=7, cor='#333', halign=ha)


def vbat_rot(p, para='left'):
    """rotulo de rede VBAT (mesma rede da bateria)."""
    x2 = p[0] - 0.8 if para == 'left' else p[0] + 0.8
    w(d, p, (x2, p[1]), color=VERM)
    rot(d, (x2 - 0.1 if para == 'left' else x2 + 0.1, p[1]), 'VBAT', fs=8, cor=VERM,
        halign='right' if para == 'left' else 'left')


# fronteira do CI
caixa(d, -1.8, 2.2, 16.2, -12.6, cor='#777', ls='--', lw=1.2)
rot(d, (-1.6, -12.3), 'CI CMOS 130 nm (simulado com SKY130)', fs=8, cor='#777', halign='left')

# ---------------- blocos ----------------
bloco(0, 0, 4.2, -5, 'Cold-Start', 'fonte + regulador + det. de escuro', '#2a9d5c')
bloco(6, -1.3, 9.2, -3.9, 'Oscilador', 'anel + pulso t_on', '#e09f1f')
bloco(11, 0, 15, -4, 'Boost', 'chave NMOS (diodo externo)', '#7b4fb0')
bloco(3, -8, 13.5, -11.4, 'Battery Threshold Control', 'ref. 2T + 2 comparadores + histerese', AZ, ty=1.3)

# pinos do Cold-Start
pin((0, -1.6), 'VBAT'); pin((0, -2.8), 'TRIGGER')
pin((1.4, -5), 'CTRL_LOW', dy=0.3, dx=0.0); pin((3.2, -5), 'CTRL_HIGH', dy=0.6, dx=-0.6)
pin((4.2, -2.6), 'VDD', ha='right'); pin((3.7, 0), 'VIN_DC', dy=-0.35, dx=-0.1, ha='right')
# Oscilador
pin((6, -2.6), 'VDD'); pin((9.2, -2.6), 'CLK', ha='right')
# Boost
pin((11.6, 0), 'LBST', dy=-0.35, dx=0.15); pin((11, -2.6), 'CLK')
# Threshold
pin((4.5, -8), 'VBAT', dy=-0.35)
pin((8.0, -8), 'CTRL_LOW', dy=-0.35); pin((10.5, -8), 'CTRL_HIGH', dy=-0.35)
for x, n in zip((4.0, 6.2, 8.4, 10.6, 12.8), ('T_R', 'T_DH', 'T_D', 'T_U', 'T_UH')):
    pin((x, -11.4), n, dy=0.35, dx=0.0)

# ---------------- ligacoes internas ----------------
w(d, (4.2, -2.6), (6, -2.6)); rot(d, (5.1, -2.35), 'VDD', fs=8, cor=AZ)
w(d, (9.2, -2.6), (11, -2.6)); rot(d, (10.1, -2.35), 'CLK', fs=8, cor=AZ)
w(d, (8.0, -8), (8.0, -6.6), (1.4, -6.6), (1.4, -5))
w(d, (10.5, -8), (10.5, -6.0), (3.2, -6.0), (3.2, -5))
rot(d, (5.5, -6.85), 'CTRL_LOW (ativo-baixo)', fs=7, cor=AZ)
rot(d, (6.8, -5.75), 'CTRL_HIGH (ativo-baixo)', fs=7, cor=AZ)
vbat_rot((0, -1.6), 'left')
vbat_rot((4.5, -8), 'left')
w(d, (0, -2.8), (-2.8, -2.8))

# ---------------- externos ----------------
# TRIGGER
d.add(elm.SourceV().at((-2.8, -5.8)).up().to((-2.8, -2.8)).label('TRIGGER\n(fonte de\npartida)', loc='bottom', fontsize=FS - 1))
gnd(d, (-2.8, -5.8))
# celula + Cin + L
d.add(elm.SourceI().at((5.2, 2.8)).up().to((5.2, 4.8)).label('célula FV\n0,4–0,8 V', loc='bottom', fontsize=FS - 1))
gnd(d, (5.2, 2.8))
w(d, (5.2, 4.8), (8.0, 4.8)); dot(d, (7.2, 4.8), 'VIN_DC', loc='top')
d.add(elm.Capacitor().at((7.2, 4.8)).down().to((7.2, 3.0)).label('Cin', loc='bottom', fontsize=FS - 1))
gnd(d, (7.2, 3.0))
d.add(elm.Inductor2(loops=4).at((8.0, 4.8)).right().to((11.0, 4.8)).label('L 220 µH', loc='top', fontsize=FS - 1))
w(d, (11.0, 4.8), (11.6, 4.8), (11.6, 0))
dot(d, (11.6, 4.8))
d.add(elm.Diode().at((11.6, 4.8)).right().to((14.6, 4.8)).label('Schottky externo (v2)', loc='top', fontsize=FS - 1, color=AZ))
w(d, (14.6, 4.8), (18.2, 4.8), (18.2, -1.6))
rot(d, (16.4, 5.1), 'VSTOR', fs=8, cor=VERM)
# VIN_DC tambem entra no Cold-Start (detector de escuro, v2)
w(d, (3.7, 0), (3.7, 5.5), (6.4, 5.5), (6.4, 4.8), color=AZ)
dot(d, (6.4, 4.8))
rot(d, (3.85, 1.2), 'VIN_DC → detector' + chr(10) + 'de escuro (v2)', fs=7, cor=AZ, halign='left')
# bateria
w(d, (17.0, -1.6), (18.2, -1.6))
dot(d, (17.0, -1.6))
d.add(elm.Capacitor().at((17.0, -1.6)).down().to((17.0, -3.6)).label('Cout', loc='bottom', fontsize=FS - 1))
gnd(d, (17.0, -3.6))
d.add(elm.Battery().at((18.2, -4.4)).up().to((18.2, -1.6)).label('Li-ion', loc='bottom', fontsize=FS - 1))
gnd(d, (18.2, -4.4))
rot(d, (18.5, -0.9), 'VBAT', fs=8, cor=VERM, halign='left')
# divisor externo
y = -13.6
for x in (4.0, 6.2, 8.4, 10.6, 12.8):
    w(d, (x, -11.4), (x, y)); dot(d, (x, y))
for (x0, x1, n) in ((4.0, 6.2, 'R1'), (6.2, 8.4, 'Rhd'), (8.4, 10.6, 'R2'), (10.6, 12.8, 'Rhu'), (12.8, 15.0, 'R3')):
    d.add(elm.Resistor().at((x0, y)).right().to((x1, y)).label(n, loc='bottom', fontsize=FS - 1))
gnd(d, (15.0, y))
rot(d, (9.5, -14.6), 'divisor externo (≈ 100 MΩ na v2): limites 4,2/4,1 V e 3,0/3,1 V', fs=7, cor='#555')

notas = [
    'Fluxo:  célula → L → [Boost] → Schottky → VSTOR = VBAT (bateria).   [Threshold] mede VBAT pelo divisor → CTRL_LOW / CTRL_HIGH → [Cold-Start]',
    '        → VDD (1,8 V) → [Oscilador] → CLK (pulsos de 751 ns a 52,7 kHz) → chave do [Boost].',
    'Sem luz (VIN_DC < ~0,36 V) → o detector de escuro do Cold-Start desliga VDD → o oscilador não gasta a bateria à noite (v2).',
    'VBAT > 4,2 V → CTRL_HIGH = 0 → Cold-Start desliga VDD → CLK = 0 → boost para (sem precisar de enable).',
    'VBAT < 3,0 V → CTRL_LOW = 0 → Cold-Start passa a se alimentar do TRIGGER.   Tudo em 0 V → estado 1-1 → partida pelo TRIGGER.',
    'Rótulos vermelhos “VBAT” = mesma rede (terminal + da bateria).',
]
for i, t in enumerate(notas):
    rot(d, (-4.0, -15.6 - 0.45 * i), t, halign='left', fs=8, cor='#333')
salvar_esq(d, 'int')
