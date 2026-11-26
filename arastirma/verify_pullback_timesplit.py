"""Grimes' core template: after a strong MOMENTUM move, buy the first PULLBACK in the trend direction (and the mirror
for shorts). Daily, 2005+, four groups (index ETFs, 30 large-cap stocks, commodity ETFs, FX majors). No costs.
Momentum event (day m): close > EMA20 + 2.25*ATR20 (upper Keltner, long) / close < EMA20 - 2.25*ATR20 (short).
First pullback (day p, 3..20 days after m): low touches YESTERDAY's EMA20 (no look-ahead: Grimes' 'time machine'
warning - today's EMA moves intrabar). Fill at min(open, EMA20[p-1]) (long). Skip if price closed beyond the opposite
Keltner band first (trend broken).
Measured simply (Grimes: 'just look at returns over different horizons'): forward return from fill to close of
p+h, h = 5/10/20, in ATR units, signed in trade direction, minus the symbol's unconditional h-day drift (signed).
Baselines: (a) any day where the trend state holds (close > EMA20 and EMA20 rising for long), entered at close,
signed+drift-adjusted, 1-in-5 sampled; (b) the momentum day close itself (chasing).
Also a simple trade version: stop 1 ATR beyond fill, target 2R, 20-day time exit -> mean R.
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GROUPS = {
    "INDEX": "SPY QQQ IWM DIA EEM EFA EWJ EWG MDY".split(),
    "INDEX2 (out-of-sample country ETFs)": "EWU EWC EWA EWH EWT EWY EWW EWS EWL EWQ EWP EWI".split(),
    "STOCKS": ("AAPL MSFT JNJ PG KO PEP XOM CVX JPM BAC WFC GE IBM INTC CSCO ORCL WMT HD MCD DIS MRK PFE T VZ MMM "
               "CAT BA HON UNH AMGN").split(),
    "COMMOD": "GLD SLV USO UNG DBA DBC PPLT PALL UGA CPER CORN WEAT SOYB".split(),
    "FX": "EURUSD=X GBPUSD=X USDJPY=X AUDUSD=X USDCAD=X USDCHF=X NZDUSD=X".split(),
}
HS = (5, 10, 20)


def ema(x, n):
    a = 2 / (n + 1)
    out = np.empty_like(x)
    out[0] = x[0]
    for i in range(1, len(x)):
        out[i] = a * x[i] + (1 - a) * out[i - 1]
    return out


def trade(O, Hh, L, C, t, fill, side, a, k=2.0, maxd=20):
    stop = fill - side * a
    tgt = fill + side * k * a
    # same-day: assume worst case if bar after fill hits stop (we filled intraday at a limit; check day t close)
    for j in range(t, min(t + 1 + maxd, len(C))):
        lo, hi = (L[j], Hh[j])
        if j == t:   # on fill day only the part after fill is unknown; be conservative: stop if close beyond stop
            if (side == 1 and C[j] <= stop) or (side == -1 and C[j] >= stop):
                return -1.0
            continue
        if (side == 1 and lo <= stop) or (side == -1 and hi >= stop):
            return -1.0
        if (side == 1 and hi >= tgt) or (side == -1 and lo <= tgt):
            return k
    j = min(t + maxd, len(C) - 1)
    return side * (C[j] - fill) / a


rows = {}
for g, syms in GROUPS.items():
    R = {k: {h: [] for h in HS} for k in ("pullback", "trend-state day", "momentum-day close")}
    tr_R, yrs_pb, tr_side, base_tr, base_yr, base_sd = [], [], [], [], [], []
    for sym in syms:
        d = yf.download(sym, start="2004-01-01", interval="1d", progress=False, auto_adjust=True)
        if d is None or len(d) < 300:
            continue
        if hasattr(d.columns, "levels"):
            d.columns = d.columns.get_level_values(0)
        d = d.dropna()
        d = d[(d["High"] > 0) & (d["Low"] > 0)]
        O, Hh, L, C = (d[c].values for c in ("Open", "High", "Low", "Close"))
        yr = d.index.year.values
        tr = np.maximum(Hh - L, np.maximum(abs(Hh - np.roll(C, 1)), abs(L - np.roll(C, 1))))
        atr = np.convolve(tr, np.ones(20) / 20, mode="full")[:len(tr)]
        e = ema(C, 20)
        T = len(C)
        drift = {h: np.nanmean([(C[t + h] - C[t]) / atr[t - 1] for t in range(30, T - h) if yr[t] >= 2005])
                 for h in HS}
        rng = np.random.default_rng(sum(map(ord, sym)))
        last_m = {1: -99, -1: -99}
        for t in range(30, T - 21):
            if yr[t] < 2005 or atr[t - 1] <= 0:
                continue
            a = atr[t - 1]
            # baseline (a): trend-state day
            for side in (1, -1):
                state = (side * (C[t] - e[t]) > 0) and (side * (e[t] - e[t - 5]) > 0)
                if state and rng.random() < 0.2:
                    for h in HS:
                        R["trend-state day"][h].append(side * ((C[t + h] - C[t]) / a - drift[h]))
                    base_tr.append(trade(O, Hh, L, C, t, C[t], side, a)); base_yr.append(yr[t]); base_sd.append(side)
            # momentum events
            for side in (1, -1):
                band = e[t] + side * 2.25 * atr[t]
                if side * (C[t] - band) <= 0 or t - last_m[side] < 20:
                    continue
                last_m[side] = t
                for h in HS:
                    R["momentum-day close"][h].append(side * ((C[t + h] - C[t]) / a - drift[h]))
                for p in range(t + 3, min(t + 21, T - 21)):
                    lvl = e[p - 1]
                    opp = e[p - 1] - side * 2.25 * atr[p - 1]
                    if side * (C[p - 1] - opp) < 0:      # trend broken before pullback
                        break
                    touched = (L[p] <= lvl) if side == 1 else (Hh[p] >= lvl)
                    if not touched:
                        continue
                    fill = min(O[p], lvl) if side == 1 else max(O[p], lvl)
                    ap = atr[p - 1]
                    for h in HS:
                        R["pullback"][h].append(side * ((C[p + h] - fill) / ap - drift[h]))
                    tr_R.append(trade(O, Hh, L, C, p, fill, side, ap)); yrs_pb.append(yr[p]); tr_side.append(side)
                    break
    rows[g] = (R, np.array(tr_R), np.array(yrs_pb), np.array(tr_side), np.array(base_tr), np.array(base_yr), np.array(base_sd))


def f(v):
    v = np.array(v)
    return f"{v.mean():+.3f} (se {v.std()/np.sqrt(len(v)):.3f})" if len(v) > 1 else "n/a"


print("Round 36: TIME-split re-test of the pullback edge (Grimes: a different ticker is not out-of-sample).")
print("Pullback trade minus random trend-state-day trade (same exits), by period and side. R per trade (se)")
PER = (("2005-09", 2005, 2010), ("2010-14", 2010, 2015), ("2015-19", 2015, 2020), ("2020+", 2020, 2100))
for g, (R, trR, y, sd, btr, by, bsd) in rows.items():
    print(); print(g)
    for side, lab in ((1, "LONG "), (-1, "SHORT"), (0, "BOTH ")):
        cells = []
        for name, a, b in PER + (("2015+", 2015, 2100),):
            m = (y >= a) & (y < b) & ((sd == side) if side else True)
            mb = (by >= a) & (by < b) & ((bsd == side) if side else True)
            if m.sum() < 10:
                cells.append(f"{name} n/a"); continue
            diff = trR[m].mean() - btr[mb].mean()
            se = np.sqrt(trR[m].var() / m.sum() + btr[mb].var() / mb.sum())
            cells.append(f"{name} {diff:+.2f} ({se:.2f}) n={m.sum()}")
        print(f"  {lab}: " + " | ".join(cells))
