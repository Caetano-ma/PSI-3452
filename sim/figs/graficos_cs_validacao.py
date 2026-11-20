"""Graficos de validacao do Cold-Start, bloco a bloco (A..G) e do modulo.
Dados: sim/figs/tb/csv_*.spice -> sim/figs/dados/csv_*.txt
Saida: 1_cold_start/validacao/
"""
from util import *

nA, uA, ms = 1e9, 1e6, 1e3
CANTOS = ['tt', 'ff', 'ss', 'fs', 'sf']
COR_CANTO = {'tt': 'k', 'ff': C[1], 'ss': C[0], 'fs': C[3], 'sf': C[4]}


def at(d, k, x):
    return float(np.interp(x, d['_x'], d[k]))


def nota(a, x, y, txt, **kw):
    kw.setdefault('fontsize', 8)
    kw.setdefault('color', '#333')
    a.text(x, y, txt, **kw)


def caixa_ok(a, txt, loc=(0.02, 0.97), va='top', ha='left'):
    """caixa com o criterio de aprovacao."""
    a.text(*loc, txt, transform=a.transAxes, fontsize=7.5, va=va, ha=ha,
           bbox=dict(boxstyle='round,pad=0.35', fc='#eef6ee', ec=C[2], lw=0.8))


# ------------------------------------------------------------------- A
def bloco_A():
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.3))
    for i, v in enumerate(['2.0', '3.3', '3.7', '4.3']):
        d = ler(f'csv_A_{v}.txt'); x = d['_x']; vs = float(v)
        m = x <= vs
        y = d['v(nlow)']
        vm = x[np.argmin(abs(y - x))]
        ax[0].plot(x[m], y[m], color=C[i], lw=1.8, label=f'VS = {vs:.1f} V   (Vm = {vm:.2f} V)')
        ax[0].plot(vm, vm, 'o', color=C[i], ms=4)
        ax[1].plot(x[m], np.maximum(d['is'][m], 1e-13) * uA, color=C[i], lw=1.5, label=f'VS = {vs:.1f} V')
    ax[0].plot([0, 4.3], [0, 4.3], color='#aaa', lw=0.8, ls=':')
    ax[0].set(xlabel='CTRL_LOW (= CTRL_HIGH) (V)', ylabel='nlow, nhigh (V)',
              title='A. Transferência dos inversores (DC sweep da entrada)')
    ax[0].legend(fontsize=8, loc='upper right')
    caixa_ok(ax[0], 'OK se: saída = VS com entrada 0 e = 0 com entrada VS;\n'
             'Vm ≈ 0,4·VS (≈ 1,5 V com VS = 3,7 V);\nnlow e nhigh idênticas', loc=(0.50, 0.15), va='bottom')
    ax[1].set(yscale='log', ylim=(1e-7, 300), xlabel='CTRL_LOW (= CTRL_HIGH) (V)',
              ylabel='corrente de VS (µA)', title='A. Consumo: só na transição (pico) e ~pA parado')
    ax[1].legend(fontsize=8, loc='upper right')
    caixa_ok(ax[1], 'OK se: nos extremos (0 e VS) < 1 nA;\npico ~50 µA (VS = 3,7 V) só durante a\n'
             'transição: as bordas de CTRL devem ser rápidas', loc=(0.02, 0.03), va='bottom')
    fig.suptitle('Bloco A: cs_inv_ctrl  (fonte VS ideal; CTRL_LOW e CTRL_HIGH ligados à mesma fonte)', fontweight='bold')
    salvar(fig, 'csv', 'A_inversores.png')


