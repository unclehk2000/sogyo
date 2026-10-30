"""Sōgyo outcomes on all NQ days: (1) the target map (zone touched by time, full fill, by gap size, conditional decay);
(2) the NY AM wall at Z by the card's context, against symmetric placebo races at the 0.375 / 0.625 fractions;
(3) the flipped wall (through-and-retest, 09:30-11:59) against equal-width decoys. Periods: 2018, 2019-21 (never tested
before: the earlier study had 2018 and 2022-26 only), 2022-26."""
import pickle, numpy as np, pandas as pd
X = pd.read_pickle('days.pkl'); P = pickle.load(open('paths.pkl', 'rb'))
b = pd.read_pickle('/home/claude/kyw/bars_NQ_all.pkl')
H, L, C, hm = b.High.to_numpy(), b.Low.to_numpy(), b.Close.to_numpy(), b.hm.to_numpy()
CK = [935, 945, 1000, 1030, 1100, 1200, 1615]
def first_touch(idx, lo, hi):
    """first bar in idx trading inside or through [lo, hi]"""
    k = np.flatnonzero((L[idx] <= hi) & (H[idx] >= lo))
    return k[0] if len(k) else None
def race(idx, k0, up_lv, dn_lv, mid, end_hm, open_up):
    """from bar k0+1: which of up_lv / dn_lv first; unresolved -> side of mid at the last bar before end_hm.
    returns 1 if price went the 'open' way (up if open_up)"""
    seg = idx[k0 + 1:]; seg = seg[hm[seg] < end_hm]
    if not len(seg): return np.nan
    u = np.flatnonzero(H[seg] >= up_lv); d = np.flatnonzero(L[seg] <= dn_lv)
    tu = u[0] if len(u) else 10 ** 9; tdn = d[0] if len(d) else 10 ** 9
    if tu == tdn:
        if tu == 10 ** 9: went_up = C[seg[-1]] > mid
        else: return np.nan
    else: went_up = tu < tdn
    return float(went_up == open_up)
rows = []
for r in X.itertuples():
    idx = P[r.day]; t = hm[idx]
    zlo, zhi = min(r.ce1, r.ce2), max(r.ce1, r.ce2); F = (r.c1 + r.c2) / 2; G = abs(r.o - F); s = np.sign(F - r.o)   # s: direction to the fill
    near = r.ce1 if abs(r.ce1 - r.o) <= abs(r.ce2 - r.o) else r.ce2; far = r.ce2 if near == r.ce1 else r.ce1
    rec = dict(day=r.day, period=r.period, year=r.year, ctx=r.ctx, split=r.split, gapPct=r.gapPct, wPct=r.wPct, gapA=r.gapA, onA=r.onA)
    # (1) touches
    for nm, lo, hi in (('near', near, near), ('far', far, far), ('zone', zlo, zhi), ('fill', r.c1, r.c1)):
        k = first_touch(idx, min(lo, hi), max(lo, hi))
        rec[f't_{nm}'] = int(t[k]) if k is not None else np.nan
    # (2) NY AM wall at Z and the placebos (aligned days, gap >= 0.10%)
    if not r.split and r.gapPct >= 0.10 and G > 0:
        am = idx[t < 1100]
        for q in (0.375, 0.5, 0.625):
            lv = r.o + s * q * G
            k = first_touch(am, lv, lv)
            if k is None: rec[f'w{q}'] = np.nan; continue
            up_lv, dn_lv = lv + 0.5 * G, lv - 0.5 * G          # symmetric: half a gap each way
            open_up = s < 0                                       # the open is above the level when the fill is below
            rec[f'w{q}'] = race(am, k, up_lv, dn_lv, lv, 1100, open_up)
            if q == 0.5: rec['wTouchHm'] = int(hm[am[k]])
    # (3) flipped wall: through 0.125 G past the far edge toward the fill, then back to the far edge from the fill side
    if not r.split and r.gapPct >= 0.10 and G > 0:
        w = idx[t < 1200]; zw = zhi - zlo
        for nm, cz in (('z', (zlo + zhi) / 2), ('d375', r.o + s * 0.375 * G), ('d625', r.o + s * 0.625 * G)):
            lo_, hi_ = cz - zw / 2, cz + zw / 2
            farE = hi_ if s < 0 else lo_                           # edge on the fill side... (s<0: fill below, far edge = lower)
            farE = lo_ if s < 0 else hi_
            thr = farE + s * 0.125 * G
            th = np.flatnonzero((L[w] <= thr) if s < 0 else (H[w] >= thr))
            if not len(th): rec[f'f_{nm}'] = np.nan; continue
            k1 = th[0]
            back = np.flatnonzero((H[w[k1 + 1:]] >= farE) if s < 0 else (L[w[k1 + 1:]] <= farE))
            if not len(back): rec[f'f_{nm}'] = np.nan; continue
            k2 = k1 + 1 + back[0]
            # from the retest: 0.25 G further toward the fill (wall holds) vs 0.25 G back toward the open
            up_lv, dn_lv = farE + 0.25 * G, farE - 0.25 * G
            fill_down = s < 0
            res = race(w, k2, up_lv, dn_lv, farE, 1200, not fill_down)   # 'open_up' param: success = went toward the fill
            rec[f'f_{nm}'] = res
    rows.append(rec)
T = pd.DataFrame(rows); T.to_pickle('out.pkl'); print(T.shape)
