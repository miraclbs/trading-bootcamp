"""Round 55: Trader Dante, "Should I Scale Out Of Trades?" (CDOuxZTsq5o):
 "I don't scale out; it is a mathematically unsound play, trading your P&L. If you believe it goes 50 ticks, why take
  10, 20, 25? And nobody scales out of losers - if scaling out were great, you'd do it on losers too."
Test the same entries with different exits, on three entry sets:
  (a) mean reversion with a known edge: Connors RSI-2 longs on US index ETFs (RSI2 < 10, close > SMA200), 2005+;
  (b) trend with a known edge: 20-day breakout on 11 commodity futures (long and short), 2005+;
  (c) random entries on the same markets (no edge).
Initial risk 1R = 1 x ATR14 from the entry (next open). Exits (daily bars; if stop and target fall in the same bar the
order is a coin flip):
  ALL-2R  : full size, target 2R, stop 1R, time exit after 15 bars
  SCALE   : 1/3 at +0.5R, 1/3 at +1R, 1/3 at +2R (stop 1R on what is left), 15 bars
  SCALE+L : SCALE, plus 1/3 cut at -0.5R ("scaling out of losers", Dante's symmetry test)
  TRAIL   : full size, stop 1R, then exit on a close below the 10-day low (long) / above the 10-day high, 60 bars
  HALF+TR : 1/2 at +2R, rest trailing as TRAIL
Report mean R per trade (se), standard deviation, and mean/sd.
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RNG = np.random.default_rng(55)


def load(s):
    d = yf.download(s, start="2004-01-01", interval="1d", progress=False, auto_adjust=True)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna(); d = d[(d["High"] > d["Low"]) & (d["Low"] > 0)]
    return d


def run_exit(O, H, L, C, lo10, hi10, t, side, a, mode):
    """entry at O[t]; returns R (size-weighted, total size 1)."""
    e = O[t]; R = a
    pieces = {"ALL-2R": [(1.0, 2.0)], "SCALE": [(1 / 3, 0.5), (1 / 3, 1.0), (1 / 3, 2.0)],
              "SCALE+L": [(1 / 3, 0.5), (1 / 3, 1.0), (1 / 3, 2.0)], "TRAIL": [(1.0, None)],
              "HALF+TR": [(0.5, 2.0), (0.5, None)]}[mode]
    open_ = [list(p) for p in pieces]  # [size, target or None]
    loser_cut = mode == "SCALE+L"
    total = 0.0
    maxh = 60 if mode in ("TRAIL", "HALF+TR") else 15
    for j in range(t, min(t + maxh, len(C))):
        hi = side * (H[j] - e) / R if side == 1 else side * (L[j] - e) / R  # best excursion in R
        lo = side * (L[j] - e) / R if side == 1 else side * (H[j] - e) / R  # worst excursion in R
        stop_hit = lo <= -1.0
        tgts = [p for p in open_ if p[1] is not None and hi >= p[1]]
        if stop_hit and tgts and RNG.random() < 0.5:
            stop_hit_first = False
        else:
            stop_hit_first = stop_hit
        if stop_hit_first:
            total += sum(p[0] for p in open_) * -1.0; open_ = []; break
        for p in tgts:
            total += p[0] * p[1]; open_.remove(p)
        if loser_cut and lo <= -0.5 and open_:
            p = open_[-1]; total += p[0] * -0.5; open_.remove(p); loser_cut = False
        if stop_hit and open_:
            total += sum(p[0] for p in open_) * -1.0; open_ = []; break
        if not open_:
            break
        trail_exit = (side == 1 and C[j] < lo10[j]) or (side == -1 and C[j] > hi10[j])
        if trail_exit and j > t:
            rr = side * (C[j] - e) / R
            for p in [p for p in open_ if p[1] is None]:
                total += p[0] * rr; open_.remove(p)
            if not open_:
                break
    if open_:
        j = min(t + maxh, len(C)) - 1
        rr = side * (C[j] - e) / R
        total += sum(p[0] for p in open_) * rr
    return total


MODES = ["ALL-2R", "SCALE", "SCALE+L", "TRAIL", "HALF+TR"]
SETS = {"(a) RSI-2 index longs": [], "(b) commodity 20d breakout": [], "(c) random entries": []}
IDX = "SPY QQQ IWM DIA".split()
COM = "GC=F SI=F CL=F HG=F NG=F ZC=F ZS=F ZW=F KC=F SB=F CT=F".split()
for s in IDX + COM:
    d = load(s)
    if len(d) < 600:
        continue
    O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    yr = d.index.year.values
    tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = pd.Series(tr).rolling(14).mean().to_numpy()
    lo10 = pd.Series(L).rolling(10).min().shift(1).to_numpy(); hi10 = pd.Series(H).rolling(10).max().shift(1).to_numpy()
    sma200 = pd.Series(C).rolling(200).mean().to_numpy()
    dlt = np.diff(C, prepend=C[0]); up = pd.Series(np.maximum(dlt, 0)).ewm(alpha=0.5, adjust=False).mean()
    dn = pd.Series(np.maximum(-dlt, 0)).ewm(alpha=0.5, adjust=False).mean(); rsi2 = (100 - 100 / (1 + up / dn)).to_numpy()
    hi20 = pd.Series(H).rolling(20).max().shift(1).to_numpy(); lo20 = pd.Series(L).rolling(20).min().shift(1).to_numpy()
    busy = -1
    for t in range(210, len(C) - 2):
        if yr[t] < 2005 or np.isnan(atr[t - 1]):
            continue
        a = atr[t - 1]
        if s in IDX and t > busy and rsi2[t - 1] < 10 and C[t - 1] > sma200[t - 1]:
            SETS["(a) RSI-2 index longs"].append([run_exit(O, H, L, C, lo10, hi10, t, 1, a, m) for m in MODES]); busy = t + 3
        if s in COM and t > busy:
            side = 1 if C[t - 1] > hi20[t - 1] else -1 if C[t - 1] < lo20[t - 1] else 0
            if side:
                SETS["(b) commodity 20d breakout"].append([run_exit(O, H, L, C, lo10, hi10, t, side, a, m) for m in MODES])
                busy = t + 10
        if RNG.random() < 0.01:
            side = 1 if RNG.random() < 0.5 else -1
            SETS["(c) random entries"].append([run_exit(O, H, L, C, lo10, hi10, t, side, a, m) for m in MODES])

print("Same entries, different exits. Cells: mean R (se) | sd | mean/sd   (no costs; scaling adds commissions in reality)")
for k, rows in SETS.items():
    r = np.array(rows)
    print(f"\n{k}: n={len(r)}")
    for i, m in enumerate(MODES):
        x = r[:, i]
        print(f"   {m:8s}: {x.mean():+.3f}R ({x.std() / np.sqrt(len(x)):.3f}) | sd {x.std():.2f} | {x.mean() / x.std():+.3f}")