# ------------------------------------------------------------------- B
def bloco_B():
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))
    tit = ['B1. Normal: CTRL_LOW = VBAT (nlow = 0)\nTRIGGER = 0 V (ausente)',
           'B2. LOW ativo: CTRL_LOW = 0 (nlow = VS)\nTRIGGER = 3,3 V, varre VBAT',
           'B3. Bateria morta: VBAT = 0, LOW ativo\nvarre TRIGGER']
    xl = ['VBAT (V)', 'VBAT (V)', 'TRIGGER (V)']
    for i, n in enumerate(['B1', 'B2', 'B3']):
        d = ler(f'csv_{n}.txt'); x = d['_x']; a = ax[i]
        a.plot(x, d['v(vs)'], color=C[5], lw=2, label='VS')
        a.plot(x, x, color='#bbb', lw=0.8, ls=':')
        a.set(xlabel=xl[i], ylabel='VS (V)', ylim=(-0.1, 4.6), title=tit[i])
        a2 = a.twinx(); a2.grid(False)
        a2.plot(x, d['ib'] * nA, color='k', lw=1.2, ls='--', label='I(VBAT)')
        a2.plot(x, d['it'] * nA, color=C[3], lw=1.2, ls='-.', label='I(TRIGGER)')
        a2.set_ylabel('corrente fornecida (nA)'); a2.set_ylim(-10, 330)
        h1, l1 = a.get_legend_handles_labels(); h2, l2 = a2.get_legend_handles_labels()
        a.legend(h1 + h2, l1 + l2, fontsize=8, loc='upper left')
    d = ler('csv_B2.txt')
    nota(ax[1], 0.2, 2.95, f'VS = TRIGGER − Vdiodo = {at(d, "v(vs)", 1):.2f} V')
    nota(ax[1], 2.3, 1.3, 'VBAT > VS + 0,6 V:\no diodo de corpo de\nXSB conduz →', ha='center')
    caixa_ok(ax[0], 'OK se: VS = VBAT (queda < 10 mV)\ne I(TRIGGER) = 0 (sem retorno)', loc=(0.45, 0.08), va='bottom')
    caixa_ok(ax[1], 'OK se: VS ≈ 2,74 V vindo do TRIGGER\ne I(VBAT) ≈ 0 enquanto VBAT < ~3,2 V', loc=(0.03, 0.10), va='bottom')
    caixa_ok(ax[2], 'OK se: VS = TRIGGER − 0,56 V\ne I(VBAT) = 0', loc=(0.45, 0.08), va='bottom')
    fig.suptitle('Bloco B: cs_sel_fonte  (carga de 15 MΩ em VS ≈ consumo do chip; nlow imposto por fonte: 0 ou vcvs = VS)',
                 fontweight='bold')
    salvar(fig, 'csv', 'B_selecao_de_fonte.png')


# ------------------------------------------------------------------- C
def bloco_C():
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.3))
    d = ler('csv_C_vs.txt'); m = d['_x'] >= 1.4; x = d['_x'][m]
    a = ax[0]
    a.plot(x, d['ipm'][m] * nA, color=C[0], lw=2, label='I(XPM) → VG')
    a.plot(x, d['ipd'][m] * nA, color=C[1], lw=2, label='I(XPD) → dk')
    a.plot(x, d['is'][m] * nA, color='k', lw=1.2, ls='--', label='I(VS) total')
    a.set(xlabel='VS (V)', ylabel='nA', ylim=(0, 32), title='C. Correntes × VS (VG = 1 V, dk = 0,3 V)')
    a.legend(fontsize=8, loc='lower right')
    i37 = (at(d, 'ipm', 3.7) * nA, at(d, 'ipd', 3.7) * nA, at(d, 'is', 3.7) * nA)
    caixa_ok(a, f'OK se (VS = 3,7 V): I(XPM) ≈ {i37[0]:.1f} nA,\nI(XPD) ≈ {i37[1]:.1f} nA, total ≈ {i37[2]:.0f} nA;\n'
             'quase planas para VS > 2,5 V', loc=(0.03, 0.97))
    a = ax[1]
    g = ler('csv_C_vg.txt'); k = ler('csv_C_dk.txt')
    a.plot(g['_x'], g['ipm'] * nA, color=C[0], lw=2, label='I(XPM) × V(VG)')
    a.plot(k['_x'], k['ipd'] * nA, color=C[1], lw=2, label='I(XPD) × V(dk)')
    a.axvline(2.28, color=C[0], ls=':', lw=1); nota(a, 2.32, 1, 'VG de\noperação')
    a.set(xlabel='tensão na saída (V)   [VS = 3,7 V]', ylabel='nA', ylim=(0, 14),
          title='C. Saída como fonte de corrente (compliance)')
    a.legend(fontsize=8, loc='upper right')
    caixa_ok(a, 'OK se: a corrente varia < 15 %\nde 0 V até ~3,3 V na saída', loc=(0.03, 0.03), va='bottom')
    a = ax[2]
    t = ler('csv_C_temp.txt')
    a.plot(t['_x'], t['ipm'] * nA, color=C[0], lw=2, label='I(XPM)')
    a.plot(t['_x'], t['ipd'] * nA, color=C[1], lw=2, label='I(XPD)')
    a.plot(t['_x'], t['is'] * nA, color='k', lw=1.2, ls='--', label='I(VS)')
    a.set(yscale='log', xlabel='temperatura (°C)', ylabel='nA', title='C. × temperatura (VS = 3,7 V)')
    a.legend(fontsize=8, loc='lower right')
    caixa_ok(a, 'Esperado: sobe ~exponencialmente\n(nativo em sublimiar): ~1 nA a −20 °C,\n~70 nA a 85 °C. É normal.',
             loc=(0.03, 0.97))
    fig.suptitle('Bloco C: cs_bias_na  (VS, VG e dk forçados por fontes de tensão; a corrente medida é a que entra nelas)',
                 fontweight='bold')
    salvar(fig, 'csv', 'C_fonte_nA_espelho.png')


