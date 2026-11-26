"""Round 36: Adam Grimes on Desire To TRADE (ZHoPjGvQk4Y):
 (1) "I went back over my trades (~200 hours by hand): taking everything off at a 1R target gave a smoother equity
     curve AND more money than my trailing stops; 2R was not better." (He trades trend pullbacks, mostly stocks /
     indices, daily.)
 (2) Quick pattern test: "write it as a system with a 1:1 stop and target; if the target is hit more than 50% of
     the time consistently, the pattern has an edge" - with a 'null/drift probability' baseline.
Test on the same pullback signals as verify_pullback.py (first EMA20 touch after a Keltner momentum day), index ETFs
and 30 large stocks, daily 2005+, no costs, initial stop 1 ATR. Exits: fixed target 0.5R / 1R / 2R (20-day time
stop), Brandt 3-day trailing (exit on close beyond the 3-day low/high, after initial stop), 10-day trailing.
Same exits on random trend-state days (side-matched) = baseline. Report mean R, win rate, mean/std, by period.
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GROUPS = {"INDEX+COUNTRY ETFs": ("SPY QQQ IWM DIA EEM EFA EWJ EWG MDY EWU EWC EWA EWH EWT EWY EWW EWS EWL EWQ EWP "
                                 "EWI").split(),
          "STOCKS": ("AAPL MSFT JNJ PG KO PEP XOM CVX JPM BAC WFC GE IBM INTC CSCO ORCL WMT HD MCD DIS MRK PFE T VZ "
                     "MMM CAT BA HON UNH AMGN").split()}
EXITS = ("T0.5", "T1", "T2", "trail3", "trail10")


def ema(x, n):
    a = 2 / (n + 1); out = np.empty_like(x); out[0] = x[0]
    for i in range(1, len(x)):
        out[i] = a * x[i] + (1 - a) * out[i - 1]
    return out


def exits(O, H, L, C, t, fill, side, a, maxd=20, maxtrail=120):
    res = {}
    stop = fill - side * a
    for k in (0.5, 1.0, 2.0):
        tgt = fill + side * k * a; out = None
        for j in range(t, min(t + 1 + maxd, len(C))):
            if j == t:
                if side * (C[j] - stop) <= 0: out = -1.0; break
                continue
            if (side == 1 and L[j] <= stop) or (side == -1 and H[j] >= stop): out = -1.0; break
            if (side == 1 and H[j] >= tgt) or (side == -1 and L[j] <= tgt): out = k; break
        if out is None:
            j = min(t + maxd, len(C) - 1); out = side * (C[j] - fill) / a
        res[f"T{k:g}"] = out
    for n, lab in ((3, "trail3"), (10, "trail10")):
        out = None
        for j in range(t, min(t + 1 + maxtrail, len(C))):
            if j == t:
                if side * (C[j] - stop) <= 0: out = -1.0; break
                continue
            if (side == 1 and L[j] <= stop) or (side == -1 and H[j] >= stop):
                out = side * (min(O[j], stop) if side == 1 else max(O[j], stop)) - side * fill
                out = out / a; break
            lvl = L[max(t, j - n):j].min() if side == 1 else H[max(t, j - n):j].max()
            if j - t >= n and side * (C[j] - lvl) < 0:
                out = side * (C[j] - fill) / a; break
        if out is None:
            j = min(t + maxtrail, len(C) - 1); out = side * (C[j] - fill) / a
        res[lab] = out
    return res


for g, syms in GROUPS.items():
    sig = {e: [] for e in EXITS}; base = {e: [] for e in EXITS}; sy, sd, by, bd = [], [], [], []
    for sym in syms:
        d = yf.download(sym, start="2004-01-01", interval="1d", progress=False, auto_adjust=True)
        if d is None or len(d) < 300:
            continue
        if hasattr(d.columns, "levels"):
            d.columns = d.columns.get_level_values(0)
        d = d.dropna(); d = d[(d["High"] > 0) & (d["Low"] > 0)]
        O, H, L, C = (d[c].values for c in ("Open", "High", "Low", "Close")); yr = d.index.year.values
        tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)), abs(L - np.roll(C, 1))))
        atr = np.convolve(tr, np.ones(20) / 20, mode="full")[:len(tr)]; e = ema(C, 20); T = len(C)
        rng = np.random.default_rng(sum(map(ord, sym))); last_m = {1: -99, -1: -99}
        for t in range(30, T - 21):
            if yr[t] < 2005 or atr[t - 1] <= 0:
                continue
            for side in (1, -1):
                if (side * (C[t] - e[t]) > 0) and (side * (e[t] - e[t - 5]) > 0) and rng.random() < 0.2:
                    r = exits(O, H, L, C, t, C[t], side, atr[t - 1])
                    for k in EXITS: base[k].append(r[k])
                    by.append(yr[t]); bd.append(side)
                band = e[t] + side * 2.25 * atr[t]
                if side * (C[t] - band) <= 0 or t - last_m[side] < 20:
                    continue
                last_m[side] = t
                for p in range(t + 3, min(t + 21, T - 21)):
                    if side * (C[p - 1] - (e[p - 1] - side * 2.25 * atr[p - 1])) < 0:
                        break
                    if not ((L[p] <= e[p - 1]) if side == 1 else (H[p] >= e[p - 1])):
                        continue
                    fill = min(O[p], e[p - 1]) if side == 1 else max(O[p], e[p - 1])
                    r = exits(O, H, L, C, p, fill, side, atr[p - 1])
                    for k in EXITS: sig[k].append(r[k])
                    sy.append(yr[p]); sd.append(side)
                    break
    sy, sd, by, bd = map(np.array, (sy, sd, by, bd))
    print(f"\n=== {g}: pullback n={len(sy)}, baseline n={len(by)} (no costs, R per trade) ===")
    for side, lab in ((1, "LONG"), (-1, "SHORT")):
        print(f"  {lab}: exit | pullback mean R / win% / mean/std | baseline mean R / win% | diff (se) | "
              f"diff 2005-14 | diff 2015+")
        for k in EXITS:
            s = np.array(sig[k]); b = np.array(base[k]); m = sd == side; mb = bd == side
            diff = s[m].mean() - b[mb].mean(); se = np.sqrt(s[m].var() / m.sum() + b[mb].var() / mb.sum())
            d1 = s[m & (sy < 2015)].mean() - b[mb & (by < 2015)].mean()
            d2 = s[m & (sy >= 2015)].mean() - b[mb & (by >= 2015)].mean()
            print(f"    {k:8s} | {s[m].mean():+.3f} / {np.mean(s[m] > 0):3.0%} / {s[m].mean() / s[m].std():+.3f} | "
                  f"{b[mb].mean():+.3f} / {np.mean(b[mb] > 0):3.0%} | {diff:+.3f} ({se:.3f}) | {d1:+.3f} | {d2:+.3f}")
