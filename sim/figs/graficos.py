"""Gera os graficos de todos os modulos a partir de sim/figs/dados/."""
import sys
from util import *

us, ms, uA, nA, uW = 1e6, 1e3, 1e6, 1e9, 1e6


def tabela(nome):
    caminho = os.path.join(DADOS, nome)
    with open(caminho) as f:
        hdr = f.readline().split()
        linhas = [l.split() for l in f if l.strip()]
    return hdr, linhas


def cruzamentos(t, y, nivel, sentido):
    """tempos em que y cruza 'nivel' (sentido=+1 subindo, -1 descendo)."""
    s = np.sign(y - nivel)
    idx = np.where(np.diff(s) == 2 * sentido)[0]
    return t[idx]


def faixa_estados(ax, regioes):
    for (t0, t1, txt, cor) in regioes:
        ax.axvspan(t0, t1, color=cor, alpha=0.10, lw=0)
        ax.text((t0 + t1) / 2, 1.0, txt, transform=ax.get_xaxis_transform(),
                ha='center', va='bottom', fontsize=8, color='#333')


# =================================================================== Cold-Start
def cold_start():
    print('Cold-Start')
    L = ler('cs_linha.txt'); Cg = ler('cs_carga.txt'); T = ler('cs_temp.txt')
    fig, ax = plt.subplots(1, 3, figsize=(13, 4))
    a = ax[0]
    mk = L['_x'] >= 1.2
    L = {k: v[mk] for k, v in L.items()}
    a.plot(L['_x'], L['v(vdd)'], color=C[0], lw=2, label='VDD')
    a.plot(L['_x'], L['v(x1.vg)'], color=C[3], lw=1.2, ls='--', label='VG (pilha de diodos)')
    a.plot(L['_x'], L['v(x1.vs)'], color=C[5], lw=1, ls=':', label='VS (fonte selecionada)')
    a.set_ylim(0, 4.8)
    a.set(xlabel='VBAT (V)', ylabel='tensão (V)', title='Regulação de linha (carga 2 µA)')
    a.axvspan(2.9, 4.4, color=C[2], alpha=0.08)
    a.text(3.65, 0.2, 'faixa útil da bateria', ha='center', fontsize=8, color=C[2])
    a.legend(loc='upper left')
    a2 = a.twinx(); a2.grid(False)
    a2.plot(L['_x'], L['ib'] * uA, color=C[1], lw=0.8, alpha=0.6)
    a2.set_ylabel('corrente de VBAT (µA)', color=C[1]); a2.set_ylim(0, 6)
    a = ax[1]
    a.plot(Cg['_x'] * uA, Cg['v(vdd)'], color=C[0], lw=2)
    a.set(xlabel='corrente de carga em VDD (µA)', ylabel='VDD (V)', title='Regulação de carga (VBAT = 3,7 V)')
    a.axvline(1.2 / 2.2, color=C[3], ls='--', lw=1)
    a.text(0.7, Cg['v(vdd)'].min() + 0.01, '← consumo do\n    oscilador (~0,5 µA)', fontsize=8, color=C[3])
    a = ax[2]
    a.plot(T['_x'], T['v(vdd)'], color=C[0], lw=2)
    a.axvspan(0, 60, color=C[2], alpha=0.08)
    a.set(xlabel='temperatura (°C)', ylabel='VDD (V)', title='VDD × temperatura (VBAT = 3,7 V)')
    salvar(fig, 'cs', 'regulacao_linha_carga_temperatura.png')

    E = ler('cs_estados.txt'); t = E['_x'] * ms
    reg = [(0, 1, '0-0  normal\n(regula de VBAT)', C[2]), (1, 2, '1-0  VBAT < T_D\n(regula do TRIGGER)', C[3]),
           (2, 3, '0-1  VBAT > T_U\n(VDD desligado)', C[1]), (3, 4, '1-1  power-on\n(regula do TRIGGER)', C[0])]
    fig, ax = plt.subplots(3, 1, figsize=(11, 8.5), sharex=True)
    a = ax[0]
    a.plot(t, E['v(vbat)'], color='k', lw=1.6, label='VBAT')
    a.plot(t, E['v(ctrl_low)'], color=C[1], lw=1.4, ls='--', label='CTRL_LOW')
    a.plot(t, E['v(ctrl_high)'], color=C[4], lw=1.4, ls=':', label='CTRL_HIGH')
    a.axhline(3.3, color=C[3], lw=1, alpha=0.8, label='TRIGGER = 3,3 V')
    a.set_ylabel('V'); a.legend(loc='center right', ncol=2, fontsize=8); a.set_ylim(-0.3, 5)
    faixa_estados(a, reg)
    a = ax[1]
    a.plot(t, E['v(x1.vs)'], color=C[5], lw=1.2, label='VS (fonte selecionada)')
    a.plot(t, E['v(vdd)'], color=C[0], lw=2, label='VDD → oscilador')
    a.set_ylabel('V'); a.legend(loc='center right', fontsize=8)
    for (t0, t1, _, cor) in reg:
        a.axvspan(t0, t1, color=cor, alpha=0.10, lw=0)
    a = ax[2]
    a.plot(t, E['ibat'] * uA, color='k', lw=1.4, label='corrente de VBAT')
    a.plot(t, E['itrg'] * uA, color=C[3], lw=1.4, ls='--', label='corrente do TRIGGER')
    a.set(ylabel='µA', xlabel='tempo (ms)'); a.legend(loc='center right', fontsize=8)
    a.set_ylim(-0.5, 4)
    a.annotate('0,9 µA: fuga do seguidor nativo XMF\n(Vgs = 0) pelo pull-down de VDD\n→ ponto a melhorar', xy=(2.5, 0.93),
               xytext=(2.15, 2.6), fontsize=8, color=C[1], arrowprops=dict(arrowstyle='->', color=C[1]))
    for (t0, t1, _, cor) in reg:
        a.axvspan(t0, t1, color=cor, alpha=0.10, lw=0)
    fig.suptitle('Cold-Start: os 4 estados de CTRL_LOW / CTRL_HIGH (carga 1 MΩ ≈ oscilador)', fontweight='bold')
    salvar(fig, 'cs', 'estados_de_controle.png')