# ------------------------------------------------------------------- D
def bloco_D():
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.3))
    d = ler('csv_D_iv.txt'); a = ax[0]
    a.plot(d['_x'], np.maximum(d['ig'], 1e-15) * nA, color=C[0], lw=2)
    vop = np.interp(np.log10(10.5e-9), np.log10(np.maximum(d['ig'], 1e-18)), d['_x'])
    a.plot(vop, 10.5, 'o', color=C[1]); a.axhline(10.5, color=C[1], lw=0.8, ls=':')
    nota(a, vop - 0.1, 25, f'ponto de operação\n10,5 nA (do bloco C) → VG = {vop:.2f} V', ha='right', color=C[1])
    a.set(yscale='log', ylim=(1e-3, 1e4), xlabel='VG (V)', ylabel='corrente na pilha (nA)',
          title='D. Curva I–V da pilha (DC sweep de VG)')
    caixa_ok(a, 'OK se: ~0,48 V por década de corrente\n(3 diodos em sublimiar, com efeito de corpo)\n'
             'e VG ≈ 2,28 V com 10,5 nA', loc=(0.03, 0.97))
    a = ax[1]
    for i, (c, cor) in enumerate([('3n', C[3]), ('10n', C[1]), ('30n', C[4])]):
        t = ler(f'csv_D_temp_{c}.txt')
        a.plot(t['_x'], t['v(vg)'], color=cor, lw=2, label=f'I = {c[:-1]} nA (fonte ideal)')
    a.set(xlabel='temperatura (°C)', ylabel='VG (V)', title='D. VG × temperatura com corrente FIXA')
    a.legend(fontsize=8, loc='upper right')
    caixa_ok(a, 'Esperado: ≈ −8 mV/°C com corrente fixa.\nNo módulo, a corrente do bloco C sobe com T\n'
             'e compensa: VDD varia só ~0,1 V de −20 a 85 °C', loc=(0.50, 0.12), va='bottom')
    fig.suptitle('Bloco D: cs_ref_pilha  (VG forçado por fonte de tensão / alimentado por fonte de corrente ideal)',
                 fontweight='bold')
    salvar(fig, 'csv', 'D_pilha_de_diodos.png')


# ------------------------------------------------------------------- E
def bloco_E():
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.3))
    a = ax[0]
    for f, lab, cor in [('csv_E_vg_10n.txt', '10 nA', C[3]), ('csv_E_vg.txt', '0,15 µA', C[0]), ('csv_E_vg_2u.txt', '2 µA', C[1])]:
        d = ler(f); a.plot(d['_x'], d['v(vdd)'], color=cor, lw=1.8, label=f'carga {lab}')
    a.plot([0, 3.2], [0, 3.2], color='#bbb', lw=0.8, ls=':')
    d = ler('csv_E_vg.txt'); v = at(d, 'v(vdd)', 2.28)
    a.plot(2.28, v, 'o', color=C[0]); nota(a, 2.35, v - 0.35, f'VG = 2,28 V →\nVDD = {v:.2f} V', color=C[0])
    a.set(xlabel='VG (V)', ylabel='VDD (V)', title='E. VDD × VG (VS = 3,7 V)')
    a.legend(fontsize=8, loc='upper left')
    caixa_ok(a, 'OK se: VDD = VG − ~0,45 V,\ninclinação ≈ 0,87 (efeito de corpo)', loc=(0.45, 0.03), va='bottom')
    a = ax[1]
    d = ler('csv_E_carga.txt')
    a.plot(d['_x'] * uA, d['v(vdd)'], color=C[0], lw=2)
    a.axvline(0.13, color=C[3], ls='--', lw=1); nota(a, 0.5, at(d, 'v(vdd)', 0.13e-6), '← oscilador (~0,13 µA)', color=C[3])
    a.set(xscale='log', xlabel='corrente de carga em VDD (µA)', ylabel='VDD (V)', title='E. Regulação de carga (VG = 2,25 V)')
    caixa_ok(a, 'OK se: cai ~60–80 mV por década\nde carga (sublimiar)', loc=(0.03, 0.03), va='bottom')
    a = ax[2]
    d = ler('csv_E_fuga.txt'); a.plot(d['_x'], d['il'] * nA, color='k', lw=2, label='× VS (27 °C)')
    a.set(xlabel='VS (V)', ylabel='fuga de VS (nA)', yscale='log', ylim=(0.3, 300), title='E. Fuga do seguidor desligado (VG = VDD = 0)')
    t = ler('csv_E_fuga_temp.txt')
    a2 = a.twiny(); a2.grid(False)
    a2.plot(t['_x'], t['il'] * nA, color=C[1], lw=1.5, ls='--')
    a2.set_xlabel('temperatura (°C)  [tracejado, VS = 3,7 V]', color=C[1])
    caixa_ok(a, 'OK se: ~10 nA a 27 °C (nativo com Vgs = 0, L = 4).\nSobe com T (~70 nA a 85 °C)', loc=(0.03, 0.97))
    fig.suptitle('Bloco E: cs_seguidor  (VS = 3,7 V e VG forçados por fontes; carga em VDD por fonte de corrente)',
                 fontweight='bold')
    salvar(fig, 'csv', 'E_seguidor.png')


