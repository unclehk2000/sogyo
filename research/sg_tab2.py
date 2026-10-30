import sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0, '/home/claude/gh2/stats-kit'); from stats_kit import check, table
T = pd.read_pickle('out.pkl'); T['date'] = T.day; T = T.set_index('date')
hmin = lambda v: np.nan if v != v else (int(v) // 100) * 60 + int(v) % 100
T['zone'] = T.t_near.notna(); T['fill'] = T.t_fill.notna(); T['z10'] = T.t_near.map(hmin) < 600
print('=== target map by the card context (all NQ days)')
g = T.groupby('ctx').agg(n=('zone', 'size'), zone_by_10=('z10', 'mean'), zone_RTH=('zone', 'mean'), fill_RTH=('fill', 'mean')).round(3)
print(g.to_string())
for c in ('GREEN', 'NEUTRAL', 'RED'):
    print(c, T[T.ctx == c].groupby('period')[['zone', 'fill']].mean().round(3).to_dict('index'))
S = T[T.split]
print('SPLIT days', len(S), '| CE1 touched', round(S.t_near.notna().mean(), 3), '(near)', round(S.t_far.notna().mean(), 3), '(far) | both', round((S.t_near.notna() & S.t_far.notna()).mean(), 3))
print('\n=== the wall as continuous factors (NQ, touched in NY AM), by period')
W = T.dropna(subset=['w0.5']).copy(); W['lg'] = np.log(W.gapA.clip(0.01)); W['lo'] = np.log(W.onA)
rr = [check(W, 'Q("w0.5") ~ lg + lo', 'lg', period_col='period', group_col=None, test='hold ~ log gap/ATR (ON held)'),
      check(W, 'Q("w0.5") ~ lg + lo', 'lo', period_col='period', group_col=None, test='hold ~ log ON/ATR (gap held)')]
W3 = W.dropna(subset=['w0.375', 'w0.625']).copy(); W3['zs'] = W3['w0.5'] - (W3['w0.375'] + W3['w0.625']) / 2
rr += [check(W3, 'zs ~ lg + lo', 'lo', period_col='period', group_col=None, test='zone premium ~ log ON/ATR')]
print(table(rr)[['coef', 'p', 'n', '2018', '2019-21', '2022-26', 'ok']].round(4).to_string())
W['onq'] = pd.qcut(W.onA, 4); print(W.groupby('onq')[['w0.5', 'w0.375', 'w0.625']].mean().round(3).assign(n=W.groupby('onq').size()).to_string())
W['gq'] = pd.qcut(W.gapA, 4); print(W.groupby('gq')[['w0.5', 'w0.375', 'w0.625']].mean().round(3).assign(n=W.groupby('gq').size()).to_string())
print('\nwall touch minute (median)', W.wTouchHm.median())