# =================================================================== Oscilador
def oscilador():
    print('Oscilador')
    O = ler('osc_ondas.txt'); t = O['_x'] * us
    m = (t > 30) & (t < 52)
    fig, ax = plt.subplots(4, 1, figsize=(11, 9), sharex=True)
    for i in range(5):
        ax[0].plot(t[m], O[f'v(x1.r{i+1})'][m], lw=1.2, color=plt.cm.viridis(i / 5), label=f'r{i+1}')
    ax[0].set(ylabel='V', title='Nós do anel (bordas de descida lentas: corrente limitada pelos nativos)')
    ax[0].legend(ncol=5, fontsize=8, loc='upper right')
    ax[1].plot(t[m], O['v(x1.s2)'][m], color=C[0], lw=1.4, label='s2 (borda afiada)')
    ax[1].plot(t[m], O['v(x1.d3)'][m], color=C[3], lw=1.4, ls='--', label='d3 (s2 atrasado e invertido)')
    ax[1].set(ylabel='V', title='Detector de borda'); ax[1].legend(fontsize=8, loc='upper right')
    ax[2].plot(t[m], O['v(clk)'][m], color=C[1], lw=1.6)
    ax[2].set(ylabel='V', title='CLK (para o gate da chave do Boost)')
    # media movel de 1 us (a corrente instantanea da fonte ideal oscila numericamente)
    # -> usa a carga integrada Q(t) = int i dt, que nao sofre com a oscilacao
    q = np.concatenate([[0], np.cumsum(0.5 * (O['idd'][1:] + O['idd'][:-1]) * np.diff(O['_x']))])
    tu = np.arange(t[m][0] + 0.5, t[m][-1] - 0.5, 0.01)
    imov = (np.interp(tu + 0.5, t, q) - np.interp(tu - 0.5, t, q)) / 1e-6
    c = cruzamentos(t, O['v(clk)'], 1.1, +1)
    c = c[(c > 20) & (c < 70)]
    imed = (np.interp(c[-1], t, q) - np.interp(c[0], t, q)) / ((c[-1] - c[0]) * 1e-6)
    ax[3].plot(tu, imov * uA, color=C[5], lw=1.2)
    ax[3].axhline(imed * uA, color=C[1], ls='--', lw=1)
    ax[3].set(ylabel='µA', xlabel='tempo (µs)',
              title=f'Corrente de VDD (média móvel de 1 µs; média por período {imed*uA:.2f} µA → {imed*2.2*uW:.2f} µW)')
    salvar(fig, 'osc', 'formas_de_onda.png')

    # zoom num pulso
    c = cruzamentos(t, O['v(clk)'], 1.1, +1)
    t0 = c[c > 35][0]
    m = (t > t0 - 0.6) & (t < t0 + 1.4)
    f = cruzamentos(t[m], O['v(clk)'][m], 1.1, -1)[0]
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(t[m] - t0, O['v(x1.s2)'][m], color=C[0], lw=1.4, label='s2')
    ax.plot(t[m] - t0, O['v(x1.d3)'][m], color=C[3], lw=1.4, ls='--', label='d3')
    ax.plot(t[m] - t0, O['v(x1.pn)'][m], color=C[5], lw=1, ls=':', label='pn (saída do NAND)')
    ax.plot(t[m] - t0, O['v(clk)'][m], color=C[1], lw=2, label='CLK')
    ax.annotate('', xy=(f - t0, 2.45), xytext=(0, 2.45), arrowprops=dict(arrowstyle='<->', color='k'))
    ax.text((f - t0) / 2, 2.52, f't_on = {1e3*(f - t0):.0f} ns', ha='center', fontsize=9)
    ax.set(xlabel='tempo (µs, relativo à subida do CLK)', ylabel='V', ylim=(-0.2, 2.8),
           title='Geração do pulso: CLK = s2 AND d3 (largura = atraso da cadeia de 3 inversores)')
    ax.legend(loc='center right', fontsize=8)
    salvar(fig, 'osc', 'pulso_clk_zoom.png')

    # VDD cortado
    m = (t > 55) & (t < 100)
    fig, ax = plt.subplots(2, 1, figsize=(10, 5.5), sharex=True)
    ax[0].plot(t[m], O['v(vdd)'][m], color='k', lw=1.6, label='VDD')
    ax[0].set(ylabel='V', title='Requisito: sem VDD, o CLK tem que ir a 0 V (chave do boost aberta)')
    ax[0].legend(fontsize=8)
    ax[1].plot(t[m], O['v(clk)'][m], color=C[1], lw=1.4, label='CLK')
    ax[1].plot(t[m], O['v(x1.r1)'][m], color=C[0], lw=0.8, alpha=0.7, label='r1')
    ax[1].set(ylabel='V', xlabel='tempo (µs)'); ax[1].legend(fontsize=8)
    ax[1].axvspan(75, 100, color=C[2], alpha=0.1)
    ax[1].text(87, 1.2, 'VDD = 0 → CLK fica em 0 V (chave aberta).\nNós internos podem reter alguma carga, mas sem\nalimentação nenhum inversor consegue levantar o CLK.', ha='center', fontsize=9, color=C[2])
    salvar(fig, 'osc', 'corte_de_vdd.png')

    V = ler('osc_vdd.txt')
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.6))
    ax[0].plot(V['vdd'], V['freq'] / 1e3, 'o-', color=C[0]); ax[0].set(xlabel='VDD (V)', ylabel='kHz', title='Frequência')
    ax[1].plot(V['vdd'], V['ton'] * 1e9, 'o-', color=C[1]); ax[1].set(xlabel='VDD (V)', ylabel='ns', title='Largura do pulso t_on')
    ax[2].plot(V['vdd'], V['pw'] * uW, 'o-', color=C[2]); ax[2].set(xlabel='VDD (V)', ylabel='µW', title='Consumo (com a chave)')
    for a in ax:
        a.axvline(2.2, color='#999', ls='--', lw=1)
    fig.suptitle('Oscilador × tensão de alimentação (VDD nominal = 2,2 V)', fontweight='bold')
    salvar(fig, 'osc', 'f_ton_consumo_vs_vdd.png')