# ------------------------------------------------------------------- F
def bloco_F():
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.3))
    a = ax[0]
    for c, cor, lab in [('0', C[5], 'CTRL_LOW = 0'), ('3.7', C[1], 'CTRL_LOW = 3,7 V')]:
        d = ler(f'csv_F_cl{c}.txt')
        a.plot(d['_x'], np.maximum(d['ikg'], 1e-15) * nA, color=cor, lw=2, label=f'{lab}: I de VG')
        a.plot(d['_x'], np.maximum(d['ikd'], 1e-15) * nA, color=cor, lw=1.2, ls='--', label=f'{lab}: I de VDD')
    a.axhline(10.5, color=C[0], ls=':', lw=1); nota(a, 0.05, 14, 'corrente que o bloco C injeta em VG (10,5 nA)', color=C[0])
    a.set(yscale='log', ylim=(1e-4, 1e6), xlabel='nhigh (V)', ylabel='corrente puxada (nA)',
          title='F. Corrente de desligamento × nhigh')
    a.legend(fontsize=7.5, loc='center right')
    a = ax[1]
    combos = [('0', 0.0, 'CTRL_LOW=0\nnhigh=0'), ('0', 3.7, 'CTRL_LOW=0\nnhigh=1'),
              ('3.7', 0.0, 'CTRL_LOW=1\nnhigh=0'), ('3.7', 3.7, 'CTRL_LOW=1\nnhigh=1\n(estado 0-1)')]
    vals = [(max(at(ler(f'csv_F_cl{c}.txt'), 'ikg', v), 1e-15), max(at(ler(f'csv_F_cl{c}.txt'), 'ikd', v), 1e-15))
            for c, v, _ in combos]
    xx = np.arange(4)
    a.bar(xx - 0.18, [v[0] * nA for v in vals], 0.36, color=C[0], label='de VG (XK1–XK2)')
    a.bar(xx + 0.18, [v[1] * nA for v in vals], 0.36, color=C[3], label='de VDD (XK3–XK4)')
    for i, v in enumerate(vals):
        nota(a, i, max(v) * nA * 2, (f'{v[0]*uA:.0f} µA' if v[0] > 1e-6 else f'{v[0]*1e12:.1f} pA'), ha='center')
    a.set_xticks(xx); a.set_xticklabels([c[2] for c in combos], fontsize=8)
    a.set(yscale='log', ylim=(1e-4, 1e7), ylabel='corrente puxada (nA)', title='F. Tabela-verdade (VG = 2,25 V, VDD = 1,8 V)')
    a.legend(fontsize=8, loc='upper left')
    caixa_ok(a, 'OK se: só a última coluna\nconduz (centenas de µA);\nas outras < 1 nA', loc=(0.40, 0.97))
    fig.suptitle('Bloco F: cs_desliga  (VG e VDD forçados por fontes de tensão; CTRL_LOW e nhigh por fontes DC)',
                 fontweight='bold')
    salvar(fig, 'csv', 'F_desligamento.png')


