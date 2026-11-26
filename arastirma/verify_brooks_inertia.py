"""Brooks, 'Trading the Open' (TradersEXPO, S9b7hwEzMSk) - testable claims:
 A 'Markets have inertia': after 4 consecutive bull days (close > open), expect another bull day.
 B After a run of doji / trading-range days, today is likely another trading-range day (closes near its open).
 C A big bear day after a tight 2-week range -> 'more likely a two-day trading range': next day reverses up.
 D On trading-range days 'any rally in the middle third of the day has a 60-70% chance to come back and test the
   open later in the day' (intraday, 1h bars, ~2 years).
Daily part: 2005+, 14 ETFs, regular-session bodies (close vs open, i.e. no overnight gap).
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DSYMS = "SPY QQQ IWM DIA MDY XLK XLF XLE XLV XLI XLY XLP EFA EEM".split()

A = {"cond": [], "base": []}; B = {"cond": [], "base": []}; Cc = {"cond": [], "base": []}
for sym in DSYMS:
    d = yf.download(sym, start="2004-06-01", interval="1d", progress=False, auto_adjust=True)
    if d is None or len(d) < 500:
        continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna(); d = d[d["High"] > d["Low"]]
    O, Hh, L, C = (d[c].values for c in ("Open", "High", "Low", "Close"))
    yr = d.index.year.values; T = len(C)
    bull = C > O
    rng = Hh - L
    dojish = np.abs(C - O) < 0.3 * rng                     # closes near its open
    tr = np.maximum(rng, np.maximum(abs(Hh - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = np.convolve(tr, np.ones(14) / 14, mode="full")[:T]
    for t in range(20, T):
        if yr[t] < 2005:
            continue
        A["base"].append(bull[t]); B["base"].append(dojish[t])
        if bull[t - 4:t].all():
            A["cond"].append(bull[t])
        if dojish[t - 4:t].sum() >= 3:
            B["cond"].append(dojish[t])
        # C: tight 10-day range before a big bear day at t-1, outcome = day t bull?
        a = atr[t - 2]
        if a > 0:
            tight = (Hh[t - 11:t - 1].max() - L[t - 11:t - 1].min()) < 3.0 * a
            bigbear = (O[t - 1] - C[t - 1]) > 1.0 * a and (C[t - 1] - L[t - 1]) < 0.25 * rng[t - 1]
            if bigbear:
                Cc["base"].append(bull[t])          # big bear day, any background
                if tight:
                    Cc["cond"].append(bull[t])


def rep(name, D, what):
    c, b = np.array(D["cond"]), np.array(D["base"])
    se = np.sqrt(c.mean() * (1 - c.mean()) / len(c))
    print(f"{name}: {what} {c.mean():.1%} (n={len(c)}, se {se:.1%}) vs baseline {b.mean():.1%} (n={len(b)}) "
          f"-> diff {100*(c.mean()-b.mean()):+.1f} pts")


print("DAILY (14 ETFs, 2005+)")
rep("A after 4 bull days in a row", A, "P(bull day)")
rep("B after >=3 of last 4 days doji-ish", B, "P(doji-ish day, |C-O|<0.3 range)")
rep("C big bear day after tight 10d range (vs big bear day any background)", Cc, "P(next day bull)")

# D: intraday, 1h bars
print("\nINTRADAY (1h, ~2 years): rally at the 12:30 bar close >= 0.5 x average daily range above the open")
for sym in ("SPY", "QQQ", "IWM", "DIA"):
    d = yf.download(sym, period="730d", interval="1h", progress=False, auto_adjust=False, prepost=False)
    if d is None or len(d) < 300:
        continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna()
    idx = d.index.tz_convert("America/New_York")
    O, Hh, L, C = (d[c].values for c in ("Open", "High", "Low", "Close"))
    days = {}
    for i, ts in enumerate(idx):
        if (9, 30) <= (ts.hour, ts.minute) and ts.hour < 16:
            days.setdefault(ts.date(), []).append(i)
    dl = sorted(days); rngs = []; info = []
    for day in dl:
        b = days[day]
        if len(b) < 7 or idx[b[0]].hour != 9:
            continue
        op = O[b[0]]; hi = Hh[b].max(); lo = L[b].min()
        rngs.append(hi - lo)
        info.append((day, b, op))
    rngs = np.array(rngs)
    res = {"all": [], "tr_bg": []}; recent = []
    for k, (day, b, op) in enumerate(info):
        avg = rngs[max(0, k - 20):k].mean() if k >= 5 else np.nan
        if not np.isfinite(avg):
            continue
        # background: >=3 of the prior 4 sessions closed within 30% of range from their open
        bg = []
        for (d2, b2, op2) in info[max(0, k - 4):k]:
            hi2, lo2 = Hh[b2].max(), L[b2].min()
            bg.append(abs(C[b2[-1]] - op2) < 0.3 * (hi2 - lo2))
        tr_bg = len(bg) == 4 and sum(bg) >= 3
        j = b[3]                                   # 12:30 bar
        for side in (1, -1):
            if side * (C[j] - op) >= 0.5 * avg:
                later = b[4:]
                touched = (L[later].min() <= op) if side == 1 else (Hh[later].max() >= op)
                res["all"].append(touched)
                if tr_bg:
                    res["tr_bg"].append(touched)
    a1, a2 = np.array(res["all"]), np.array(res["tr_bg"])
    print(f"  {sym}: P(test the open later) all strong mid-day moves {a1.mean():.0%} (n={len(a1)}) | "
          f"after trading-range background {a2.mean() if len(a2) else float('nan'):.0%} (n={len(a2)})")