# =================================================================== Referencia
def referencia():
    print('Referência')
    R = ler('ref_vbat.txt'); T = ler('ref_temp.txt')
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(R['_x'], R['v(vref)'] * 1e3, color=C[0], lw=2)
    ax.set(xlabel='VBAT (V)', ylabel='VREF (mV)', title='VREF × VBAT (27 °C)', ylim=(0, 160))
    ax.axvspan(2.5, 4.2, color=C[2], alpha=0.08)
    v25, v42 = np.interp([2.5, 4.2], R['_x'], R['v(vref)'])
    ax.text(3.35, 60, f'2,5→4,2 V: VREF varia {1e3*(v42-v25):.1f} mV\n({1e3*(v42-v25)/1.7:.2f} mV/V)', ha='center', fontsize=9, color=C[2])
    a2 = ax.twinx(); a2.grid(False)
    a2.plot(R['_x'], R['ib'] * 1e12, color=C[1], lw=1, alpha=0.7)
    a2.set_ylabel('corrente consumida (pA)', color=C[1]); a2.set_ylim(0, 20)
    salvar(fig, 'ref', 'vref_vs_vbat.png')

    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(T['_x'], T['v(vref)'] * 1e3, color=C[0], lw=2)
    ax.axvspan(0, 60, color=C[2], alpha=0.08)
    m = (T['_x'] >= 0) & (T['_x'] <= 60)
    lo, hi = T['v(vref)'][m].min() * 1e3, T['v(vref)'][m].max() * 1e3
    ax.text(30, lo - 8, f'0–60 °C: {lo:.1f} a {hi:.1f} mV', ha='center', fontsize=9, color=C[2])
    ax.set(xlabel='temperatura (°C)', ylabel='VREF (mV)', title='VREF × temperatura (VBAT = 3,7 V)')
    salvar(fig, 'ref', 'vref_vs_temperatura.png')

    # varredura de geometria (resultados da exploracao inicial, ver sim/03_referencia/sweep)
    temps = [-20, 0, 27, 60, 85]
    cfgs = {
        'M1 10/4, M2 2/2':   [173.4, 193.0, 204.9, 213.8, 219.6],
        'M1 10/4, M2 10/1':  [159.8, 167.0, 170.5, 173.0, 174.6],
        'M1 1/8, M2 4/1':    [117.4, 130.3, 134.0, 133.3, 131.8],
        'M1 1/4, M2 10/1 (escolhida)': [125.9, 132.8, 133.5, 131.7, 129.7],
        'M1 1/4, M2 20/1':   [118.7, 121.7, 120.3, 116.9, 113.8],
        'M1 1/25, M2 10/1':  [91.5, 99.0, 97.7, 92.1, 87.1],
    }
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    for i, (k, v) in enumerate(cfgs.items()):
        esc = 'escolhida' in k
        ax.plot(temps, v, 'o-', lw=2.6 if esc else 1.2, color='k' if esc else plt.cm.tab10(i), label=k)
    ax.set(xlabel='temperatura (°C)', ylabel='VREF (mV)',
           title='Escolha das dimensões (W/L em µm): a razão W/L ajusta o coeficiente de temperatura')
    ax.legend(fontsize=8, ncol=2)
    salvar(fig, 'ref', 'escolha_das_dimensoes.png')


