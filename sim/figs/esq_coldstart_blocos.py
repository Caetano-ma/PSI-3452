"""Esquematico do Cold-Start dividido em blocos (guia para redesenhar no Virtuoso).

Cada bloco e desenhado isolado; as ligacoes entre blocos sao feitas por nome
de rede (wire label), como no Virtuoso. Gera 1_cold_start/esquematico_blocos.png.
"""
from util import *

AZ = '#1f5fa8'    # redes internas (wire labels)
VM = '#d1495b'    # pinos do bloco
CX = '#7a7a7a'    # caixas

d = desenho()


class Bloco:
    """Desenha em coordenadas locais deslocadas por (ox, oy)."""

    def __init__(self, ox, oy, larg, alt, titulo, sub):
        self.ox, self.oy = ox, oy
        caixa(d, ox, oy, ox + larg, oy - alt, cor=CX)
        rot(d, (ox + 0.25, oy - 0.4), titulo, halign='left', fs=10)
        rot(d, (ox + 0.25, oy - 0.85), sub, halign='left', fs=7, cor='#555')

    def p(self, x, y):
        return (self.ox + x, self.oy + y)

    def N(self, x, y, **kw):
        return N(d, self.ox + x, self.oy + y, **kw)

    def P(self, x, y, **kw):
        return P(d, self.ox + x, self.oy + y, **kw)

    def w(self, *pts):
        w(d, *[self.p(*q) for q in pts])

    def dot(self, x, y):
        dot(d, self.p(x, y))

    def gnd(self, x, y):
        gnd(d, self.p(x, y))

    def rede(self, x, y, txt, ha='center', va='center'):
        rot(d, self.p(x, y), txt, halign=ha, valign=va, fs=9, cor=AZ)

    def pino(self, x, y, txt, ha='center', va='center'):
        d.add(elm.Dot(radius=0.1, open=True).theta(0).at(self.p(x, y)))
        dx = {'left': 0.2, 'right': -0.2, 'center': 0}[ha]
        dy = {'bottom': 0.22, 'top': -0.22, 'center': 0}[va]
        rot(d, self.p(x + dx, y + dy), txt, halign=ha, valign=va, fs=9, cor=VM)

    def txt(self, x, y, t, ha='left', fs=7, cor='#555'):
        rot(d, self.p(x, y), t, halign=ha, fs=fs, cor=cor)


rot(d, (0, 1.6), 'Cold-Start (v2) dividido em blocos: guia para o Virtuoso', halign='left', fs=13)
rot(d, (0, 0.95),
    'Azul = rede interna (wire label: mesmo nome = mesmo fio)  •  vermelho = pino do bloco  •  '
    'traço vermelho = NMOS nativo  •  W/L em µm, nf = 1  •  bulk: todo PMOS em VS, todo NMOS em GND',
    halign='left', fs=8, cor='#555')

# =========================================================== A: inversores
A = Bloco(0, 0, 13.0, 7.0, 'A. Inversores de controle', 'alimentados por VS (não por VBAT)')
for x, ent, sai, np_, nn in ((3.2, 'CTRL_LOW', 'nlow', 'XILP', 'XILN'),
                             (10.0, 'CTRL_HIGH', 'nhigh', 'XIHP', 'XIHN')):
    A.rede(x, -1.55, 'VS', va='bottom')
    A.w((x, -1.6), (x, -1.9))
    A.P(x, -1.9, gate='left', nome=np_, wl='pmoshv 1/1')
    A.N(x, -3.4, gate='left', nome=nn, wl='nmoshv 1/1')
    A.gnd(x, -4.9)
    g = x - 1.37
    A.w((g, -2.65), (g, -4.15))
    A.dot(g, -3.4)
    A.w((g - 1.0, -3.4), (g, -3.4))
    A.pino(g - 1.0, -3.4, ent, ha='center', va='top')
    A.dot(x, -3.4)
    A.w((x, -3.4), (x + 2.0, -3.4))
    A.rede(x + 2.1, -3.4, sai, ha='left')