# ------------------------------------------------------------------- G
def bloco_G():
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.3))
    a = ax[0]
    d = ler('csv_G_ild.txt')
    a.plot(d['_x'], np.maximum(-d['ild'], 1e-15) * nA, color=C[2], lw=2, label='I(XLD) (dk = 0,5 V)')
    a.axhline(5.8, color=C[1], ls='--', lw=1.2, label='I(XPD) do bloco C ≈ 5,8 nA')
    x0 = np.interp(np.log10(5.8e-9), np.log10(np.maximum(-d['ild'], 1e-18)), d['_x'])
    a.axvline(x0, color='#999', ls=':', lw=1); nota(a, x0 + 0.02, 0.0016, f'cruzamento\n≈ {x0:.2f} V = limiar')
    a.set(yscale='log', ylim=(1e-3, 1e4), xlabel='VIN_DC (V)', ylabel='nA', title='G. Corrente do XLD × VIN_DC')
    a.legend(fontsize=8, loc='upper left')
    caixa_ok(a, 'OK se: ~125 mV por década e cruza\nos ~6 nA do XPD em VIN_DC ≈ 0,37 V', loc=(0.40, 0.25), va='bottom')
    a = ax[1]
    d = ler('csv_G_kill.txt')
    a.plot(d['_x'], np.maximum(d['ikg'], 1e-15) * nA, color=C[0], lw=2, label='XKD1 (de VG)')
    a.plot(d['_x'], np.maximum(d['ikd'], 1e-15) * nA, color=C[3], lw=1.4, ls='--', label='XKD2 (de VDD)')
    a.axhline(10.5, color=C[0], ls=':', lw=1); nota(a, 1.6, 4, '10,5 nA (bloco C → VG)', color=C[0])
    a.set(yscale='log', ylim=(1e-4, 1e6), xlabel='dk (V)', ylabel='corrente puxada (nA)',
          title='G. Desligamento × dk (VIN_DC = 0)')
    a.legend(fontsize=8, loc='lower right')
    caixa_ok(a, 'OK se: < 0,1 nA com dk ≈ 0 (luz)\ne > 100 µA com dk = VS (escuro)', loc=(0.03, 0.97))
    a = ax[2]
    for t, cor in [('-20', C[0]), ('27', 'k'), ('85', C[1])]:
        d = ler(f'csv_CG_{t}.txt'); x = d['_x']
        lim = x[np.argmax(d['v(dk)'] < 1.0)]
        a.plot(x, d['v(dk)'], color=cor, lw=2, label=f'{t} °C  (limiar {lim:.2f} V)')
    a.set(xlabel='VIN_DC (V)', ylabel='dk (V)', title='C + G juntos: nó dk × VIN_DC (VS = 3,7 V)')
    a.legend(fontsize=8, loc='upper right')
    caixa_ok(a, 'OK se: dk = VS no escuro, dk ≈ 0\ncom luz; limiar ≈ 0,35 V (27 °C),\n'
             'entre ~0,28 e ~0,39 V de −20 a 85 °C', loc=(0.50, 0.12), va='bottom')
    fig.suptitle('Bloco G: cs_det_escuro  (isolado: dk, VG e VDD forçados por fontes;  à direita: com o bloco C dando a corrente de dk)',
                 fontweight='bold')
    salvar(fig, 'csv', 'G_detector_de_escuro.png')


