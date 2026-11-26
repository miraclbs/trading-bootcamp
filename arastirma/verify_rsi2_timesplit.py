"""Round 37: time-split re-test of Connors RSI(2) (round 24 found +0.33R per trade after 2009) against a
PERIOD-matched random baseline (lesson from round 36: the pullback edge vanished after 2015 once the baseline was
matched). Rule (Connors): close > SMA200 and RSI(2) < 10 -> buy at close; exit at the first close > SMA5 (max 10 days).
Baseline: for every RSI-2 trade, 5 random days in the same symbol and the same period with close > SMA200, held for
the same number of days. Units: ATR(14) at entry (R) and %. 21 index/country ETFs, daily, no costs.
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SYMS = ("SPY QQQ IWM DIA EEM EFA EWJ EWG MDY EWU EWC EWA EWH EWT EWY EWW EWS EWL EWQ EWP EWI").split()
PER = (("2003-09", 2003, 2010), ("2010-14", 2010, 2015), ("2015-19", 2015, 2020), ("2020+", 2020, 2100),
       ("2015+", 2015, 2100))


def rsi(c, n=2):
    d = np.diff(c, prepend=c[0]); up = np.clip(d, 0, None); dn = np.clip(-d, 0, None)
    au = np.zeros_like(c); ad = np.zeros_like(c)
    for i in range(1, len(c)):
        au[i] = au[i - 1] + (up[i] - au[i - 1]) / n; ad[i] = ad[i - 1] + (dn[i] - ad[i - 1]) / n
    return 100 - 100 / (1 + au / np.where(ad == 0, 1e-12, ad))


rows = []   # (year, R, pct, baseR, basepct)
for s in SYMS:
    d = yf.download(s, start="2002-01-01", interval="1d", progress=False, auto_adjust=True)
    if d is None or len(d) < 400:
        continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna()
    H, L, C = (d[c].values for c in ("High", "Low", "Close")); yr = d.index.year.values
    tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = np.convolve(tr, np.ones(14) / 14, mode="full")[:len(tr)]
    sma200 = np.convolve(C, np.ones(200) / 200, mode="full")[:len(C)]; sma5 = np.convolve(C, np.ones(5) / 5, mode="full")[:len(C)]
    r2 = rsi(C); T = len(C); rng = np.random.default_rng(sum(map(ord, s)))
    up_days = np.array([t for t in range(201, T - 11) if C[t] > sma200[t]])
    t = 201
    while t < T - 11:
        if C[t] > sma200[t] and r2[t] < 10:
            h = 1
            while h < 10 and C[t + h] <= sma5[t + h]:
                h += 1
            R = (C[t + h] - C[t]) / atr[t]; pct = C[t + h] / C[t] - 1
            same = up_days[(yr[up_days] >= (yr[t] // 5) * 5) & (yr[up_days] < (yr[t] // 5) * 5 + 5)]
            pick = rng.choice(same, 5) if len(same) else rng.choice(up_days, 5)
            bR = np.mean([(C[u + h] - C[u]) / atr[u] for u in pick]); bp = np.mean([C[u + h] / C[u] - 1 for u in pick])
            rows.append((yr[t], R, pct, bR, bp))
            t += h + 1
        else:
            t += 1
A = np.array(rows)
print(f"Connors RSI(2) long, 21 index/country ETFs, n={len(A)} trades, no costs. RSI-2 minus period-matched random "
      f"entry with the same holding period (5-year buckets)")
print("  period  |   n  | RSI-2 R / %      | baseline R / %   | diff R (se)   | diff % | win RSI-2 / base")
for name, a, b in PER:
    m = (A[:, 0] >= a) & (A[:, 0] < b)
    x = A[m]; diff = x[:, 1] - x[:, 3]
    print(f"  {name:8s}| {m.sum():4d} | {x[:, 1].mean():+.3f} / {x[:, 2].mean():+.2%} | {x[:, 3].mean():+.3f} / "
          f"{x[:, 4].mean():+.2%} | {diff.mean():+.3f} ({diff.std() / np.sqrt(len(diff)):.3f}) | "
          f"{(x[:, 2] - x[:, 4]).mean():+.2%} | {np.mean(x[:, 1] > 0):.0%}")