# =========================================================== B: selecao de fonte
B = Bloco(13.5, 0, 12.0, 7.0, 'B. Seleção de fonte', 'gera VS a partir do TRIGGER ou da VBAT')
B.pino(3.5, -1.5, 'TRIGGER', va='bottom')
d.add(elm.Diode().at(B.p(3.5, -1.5)).down().to(B.p(3.5, -3.1)))
B.txt(2.95, -2.0, 'DTR  diodevdd_2kv', ha='right', fs=8, cor='#111')
B.txt(2.95, -2.4, 'PAD = TRIGGER', ha='right')
B.txt(2.95, -2.75, 'VDD = trd   VSS = GND', ha='right')
B.dot(3.5, -3.1)
B.rede(3.75, -3.1, 'trd', ha='left')
B.w((3.5, -3.1), (3.5, -3.3))
B.P(3.5, -3.3, gate='left', nome='XST', wl='pmoshv 10/0,5')
B.w((2.13, -4.05), (1.8, -4.05))
B.pino(1.8, -4.05, 'CTRL_LOW', ha='right', va='top')
B.pino(9.5, -2.4, 'VBAT', va='bottom')
B.w((9.5, -2.4), (9.5, -3.3))
B.P(9.5, -3.3, gate='right', nome='XSB', wl='pmoshv 10/0,5')
B.w((10.87, -4.05), (11.1, -4.05))
B.rede(11.15, -4.05, 'nlow', ha='left')
B.w((3.5, -4.8), (3.5, -5.5), (9.5, -5.5), (9.5, -4.8))
B.dot(6.5, -5.5)
B.w((6.5, -5.5), (6.5, -6.1))
B.rede(6.5, -6.2, 'VS', va='top')
B.txt(6.5, -5.2, 'n-well das duas chaves = VS', ha='center')

# =========================================================== C: fonte de nA + espelho
C = Bloco(26.0, 0, 12.0, 7.0, 'C. Fonte de nA + espelho PMOS',
          'XPB, XPM e XPD juntos no layout (mesma orientação; XPD tem L = 8)')
C.rede(0.6, -1.6, 'VS', ha='left')
C.w((1.1, -1.6), (10.0, -1.6))
for x in (2.5, 6.0, 10.0):
    C.dot(x, -1.6)
C.P(2.5, -1.6, gate='right', nome='XPB', wl='pmoshv 2/4', lado='left')
C.P(6.0, -1.6, gate='left', nome='XPM', wl='pmoshv 2/4')
C.P(10.0, -1.6, gate='left', nome='XPD', wl='pmoshv 1/8')
C.w((3.87, -2.35), (4.63, -2.35))
C.dot(4.25, -2.35)
C.w((2.5, -3.1), (2.5, -3.9))
C.dot(2.5, -3.4)
C.w((2.5, -3.4), (4.25, -3.4), (4.25, -2.35))
C.rede(4.4, -3.4, 'nb', ha='left')
C.N(2.5, -3.9, gate='left', nome='XMB', wl='nativo 10/4', nativo=True)
C.w((1.13, -4.65), (1.13, -5.6), (2.5, -5.6))
C.w((2.5, -5.4), (2.5, -5.6))
C.gnd(2.5, -5.6)
C.txt(3.1, -5.7, 'Vgs = 0  →  ~10 nA')
C.w((8.63, -2.35), (8.2, -2.35))
C.rede(8.1, -2.35, 'nb', ha='right')
C.w((6.0, -3.1), (6.0, -4.3))
C.rede(6.0, -4.4, 'VG', va='top')
C.txt(6.0, -4.95, '~10 nA para a pilha', ha='center')
C.w((10.0, -3.1), (10.0, -4.3))
C.rede(10.0, -4.4, 'dk', va='top')
C.txt(10.0, -4.95, '~6 nA para o detector', ha='center')

# =========================================================== D: pilha de diodos
D = Bloco(0, -7.5, 6.5, 8.0, 'D. Pilha de diodos', 'define VG ≈ 2,27 V')
D.rede(2.8, -1.2, 'VG', va='bottom')
D.w((2.8, -1.25), (2.8, -1.6))
for i, y in enumerate((-1.6, -3.6, -5.6)):
    D.N(2.8, y, gate='left', nome=f'XD{i + 1}', wl='nmoshv 6/1')
    D.w((1.43, y - 0.75), (1.43, y + 0.25), (2.8, y + 0.25))
    D.dot(2.8, y + 0.25)
    if i < 2:
        D.w((2.8, y - 1.5), (2.8, y - 2.0))
D.gnd(2.8, -7.1)

# =========================================================== E: seguidor
E = Bloco(7.0, -7.5, 7.5, 8.0, 'E. Seguidor de fonte', 'VDD = VG − Vgs ≈ 1,83 V')
E.rede(3.5, -1.3, 'VS', va='bottom')
E.w((3.5, -1.35), (3.5, -2.0))
E.N(3.5, -2.0, gate='left', nome='XMF', wl='nativo 10/4', nativo=True)
E.w((2.13, -2.75), (1.4, -2.75))
E.rede(1.3, -2.75, 'VG', ha='right')
E.w((3.5, -3.5), (3.5, -4.3), (5.6, -4.3))
E.pino(5.6, -4.3, 'VDD', va='bottom')
E.txt(0.3, -5.6, 'saída do bloco → oscilador', fs=8, cor='#111')
E.txt(0.3, -6.1, 'Cvdd = 10 pF de VDD ao GND fica FORA')
E.txt(0.3, -6.5, 'do Cold-Start (nível do chip / testbench)')
E.txt(0.3, -7.2, 'L = 4 limita a fuga com Vgs = 0 a ~10 nA')

