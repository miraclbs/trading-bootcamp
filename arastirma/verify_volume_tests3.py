"""Robustness for (B2) 'high-RVOL down bar closing in lower half' -> forward 7-bar return.
Split-half by date + per symbol + non-overlapping (keep only first signal per day)."""
import sys
from collections import defaultdict
import numpy as np
src = open("verify_volume_tests.py", encoding="utf-8").read().split('print("=== (A)')[0]
exec(src)
rows = []
for sym in SYMS:
    atr = daily_atr(sym)
    df = dl(sym, "730d", "1h").tz_convert("America/New_York").between_time("09:30", "15:59")
    df = df[df["Volume"] > 0].copy()
    df["hour"] = df.index.hour; df["date"] = df.index.date
    df["hvol"] = df.groupby("hour")["Volume"].transform(lambda s: s.shift(1).rolling(20).mean())
    rv = (df["Volume"] / df["hvol"]).values
    C, O_, H_, L_ = df["Close"].values, df["Open"].values, df["High"].values, df["Low"].values
    dates = df["date"].values
    at = np.array([atr.get(d, np.nan) for d in dates], dtype=float)
    seen = set()
    for i in range(len(df) - 7):
        if not np.isfinite(at[i]) or not np.isfinite(rv[i]): continue
        rng = H_[i] - L_[i]
        if C[i] < O_[i] and rng > 0 and rv[i] >= 1.5 and (C[i] - L_[i]) / rng < 0.5 and (sym, dates[i]) not in seen:
            seen.add((sym, dates[i]))
            rows.append((sym, dates[i], (C[i+7] - C[i]) / at[i]))
rows.sort(key=lambda r: r[1])
mid = rows[len(rows)//2][1]
def s(v):
    v = np.array(v); return f"N={len(v):4d} mean {v.mean():+.3f} (se {v.std()/np.sqrt(len(v)):.3f}) up% {np.mean(v>0):.0%}"
print("first signal per symbol-day only (non-overlapping within day)")
print(" all     :", s([r[2] for r in rows]))
print(" 1st half:", s([r[2] for r in rows if r[1] < mid]))
print(" 2nd half:", s([r[2] for r in rows if r[1] >= mid]))
for sym in SYMS:
    print(f" {sym}     :", s([r[2] for r in rows if r[0] == sym]))
