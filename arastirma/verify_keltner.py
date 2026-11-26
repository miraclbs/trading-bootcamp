"""Round 57: Adam Grimes, Better System Trader ep. 55 (UVtbKTdo-Vc) on Keltner channels:
 (1) "There is a tendency for reversal outside of a band ... but good luck fading every touch of a band; it differs by
     asset class and time frame and is streaky."
 (2) "If a market went to an upper band, made a low-volatility reversal and did not pull back much from that band,
     there's an edge for continued momentum in that direction."
 (3) "Bollinger vs Keltner: very similar statistics, the concept is what matters."
Test (daily, 2005+): Keltner = EMA20 +/- 2.25 x ATR20; Bollinger = SMA20 +/- 2 x stdev20.
 Fade: close beyond a band -> enter AGAINST it at the next open; forward 5- and 10-day return in ATR units minus the
 same-side unconditional forward return of that market (drift-matched baseline).
 Momentum continuation: close beyond the band, then within 3 days a pullback day (close back toward the average) with
 a range below the 20-day average range whose close stays more than 1 ATR beyond the average -> enter WITH the move at
 the next open; same measurement.
Markets: index ETFs, sector/country ETFs, bonds, gold, oil, and commodity futures. Split 2005-14 / 2015+.
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SYMS = ("SPY QQQ IWM DIA EFA EEM EWJ EWG XLE XLF XLK TLT IEF GLD SLV USO "
        "GC=F CL=F HG=F ZC=F ZS=F ZW=F KC=F SB=F").split()
res = {}


def add(k, per, v):
    res.setdefault((k, per), []).append(v)


for s in SYMS:
    d = yf.download(s, start="2004-01-01", interval="1d", progress=False, auto_adjust=True)
    if d is None or len(d) < 800:
        continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna(); d = d[(d["High"] > d["Low"]) & (d["Low"] > 0)]
    O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    yr = d.index.year.values
    tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = pd.Series(tr).rolling(20).mean().to_numpy()
    rng20 = pd.Series(H - L).rolling(20).mean().to_numpy()
    ema = pd.Series(C).ewm(span=20, adjust=False).mean().to_numpy()
    sma = pd.Series(C).rolling(20).mean().to_numpy(); sd = pd.Series(C).rolling(20).std().to_numpy()
    bands = {"Keltner": (ema + 2.25 * atr, ema - 2.25 * atr, ema), "Bollinger": (sma + 2 * sd, sma - 2 * sd, sma)}
    n = len(C)
    f5 = np.full(n, np.nan); f10 = np.full(n, np.nan)
    f5[:-6] = (C[6:] - O[1:-5]); f10[:-11] = (C[11:] - O[1:-10])  # entry next open (t+1), exit close t+5 / t+10
    base5 = np.nanmean(f5[30:] / atr[30:]); base10 = np.nanmean(f10[30:] / atr[30:])
    for name, (up, dn, mid) in bands.items():
        last = -10
        for t in range(30, n - 12):
            if yr[t] < 2005 or np.isnan(atr[t]) or np.isnan(up[t]):
                continue
            per = "2005-14" if yr[t] < 2015 else "2015+"
            side = 1 if C[t] > up[t] else -1 if C[t] < dn[t] else 0
            if side and t > last:
                # fade: trade against the band break
                add((name, "fade 5d"), per, -side * f5[t] / atr[t] - (-side * base5))
                add((name, "fade 10d"), per, -side * f10[t] / atr[t] - (-side * base10))
                # continuation: low-volatility pullback that stays > 1 ATR beyond the average, within 3 days
                for k in range(t + 1, min(t + 4, n - 12)):
                    pulled = side * (C[k] - C[k - 1]) < 0
                    if pulled and (H[k] - L[k]) < rng20[k] and side * (C[k] - mid[k]) > atr[k]:
                        add((name, "momentum 10d"), per, side * f10[k] / atr[k] - side * base10)
                        break
                last = t + 5

print("Excess forward return in ATR units vs the same-side unconditional return (positive = edge). mean (se, n)")
for name in ("Keltner", "Bollinger"):
    for kind in ("fade 5d", "fade 10d", "momentum 10d"):
        cells = []
        for per in ("2005-14", "2015+"):
            x = np.array(res.get(((name, kind), per), []))
            cells.append(f"{per}: {x.mean():+.3f} ({x.std() / np.sqrt(len(x)):.3f}, n={len(x)})" if len(x) else f"{per}: n=0")
        print(f"   {name:9s} {kind:13s} | " + " | ".join(cells))
