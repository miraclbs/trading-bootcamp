"""Round 54: Zamco ($1.3M prop payouts), Titans of Tomorrow (jw-HOnDexEc):
 "My strategy is basic trend continuation (break of structure, retest of an inefficiency), mostly gold, DAX, NASDAQ;
  I try to catch the whole daily candle. Oct-Nov-Dec 2025 made ~60-70% of my year (~$0.5M) - market conditions were
  great for my strategy." The host notes: "gold and indexes are naturally appreciating assets, so the buys work."
Question: how much of a long-biased intraday trend strategy's result can come from the market's drift alone?
Test: RANDOM entries (no skill) at the daily open, stop 0.5 x ATR14(daily) and target 1.0 x ATR (RR 2, break-even
win rate 33.3%), exit at the close if neither is hit ('catch the daily candle'); intraday path approximated with
daily OHLC (if both levels inside the day range -> coin flip; a first run that counted them as stops gave biased, e.g. EURUSD 7% win rates). Long vs short, per year,
gold futures, Nasdaq futures, DAX, EURUSD; plus Q4 2025.
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RNG = np.random.default_rng(54)


def trade(o, h, l, c, a, side):
    stop = o - side * 0.5 * a; tgt = o + side * 1.0 * a
    hit_stop = (l <= stop) if side == 1 else (h >= stop)
    hit_tgt = (h >= tgt) if side == 1 else (l <= tgt)
    if hit_stop and hit_tgt:  # order unknown inside a daily bar -> coin flip (unbiased under a random walk)
        return -1.0 if RNG.random() < 0.5 else 2.0
    if hit_stop:
        return -1.0
    if hit_tgt:
        return 2.0
    return side * (c - o) / (0.5 * a)


for s, name in (("GC=F", "Gold"), ("NQ=F", "Nasdaq 100"), ("^GDAXI", "DAX"), ("EURUSD=X", "EURUSD")):
    d = yf.download(s, start="2014-06-01", interval="1d", progress=False, auto_adjust=True)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna(); d = d[(d["High"] > d["Low"])]
    O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = pd.Series(tr).rolling(14).mean().shift(1).to_numpy()
    yrs = d.index.year.values; mon = d.index.month.values
    rows = []
    for t in range(20, len(C)):
        if np.isnan(atr[t]):
            continue
        rows.append((yrs[t], mon[t], trade(O[t], H[t], L[t], C[t], atr[t], 1), trade(O[t], H[t], L[t], C[t], atr[t], -1),
                     C[t] / C[t - 1] - 1))
    r = pd.DataFrame(rows, columns=["y", "m", "long", "short", "ret"])
    print(f"\n=== {name}: random daily entries, RR 2 (stop 0.5 ATR / target 1 ATR, else exit at close) ===")
    print("   year | long: mean R / win | short: mean R / win | buy&hold")
    for y, g in r.groupby("y"):
        if y < 2015:
            continue
        print(f"   {y} | {g['long'].mean():+.3f}R / {np.mean(g['long'] > 0):.0%} | {g['short'].mean():+.3f}R / "
              f"{np.mean(g['short'] > 0):.0%} | {np.prod(1 + g['ret']) - 1:+.0%}")
    q = r[(r.y == 2025) & (r.m >= 10)]
    if len(q):
        print(f"   Q4 2025 | {q['long'].mean():+.3f}R / {np.mean(q['long'] > 0):.0%} | {q['short'].mean():+.3f}R / "
              f"{np.mean(q['short'] > 0):.0%} | {np.prod(1 + q['ret']) - 1:+.0%}")
    allp = r[r.y >= 2015]
    print(f"   2015+ all | {allp['long'].mean():+.3f}R | {allp['short'].mean():+.3f}R")
