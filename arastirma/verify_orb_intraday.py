"""Round 21: an INTRADAY candidate for prop trading (needs >= 10-15 R per year, see 09 §2 item 6).
Opening-range breakout built on Brooks' finding (verified in verify_brooks_open.py): the day's high or low is usually
set early, and once the opening range breaks, the opposite extreme tends to hold.
Data: yfinance 1h bars, last ~730 days, US ETFs in regular hours (bars start 9:30, 10:30, ... 15:30 ET).
OR = first 1h bar (9:30-10:30).
  A  ORB, stop = opposite end of OR: first later 1h bar that CLOSES beyond the OR -> enter at that close in breakout
     direction, stop at the other side of the OR, exit at the 15:30 bar close (EOD). One trade per day.
  B  same entry, stop = OR midpoint (smaller R, more stop-outs)
  C  RANDOM-direction entry at the 11:30 bar close, stop distance = OR range, EOD exit  (baseline)
Costs: $0.02/share round trip on ETFs, converted to R. Stops filled at stop price (no intrabar gap modelling except
when an hourly bar opens beyond the stop -> fill at open).
Reported: mean net R, se, halves, trades/yr, net R/yr per symbol. Index ETFs are ~one bet: count R/yr for ONE of them.
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SYMS = ("SPY", "QQQ", "IWM", "DIA", "GLD", "TLT", "XLE", "XLF", "SMH", "EEM")
COST = 0.02


def run(O, Hh, L, C, i0, i1, side, entry_i, entry_px, stop):
    R = abs(entry_px - stop)
    if R <= 0:
        return None
    for j in range(entry_i + 1, i1 + 1):
        if side == 1:
            if O[j] <= stop: return (O[j] - entry_px) / R
            if L[j] <= stop: return (stop - entry_px) / R
        else:
            if O[j] >= stop: return (entry_px - O[j]) / R
            if Hh[j] >= stop: return (entry_px - stop) / R
    return side * (C[i1] - entry_px) / R


print("1h bars ~2 years, regular hours. Net R per trade after $0.02/share cost.")
for sym in SYMS:
    d = yf.download(sym, period="730d", interval="1h", progress=False, auto_adjust=False, prepost=False)
    if d is None or len(d) < 500:
        print(f"{sym}: no data"); continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna()
    idx = d.index.tz_convert("America/New_York")
    O, Hh, L, C = (d[c].values for c in ("Open", "High", "Low", "Close"))
    days = {}
    for i, ts in enumerate(idx):
        if (ts.hour, ts.minute) < (9, 30) or ts.hour >= 16:
            continue
        days.setdefault(ts.date(), []).append(i)
    res = {"A": [], "B": [], "C": []}; half = {"A": [], "B": [], "C": []}
    rng = np.random.default_rng(sum(map(ord, sym)))
    dl = sorted(days); mid = dl[len(dl) // 2]
    for day in dl:
        bars = days[day]
        if len(bars) < 6 or idx[bars[0]].hour != 9:
            continue
        i0, i1 = bars[0], bars[-1]
        orh, orl = Hh[i0], L[i0]
        if orh <= orl:
            continue
        h = 0 if day < mid else 1
        # A/B: first close beyond OR
        for j in bars[1:-1]:
            side = 1 if C[j] > orh else (-1 if C[j] < orl else 0)
            if side == 0:
                continue
            px = C[j]
            for key, stop in (("A", orl if side == 1 else orh), ("B", (orh + orl) / 2)):
                r = run(O, Hh, L, C, i0, i1, side, j, px, stop)
                if r is not None:
                    res[key].append(r - COST / abs(px - stop)); half[key].append(h)
            break
        # C: random direction at the 11:30 bar close (3rd bar), stop distance = OR range
        j = bars[2]; side = 1 if rng.random() < 0.5 else -1
        stop = C[j] - side * (orh - orl)
        r = run(O, Hh, L, C, i0, i1, side, j, C[j], stop)
        if r is not None:
            res["C"].append(r - COST / (orh - orl)); half["C"].append(h)
    ndays = len(dl); yrs = ndays / 252
    line = f"{sym:4s} ({ndays} days)"
    for key, lab in (("A", "ORB stop=OR"), ("B", "ORB stop=mid"), ("C", "random")):
        v = np.array(res[key]); hh = np.array(half[key])
        if len(v) == 0:
            continue
        line += (f" | {lab}: {v.mean():+.3f}R (se {v.std()/np.sqrt(len(v)):.3f}) n={len(v)} "
                 f"h1 {v[hh == 0].mean():+.2f} h2 {v[hh == 1].mean():+.2f} R/yr {v.sum()/yrs:+.1f}")
    print(line)