# ------------------------------------------------------------------- modulo
def modulo_dc():
    L = ler('csv_M_linha_tt.txt'); Cg = ler('csv_M_carga_tt.txt'); T = ler('csv_M_temp_tt.txt'); R = ler('csv_M_trg_tt.txt')
    fig, ax = plt.subplots(2, 2, figsize=(13, 8.2))
    a = ax[0, 0]
    m = L['_x'] >= 1.0
    L = {k: v[m] for k, v in L.items()}
    a.plot(L['_x'], L['v(vdd)'], color=C[0], lw=2, label='VDD')
    a.plot(L['_x'], L['v(x1.vg)'], color=C[3], lw=1.2, ls='--', label='VG')
    a.plot(L['_x'], L['v(x1.vs)'], color=C[5], lw=1, ls=':', label='VS')
    a.axvspan(2.9, 4.3, color=C[2], alpha=0.08); nota(a, 3.6, 1.45, 'faixa útil da bateria', ha='center', color=C[2])
    a.set(xlabel='VBAT (V)', ylabel='V', ylim=(0, 4.7), title='Linha: estado 0-0 (CTRL_LOW = CTRL_HIGH = VBAT), carga 0,15 µA')
    a.legend(fontsize=8, loc='upper left')
    a2 = a.twinx(); a2.grid(False); a2.plot(L['_x'], L['ib'] * nA, color=C[1], lw=0.9, alpha=0.7)
    a2.set_ylabel('I(VBAT) (nA)', color=C[1]); a2.set_ylim(0, 400)
    caixa_ok(a, f'OK se: VDD = {at(L, "v(vdd)", 2.9):.2f}–{at(L, "v(vdd)", 4.3):.2f} V de 2,9 a 4,3 V;\n'
             f'I(VBAT) ≈ {at(L, "ib", 3.7)*nA:.0f} nA (150 da carga + ~27 próprios)', loc=(0.30, 0.04), va='bottom')
    a = ax[0, 1]
    a.plot(R['_x'], R['v(vdd)'], color=C[0], lw=2, label='VDD')
    a.plot(R['_x'], R['v(x1.vs)'], color=C[5], lw=1, ls=':', label='VS')
    a.plot(R['_x'], R['v(x1.vg)'], color=C[3], lw=1.2, ls='--', label='VG')
    tmin = R['_x'][np.argmax(R['v(vdd)'] > 1.6)]
    a.axvline(tmin, color='#999', ls=':', lw=1); nota(a, tmin + 0.05, 3.6, f'VDD > 1,6 V\na partir de {tmin:.2f} V')
    a.set(xlabel='TRIGGER (V)', ylabel='V', ylim=(0, 4.7), title='Partida a frio: VBAT = 0, estado 1-1, varre TRIGGER')
    a.legend(fontsize=8, loc='upper left')
    caixa_ok(a, f'OK se: VDD ≈ {at(R, "v(vdd)", 3.3):.2f} V com TRIGGER = 3,3 V;\n'
             f'I(TRIGGER) ≈ {at(R, "it", 3.3)*nA:.0f} nA; I(VBAT) = 0', loc=(0.38, 0.03), va='bottom')
    a = ax[1, 0]
    a.plot(Cg['_x'] * uA, Cg['v(vdd)'], color=C[0], lw=2)
    a.axvline(0.13, color=C[3], ls='--', lw=1); nota(a, 0.16, at(Cg, 'v(vdd)', 0.13e-6) + 0.02, 'oscilador', color=C[3])
    a.set(xscale='log', xlabel='carga em VDD (µA)', ylabel='VDD (V)', title='Carga (VBAT = 3,7 V)')
    caixa_ok(a, f'OK se: VDD ≈ {at(Cg, "v(vdd)", 0.13e-6):.2f} V com 0,13 µA\ne > 1,65 V até ~5 µA',
             loc=(0.55, 0.97))
    a = ax[1, 1]
    a.plot(T['_x'], T['v(vdd)'], color=C[0], lw=2, label='VDD')
    a.plot(T['_x'], T['v(x1.vg)'], color=C[3], lw=1.2, ls='--', label='VG')
    a.set(xlabel='temperatura (°C)', ylabel='V', title='Temperatura (VBAT = 3,7 V)')
    a.legend(fontsize=8, loc='lower right')
    caixa_ok(a, f'OK se: VDD de {at(T, "v(vdd)", -20):.2f} V (−20 °C)\na {at(T, "v(vdd)", 85):.2f} V (85 °C)',
             loc=(0.03, 0.97))
    fig.suptitle('Módulo cold_start (hierárquico): DC, canto típico (tt)', fontweight='bold')
    salvar(fig, 'csv', 'modulo_1_dc.png')


def modulo_luz():
    D = ler('csv_M_luz_tt.txt')
    fig, ax = plt.subplots(2, 1, figsize=(9.5, 6.4), sharex=True)
    ax[0].plot(D['_x'], D['v(vdd)'], color=C[0], lw=2, label='VDD')
    ax[0].plot(D['_x'], D['v(x1.dk)'], color=C[1], lw=1.4, ls='--', label='dk (alto = escuro)')
    lim = D['_x'][np.argmax(D['v(vdd)'] > 0.9)]
    ax[0].axvline(lim, color='#999', ls=':', lw=1); nota(ax[0], lim + 0.01, 2.6, f'limiar ≈ {lim:.2f} V', fontsize=9)
    ax[0].set(ylabel='V', title='Detector de escuro no módulo (VBAT = 3,7 V, estado 0-0, carga 0,15 µA)')
    ax[0].legend(fontsize=8, loc='center right')
    caixa_ok(ax[0], 'OK se: VDD = 0 com VIN_DC < limiar;\nVDD ≈ 1,84 V acima de ~0,40 V', loc=(0.02, 0.6))
    ax[1].plot(D['_x'], D['ib'] * nA, color='k', lw=1.6)
    ax[1].set(xlabel='VIN_DC (V)', ylabel='I(VBAT) (nA)', yscale='log')
    caixa_ok(ax[1], f'OK se: ~{at(D, "ib", 0.1)*nA:.0f} nA no escuro (bias ~27 nA + fuga);\n'
             f'~{at(D, "ib", 0.6)*nA:.0f} nA com luz (inclui a carga de 150 nA)', loc=(0.02, 0.95))
    salvar(fig, 'csv', 'modulo_2_luz_escuro.png')


