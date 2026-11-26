"""Round 45: Peter Brandt on Words of Rizdom (02tMCQLFIjg): "15% of my trades make 85% of the profit. Those trades
worked right away and never looked back. If I take the big winners and ask how many I would have lost had I got out
of them any day they had a losing close - I don't lose much. If I do that to the losers it changes the whole net."
His rules: "if a position is a loser on a Friday afternoon we're out" and "if we have a loss in a trade for two
straight days but it hasn't hit our stop, we cut and run."
Test: Brandt-style trend entries (20-day close breakout, long & short) and random-direction entries on commodity ETFs
and commodity futures, daily 2005+, no costs. Exit = Brandt 3-day trailing stop with 1-ATR initial stop (as
verify_brandt_exits.py). Add early-exit filters:
  F1 exit at the close of the first day that closes below entry (long) - 'any losing close'
  F2 exit after TWO consecutive losing closes (vs entry)
  F3 exit on Friday's close if the trade is at a loss
Report: mean R, share of total profit from the top 15% of trades, how many top-15% winners each filter would have cut.
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GROUPS = {"COMMOD ETF": "GLD SLV USO UNG DBA DBC PPLT PALL CPER CORN WEAT SOYB".split(),
          "COMMOD FUT": "GC=F SI=F CL=F NG=F HG=F ZC=F ZS=F ZW=F KC=F SB=F CT=F LE=F".split()}


def trade(O, H, L, C, wd, t, side, a, filt, maxd=120):
    entry = C[t]; stop = entry - side * a; hi_day = t; losing_streak = 0
    for j in range(t + 1, min(t + 1 + maxd, len(C))):
        # initial / trailing stop hit (gap -> open)
        if (side == 1 and L[j] <= stop) or (side == -1 and H[j] >= stop):
            px = min(O[j], stop) if side == 1 else max(O[j], stop)
            return side * (px - entry) / a
        losing = side * (C[j] - entry) < 0
        losing_streak = losing_streak + 1 if losing else 0
        if filt == "F1" and losing:
            return side * (C[j] - entry) / a
        if filt == "F2" and losing_streak >= 2:
            return side * (C[j] - entry) / a
        if filt == "F3" and losing and wd[j] == 4:
            return side * (C[j] - entry) / a
        # Brandt 3-day trailing: new extreme day; a later close beyond that day's low/high -> stop to that close day's extreme
        if (side == 1 and H[j] >= H[hi_day]) or (side == -1 and L[j] <= L[hi_day]):
            hi_day = j
        elif (side == 1 and C[j] < L[hi_day]) or (side == -1 and C[j] > H[hi_day]):
            ns = L[j] if side == 1 else H[j]
            stop = max(stop, ns) if side == 1 else min(stop, ns)
    j = min(t + maxd, len(C) - 1)
    return side * (C[j] - entry) / a


for g, syms in GROUPS.items():
    res = {k: {"brk": [], "rnd": []} for k in ("base", "F1", "F2", "F3")}
    for s in syms:
        d = yf.download(s, start="2004-01-01", interval="1d", progress=False, auto_adjust=True)
        if d is None or len(d) < 500:
            continue
        if hasattr(d.columns, "levels"):
            d.columns = d.columns.get_level_values(0)
        d = d.dropna(); d = d[(d["High"] > 0) & (d["Low"] > 0)]
        O, H, L, C = (d[c].values for c in ("Open", "High", "Low", "Close")); wd = d.index.dayofweek.values
        yr = d.index.year.values
        tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)), abs(L - np.roll(C, 1))))
        atr = np.convolve(tr, np.ones(20) / 20, mode="full")[:len(tr)]
        rng = np.random.default_rng(sum(map(ord, s)))
        busy = -1
        for t in range(25, len(C) - 2):
            if yr[t] < 2005 or atr[t] <= 0 or t <= busy:
                continue
            side = 0
            if C[t] > C[t - 20:t].max(): side = 1
            elif C[t] < C[t - 20:t].min(): side = -1
            if side:
                for k in res:
                    res[k]["brk"].append(trade(O, H, L, C, wd, t, side, atr[t], k))
                busy = t + 5
            if rng.random() < 0.04:
                rs = 1 if rng.random() < 0.5 else -1
                for k in res:
                    res[k]["rnd"].append(trade(O, H, L, C, wd, t, rs, atr[t], k))
    print(f"\n=== {g} (Brandt 3-day trailing exit, 1-ATR initial stop, no costs) ===")
    for entry in ("brk", "rnd"):
        base = np.array(res["base"][entry])
        order = np.argsort(base)[::-1]; top = order[:max(1, int(0.15 * len(base)))]
        share = base[top].sum() / base.sum() if base.sum() > 0 else np.nan
        print(f"  {'20-day breakout' if entry == 'brk' else 'random entry'}: n={len(base)} | base mean {base.mean():+.3f}R "
              f"(top 15% of trades = {share:.0%} of net)")
        for k, lab in (("F1", "exit on first losing close"), ("F2", "exit after 2 losing closes"),
                       ("F3", "exit losers on Friday")):
            r = np.array(res[k][entry])
            cut_top = np.mean(r[top] < base[top] - 1e-9)
            print(f"    {lab:28s}: mean {r.mean():+.3f}R (diff {r.mean() - base.mean():+.3f}) | top-15% winners cut "
                  f"{cut_top:.0%} | win rate {np.mean(r > 0):.0%} vs {np.mean(base > 0):.0%}")
