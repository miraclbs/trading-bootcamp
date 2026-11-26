"""Side check (user request, 2026-11-22): tweet by @RohOnChain "mathematically unbeatable strategy, 70% win rate":
 "2 candles (yesterday's daily + the last 4 hours) give the direction: both green = only buy, both red = only sell;
  the bot fires only in the first hour of each session (Asia / London / New York); $100 risk for $100 (1:1),
  7 out of 10 win."
Simplified test on 1h data (~2y): at each session start (00:00, 07:00, 13:00 UTC), bias = colour of yesterday's UTC
daily candle AND colour of the last 4 completed hourly bars (open of 4h window -> last close). If they agree, enter in
that direction at the session's first-hour open; stop and target 1 x ATR(24 bars) (1:1); exit at whichever is hit
first within 24 bars, else at the close of bar 24. Baselines: same times, opposite direction, and random direction.
The tweet's extra filters (break + small pullback, skip compressed markets) are not modelled - they reduce the trade
count; a 70% hit rate would still require the base bias to carry a large edge.
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SYMS = ["BTC-USD", "ETH-USD", "EURUSD=X", "GBPUSD=X", "GC=F", "NQ=F", "ES=F"]
rng = np.random.default_rng(7)


def outcome(H, L, C, O, t, side, a, maxb=24):
    entry = O[t]; stop = entry - side * a; tgt = entry + side * a
    for j in range(t, min(t + maxb, len(C))):
        hit_s = L[j] <= stop if side == 1 else H[j] >= stop
        hit_t = H[j] >= tgt if side == 1 else L[j] <= tgt
        if hit_s:                      # pessimistic when both in one bar
            return -1.0
        if hit_t:
            return 1.0
    j = min(t + maxb - 1, len(C) - 1)
    return side * (C[j] - entry) / a


allr = {"bias": [], "opp": [], "rnd": []}
print("2-candle bias, 1:1 at session-start hours. win rate (mean R) n")
for s in SYMS:
    d = yf.download(s, period="730d", interval="1h", progress=False, auto_adjust=False)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d[["Open", "High", "Low", "Close"]].dropna(); d.index = d.index.tz_convert("UTC")
    O, H, L, C = (d[c].values for c in ("Open", "High", "Low", "Close"))
    tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = pd.Series(tr).rolling(24).mean().values
    day = d.index.normalize()
    daily = d.groupby(day).agg(o=("Open", "first"), c=("Close", "last"))
    res = {"bias": [], "opp": [], "rnd": []}
    for t in range(30, len(C) - 25):
        if d.index[t].hour not in (0, 7, 13) or np.isnan(atr[t]):
            continue
        prev_day = day[t] - pd.Timedelta(days=1)
        if prev_day not in daily.index:
            continue
        dcol = np.sign(daily.at[prev_day, "c"] - daily.at[prev_day, "o"])
        hcol = np.sign(C[t - 1] - O[t - 4])
        if dcol == 0 or dcol != hcol:
            continue
        side = int(dcol)
        res["bias"].append(outcome(H, L, C, O, t, side, atr[t]))
        res["opp"].append(outcome(H, L, C, O, t, -side, atr[t]))
        res["rnd"].append(outcome(H, L, C, O, t, int(rng.choice([-1, 1])), atr[t]))
    for k in res:
        allr[k] += res[k]
    b, o, r = (np.array(res[k]) for k in ("bias", "opp", "rnd"))
    print(f"  {s:9s}: bias {np.mean(b > 0):.0%} ({b.mean():+.3f}R) n={len(b)} | opposite {np.mean(o > 0):.0%} "
          f"({o.mean():+.3f}R) | random {np.mean(r > 0):.0%} ({r.mean():+.3f}R)")
b, o, r = (np.array(allr[k]) for k in ("bias", "opp", "rnd"))
print(f"\nPOOLED: bias win {np.mean(b > 0):.1%} ({b.mean():+.3f}R, se {b.std() / np.sqrt(len(b)):.3f}) n={len(b)} | "
      f"opposite {np.mean(o > 0):.1%} ({o.mean():+.3f}R) | random {np.mean(r > 0):.1%} ({r.mean():+.3f}R) | claimed: 70%")
