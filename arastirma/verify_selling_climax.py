"""VSA/Wyckoff 'selling climax' WITH BACKGROUND, on DAILY data (bigger samples, 2005+).
Background: 10-day return <= -1.5 * ATR14 (a real decline) AND close within 5% of the 20-day low.
Event bars (day t):
  climax_offlow : volume >= 2.0x 20d avg, range >= 1.2x ATR14, close in UPPER half (closes well off the low)  [VSA stopping volume / Wyckoff SC]
  climax_onlow  : same volume/range, close in LOWER third (closes near the low)                            ['weakness']
  decline_any   : background condition only (any day)
Forward returns t+5, t+10, t+20 in ATR units, compared with unconditional days. Split by period (2005-2014 / 2015+).
Symbols: SPY QQQ IWM DIA GLD TLT XLE XLF EEM.  No costs. Overlapping events within 5 days are skipped.
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SYMS = ("SPY", "QQQ", "IWM", "DIA", "GLD", "TLT", "XLE", "XLF", "EEM")
H = (5, 10, 20)
res = {k: {h: [] for h in H} for k in ("all_days", "decline_any", "climax_offlow", "climax_onlow")}
res_period = {k: {p: [] for p in ("2005-14", "2015+")} for k in ("climax_offlow", "climax_onlow", "all_days")}

for sym in SYMS:
    d = yf.download(sym, start="2004-06-01", interval="1d", progress=False, auto_adjust=True)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna()
    O, Hh, L, C, V = (d[c].values for c in ("Open", "High", "Low", "Close", "Volume"))
    tr = np.maximum(Hh - L, np.maximum(abs(Hh - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = np.convolve(tr, np.ones(14) / 14, mode="full")[:len(tr)]
    vavg = np.convolve(V, np.ones(20) / 20, mode="full")[:len(V)]
    years = d.index.year.values
    last = {"climax_offlow": -99, "climax_onlow": -99}
    for t in range(25, len(C) - 20):
        a = atr[t - 1]
        if a <= 0 or vavg[t - 1] <= 0:
            continue
        fr = {h: (C[t + h] - C[t]) / a for h in H}
        per = "2005-14" if years[t] < 2015 else "2015+"
        if years[t] < 2005:
            continue
        for h in H:
            res["all_days"][h].append(fr[h])
        res_period["all_days"][per].append(fr[10])
        decline = (C[t] - C[t - 10]) <= -1.5 * a and C[t] <= L[t - 19:t + 1].min() * 1.05
        if not decline:
            continue
        for h in H:
            res["decline_any"][h].append(fr[h])
        rng = Hh[t] - L[t]
        if rng <= 0:
            continue
        loc = (C[t] - L[t]) / rng
        big = V[t] >= 2.0 * vavg[t - 1] and rng >= 1.2 * a
        if not big:
            continue
        kind = "climax_offlow" if loc >= 0.5 else ("climax_onlow" if loc <= 0.33 else None)
        if kind and t - last[kind] > 5:
            last[kind] = t
            for h in H:
                res[kind][h].append(fr[h])
            res_period[kind][per].append(fr[10])


def fmt(v):
    v = np.array(v)
    if len(v) == 0:
        return "n=0"
    return f"n={len(v):5d} mean {v.mean():+.2f} (se {v.std()/np.sqrt(len(v)):.2f}) up {np.mean(v>0):.0%}"


print("Forward return in ATR units (9 ETFs pooled, daily, 2005+)")
for k in res:
    print(f"{k:14s} | " + " | ".join(f"+{h}d {fmt(res[k][h])}" for h in H))
print("\n+10d by period:")
for k in res_period:
    print(f"{k:14s} | " + " | ".join(f"{p}: {fmt(v)}" for p, v in res_period[k].items()))
