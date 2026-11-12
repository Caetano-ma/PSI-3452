"""Utilitarios comuns: leitura dos dados do ngspice, pastas de saida e
helpers de desenho de esquematicos (schemdraw)."""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

BASE = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(BASE, 'dados')
RAIZ = os.path.abspath(os.path.join(BASE, '..', '..'))

PASTAS = {
    'cs':    '1_cold_start',
    'osc':   '2_oscilador',
    'ref':   '3_referencia_de_tensao',
    'comp':  '4_comparador',
    'thr':   '5_battery_threshold_control',
    'boost': '6_boost',
    'int':   'integração',
}


def saida(chave, arquivo):
    p = os.path.join(RAIZ, PASTAS[chave])
    os.makedirs(p, exist_ok=True)
    return os.path.join(p, arquivo)


def ler(nome):
    """Le um arquivo do wrdata (com wr_vecnames e wr_singlescale)."""
    caminho = os.path.join(DADOS, nome)
    with open(caminho) as f:
        hdr = f.readline().split()
    d = np.loadtxt(caminho, skiprows=1)
    out = {h: d[:, i] for i, h in enumerate(hdr)}
    out['_x'] = d[:, 0]
    return out


# ------------------------------------------------------------------ graficos
plt.rcParams.update({
    'figure.dpi': 110, 'savefig.dpi': 160, 'font.size': 10,
    'axes.grid': True, 'grid.alpha': 0.35, 'axes.titlesize': 11,
    'axes.titleweight': 'bold', 'legend.fontsize': 9,
    'figure.constrained_layout.use': True,
})
C = ['#1f5fa8', '#d1495b', '#2a9d5c', '#e09f1f', '#7b4fb0', '#555555']


def salvar(fig, chave, arquivo):
    caminho = saida(chave, arquivo)
    fig.savefig(caminho)
    plt.close(fig)
    print('  ->', os.path.relpath(caminho, RAIZ))


# -------------------------------------------------------------- esquematicos
schemdraw.use('matplotlib')
FS = 9      # fonte dos rotulos


def desenho():
    d = schemdraw.Drawing(show=False)
    d.config(fontsize=FS, lw=1.3)
    return d


def _rotulo_fet(d, x, y, gate, txt, wl, lado):
    if lado == 'auto':
        lado = 'right' if gate == 'left' else 'left'
    if lado == 'none' or not (txt or wl):
        return
    dx = 0.25 if lado == 'right' else -0.25
    ha = 'left' if lado == 'right' else 'right'
    if txt:
        d.add(elm.Label().theta(0).at((x + dx, y - 0.5))
              .label(txt, fontsize=FS - 1, halign=ha))
    if wl:
        d.add(elm.Label().theta(0).at((x + dx, y - 1.0))
              .label(wl, fontsize=FS - 2, color='#555', halign=ha))


def N(d, x, y, gate='left', nome='', wl='', nativo=False, lado='auto'):
    """NMOS com dreno em (x, y) e fonte em (x, y-1.5); gate em x-+1.37."""
    e = elm.NFet().theta(0).at((x, y))
    if gate == 'left':
        e = e.reverse()
    d.add(e)
    if nativo:
        # marca de dispositivo nativo: canal grosso (retangulo cheio)
        sx = -1 if gate == 'left' else 1
        d.add(elm.Line(lw=3.2, color='#c0392b').at((x + sx * 0.62, y - 0.42))
              .to((x + sx * 0.62, y - 1.08)))
    _rotulo_fet(d, x, y, gate, nome, wl, lado)
    return e


def P(d, x, y, gate='left', nome='', wl='', lado='auto'):
    """PMOS com fonte em (x, y) e dreno em (x, y-1.5); gate em x-+1.37."""
    e = elm.PFet().theta(0).at((x, y))
    if gate == 'left':
        e = e.reverse()
    d.add(e)
    _rotulo_fet(d, x, y, gate, nome, wl, lado)
    return e


def w(d, *pts, **kw):
    """Fio poligonal passando pelos pontos."""
    for a, b in zip(pts[:-1], pts[1:]):
        d.add(elm.Line(**kw).at(a).to(b))


def dot(d, p, txt=None, loc='top'):
    e = elm.Dot(radius=0.07).theta(0).at(p)
    if txt:
        e = e.label(txt, loc=loc, fontsize=FS)
    d.add(e)


def gnd(d, p):
    d.add(elm.Ground().theta(0).at(p))


def vdd(d, p, txt='VBAT'):
    d.add(elm.Vdd().theta(0).at(p).label(txt, fontsize=FS))


def rot(d, p, txt, halign='center', valign='center', cor='#111', fs=FS, **kw):
    d.add(elm.Label().theta(0).at(p).label(txt, fontsize=fs, color=cor,
                                  halign=halign, valign=valign, **kw))


def caixa(d, x0, y0, x1, y1, cor='#888', ls='--', lw=1.0):
    for a, b in [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)),
                 ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]:
        d.add(elm.Line(color=cor, ls=ls, lw=lw).at(a).to(b))


def salvar_esq(d, chave, arquivo='esquematico.png'):
    caminho = saida(chave, arquivo)
    d.save(caminho, dpi=170)
    print('  ->', os.path.relpath(caminho, RAIZ))


class _Pt:
    def __init__(self, x, y):
        self.x, self.y = x, y


class Inversor:
    """Simbolo de inversor desenhado a mao: entrada em (x, y), saida em (x+1.0, y)."""
    def __init__(self, d, x, y):
        h = 0.42
        for a, b in [((x, y + h), (x, y - h)), ((x, y + h), (x + 0.78, y)),
                     ((x, y - h), (x + 0.78, y))]:
            d.add(elm.Line().at(a).to(b))
        d.add(elm.Dot(radius=0.1, open=True).theta(0).at((x + 0.88, y)))
        d.add(elm.Line().at((x + 0.98, y)).to((x + 1.0, y)))
        self.in1 = _Pt(x, y)
        self.out = _Pt(x + 1.0, y)
