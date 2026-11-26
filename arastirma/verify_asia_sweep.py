"""Round 31: FTMO interview "$197K with GBPUSD" (gMk5QKiUNRo), trader Leo (15m GBPUSD, London/NY first 3 hours).
Claims tested on ~2 years of 1h bars (yfinance, UTC):
 (1) "About 80% of all Asia sessions get stopped out at both extremes" (both Asia high and Asia low are taken out later
     in the day).  Asia = 00-07 UTC, rest of day = 07-21 UTC.
 (2) Implied edge: once one Asia extreme is swept, price goes for the OTHER extreme ("stop hunt, then reverse").
 (3) "The first hour of every session is a trap / stop hunt" -> first hour return predicts the opposite move in the
     next 3 hours (London 07-08 vs 08-11 UTC, New York 13-14 vs 14-17 UTC).
Baseline: hour-of-day bootstrap. Each simulated day is built by stacking, for every hour, the (high, low, close)
moves of a random real bar from the SAME hour-of-day. This keeps the intraday volatility profile (quiet Asia, busy
London/NY) and the bar shape, but destroys any dependence between hours. If the real numbers match the baseline, the
pattern is volatility geometry, not stop hunting.
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(31)
SYMS = ["GBPUSD=X", "EURUSD=X", "USDJPY=X", "AUDUSD=X", "GC=F", "NQ=F"]
REPS = 30


def load(sym):
    d = yf.download(sym, period="730d", interval="1h", progress=False, auto_adjust=False)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d[["Open", "High", "Low", "Close"]].dropna()
    d.index = d.index.tz_convert("UTC")
    d = d[d.index.dayofweek < 5]
    return d


def day_table(d):
    """per-day array [24 hours x (open, high, low, close)] relative to the 00 UTC open; keep complete 00-21 days"""
    out = {}
    for day, g in d.groupby(d.index.date):
        hrs = g.index.hour
        if not all(h in set(hrs) for h in range(0, 21)):
            continue
        g = g[~g.index.hour.duplicated()]
        g.index = g.index.hour
        g = g.loc[0:20]
        base = g["Open"].iloc[0]
        out[day] = np.log(g[["Open", "High", "Low", "Close"]].values / base)
    return out


def measures(days):
    both = one = rev_n = rev_y = 0
    for a in days:
        asia_hi = a[0:7, 1].max(); asia_lo = a[0:7, 2].min()
        rest = a[7:21]
        hi_t = np.argmax(rest[:, 1] > asia_hi) if (rest[:, 1] > asia_hi).any() else None
        lo_t = np.argmax(rest[:, 2] < asia_lo) if (rest[:, 2] < asia_lo).any() else None
        both += (hi_t is not None) and (lo_t is not None)
        one += (hi_t is not None) or (lo_t is not None)
        if hi_t is not None or lo_t is not None:
            if hi_t is not None and lo_t is not None and hi_t == lo_t:
                continue                                    # same bar takes both: order unknown
            first = "hi" if (lo_t is None or (hi_t is not None and hi_t < lo_t)) else "lo"
            rev_n += 1
            rev_y += (lo_t is not None) if first == "hi" else (hi_t is not None)
    n = len(days)
    return both / n, one / n, rev_y / max(rev_n, 1)


def first_hour_corr(days, h0, h1, h2):
    x = np.array([a[h0, 3] - a[h0, 0] for a in days])
    y = np.array([a[h2 - 1, 3] - a[h1, 0] for a in days])
    return np.corrcoef(x, y)[0, 1], np.mean(np.sign(x) != np.sign(y))


def bootstrap(days):
    arr = np.stack(days)                                   # (ndays, 21, 4)
    rel = arr - arr[:, :, [0]]                             # bar moves relative to its own open
    n = len(arr); sims = []
    for _ in range(n):
        pick = rng.integers(0, n, 21)
        bars = rel[pick, np.arange(21)]                    # random real bar for each hour-of-day
        opens = np.concatenate([[0.0], np.cumsum(bars[:-1, 3])])
        sims.append(bars + opens[:, None])
    return sims


print("Asia range = 00-07 UTC; rest = 07-21 UTC. Real vs hour-of-day bootstrap (mean of", REPS, "reps)")
print(f"{'symbol':9s} {'days':>5s} | both swept real/base | >=1 swept real/base | opposite after first sweep real/base"
      f" | London 1st-hr reversal real/base | NY 1st-hr reversal real/base")
for s in SYMS:
    try:
        d = load(s)
    except Exception as ex:
        print(s, "load failed", ex); continue
    tab = day_table(d)
    days = list(tab.values())
    if len(days) < 200:
        print(s, "too few complete days", len(days)); continue
    b, o, r = measures(days)
    lc, lr = first_hour_corr(days, 7, 8, 11)
    nc, nr = first_hour_corr(days, 13, 14, 17)
    bb, bo, br, blr, bnr = [], [], [], [], []
    for _ in range(REPS):
        sim = bootstrap(days)
        x = measures(sim); bb.append(x[0]); bo.append(x[1]); br.append(x[2])
        blr.append(first_hour_corr(sim, 7, 8, 11)[1]); bnr.append(first_hour_corr(sim, 13, 14, 17)[1])
    sd = np.std(br)
    print(f"{s:9s} {len(days):5d} | {b:5.0%} / {np.mean(bb):4.0%}        | {o:5.0%} / {np.mean(bo):4.0%}       | "
          f"{r:5.0%} / {np.mean(br):4.0%} (z {(r - np.mean(br)) / sd:+.1f})              | "
          f"{lr:4.0%} / {np.mean(blr):4.0%} (corr {lc:+.2f})       | {nr:4.0%} / {np.mean(bnr):4.0%} (corr {nc:+.2f})")