# =========================================================== F: desligamento
F = Bloco(15.0, -7.5, 11.5, 8.0, 'F. Desligamento (estado 0-1)', 'zera VG e VDD se CTRL_LOW = 1 e CTRL_HIGH = 0')
for x, topo, meio, n1, n2 in ((2.8, 'VG', 'kx', 'XK1', 'XK2'), (8.0, 'VDD', 'kz', 'XK3', 'XK4')):
    F.rede(x, -1.3, topo, va='bottom')
    F.w((x, -1.35), (x, -2.0))
    F.N(x, -2.0, gate='right', nome=n1, wl='nmoshv 1/0,5', lado='left')
    F.N(x, -3.5, gate='right', nome=n2, wl='nmoshv 1/0,5', lado='left')
    F.rede(x - 0.25, -3.5, meio, ha='right')
    F.gnd(x, -5.0)
    F.w((x + 1.37, -2.75), (x + 1.6, -2.75))
    F.pino(x + 1.6, -2.75, 'CTRL_LOW', ha='left', va='bottom')
    F.w((x + 1.37, -4.25), (x + 1.6, -4.25))
    F.rede(x + 1.7, -4.25, 'nhigh', ha='left')

# =========================================================== G: detector de escuro
G = Bloco(27.0, -7.5, 11.0, 8.0, 'G. Detector de escuro', 'sem luz: dk alto → zera VG e VDD')
G.rede(3.4, -1.3, 'dk', va='bottom')
G.w((3.4, -1.35), (3.4, -2.0))
G.N(3.4, -2.0, gate='left', nome='XLD', wl='nmoshv 40/0,5')
G.w((2.03, -2.75), (1.4, -2.75))
G.pino(1.4, -2.75, 'VIN_DC', ha='right', va='top')
G.gnd(3.4, -3.5)
G.txt(0.3, -5.6, 'liga com VIN_DC > ~0,36 V e vence', fs=7)
G.txt(0.3, -6.0, 'os ~6 nA que XPD injeta em dk', fs=7)
for x, topo, nome in ((7.4, 'VG', 'XKD1'), (9.9, 'VDD', 'XKD2')):
    G.rede(x, -1.3, topo, va='bottom')
    G.w((x, -1.35), (x, -2.0))
    G.N(x, -2.0, gate='left', nome=nome, wl='', lado='none')
    G.txt(x, -4.5, nome, ha='center', fs=8, cor='#111')
    G.txt(x, -4.9, 'nmoshv 1/0,5', ha='center')
    G.w((x - 1.37, -2.75), (x - 1.6, -2.75))
    G.rede(x - 1.7, -2.75, 'dk', ha='right')
    G.gnd(x, -3.5)

# =========================================================== tabela de redes
linhas = [
    ('Rede', 'Sai de', 'Vai para', ''),
    ('VS', 'B', 'A, C, E', 'alimentação interna (fonte selecionada)'),
    ('nlow / nhigh', 'A', 'B / F', 'CTRL_LOW e CTRL_HIGH invertidos'),
    ('VG', 'C (XPM)', 'D, E, F (XK1), G (XKD1)', 'gate do seguidor'),
    ('dk', 'C (XPD)', 'G', 'escuro = alto'),
    ('VDD', 'E', 'F (XK3), G (XKD2), pino', 'saída do Cold-Start'),
    ('nb, trd, kx, kz, n1, n2', '—', '—', 'internas a um único bloco'),
    ('Pinos', '', 'VBAT, TRIGGER, CTRL_LOW, CTRL_HIGH, VIN_DC, VDD, GND', ''),
]
y0 = -16.4
rot(d, (0, y0), 'Ligações entre blocos (no Virtuoso: wire labels com estes nomes, sem fios cruzando a folha)',
    halign='left', fs=10)
cols = (0.2, 7.0, 11.0, 20.0)
for i, ln in enumerate(linhas):
    y = y0 - 0.65 - 0.48 * i
    for c, t in zip(cols, ln):
        rot(d, (c, y), t, halign='left', fs=8, cor='#111' if i == 0 else '#333')

salvar_esq(d, 'cs', 'esquematico_blocos.png')
