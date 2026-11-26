"""Follow-up with bigger samples. (A2) prior-day profile from 1h bars over ~2y (coarse) -> POC/VAH/VAL vs random.
(B2) pooled SPY/QQQ/IWM 1h: high-RVOL (>=1.5x same-hour 20d avg) DOWN bars split by close location:
     'stopping' (close in upper half) vs 'weakness' (close in lower half), forward 7-bar return in daily ATR."""
import importlib.util, random, sys
from collections import defaultdict
import numpy as np
spec = importlib.util.spec_from_file_location("v", "verify_volume_tests.py")
src = open("verify_volume_tests.py", encoding="utf-8").read().split('print("=== (A)')[0]
exec(src)
random.seed(11)
print("=== (A2) 1h-bar prior-day profile, ~2y ===")
agg = defaultdict(lambda: [0, 0])
for sym in SYMS:
    atr = daily_atr(sym)
    df = dl(sym, "730d", "1h").tz_convert("America/New_York").between_time("09:30", "15:59")
    days = [(d, g) for d, g in df.groupby(df.index.date) if len(g) >= 6]
    for i in range(1, len(days)):
        (pd, prev), (d, g) = days[i-1], days[i]
        a = atr.get(pd); lv = profile_levels(prev, nbins=40)
        if lv is None or a is None or a != a: continue
        X = 0.25 * a; O = g["Open"].values[0]; H, L = g["High"].values, g["Low"].values
        for name, lvl in lv.items():
            if abs(lvl - O) < 1e-9: continue
            above = lvl > O
            r = touch(H, L, lvl, above, X)
            if r is not None: agg[name][0] += r; agg[name][1] += 1
            dist = abs(lvl - O) * random.uniform(0.5, 1.5)
            r2 = touch(H, L, O + dist if above else O - dist, above, X)
            if r2 is not None: agg["random"][0] += r2; agg["random"][1] += 1
for k, (w, n) in agg.items():
    p = w / max(n, 1); se = (p*(1-p)/max(n,1))**0.5
    print(f"  {k:7s}: rejection {w}/{n} = {p:.1%} (se {se:.1%})")
print("\n=== (B2) pooled high-RVOL down bars, 1h ~2y, forward 7 bars (daily-ATR units) ===")
res = defaultdict(list)
for sym in SYMS:
    atr = daily_atr(sym)
    df = dl(sym, "730d", "1h").tz_convert("America/New_York").between_time("09:30", "15:59")
    df = df[df["Volume"] > 0].copy()
    df["hour"] = df.index.hour; df["date"] = df.index.date
    df["hvol"] = df.groupby("hour")["Volume"].transform(lambda s: s.shift(1).rolling(20).mean())
    rv = (df["Volume"] / df["hvol"]).values
    C, O_, H_, L_ = df["Close"].values, df["Open"].values, df["High"].values, df["Low"].values
    at = np.array([atr.get(d, np.nan) for d in df["date"]], dtype=float)
    for i in range(len(df) - 7):
        if not np.isfinite(at[i]) or not np.isfinite(rv[i]): continue
        fr = (C[i+7] - C[i]) / at[i]
        res["all"].append(fr)
        if C[i] < O_[i]:
            res["down_all"].append(fr)
            rng = H_[i] - L_[i]
            if rng > 0 and rv[i] >= 1.5:
                loc = (C[i] - L_[i]) / rng
                res["hiRV_down_upperclose(stopping)" if loc >= 0.5 else "hiRV_down_lowerclose(weakness)"].append(fr)
for k, v in res.items():
    v = np.array(v); print(f"  {k:32s} N={len(v):5d} mean {v.mean():+.3f} ATR (se {v.std()/np.sqrt(len(v)):.3f}) up% {np.mean(v>0):.0%}")
