"""Round 51: Lance Breitstein, "The 2 Swing Trading Strategies That Made me Millions" (k-X0164r66U).
 (A) Capitulation mean reversion: "a sharp extended move, accelerating at an unsustainable rate, massive volume;
     buy the right side of the V when the trend breaks; initial stop at the lows, trail with prior daily bar lows."
 (B) Continuation: "major multi-month breakouts of in-play stocks (volume / catalyst); buy the breakout level, initial
     stop below the level or the day's low, trail with prior daily bar lows or the 20-day moving average."
Mechanical approximation, daily, 50 liquid US stocks (survivorship: today's names), no costs:
 A setup: C[t-1] <= C[t-11] - 4*ATR20, last 3 days carry >= 40% of the 10-day drop, max volume of last 3 days >=
   2x the 50-day average. Trigger within 5 days: price trades above the prior day's high (buy stop there).
   Initial stop = lowest low of the decline. Exits: (1) prior-day-low trail, (2) close below SMA20... for longs
   after a crash we use SMA5 instead (SMA20 is far above) -> exit (2) = close below 5-day SMA; max 60 days.
 B setup: close > highest high of prior 120 days with volume >= 1.5x 50-day avg. Entry = the CLOSE of day t (a buy-stop at the 120-day high would need the close filter = look-ahead; first run did that and showed a fake +1.1R)
   Initial stop = day t low (min 0.5 ATR). Exits: (1) prior-day-low trail, (2) close below SMA20;
   max 120 days.
 Baseline: random long entries on the same stocks with the same stop construction and exits (dates random).
Report mean R, mean % return per trade, win rate, n; periods 2005-14 and 2015+.
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SYMS = ("NVDA AMD TSLA NFLX META AMZN AAPL MSFT GOOGL CRM ADBE AVGO MU QCOM INTC CSCO ORCL IBM JPM BAC GS MS C WFC "
        "XOM CVX COP SLB CAT DE BA GE HON MMM UNH JNJ PFE MRK LLY ABBV WMT HD COST NKE MCD SBUX DIS KO PEP PG").split()


def manage(O, H, L, C, sma, t, entry, stop0, mode, maxh, today=True):
    risk = entry - stop0
    if risk <= 0:
        return None
    if today and L[t] <= stop0:  # entry-day check uses the low (conservative for intraday buy-stops)
        return -1.0, (stop0 / entry - 1)
    for j in range(t + 1, min(t + maxh + 1, len(C))):
        stop = max(stop0, L[j - 1]) if mode == "pdl" else stop0
        if L[j] <= stop:
            px = min(O[j], stop)
            return (px - entry) / risk, px / entry - 1
        if mode == "sma" and C[j] < sma[j]:
            return (C[j] - entry) / risk, C[j] / entry - 1
    j = min(t + maxh, len(C) - 1)
    return (C[j] - entry) / risk, C[j] / entry - 1


res = {}
def add(key, per, out):
    if out is not None:
        res.setdefault((key, per), []).append(out)


for s in SYMS:
    d = yf.download(s, start="2004-01-01", interval="1d", progress=False, auto_adjust=True)
    if d is None or len(d) < 600:
        continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna(); d = d[(d["Low"] > 0) & (d["Volume"] > 0)]
    O, H, L, C, V = (d[c].to_numpy(dtype=float) for c in ("Open", "High", "Low", "Close", "Volume"))
    yr = d.index.year.values
    tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = pd.Series(tr).rolling(20).mean().to_numpy()
    v50 = pd.Series(V).shift(1).rolling(50).mean().to_numpy()
    s5 = pd.Series(C).rolling(5).mean().to_numpy(); s20 = pd.Series(C).rolling(20).mean().to_numpy()
    hi120 = pd.Series(H).shift(1).rolling(120).max().to_numpy()
    rng = np.random.default_rng(sum(map(ord, s)))
    busyA = busyB = -1
    for t in range(130, len(C) - 2):
        if yr[t] < 2005 or np.isnan(atr[t - 1]) or np.isnan(v50[t - 1]):
            continue
        per = "2005-14" if yr[t] < 2015 else "2015+"
        # --- A: capitulation, right side of the V
        drop10 = C[t - 11] - C[t - 1]
        if t > busyA and drop10 >= 4 * atr[t - 1] and (C[t - 4] - C[t - 1]) >= 0.4 * drop10 \
                and V[t - 3:t].max() >= 2 * v50[t - 1]:
            low = L[t - 11:t].min()
            for k in range(t, min(t + 5, len(C) - 1)):
                low = min(low, L[k - 1])
                if H[k] > H[k - 1]:
                    entry = max(O[k], H[k - 1]); stop0 = low
                    add("A pdl", per, manage(O, H, L, C, s5, k, entry, stop0, "pdl", 60))
                    add("A sma5", per, manage(O, H, L, C, s5, k, entry, stop0, "sma", 60))
                    busyA = k + 10
                    break
        # --- B: multi-month breakout with volume
        if t > busyB and H[t] > hi120[t] and V[t] >= 1.5 * v50[t] and C[t] > hi120[t]:
            entry = C[t]; stop0 = min(L[t], entry - 0.5 * atr[t - 1])  # decided at the close (no look-ahead)
            add("B pdl", per, manage(O, H, L, C, s20, t, entry, stop0, "pdl", 120, today=False))
            add("B sma20", per, manage(O, H, L, C, s20, t, entry, stop0, "sma", 120, today=False))
            busyB = t + 10
        # --- random baselines (same constructions)
        if rng.random() < 0.02:
            e = C[t]; st = min(L[t], e - 0.5 * atr[t - 1])
            add("rand B-style pdl", per, manage(O, H, L, C, s20, t, e, st, "pdl", 120, today=False))
            add("rand B-style sma20", per, manage(O, H, L, C, s20, t, e, st, "sma", 120, today=False))
            st2 = L[t - 10:t].min()
            e = O[t]
            add("rand A-style pdl", per, manage(O, H, L, C, s5, t, e, st2, "pdl", 60))
            add("rand A-style sma5", per, manage(O, H, L, C, s5, t, e, st2, "sma", 60))

print("Daily, 50 liquid US stocks, long only, no costs. Cells: mean R (se) | mean % per trade | win | n")
for key in ("A pdl", "rand A-style pdl", "A sma5", "rand A-style sma5",
            "B pdl", "rand B-style pdl", "B sma20", "rand B-style sma20"):
    cells = []
    for per in ("2005-14", "2015+"):
        a = np.array(res.get((key, per), []))
        if len(a) == 0:
            cells.append(f"{per}: n=0"); continue
        r, pc = a[:, 0], a[:, 1]
        cells.append(f"{per}: {r.mean():+.3f}R ({r.std() / np.sqrt(len(r)):.3f}) | {pc.mean():+.2%} | "
                     f"{np.mean(r > 0):.0%} | n={len(r)}")
    print(f"  {key:20s} " + "  ||  ".join(cells))
