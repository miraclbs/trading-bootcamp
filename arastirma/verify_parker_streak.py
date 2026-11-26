"""Round 56: Meb Faber & Jerry Parker (ex-Turtle, Chesapeake), "Does Trend Following Work?" (2oXvQ-8Bj9E).
 (1) Parker: "Don't shy away from markets that have been really bad - multiple losers in a row; people write them off.
     The more pain and suffering you've experienced in a market, the more expectation is building" (cocoa example).
 (2) Faber: "An almost guaranteed 100% batting average: buy anything and exit at the first profitable close. The problem:
     giant losers - median holding 3 days, mean holding a year."
Test 1: long-term trend system per market (Parker: >= 100-day look-back, average hold ~1 year): enter long/short on a
 close beyond the 100-day high/low, exit on a close beyond the 50-day opposite extreme, initial risk unit 1R = 2 x ATR20
 (no stop other than the exit). 25+ futures (commodities, rates, currencies, equity indices), daily 2000+.
 Group each trade by how many losing trades in a row that market had just before it.
Test 2: random entries on the same markets, exit at the first close in profit (or after 250 days); win rate, mean R,
 worst 1% and the share of trades still open after 60 days.
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(56)
SYMS = ("GC=F SI=F HG=F PL=F CL=F NG=F HO=F ZC=F ZS=F ZW=F ZL=F KC=F SB=F CC=F CT=F LE=F HE=F "
        "ZN=F ZB=F ZF=F 6E=F 6J=F 6B=F 6A=F 6C=F 6S=F ES=F NQ=F YM=F RTY=F").split()

trades = []      # (sym, year, R, prior_loss_streak)
fpc = []         # first-profitable-close results: (R, days)
for s in SYMS:
    d = yf.download(s, start="1999-01-01", interval="1d", progress=False, auto_adjust=True)
    if d is None or len(d) < 1500:
        continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna(); d = d[(d["High"] > d["Low"]) & (d["Low"] > 0)]
    H, L, C = (d[c].to_numpy(float) for c in ("High", "Low", "Close"))
    yr = d.index.year.values
    tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = pd.Series(tr).rolling(20).mean().to_numpy()
    hi100 = pd.Series(C).rolling(100).max().shift(1).to_numpy(); lo100 = pd.Series(C).rolling(100).min().shift(1).to_numpy()
    hi50 = pd.Series(C).rolling(50).max().shift(1).to_numpy(); lo50 = pd.Series(C).rolling(50).min().shift(1).to_numpy()
    pos = 0; entry = 0.0; risk = 0.0; streak = 0; t0 = 0
    for t in range(110, len(C)):
        if pos == 0:
            side = 1 if C[t] > hi100[t] else -1 if C[t] < lo100[t] else 0
            if side and not np.isnan(atr[t]):
                pos, entry, risk, t0 = side, C[t], 2 * atr[t], t
        else:
            ex = (pos == 1 and C[t] < lo50[t]) or (pos == -1 and C[t] > hi50[t])
            if ex or t == len(C) - 1:
                R = pos * (C[t] - entry) / risk
                trades.append((s, yr[t0], R, streak))
                streak = streak + 1 if R <= 0 else 0
                pos = 0
    # test 2: first profitable close
    for _ in range(150):
        t = rng.integers(30, len(C) - 260); side = 1 if rng.random() < 0.5 else -1
        if np.isnan(atr[t]):
            continue
        r = None
        for k in range(1, 251):
            if side * (C[t + k] - C[t]) > 0:
                r = (side * (C[t + k] - C[t]) / (2 * atr[t]), k); break
        if r is None:
            r = (side * (C[t + 250] - C[t]) / (2 * atr[t]), 250)
        fpc.append(r)

T = pd.DataFrame(trades, columns=["sym", "year", "R", "streak"])
print(f"TEST 1: 100-day breakout / 50-day exit, {T.sym.nunique()} markets, {len(T)} trades, mean {T.R.mean():+.2f}R, "
      f"win {np.mean(T.R > 0):.0%}, top 10% of trades = {T.R.nlargest(len(T) // 10).sum() / T.R[T.R > 0].sum():.0%} of gross gains")
print("   prior losing streak in that market | n | mean R (se) | win rate")
for lab, m in (("0 (last trade won)", T.streak == 0), ("1-2", T.streak.between(1, 2)), ("3-4", T.streak.between(3, 4)),
               ("5+", T.streak >= 5)):
    x = T.R[m]
    print(f"   {lab:22s} | {len(x):4d} | {x.mean():+.2f}R ({x.std() / np.sqrt(len(x)):.2f}) | {np.mean(x > 0):.0%}")
for per, m in (("2000-2012", T.year < 2013), ("2013+", T.year >= 2013)):
    a = T.R[m & (T.streak >= 3)]; b = T.R[m & (T.streak < 3)]
    print(f"   {per}: after 3+ losers {a.mean():+.2f}R (n={len(a)}) vs otherwise {b.mean():+.2f}R (n={len(b)})")

F = np.array(fpc)
print(f"\nTEST 2: random entries, exit at the first profitable close: n={len(F)} | win {np.mean(F[:, 0] > 0):.1%} | "
      f"mean {F[:, 0].mean():+.3f}R | median hold {np.median(F[:, 1]):.0f} days | mean hold {F[:, 1].mean():.0f} days | "
      f"worst 1% {np.percentile(F[:, 0], 1):+.1f}R | still open after 60 days {np.mean(F[:, 1] > 60):.1%}")