def modulo_estados():
    E = ler('csv_M_estados.txt'); t = E['_x'] * ms
    reg = [(0, 1, '0-0  normal', C[2]), (1, 2, '1-0  VBAT < T_D', C[3]), (2, 3, '0-1  VBAT > T_U', C[1]),
           (3, 4, '1-1  power-on', C[0]), (4, 5, '0-0 no escuro', C[5])]
    fig, ax = plt.subplots(3, 1, figsize=(11, 8.5), sharex=True)
    a = ax[0]
    a.plot(t, E['v(vbat)'], color='k', lw=1.6, label='VBAT')
    a.plot(t, E['v(ctrl_low)'], color=C[1], lw=1.4, ls='--', label='CTRL_LOW')
    a.plot(t, E['v(ctrl_high)'], color=C[4], lw=1.4, ls=':', label='CTRL_HIGH')
    a.axhline(3.3, color=C[3], lw=1, alpha=0.8, label='TRIGGER = 3,3 V')
    a.plot(t, E['v(vin_dc)'], color=C[2], lw=1.2, ls='-.', label='VIN_DC')
    a.set(ylabel='V', ylim=(-0.3, 5)); a.legend(loc='center right', ncol=2, fontsize=8)
    for (t0, t1, txt, cor) in reg:
        for b in ax:
            b.axvspan(t0, t1, color=cor, alpha=0.10, lw=0)
        a.text((t0 + t1) / 2, 1.0, txt, transform=a.get_xaxis_transform(), ha='center', va='bottom', fontsize=8)
    a = ax[1]
    a.plot(t, E['v(x1.vs)'], color=C[5], lw=1.2, label='VS'); a.plot(t, E['v(vdd)'], color=C[0], lw=2, label='VDD')
    a.set_ylabel('V'); a.legend(loc='center right', fontsize=8)
    esp = []
    for (t0, t1, _, _) in reg:
        m = (t > t0 + 0.5) & (t < t1 - 0.05)
        esp.append((E['v(vdd)'][m].mean(), E['v(x1.vs)'][m].mean(), E['ibat'][m].mean(), E['itrg'][m].mean()))
    for (t0, t1, _, _), (vd, vs, ib, it) in zip(reg, esp):
        nota(a, (t0 + t1) / 2, 4.2, f'VS {vs:.2f}\nVDD {vd:.2f}', ha='center')
    a.set_ylim(-0.2, 5)
    a = ax[2]
    a.plot(t, E['ibat'] * nA, color='k', lw=1.4, label='I(VBAT)')
    a.plot(t, E['itrg'] * nA, color=C[3], lw=1.4, ls='--', label='I(TRIGGER)')
    for (t0, t1, _, _), (vd, vs, ib, it) in zip(reg, esp):
        nota(a, (t0 + t1) / 2, 300, f'VBAT {abs(round(ib*nA)):.0f} nA\nTRG {abs(round(it*nA)):.0f} nA', ha='center')
    a.set(ylabel='nA', xlabel='tempo (ms)', ylim=(-30, 400)); a.legend(loc='center right', fontsize=8)
    fig.suptitle('Módulo: os 4 estados de CTRL + escuro (TRIGGER = 3,3 V, carga 15 MΩ ∥ 10 pF)', fontweight='bold')
    salvar(fig, 'csv', 'modulo_3_estados.png')
    return esp


