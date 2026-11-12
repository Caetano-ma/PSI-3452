"""Gera os testbenches de balanco de energia (v1 x v2) em sim/figs/tb/.

Bateria = fonte ideal de 3,7 V; mede-se a corrente media liquida que ENTRA nela
(carga do boost menos tudo o que o chip e o divisor consomem dela).
"""
import os

TB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tb')
LIB = '.lib "C:/Users/caean/EDA/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice" tt'

CASOS = {  # nome: (Iph, Vin inicial, tempo total, inicio da media)
    'luz':    ('50u', 0.60, '8m', '4m'),
    'meia':   ('25u', 0.45, '8m', '4m'),
    'pouca':  ('10u', 0.30, '30m', '10m'),
    'escuro': ('0',   0.0,  '4m', '2m'),
}


def divisor(S):
    return f"""\
.param VR=0.1335 S={S} VH=4.2 VHr=4.1 VL=3.0 VLr=3.1
.param R3={{S*VR/VH}}  R23={{S*VR/VL}}  R2={{R23-R3}}  R1={{S-R23}}
.param Rhd={{R23*VLr/VR - S}}
.param Rhu={{(VR/VHr*S - R3)/(1-VR/VHr)}}
R1  t_r  t_dh {{R1}}
Rhd t_dh t_d  {{Rhd}}
R2  t_d  t_u  {{R2}}
Rhu t_u  t_uh {{Rhu}}
R3  t_uh 0    {{R3}}
* capacitores externos de filtro nos taps de alta impedancia
Ctu t_u 0 10p
Ctd t_d 0 10p"""


for ver in ('v1', 'v2'):
    blocos = '../../blocos_v1' if ver == 'v1' else '../../blocos'
    for caso, (iph, vin0, tf, t0) in CASOS.items():
        if ver == 'v1':
            chip = 'XIC vbat vstor lbst trigger t_r t_u t_uh t_d t_dh chip'
            diodo = '* (v1: diodo integrado dentro do chip)'
            S = '20e6'
        else:
            chip = 'XIC vbat lbst vin_dc trigger t_r t_u t_uh t_d t_dh chip'
            diodo = 'XDS lbst vstor schottky_ext'
            S = '100e6'
        txt = f"""* Balanco de energia {ver} - caso '{caso}' (Iph = {iph}A), bateria ideal 3,7 V (corrente positiva = carregando)
{LIB}
.include "{blocos}/celula_fv.spice"
.include "{blocos}/chip.spice"
.option interp
Xcel vin_dc 0 celula_fv Iph={iph}
Cin vin_dc 0 100n IC={vin0}
L1 vin_dc lx 220u IC=0
RL lx lbst 5
{diodo}
Cout vstor 0 1u IC=3.7
* bateria ideal; a carga liquida que entra nela e integrada pelo proprio
* simulador (v(qbat) = integral de i(VB) dt, em coulombs) -> media exata,
* sem depender da grade de saida
Vmed vstor vbat 0
VB vbat 0 3.7
Bq 0 qbat I=i(VB)
Cq qbat 0 1
VT trigger 0 0
{divisor(S)}
.ic v(xic.xth.vref)=0.1335
{chip}
.control
set wr_singlescale
set wr_vecnames
tran 1u {tf} 0 20n uic
meas tran q0 find v(qbat) at={t0}
meas tran q1 find v(qbat) at={tf}
let ibat = (q1 - q0)/({float(tf[:-1])*1e-3} - {float(t0[:-1])*1e-3})
meas tran vin avg v(vin_dc) from={t0} to={tf}
meas tran vdd avg v(xic.vdd) from={t0} to={tf}
echo RESULT {ver} {caso} $&ibat $&vin $&vdd
wrdata ../dados/balanco_{ver}_{caso}.txt v(vin_dc) v(xic.vdd) v(qbat)
quit
.endc
.end
"""
        with open(os.path.join(TB, f'balanco_{ver}_{caso}.spice'), 'w') as f:
            f.write(txt)
print('ok')
