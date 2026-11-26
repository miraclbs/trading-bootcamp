"""Sweep (PDH/PDL failed breakout) with CONTEXT FILTERS. Exploratory, with a split-half robustness check.
Base setup = verify_pdh_sweep.py (first close back inside, stop = sweep extreme, target 2R, EOD exit, no costs).
Filters:
  regime   : daily close vs 50-day SMA at prior close. 'with'  = fade side agrees with regime (long PDL-sweep in bull,
             short PDH-sweep in bear); 'against' = the opposite.
  bar      : signal (entry) bar closes in the favourable 30% of its range AND body >= 50% of range.
  depth    : sweep penetration beyond the level in units of daily ATR(14): shallow <0.10, deep >=0.10.
  time     : sweep extreme printed in the first RTH hour bar vs later.
Data: yfinance 1h RTH ~2 years + daily for SMA/ATR. Multiple comparisons => treat any 'good' bucket as a HYPOTHESIS.
"""
import sys
from collections import defaultdict

import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
K = 2.0


def daily_ctx(sym):
    d = yf.download(sym, period="3y", interval="1d", progress=False, auto_adjust=False)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d["SMA50"] = d["Close"].rolling(50).mean()
    tr = (d["High"] - d["Low"]).combine((d["High"] - d["Close"].shift()).abs(), max)
    tr = tr.combine((d["Low"] - d["Close"].shift()).abs(), max)
    d["ATR14"] = tr.rolling(14).mean()
    return {idx.date(): (row["Close"], row["SMA50"], row["ATR14"]) for idx, row in d.iterrows()}


def intraday(sym):
    df = yf.download(sym, period="730d", interval="1h", prepost=False, progress=False, auto_adjust=False)
    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)
    df = df.tz_convert("America/New_York").between_time("09:30", "15:59")
    return [(dt, g) for dt, g in df.groupby(df.index.date)]


def signals(sym):
    ctx = daily_ctx(sym)
    days = intraday(sym)
    out = []
    for i in range(1, len(days)):
        (pdate, prev), (date, g) = days[i - 1], days[i]
        if pdate not in ctx:
            continue
        pclose, sma, atr = ctx[pdate]
        if sma != sma or atr != atr:  # NaN
            continue
        bull = pclose > sma
        H, L, O, C = g["High"].values, g["Low"].values, g["Open"].values, g["Close"].values
        for side in ("short", "long"):
            lvl = prev["High"].max() if side == "short" else prev["Low"].min()
            ext, ext_j, entry_i = None, None, None
            for j in range(len(g)):
                if side == "short" and H[j] > lvl and (ext is None or H[j] > ext):
                    ext, ext_j = H[j], j
                if side == "long" and L[j] < lvl and (ext is None or L[j] < ext):
                    ext, ext_j = L[j], j
                inside = (C[j] < lvl) if side == "short" else (C[j] > lvl)
                if ext is not None and inside:
                    entry_i = j
                    break
            if entry_i is None or entry_i == len(g) - 1:
                continue
            e = C[entry_i]
            R = (ext - e) if side == "short" else (e - ext)
            if R <= e * 0.0003:
                continue
            res = None
            for j in range(entry_i + 1, len(g)):
                if side == "short":
                    if H[j] >= ext: res = -1.0; break
                    if L[j] <= e - K * R: res = K; break
                else:
                    if L[j] <= ext: res = -1.0; break
                    if H[j] >= e + K * R: res = K; break
            if res is None:
                res = ((e - C[-1]) / R) if side == "short" else ((C[-1] - e) / R)
            rng = H[entry_i] - L[entry_i]
            body = abs(C[entry_i] - O[entry_i])
            if rng > 0:
                loc = (C[entry_i] - L[entry_i]) / rng  # 0 = closed at low
                strong = (body / rng >= 0.5) and ((loc <= 0.3) if side == "short" else (loc >= 0.7))
            else:
                strong = False
            depth = abs(ext - lvl) / atr
            out.append({
                "R": res, "year": 0 if i < len(days) / 2 else 1,
                "regime": "with" if ((side == "long" and bull) or (side == "short" and not bull)) else "against",
                "bar": "strong" if strong else "weak",
                "depth": "deep" if depth >= 0.10 else "shallow",
                "time": "first_hour" if ext_j == 0 else "later",
            })
    return out


allsig = []
for sym in ("SPY", "QQQ", "IWM"):
    s = signals(sym)
    for x in s:
        x["sym"] = sym
    allsig += s
    print(f"{sym}: {len(s)} signals")


def report(label, sel):
    n = len(sel)
    if n < 15:
        print(f"  {label:38s} N={n:4d} (too few)")
        return
    avg = sum(x["R"] for x in sel) / n
    halves = []
    for y in (0, 1):
        h = [x["R"] for x in sel if x["year"] == y]
        halves.append(f"{sum(h)/len(h):+.2f} (n={len(h)})" if h else "n/a")
    print(f"  {label:38s} N={n:4d} avg R {avg:+.3f} | 1st half {halves[0]} | 2nd half {halves[1]}")


print(f"\n=== ALL (3 ETFs pooled), 2R target, no costs. Random-walk expectation = 0 ===")
report("all", allsig)
for f in ("regime", "bar", "depth", "time"):
    print(f"-- by {f}")
    for v in sorted({x[f] for x in allsig}):
        report(f"{f}={v}", [x for x in allsig if x[f] == v])
print("-- combinations")
for reg in ("with", "against"):
    for bar in ("strong", "weak"):
        report(f"regime={reg} & bar={bar}", [x for x in allsig if x["regime"] == reg and x["bar"] == bar])
for reg in ("with", "against"):
    for dep in ("deep", "shallow"):
        report(f"regime={reg} & depth={dep}", [x for x in allsig if x["regime"] == reg and x["depth"] == dep])