# =================================================================== Comparador
def comparador():
    print('Comparador')
    S = ler('comp_dc_sobe.txt'); D = ler('comp_dc_desce.txt')
    fig, ax = plt.subplots(1, 3, figsize=(13, 4))
    ref = 133.5
    for a, chave, tit in ((ax[0], 'v(x1.o1)', 'o1 (saída do OTA)'), (ax[1], 'v(x1.o2)', 'o2 (2º estágio)'),
                          (ax[2], 'v(out)', 'out (Schmitt)')):
        a.plot(S['_x'] * 1e3, S[chave], color=C[0], lw=2, label='inp subindo')
        a.plot(D['_x'] * 1e3, D[chave], color=C[1], lw=1.4, ls='--', label='inp descendo')
        a.axvline(ref, color='#999', lw=1)
        a.set(xlabel='inp (mV)   [inn = 133,5 mV]', ylabel='V', title=tit)
    ax[0].legend(fontsize=8)
    fig.suptitle('Comparador: transferência DC (VBAT = 3,6 V) — offset ≈ 1 mV', fontweight='bold')
    salvar(fig, 'comp', 'transferencia_dc.png')

    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.plot(S['_x'] * 1e3, S['ib'] * nA, color=C[0], lw=2, label='inp subindo')
    ax.plot(D['_x'] * 1e3, D['ib'] * nA, color=C[1], lw=1.4, ls='--', label='inp descendo')
    ax.set(xlabel='inp (mV)', ylabel='corrente de VBAT (nA)',
           title='Consumo do comparador (pico no limiar limitado a nA)')
    ax.legend(fontsize=8)
    salvar(fig, 'comp', 'consumo.png')

    T = ler('comp_tran.txt'); t = T['_x'] * us
    fig, ax = plt.subplots(3, 1, figsize=(10, 7.5), sharex=True)
    ax[0].plot(t, T['v(inp)'] * 1e3, color=C[0], lw=1.6, label='inp')
    ax[0].plot(t, T['v(inn)'] * 1e3, color=C[5], lw=1.2, ls='--', label='inn (VREF)')
    ax[0].set(ylabel='mV', title='Entrada: degraus de ±10 mV em torno de VREF'); ax[0].legend(fontsize=8)
    ax[1].plot(t, T['v(x1.o1)'], color=C[3], lw=1.4, label='o1')
    ax[1].plot(t, T['v(x1.o2)'], color=C[4], lw=1.4, ls='--', label='o2')
    ax[1].set(ylabel='V', title='Nós internos'); ax[1].legend(fontsize=8)
    ax[2].plot(t, T['v(out)'], color=C[1], lw=2)
    up = cruzamentos(t, T['v(out)'], 1.8, +1); dn = cruzamentos(t, T['v(out)'], 1.8, -1)
    txt = []
    if len(up):
        txt.append(f'atraso subida ≈ {up[0]-100:.0f} µs')
    if len(dn):
        txt.append(f'atraso descida ≈ {dn[0]-400:.0f} µs')
    ax[2].text(0.98, 0.5, '\n'.join(txt), transform=ax[2].transAxes, ha='right', fontsize=9)
    ax[2].set(ylabel='V', xlabel='tempo (µs)', title='Saída: atraso de ~9 µs (de sobra: a bateria muda em minutos/horas)')
    salvar(fig, 'comp', 'resposta_ao_degrau.png')


