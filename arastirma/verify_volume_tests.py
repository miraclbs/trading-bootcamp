"""Two volume tests on SPY/QQQ/IWM.
(A) Prior-day VOLUME PROFILE levels (POC, VAH, VAL from 5-min bars; each bar's volume spread uniformly over its
    high-low range in price bins; value area = 70% around POC) vs RANDOM levels at the same distance scale.
    First touch today -> 'rejection' = price moves 0.25*dailyATR away from the level (back toward the open side)
    before moving 0.25*ATR through it. Data: 5-min, ~60 days.
(B) VSA 'stopping volume' bar on 1h bars (~2 years): down bar (close<open) with relative volume >= 2.0 versus the
    same hour-of-day average of the previous 20 sessions AND close in the upper half of its range.
    Compare forward return over next 3 and 7 bars (in units of daily ATR) with ALL down bars and ALL bars.
No costs. Exploratory.
"""
import random
import sys
from collections import defaultdict

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
random.seed(8)
SYMS = ("SPY", "QQQ", "IWM")


def dl(sym, period, interval):
    df = yf.download(sym, period=period, interval=interval, prepost=False, progress=False, auto_adjust=False)
    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)
    return df


def daily_atr(sym):
    d = dl(sym, "3y", "1d")
    a = (d["High"] - d["Low"]).rolling(14).mean()
    return {k.date(): v for k, v in a.items()}


def profile_levels(g, nbins=60):
    lo, hi = g["Low"].min(), g["High"].max()
    if hi <= lo:
        return None
    edges = np.linspace(lo, hi, nbins + 1)
    vol = np.zeros(nbins)
    for h, l, v in zip(g["High"].values, g["Low"].values, g["Volume"].values):
        i0 = max(0, np.searchsorted(edges, l, side="right") - 1)
        i1 = min(nbins - 1, np.searchsorted(edges, h, side="right") - 1)
        vol[i0:i1 + 1] += v / (i1 - i0 + 1)
    poc = int(vol.argmax())
    lo_i = hi_i = poc
    total, acc = vol.sum(), vol[poc]
    while acc < 0.7 * total and (lo_i > 0 or hi_i < nbins - 1):
        up = vol[hi_i + 1] if hi_i < nbins - 1 else -1
        dn = vol[lo_i - 1] if lo_i > 0 else -1
        if up >= dn:
            hi_i += 1; acc += up
        else:
            lo_i -= 1; acc += dn
    mid = (edges[:-1] + edges[1:]) / 2
    return {"POC": mid[poc], "VAH": edges[hi_i + 1], "VAL": edges[lo_i]}


def touch(H, L, lvl, above, X):
    for j in range(len(H)):
        if not (H[j] >= lvl if above else L[j] <= lvl):
            continue
        for k in range(j + 1, len(H)):
            rej = L[k] <= lvl - X if above else H[k] >= lvl + X
            brk = H[k] >= lvl + X if above else L[k] <= lvl - X
            if rej and brk:
                return None
            if rej:
                return 1
            if brk:
                return 0
        return None
    return None


print("=== (A) Prior-day volume profile levels vs random levels (5-min, ~60d) ===")
agg = defaultdict(lambda: [0, 0])
for sym in SYMS:
    atr = daily_atr(sym)
    df = dl(sym, "60d", "5m").tz_convert("America/New_York").between_time("09:30", "15:59")
    days = [(d, g) for d, g in df.groupby(df.index.date) if len(g) > 60]
    for i in range(1, len(days)):
        (pd, prev), (d, g) = days[i - 1], days[i]
        a = atr.get(pd)
        lv = profile_levels(prev)
        if lv is None or a is None or a != a:
            continue
        X = 0.25 * a
        O = g["Open"].values[0]
        H, L = g["High"].values, g["Low"].values
        for name, lvl in lv.items():
            if abs(lvl - O) < 1e-9:
                continue
            above = lvl > O
            r = touch(H, L, lvl, above, X)
            if r is not None:
                agg[name][0] += r; agg[name][1] += 1
            dist = abs(lvl - O) * random.uniform(0.5, 1.5)
            rl = O + dist if above else O - dist
            r2 = touch(H, L, rl, above, X)
            if r2 is not None:
                agg["random"][0] += r2; agg["random"][1] += 1
for k, (w, n) in agg.items():
    print(f"  {k:7s}: rejection {w}/{n} = {w/max(n,1):.1%}")

print("\n=== (B) VSA stopping-volume down bars (1h, ~2y): forward return in daily-ATR units ===")
for sym in SYMS:
    atr = daily_atr(sym)
    df = dl(sym, "730d", "1h").tz_convert("America/New_York").between_time("09:30", "15:59")
    df = df[df["Volume"] > 0].copy()
    df["hour"] = df.index.hour
    df["date"] = df.index.date
    # same-hour average volume of previous 20 sessions
    df["hvol"] = df.groupby("hour")["Volume"].transform(lambda s: s.shift(1).rolling(20).mean())
    df["rvol"] = df["Volume"] / df["hvol"]
    df["atr"] = [atr.get(d) for d in df["date"]]
    C = df["Close"].values
    out = {"stopping": defaultdict(list), "down_all": defaultdict(list), "all": defaultdict(list)}
    rng = (df["High"] - df["Low"]).values
    loc = np.where(rng > 0, (df["Close"] - df["Low"]).values / np.where(rng > 0, rng, 1), 0.5)
    down = (df["Close"] < df["Open"]).values
    rv = df["rvol"].values
    at = df["atr"].values
    for i in range(len(df) - 7):
        if at[i] is None or at[i] != at[i]:
            continue
        for hzn in (3, 7):
            fr = (C[i + hzn] - C[i]) / at[i]
            out["all"][hzn].append(fr)
            if down[i]:
                out["down_all"][hzn].append(fr)
                if rv[i] == rv[i] and rv[i] >= 2.0 and loc[i] >= 0.5:
                    out["stopping"][hzn].append(fr)
    for k in ("stopping", "down_all", "all"):
        s3, s7 = out[k][3], out[k][7]
        if not s3:
            continue
        se7 = np.std(s7) / np.sqrt(len(s7))
        print(f"  {sym} {k:9s}: N={len(s3):5d} | +3 bars mean {np.mean(s3):+.3f} ATR, up% {np.mean(np.array(s3)>0):.0%} "
              f"| +7 bars mean {np.mean(s7):+.3f} ATR (se {se7:.3f}), up% {np.mean(np.array(s7)>0):.0%}")