def modulo_partida():
    P_ = ler('csv_M_partida.txt'); t = P_['_x'] * ms
    fig, ax = plt.subplots(1, 2, figsize=(14, 4.6))
    a = ax[0]; m = t <= 0.4
    a.plot(t[m], P_['v(trigger)'][m], color=C[3], lw=1.4, label='TRIGGER')
    a.plot(t[m], P_['v(x1.vs)'][m], color=C[5], lw=1.2, ls=':', label='VS')
    a.plot(t[m], P_['v(x1.vg)'][m], color=C[4], lw=1.2, ls='--', label='VG')
    a.plot(t[m], P_['v(vdd1)'][m], color=C[0], lw=2, label='VDD')
    vfin = P_['v(vdd1)'][m][-1]
    t90 = t[np.argmax(P_['v(vdd1)'] > 0.9 * vfin)]
    a.axvline(t90, color='#999', ls=':', lw=1); nota(a, t90 + 0.02, 0.4, f'VDD a 90 %\nem t = {t90:.2f} ms')
    a.set(xlabel='tempo (ms)', ylabel='V', title='Partida a frio: VBAT = 0, TRIGGER 0 → 3,3 V (0,1–0,2 ms)')
    a.legend(fontsize=8, loc='center right')
    caixa_ok(a, f'OK se: VDD chega a ~{vfin:.2f} V\npoucos µs depois de VS\n(VG carrega com ~10 nA,\nmas a pilha é pequena)',
             loc=(0.03, 0.97))
    a = ax[1]
    a.plot(t, P_['v(vin2)'] * 5, color=C[2], lw=1.2, ls='-.', label='VIN_DC × 5')
    a.plot(t, P_['v(x2.dk)'], color=C[1], lw=1.2, ls='--', label='dk')
    a.plot(t, P_['v(x2.vg)'], color=C[4], lw=1.0, ls=':', label='VG')
    a.plot(t, P_['v(vdd2)'], color=C[0], lw=2, label='VDD')
    on = t[(t > 1.0) & (P_['v(vdd2)'] > 0.9 * 1.84)]
    t_on = (on[0] - 1.01) if len(on) else float('nan')
    off = t[(t > 3.0) & (P_['v(vdd2)'] < 0.1 * 1.84)]
    t_off = (off[0] - 3.0) if len(off) else float('nan')
    a.set(xlabel='tempo (ms)', ylabel='V', ylim=(-0.2, 4.2), title='Estado 0-0, VBAT = 3,7 V: escuro → luz (1 ms) → escuro (3 ms)')
    a.legend(fontsize=8, loc='upper right')
    caixa_ok(a, f'OK se: VDD sobe ~{t_on*1e3:.0f} µs após a luz\n e cai em ~{t_off*1e3:.0f} µs no escuro', loc=(0.03, 0.97))
    fig.suptitle('Módulo: transitórios de partida (carga 15 MΩ ∥ 10 pF)', fontweight='bold')
    salvar(fig, 'csv', 'modulo_4_partida.png')
    return t90, vfin, t_on, t_off


def modulo_cantos():
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.3))
    res = {}
    for k in CANTOS:
        L = ler(f'csv_M_linha_{k}.txt'); D = ler(f'csv_M_luz_{k}.txt'); T = ler(f'csv_M_temp_{k}.txt')
        m = L['_x'] >= 2.5
        ax[0].plot(L['_x'][m], L['v(vdd)'][m], color=COR_CANTO[k], lw=1.6, label=k)
        ax[1].plot(D['_x'], D['v(vdd)'], color=COR_CANTO[k], lw=1.6, label=k)
        ax[2].plot(T['_x'], T['v(vdd)'], color=COR_CANTO[k], lw=1.6, label=k)
        res[k] = (at(L, 'v(vdd)', 3.7), D['_x'][np.argmax(D['v(vdd)'] > 0.9)], at(D, 'ib', 0.1) * nA,
                  at(L, 'ib', 3.7) * nA - 150)
    ax[0].set(xlabel='VBAT (V)', ylabel='VDD (V)', title='VDD × VBAT (estado 0-0)')
    ax[1].set(xlabel='VIN_DC (V)', ylabel='VDD (V)', title='Limiar do detector de escuro', xlim=(0.25, 0.5))
    ax[2].set(xlabel='temperatura (°C)', ylabel='VDD (V)', title='VDD × temperatura')
    for a in ax:
        a.legend(fontsize=8, loc='lower right', title='canto', title_fontsize=8)
    v = [r[0] for r in res.values()]; th = [r[1] for r in res.values()]
    caixa_ok(ax[0], f'faixa nos cantos (3,7 V):\nVDD = {min(v):.2f} a {max(v):.2f} V', loc=(0.03, 0.97))
    caixa_ok(ax[1], f'limiar = {min(th):.2f} a {max(th):.2f} V', loc=(0.03, 0.97))
    fig.suptitle('Módulo nos cantos de processo do SKY130 (tt, ff, ss, fs, sf): use como faixa de tolerância', fontweight='bold')
    salvar(fig, 'csv', 'modulo_5_cantos.png')
    return res


if __name__ == '__main__':
    bloco_A(); bloco_B(); bloco_C(); bloco_D(); bloco_E(); bloco_F(); bloco_G()
    modulo_dc(); modulo_luz()
    esp = modulo_estados()
    print('estados (VDD, VS, Ibat nA, Itrg nA):')
    for e in esp:
        print('  %.3f %.3f %.1f %.1f' % (e[0], e[1], e[2] * nA, e[3] * nA))
    print('partida (t90 ms, VDD, t_on ms, t_off ms):', modulo_partida())
    for k, r in modulo_cantos().items():
        print('  canto', k, 'VDD %.3f  limiar %.3f  Ib_escuro %.1f nA  consumo proprio %.1f nA' % r)
    Q = ler('csv_M_eq.txt')
    print('equivalencia plano x hierarquico: max |dVDD| = %.2e V' % abs(Q['dif']).max())