# =================================================================== Threshold
def threshold():
    print('Battery Threshold Control')
    D = ler('thr.txt'); t = D['_x'] * ms
    vb = D['v(vbat)']
    fig, ax = plt.subplots(3, 1, figsize=(11, 9), sharex=True)
    ax[0].plot(t, vb, color='k', lw=1.6, label='VBAT')
    ax[0].plot(t, D['v(ctrl_low)'], color=C[1], lw=1.4, label='CTRL_LOW')
    ax[0].plot(t, D['v(ctrl_high)'], color=C[4], lw=1.4, ls='--', label='CTRL_HIGH')
    ax[0].set(ylabel='V', title='VBAT em rampa: 0 → 4,5 V → 2,6 V → 0'); ax[0].legend(fontsize=8, loc='upper left')
    for y, s in ((4.2, '4,2'), (4.1, '4,1'), (3.1, '3,1'), (3.0, '3,0')):
        ax[0].axhline(y, color='#bbb', lw=0.7, ls=':')
    ax[1].plot(t, D['v(t_d)'] * 1e3, color=C[1], lw=1.4, label='V(T_D)')
    ax[1].plot(t, D['v(t_u)'] * 1e3, color=C[4], lw=1.4, label='V(T_U)')
    ax[1].plot(t, D['v(x1.vref)'] * 1e3, color=C[0], lw=1.8, ls='--', label='VREF')
    ax[1].set(ylabel='mV', ylim=(0, 220), title='Taps do divisor × VREF (os saltos são a histerese entrando)')
    ax[1].legend(fontsize=8, loc='upper left')
    ax[2].plot(t, -D['ib'] * nA * -1, color=C[5], lw=1)
    ax[2].set(ylabel='nA', xlabel='tempo (ms)', title='Corrente de VBAT (comparadores + referência + divisor de 20 MΩ)')
    ax[2].set_ylim(0, 400)
    salvar(fig, 'thr', 'rampa_de_vbat.png')

    # laços de histerese
    k = np.argmax(vb)
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.3))
    for a, chave, nome, lims in ((ax[0], 'v(ctrl_low)', 'CTRL_LOW', (2.6, 3.4)),
                                 (ax[1], 'v(ctrl_high)', 'CTRL_HIGH', (3.9, 4.5))):
        a.plot(vb[:k], D[chave][:k] / vb[:k].clip(0.5), color=C[0], lw=2, label='VBAT subindo')
        a.plot(vb[k:], D[chave][k:] / vb[k:].clip(0.5), color=C[1], lw=2, ls='--', label='VBAT descendo')
        a.set(xlim=lims, xlabel='VBAT (V)', ylabel=f'{nome} / VBAT', title=f'Histerese de {nome}')
        a.legend(fontsize=8, loc='center left')
    u = cruzamentos(vb[:k], D['v(ctrl_low)'][:k] - vb[:k] / 2, 0, +1)
    for a, chave in ((ax[0], 'v(ctrl_low)'), (ax[1], 'v(ctrl_high)')):
        s = D[chave] - vb / 2
        ts = []
        for seg, sent in ((slice(0, k), +1), (slice(0, k), -1), (slice(k, None), +1), (slice(k, None), -1)):
            idx = np.where(np.diff(np.sign(s[seg])) == 2 * sent)[0]
            idx = idx[vb[seg][idx] > 1.5]
            if len(idx):
                v = vb[seg][idx[0]]
                a.axvline(v, color='#999', lw=0.8, ls=':')
                ts.append(v)
        a.text(0.62, 0.45, 'limiares: ' + ', '.join(f'{v:.2f} V' for v in sorted(set(np.round(ts, 3)))),
               transform=a.transAxes, fontsize=8)
    salvar(fig, 'thr', 'lacos_de_histerese.png')


