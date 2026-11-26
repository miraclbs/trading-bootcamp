"""Round 16: does the 'character' of the pullback matter? (Grimes: quiet, orderly pullbacks are better; the
structure matters more than the trigger.)  Same base setup as verify_pullback.py (first touch of yesterday's EMA20,
3..20 days after a close outside the 2.25-ATR Keltner band; fill at min(open, EMA20[p-1]); stop 1 ATR, target 2R,
20-day time exit). LONG side only (where the edge was), daily 2005+, no costs.
Features measured at the pullback day (all known at entry, no look-ahead):
  depth   : (highest high since momentum day - fill) / ATR       (how far it has pulled back)
  days    : p - m                                                  (how long the pullback took)
  quiet   : mean (H-L) of bars m+1..p-1 / ATR[m]                   (low = quiet, orderly pullback)
  thrust  : (C[m] - upper band[m]) / ATR[m]                        (strength of the momentum day)
  lt_trend: close[p-1] above 200-day SMA (1) or not (0)
Three sets: INDEX (in-sample, where the edge was found), INDEX2 (12 unseen country ETFs), STOCKS (30 large caps).
A filter is only believable if the SAME bin is better in all three sets (15 comparisons -> expect ~1 false hit).
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SETS = {
    "INDEX": "SPY QQQ IWM DIA EEM EFA EWJ EWG MDY".split(),
    "INDEX2": "EWU EWC EWA EWH EWT EWY EWW EWS EWL EWQ EWP EWI".split(),
    "STOCKS": ("AAPL MSFT JNJ PG KO PEP XOM CVX JPM BAC WFC GE IBM INTC CSCO ORCL WMT HD MCD DIS MRK PFE T VZ MMM "
               "CAT BA HON UNH AMGN").split(),
}


def ema(x, n):
    a = 2 / (n + 1)
    out = np.empty_like(x); out[0] = x[0]
    for i in range(1, len(x)):
        out[i] = a * x[i] + (1 - a) * out[i - 1]
    return out


def trade(Hh, L, C, t, fill, a, k=2.0, maxd=20):
    stop, tgt = fill - a, fill + k * a
    if C[t] <= stop:
        return -1.0
    for j in range(t + 1, min(t + 1 + maxd, len(C))):
        if L[j] <= stop:
            return -1.0
        if Hh[j] >= tgt:
            return k
    return (C[min(t + maxd, len(C) - 1)] - fill) / a


data = {}
for name, syms in SETS.items():
    rows = []
    for sym in syms:
        d = yf.download(sym, start="2004-01-01", interval="1d", progress=False, auto_adjust=True)
        if d is None or len(d) < 400:
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
        sma200 = np.convolve(C, np.ones(200) / 200, mode="full")[:len(C)]
        T = len(C); last_m = -99
        for t in range(210, T - 21):
            if yr[t] < 2005 or atr[t - 1] <= 0:
                continue
            band = e[t] + 2.25 * atr[t]
            if C[t] <= band or t - last_m < 20:
                continue
            last_m = t
            for p in range(t + 3, min(t + 21, T - 21)):
                if C[p - 1] < e[p - 1] - 2.25 * atr[p - 1]:
                    break
                lvl = e[p - 1]
                if L[p] > lvl:
                    continue
                fill = min(O[p], lvl); ap = atr[p - 1]
                r = trade(Hh, L, C, p, fill, ap)
                rows.append(dict(r=r, yr=yr[p],
                                 depth=(Hh[t:p].max() - fill) / ap,
                                 days=p - t,
                                 quiet=np.mean(Hh[t + 1:p] - L[t + 1:p]) / atr[t],
                                 thrust=(C[t] - band) / atr[t],
                                 lt_trend=1.0 if C[p - 1] > sma200[p - 1] else 0.0))
                break
    data[name] = rows
    print(f"{name}: {len(rows)} long pullback trades, avg {np.mean([x['r'] for x in rows]):+.3f}R")

print("\nAvg R by feature tercile (cut points from the pooled sample). se in brackets. 'ALL3' = same direction in all sets")
pool = [x for v in data.values() for x in v]
for feat in ("depth", "days", "quiet", "thrust", "lt_trend"):
    vals = np.array([x[feat] for x in pool])
    if feat == "lt_trend":
        cuts = [0.5]; labels = ["below 200SMA", "above 200SMA"]
    else:
        cuts = list(np.quantile(vals, [1 / 3, 2 / 3])); labels = [f"low (<{cuts[0]:.2f})", f"mid", f"high (>{cuts[1]:.2f})"]
    print(f"\n{feat}:")
    best = {}
    for name, rows in data.items():
        v = np.array([x[feat] for x in rows]); r = np.array([x["r"] for x in rows])
        b = np.digitize(v, cuts)
        parts = []
        means = []
        for i, lab in enumerate(labels):
            rr = r[b == i]
            m = rr.mean() if len(rr) else np.nan
            means.append(m)
            parts.append(f"{lab}: {m:+.3f} [{rr.std()/np.sqrt(max(len(rr),1)):.3f}] n={len(rr)}")
        best[name] = int(np.nanargmax(means)); worst = int(np.nanargmin(means))
        best[name + "_w"] = worst
        print(f"  {name:7s} " + " | ".join(parts))
    bsets = {best[n] for n in data}; wsets = {best[n + '_w'] for n in data}
    print(f"  -> best bin same in all 3 sets: {'YES ' + labels[bsets.pop()] if len(bsets) == 1 else 'no'} | "
          f"worst bin same in all 3: {'YES ' + labels[wsets.pop()] if len(wsets) == 1 else 'no'}")
