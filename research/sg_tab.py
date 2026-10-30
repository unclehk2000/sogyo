import sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0, '/home/claude/gh2/stats-kit'); from stats_kit import check, table, wilson
T = pd.read_pickle('out.pkl'); T['date'] = T.day; T = T.set_index('date')
A = T[~T.split]
hmin = lambda v: np.nan if v != v else (int(v) // 100) * 60 + int(v) % 100
print('=== 1. target map (aligned days)', len(A), '| by period', A.period.value_counts().to_dict())
for nm in ('near', 'far', 'fill'):
    tm = A[f't_{nm}'].map(hmin)
    print(f'{nm:5s}', ' '.join(f'{c}:{100 * (tm <= hmin(c) - (0 if c == 1615 else 1)).mean():5.1f}' for c in (935, 945, 1000, 1030, 1100, 1200, 1615)))
for p, g in A.groupby('period'):
    tm = g.t_near.map(hmin); tf = g.t_fill.map(hmin)
    print(f'  {p}: near by 10:00 {100 * (tm < 600).mean():.1f}  in RTH {100 * tm.notna().mean():.1f} | fill in RTH {100 * tf.notna().mean():.1f}  n {len(g)}')
A2 = A.copy(); A2['q'] = pd.qcut(A2.gapPct, 5)
tm = A2.t_near.map(hmin); A2['zt'] = tm.notna(); A2['ft'] = A2.t_fill.notna(); A2['mt'] = tm - 570
print(A2.groupby('q').agg(zone=('zt', 'mean'), fill=('ft', 'mean'), med_min=('mt', 'median'), n=('zt', 'size')).round(3).to_string())
tm = A.t_near.map(hmin)
for c, nm in ((600, '10:00'), (660, '11:00')):
    g = tm[~(tm < c)]; print(f'not touched by {nm}: touched later {100 * g.notna().mean():.1f}% (n {len(g)})')
yr = A.assign(z=A.t_near.notna()).groupby('year').z.mean().round(3); print('zone touch by year', yr.to_dict())

print('\n=== 2. NY AM wall at Z (aligned, gap >= 0.10%), symmetric race, 50% under no edge')
W = T.dropna(subset=['w0.5']).copy()
print('touched in NY AM', len(W))
def line(g, nm):
    out = f'{nm:28s} Z {100 * g["w0.5"].mean():5.1f} (n {len(g)})'
    for q in (0.375, 0.625):
        gg = g.dropna(subset=[f'w{q}']); out += f'  | {q}: {100 * gg[f"w{q}"].mean():5.1f}'
    return out
print(line(W, 'all'))
for c in ('GREEN', 'NEUTRAL', 'RED'):
    g = W[W.ctx == c]; print(line(g, c))
    for p, gg in g.groupby('period'): print('     ', line(gg, p))
rr = []
for c in ('GREEN', 'NEUTRAL', 'RED'):
    g = W[W.ctx == c].assign(x=lambda d: d['w0.5'] - 0.5)
    rr.append(check(g, 'x ~ 1', 'Intercept', period_col='period', group_col=None, test=f'{c}: Z holds vs 50%'))
W2 = W.assign(gr=(W.ctx == 'GREEN').astype(float), rd=(W.ctx == 'RED').astype(float))
rr.append(check(W2, 'Q("w0.5") ~ gr + rd', 'gr', period_col='period', group_col=None, test='GREEN vs NEUTRAL'))
rr.append(check(W2, 'Q("w0.5") ~ gr + rd', 'rd', period_col='period', group_col=None, test='RED vs NEUTRAL'))
# zone-specific: Z minus the placebo mean, same days
W3 = W.dropna(subset=['w0.375', 'w0.625']).copy(); W3['zs'] = W3['w0.5'] - (W3['w0.375'] + W3['w0.625']) / 2
for c in ('ALL', 'GREEN', 'NEUTRAL', 'RED'):
    g = W3 if c == 'ALL' else W3[W3.ctx == c]
    rr.append(check(g, 'zs ~ 1', 'Intercept', period_col='period', group_col=None, test=f'{c}: Z minus placebos, same days'))
print(table(rr)[['coef', 'p', 'n', '2018', '2019-21', '2022-26', 'ok']].round(4).to_string())

print('\n=== 3. flipped wall (through, retest, then 0.25 G toward the fill first), 09:30-11:59')
Fw = T.dropna(subset=['f_z']).copy(); Fw['wide'] = Fw.wPct >= 0.05
for nm, g in (('all', Fw), ('wide (>= 0.05%)', Fw[Fw.wide]), ('narrow', Fw[~Fw.wide])):
    dd = g.dropna(subset=['f_d375', 'f_d625'])
    print(f'{nm:16s} zone {100 * g.f_z.mean():5.1f} (n {len(g)}) | decoys .375 {100 * dd.f_d375.mean():5.1f} .625 {100 * dd.f_d625.mean():5.1f}')
    for p, gg in g.groupby('period'): print(f'      {p}: {100 * gg.f_z.mean():5.1f} (n {len(gg)})')
rr = []
for nm, g in (('all', Fw), ('wide', Fw[Fw.wide])):
    rr.append(check(g.assign(x=g.f_z - 0.5), 'x ~ 1', 'Intercept', period_col='period', group_col=None, test=f'flipped wall {nm} vs 50%'))
    dd = g.dropna(subset=['f_d375', 'f_d625']).copy(); dd['zs'] = dd.f_z - (dd.f_d375 + dd.f_d625) / 2
    rr.append(check(dd, 'zs ~ 1', 'Intercept', period_col='period', group_col=None, test=f'flipped wall {nm} minus decoys'))
print(table(rr)[['coef', 'p', 'n', '2018', '2019-21', '2022-26', 'ok']].round(4).to_string())