# =================================================================== Boost
def boost():
    print('Boost')
    B = ler('boost_ondas.txt'); t = B['_x'] * us
    il = B['i(L1)'] * 1e3; idio = B['@d.xbst.dr[id]'] * 1e3
    c = cruzamentos(t, B['v(clk)'], 1.1, +1)
    t0 = c[c > t[0] + 5][0]
    for janela, nome, tit in (((t0 - 2, t0 + 38), 'formas_de_onda_4_ciclos.png', '4 ciclos de chaveamento'),
                              ((t0 - 0.3, t0 + 1.2), 'formas_de_onda_1_ciclo.png', 'um ciclo (zoom)')):
        m = (t > janela[0]) & (t < janela[1])
        fig, ax = plt.subplots(4, 1, figsize=(10, 8.5), sharex=True)
        ax[0].plot(t[m] - t0, B['v(clk)'][m], color=C[1], lw=1.5); ax[0].set(ylabel='V', title='CLK (gate da chave)')
        ax[1].plot(t[m] - t0, B['v(lbst)'][m], color=C[4], lw=1.4); ax[1].set(ylabel='V', title='V(LBST): ~0 com a chave fechada, VBAT + Vdiodo na descarga, oscila (DCM) ao fim')
        ax[2].plot(t[m] - t0, il[m], color=C[0], lw=1.8, label='I_L (indutor)')
        ax[2].set(ylabel='mA', title='Corrente no indutor: sobe até I_pk (chave fechada) e desce pelo diodo até a bateria (I_diodo = I_L)')
        ax[3].plot(t[m] - t0, B['v(vin)'][m] * 1e3, color=C[3], lw=1.2)
        ax[3].set(ylabel='mV', xlabel='tempo (µs, relativo à subida do CLK)', title='V_in (ondulação no Cin)')
        fig.suptitle(f'Boost — {tit}  (VBAT = 3,7 V, Iph = 50 µA)', fontweight='bold')
        salvar(fig, 'boost', nome)

    # curva da celula + pontos de operacao
    hdr, lin = tabela('boost_casos.txt')
    casos = [dict(zip(hdr, l)) for l in lin]
    c50 = ler('celula_50u.txt'); c25 = ler('celula_25u.txt')
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.3))
    for cel, rot_, cor in ((c50, 'Iph = 50 µA (luz cheia)', C[0]), (c25, 'Iph = 25 µA (½ luz)', C[3])):
        v = cel['_x']; i = cel[[k for k in cel if k.startswith('i(')][0]]
        ax[0].plot(v, i * uA, color=cor, lw=2, label=rot_)
        ax[1].plot(v, v * i * uW, color=cor, lw=2, label=rot_)
        k = np.argmax(v * i)
        ax[1].plot(v[k], v[k] * i[k] * uW, 'o', mfc='none', color=cor, ms=10)
        ax[1].text(v[k], v[k] * i[k] * uW + 1.2, f'MPP {v[k]:.2f} V\n{v[k]*i[k]*uW:.1f} µW', ha='center', fontsize=8, color=cor)
    for cs in casos:
        cor = C[3] if cs['iph'] == '25' else C[1]
        ax[1].plot(float(cs['vin']), float(cs['pin']) * uW, 's', color=cor, ms=7)
    ax[1].plot([], [], 's', color=C[1], label='operação: VBAT 3,0 / 3,7 / 4,2 V (luz cheia)')
    ax[1].plot([], [], 's', color=C[3], label='operação: VBAT 3,7 V (½ luz)')
    R = 2 * 220e-6 / (534e-9 ** 2 * 101e3) * (1 - 0.6 / (3.7 + 0.77))   # (1 - Vin/Vout), Martins et al. 2017
    vv = np.linspace(0, 0.8, 50)
    ax[0].plot(vv, vv / R * uA, color='k', ls=':', lw=1.2, label=f'R_in = 2L/(t_on²f)·(1−V_in/V_out) ≈ {R/1e3:.1f} kΩ')
    NL = chr(10)
    ref = NL.join(f"VBAT {c['vbat']} V, Iph {c['iph']} µA: R_in = {float(c['vin'])**2/float(c['pin'])/1e3:.1f} kΩ"
                  for c in casos)
    ax[0].text(0.02, 0.97, 'R_in efetivo simulado (V_in²/P_in):' + NL + ref + NL +
               '(a fórmula ideal ignora perdas e o ringing em DCM)', transform=ax[0].transAxes,
               va='top', fontsize=7.5, bbox=dict(fc='white', ec='#ccc'))
    ax[0].set(xlabel='V (V)', ylabel='I (µA)', title='Curva I-V da célula × reta de carga do boost', ylim=(0, 62), xlim=(0, 0.85))
    ax[0].legend(fontsize=8)
    ax[1].set(xlabel='V (V)', ylabel='P (µW)', title='Curva P-V: ■ = ponto de operação simulado', ylim=(0, 36), xlim=(0, 0.85))
    ax[1].legend(fontsize=8, loc='upper left')
    salvar(fig, 'boost', 'celula_e_ponto_de_operacao.png')

    fig, ax = plt.subplots(figsize=(9, 4.3))
    nomes = [f"VBAT {c['vbat']} V\nIph {c['iph']} µA" for c in casos]
    x = np.arange(len(casos))
    pin = np.array([float(c['pin']) for c in casos]) * uW
    pout = np.array([float(c['pout']) for c in casos]) * uW
    posc = np.array([float(c['posc']) for c in casos]) * uW
    ax.bar(x - 0.27, pin, 0.27, color=C[0], label='P extraída da célula')
    ax.bar(x, pout, 0.27, color=C[2], label='P entregue à bateria')
    ax.bar(x + 0.27, posc, 0.27, color=C[3], label='P gasta pelo oscilador')
    for i in range(len(casos)):
        ax.text(x[i], pout[i] + 1, f'η boost {100*pout[i]/pin[i]:.0f}%\nη total {100*(pout[i]-posc[i])/pin[i]:.0f}%',
                ha='center', fontsize=8)
    ax.set_xticks(x, nomes); ax.set(ylabel='µW', title='Balanço de potência do boost', ylim=(0, 38))
    ax.legend(fontsize=8, loc='upper right')
    salvar(fig, 'boost', 'eficiencia.png')


