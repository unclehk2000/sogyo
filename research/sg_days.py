"""Sōgyo on every NQ day (2018 - 9 Oct 2026): prior 16:14 close (C1) and 16:59 close (C2), 09:30 open (O), CE1 / CE2 / Z,
the card's gap (|O - (C1 + C2) / 2|) and overnight range (18:00-09:29) in RTH ATR (mean of the last 14 RTH 09:30-16:14
ranges), the card's context, and the RTH path for the outcome scripts. Days kept: prior close and today's open on the same
contract, a full prior session (16:14 and 16:59 bars present), a full RTH today."""
import numpy as np, pandas as pd, pickle
b = pd.read_pickle('/home/claude/kyw/bars_NQ_all.pkl')[['ts', 'Open', 'High', 'Low', 'Close', 'tday', 'hm', 'Contract']].reset_index(drop=True)
O_, H_, L_, C_, hm, td, ct = (b[c].to_numpy() for c in ('Open', 'High', 'Low', 'Close', 'hm', 'tday', 'Contract'))
ds = np.r_[0, np.flatnonzero(td[1:] != td[:-1]) + 1]; de = np.r_[ds[1:], len(b)]
days = []
for s, e in zip(ds, de):
    h = hm[s:e]
    rth = np.flatnonzero((h >= 930) & (h < 1615)) + s; on = np.flatnonzero((h >= 1800) | (h < 930)) + s
    k1614 = np.flatnonzero(h == 1614); k1659 = np.flatnonzero(h == 1659)
    days.append(dict(day=pd.Timestamp(td[s]), s=s, e=e, rth=rth, on=on, i1614=s + k1614[0] if len(k1614) else -1, i1659=s + k1659[0] if len(k1659) else -1))
rows, paths = [], {}
rng = []
for i in range(1, len(days)):
    p, d = days[i - 1], days[i]
    if len(p['rth']) >= 380: rng.append((p['day'], H_[p['rth']].max() - L_[p['rth']].min()))
    if p['i1614'] < 0 or p['i1659'] < 0 or len(d['rth']) < 380 or (d['day'] - p['day']).days > 4: continue
    r0 = d['rth'][0]
    if hm[r0] != 930 or not (ct[p['i1614']] == ct[p['i1659']] == ct[r0]): continue
    hist = [x for t, x in rng if t < d['day']][-14:]
    if len(hist) < 14: continue
    atr = float(np.mean(hist))
    c1, c2, o = C_[p['i1614']], C_[p['i1659']], O_[r0]
    on = d['on']; onR = H_[on].max() - L_[on].min() if len(on) > 600 else np.nan
    gap = abs(o - (c1 + c2) / 2)
    split = np.sign(o - c1) != np.sign(o - c2)
    ctx = 'SPLIT' if split else 'RED' if gap / atr > 0.68 else 'GREEN' if onR / atr <= 0.45 else 'NEUTRAL'
    rows.append(dict(day=d['day'], c1=c1, c2=c2, o=o, ce1=(c1 + o) / 2, ce2=(c2 + o) / 2, atr=atr, gap=gap, gapA=gap / atr, onA=onR / atr,
                     gapPct=100 * abs(o - c1) / o, wPts=abs(c1 - c2) / 2, wPct=100 * abs(c1 - c2) / 2 / o, split=split, ctx=ctx, dirn=np.sign((c1 + c2) / 2 - o)))
    paths[d['day']] = d['rth']
X = pd.DataFrame(rows); X['year'] = X.day.dt.year
X['period'] = np.select([X.year == 2018, X.year <= 2021], ['2018', '2019-21'], '2022-26')
X.to_pickle('days.pkl'); pickle.dump(paths, open('paths.pkl', 'wb'))
print(len(X), 'days'); print(X.groupby('period').size().to_dict()); print(X.ctx.value_counts().to_dict())
print(X[['gapPct', 'wPts', 'wPct', 'gapA', 'onA']].describe(percentiles=[.25, .5, .75, .9]).round(3).to_string())
