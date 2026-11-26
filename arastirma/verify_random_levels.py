"""Grimes' 'Random S/R levels' question, quantified: do PDH/PDL react better than random levels?
For each RTH day (1h bars, ~2y, SPY/QQQ/IWM):
  real levels  : previous day high (above open) and low (below open), if open is inside prior range
  random levels: open + (PDH-open)*U and open - (open-PDL)*U, U~Uniform(0.5,1.5)  (same distance scale)
On the FIRST touch of a level, measure 'rejection': after the touch bar, does price move X = 0.25*dailyATR
away from the level (back toward open) before moving X through the level? Same-bar ambiguity skipped.
Under a random walk both rates ~50%.
"""
import random
import sys

import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
random.seed(3)


def get(sym):
    d = yf.download(sym, period="3y", interval="1d", progress=False, auto_adjust=False)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    atr = (d["High"] - d["Low"]).rolling(14).mean()
    atr = {k.date(): v for k, v in atr.items()}
    df = yf.download(sym, period="730d", interval="1h", prepost=False, progress=False, auto_adjust=False)
    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)
    df = df.tz_convert("America/New_York").between_time("09:30", "15:59")
    return [(dt, g) for dt, g in df.groupby(df.index.date)], atr


def first_touch_outcome(H, L, lvl, above, X):
    for j in range(len(H)):
        touched = H[j] >= lvl if above else L[j] <= lvl
        if not touched:
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


tot = {"real": [0, 0], "rand": [0, 0]}
for sym in ("SPY", "QQQ", "IWM"):
    days, atr = get(sym)
    res = {"real": [0, 0], "rand": [0, 0]}
    for i in range(1, len(days)):
        (pd, prev), (d, g) = days[i - 1], days[i]
        a = atr.get(pd)
        if a is None or a != a:
            continue
        X = 0.25 * a
        O = g["Open"].values[0]
        pdh, pdl = prev["High"].max(), prev["Low"].min()
        if not (pdl < O < pdh):
            continue
        H, L = g["High"].values, g["Low"].values
        for kind, up, dn in (("real", pdh, pdl),
                             ("rand", O + (pdh - O) * random.uniform(0.5, 1.5), O - (O - pdl) * random.uniform(0.5, 1.5))):
            for lvl, above in ((up, True), (dn, False)):
                r = first_touch_outcome(H, L, lvl, above, X)
                if r is not None:
                    res[kind][0] += r
                    res[kind][1] += 1
    for k in res:
        tot[k][0] += res[k][0]; tot[k][1] += res[k][1]
    print(f"{sym}: real PDH/PDL rejection {res['real'][0]}/{res['real'][1]} = {res['real'][0]/max(res['real'][1],1):.0%} | "
          f"random levels {res['rand'][0]}/{res['rand'][1]} = {res['rand'][0]/max(res['rand'][1],1):.0%}")
r, n = tot["real"]; q, m = tot["rand"]
print(f"POOLED: real {r}/{n} = {r/n:.1%} | random {q}/{m} = {q/m:.1%} | random-walk theory 50%")