# =================================================================== Integracao
def integracao():
    print('Integração')
    A = ler('int_A.txt'); t = A['_x'] * ms
    vb = A['v(vbat)']

    def painel(D, t, extra=None, titulo='', arquivo='', janela=None):
        m = np.ones_like(t, bool) if janela is None else (t >= janela[0]) & (t <= janela[1])
        n = 5 if extra else 4
        fig, ax = plt.subplots(n, 1, figsize=(11, 2.1 * n + 0.8), sharex=True)
        ax[0].plot(t[m], D['v(vbat)'][m], color='k', lw=1.6)
        ax[0].set(ylabel='VBAT (V)')
        ax[1].plot(t[m], D['v(xic.ctrl_low)'][m], color=C[1], lw=1.4, label='CTRL_LOW')
        ax[1].plot(t[m], D['v(xic.ctrl_high)'][m], color=C[4], lw=1.4, ls='--', label='CTRL_HIGH')
        ax[1].set(ylabel='V'); ax[1].legend(fontsize=8, loc='center right')
        ax[2].plot(t[m], D['v(xic.clk)'][m], color=C[1], lw=0.5, alpha=0.6, label='CLK')
        ax[2].plot(t[m], D['v(xic.vdd)'][m], color=C[0], lw=1.8, label='VDD')
        ax[2].set(ylabel='V'); ax[2].legend(fontsize=8, loc='center right')
        ax[3].plot(t[m], D['v(vin_dc)'][m], color=C[3], lw=1.4)
        ax[3].set(ylabel='VIN_DC (V)')
        if extra:
            extra(ax[4], m)
        ax[-1].set_xlabel('tempo (ms)')
        fig.suptitle(titulo, fontweight='bold')
        salvar(fig, 'int', arquivo)

    painel(A, t, titulo='Caso A: carga até o limite superior, parada e religamento (bateria = 47 nF, VBAT0 = 4,08 V)',
           arquivo='caso_A_limite_superior.png')
    dsp = cruzamentos(t, A['v(xic.ctrl_high)'] - vb / 2, 0, -1)
    lib = cruzamentos(t, A['v(xic.ctrl_high)'] - vb / 2, 0, +1)
    dsp = dsp[dsp > 0.5]; lib = lib[lib > 0.5]
    if len(dsp):
        td = dsp[0]
        painel(A, t, titulo=f'Caso A — zoom no disparo: VBAT = {np.interp(td, t, vb):.3f} V → CTRL_HIGH = 0 → VDD e CLK desligam',
               arquivo='caso_A_zoom_disparo.png', janela=(td - 0.15, td + 0.35))
    if len(lib):
        tl = lib[-1]
        painel(A, t, titulo=f'Caso A — zoom no religamento: VBAT = {np.interp(tl, t, vb):.3f} V → CTRL_HIGH volta → boost recomeça',
               arquivo='caso_A_zoom_religamento.png', janela=(tl - 0.15, tl + 0.35))

    B = ler('int_B.txt'); tb = B['_x'] * ms

    def extraB(a, m):
        a.plot(tb[m], -B['i(VT)'][m] * uA, color=C[3], lw=1.0, label='corrente do TRIGGER')
        a.plot(tb[m], B['v(xic.xcs.vs)'][m], color=C[5], lw=1.2, label='VS (V)')
        a.set(ylabel='µA  /  V'); a.legend(fontsize=8, loc='center right')
    painel(B, tb, extra=extraB, titulo='Caso B: VBAT baixo (2,9 V) → roda pelo TRIGGER (3,3 V) → passa para VBAT em ~3,1 V',
           arquivo='caso_B_trigger_para_vbat.png')
    tr = cruzamentos(tb, B['v(xic.ctrl_low)'] - B['v(vbat)'] / 2, 0, +1)
    tr = tr[tr > 0.5]
    if len(tr):
        painel(B, tb, extra=extraB,
               titulo=f'Caso B — zoom na troca de fonte (VBAT = {np.interp(tr[0], tb, B["v(vbat)"]):.3f} V)',
               arquivo='caso_B_zoom_troca_de_fonte.png', janela=(tr[0] - 0.1, tr[0] + 0.15))


if __name__ == '__main__':
    alvos = sys.argv[1:] or ['cold_start', 'oscilador', 'referencia', 'comparador', 'threshold', 'boost', 'integracao']
    for a in alvos:
        globals()[a]()
