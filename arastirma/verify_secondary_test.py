"""Wyckoff: buy the SECONDARY TEST (ST) / SPRING after a selling climax, versus buying the climax itself and
versus random entries in the same decline background. Daily, 9 ETFs, 2005+. No costs.
Climax (day c): decline background (10d ret <= -1.5 ATR, close within 5% of 20d low) + volume >= 2x 20d avg
                + range >= 1.2 ATR.
ST (day s, 3..15 days after c): low within [climax_low - 0.5 ATR, climax_low + 0.5 ATR], volume < 0.7 x climax
                volume, range < climax range, close > climax_low.  'spring' = ST whose low < climax_low.
Trade: long at close; stop = min(climax_low, ST low) - 0.1 ATR; target 2R; time exit after 20 days.
Baselines: (1) long at the CLIMAX close with stop = climax low - 0.1 ATR; (2) long at close of ANY decline-background
day with stop = 20d low - 0.1 ATR. Same target/time rules.
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SYMS = ("SPY", "QQQ", "IWM", "DIA", "GLD", "TLT", "XLE", "XLF", "EEM")


def trade(C, Hh, L, t, entry, stop, k=2.0, maxd=20):
    R = entry - stop
    if R <= 0:
        return None
    for j in range(t + 1, min(t + 1 + maxd, len(C))):
        if L[j] <= stop:
            return -1.0
        if Hh[j] >= entry + k * R:
            return k
    j = min(t + maxd, len(C) - 1)
    return (C[j] - entry) / R


out = {"ST (no undercut)": [], "spring (undercut)": [], "buy climax close": [], "random decline day": []}
years = {k: [] for k in out}
for sym in SYMS:
    d = yf.download(sym, start="2004-06-01", interval="1d", progress=False, auto_adjust=True)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna()
    O, Hh, L, C, V = (d[c].values for c in ("Open", "High", "Low", "Close", "Volume"))
    yr = d.index.year.values
    tr = np.maximum(Hh - L, np.maximum(abs(Hh - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = np.convolve(tr, np.ones(14) / 14, mode="full")[:len(tr)]
    vavg = np.convolve(V, np.ones(20) / 20, mode="full")[:len(V)]
    last_c = -99
    rng_seed = np.random.default_rng(hash(sym) % 2**32)
    for t in range(25, len(C) - 21):
        if yr[t] < 2005:
            continue
        a = atr[t - 1]
        if a <= 0 or vavg[t - 1] <= 0:
            continue
        decline = (C[t] - C[t - 10]) <= -1.5 * a and C[t] <= L[t - 19:t + 1].min() * 1.05
        if not decline:
            continue
        # random baseline: sample ~1 in 8 decline days to limit clustering
        if rng_seed.random() < 0.125:
            r = trade(C, Hh, L, t, C[t], L[t - 19:t + 1].min() - 0.1 * a)
            if r is not None:
                out["random decline day"].append(r); years["random decline day"].append(yr[t])
        climax = V[t] >= 2.0 * vavg[t - 1] and (Hh[t] - L[t]) >= 1.2 * a
        if not climax or t - last_c <= 15:
            continue
        last_c = t
        cl, cv, cr = L[t], V[t], Hh[t] - L[t]
        r = trade(C, Hh, L, t, C[t], cl - 0.1 * a)
        if r is not None:
            out["buy climax close"].append(r); years["buy climax close"].append(yr[t])
        for s in range(t + 3, min(t + 16, len(C) - 21)):
            if L[s] < cl - 1.0 * a:      # broke down hard -> no ST
                break
            if abs(L[s] - cl) <= 0.5 * a and V[s] < 0.7 * cv and (Hh[s] - L[s]) < cr and C[s] > cl:
                kind = "spring (undercut)" if L[s] < cl else "ST (no undercut)"
                r = trade(C, Hh, L, s, C[s], min(cl, L[s]) - 0.1 * a)
                if r is not None:
                    out[kind].append(r); years[kind].append(yr[s])
                break

print("Long trades, 2R target / stop below lows / 20-day time exit, R multiples (no costs). 9 ETFs daily 2005+")
for k, v in out.items():
    v = np.array(v)
    y = np.array(years[k])
    if len(v) == 0:
        print(f"{k:22s}: n=0"); continue
    a1 = v[y < 2015]; a2 = v[y >= 2015]
    print(f"{k:22s}: n={len(v):4d} avg {v.mean():+.3f}R (se {v.std()/np.sqrt(len(v)):.3f}) | win(2R) {np.mean(v==2.0):.0%} "
          f"stop {np.mean(v==-1.0):.0%} | 2005-14 {a1.mean() if len(a1) else float('nan'):+.2f} (n={len(a1)}) "
          f"| 2015+ {a2.mean() if len(a2) else float('nan'):+.2f} (n={len(a2)})")
