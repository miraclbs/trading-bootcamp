"""Round 23: robustness of the late-day reversal hypothesis (verify_close_reversal.py) on index FUTURES and on a
different window. yfinance futures 1h bars start on the hour (America/New_York), so the cash session's LAST HOUR is
the 15:00 bar (15:00-16:00). Signal at the 15:00 bar open: s = sign(price - previous day's 16:00 price, i.e. the close
of the previous day's 15:00 bar). Trade -s from the 15:00 open to the 15:00 bar close (16:00).
Round-trip costs (1 tick spread + commission, approx.): ES 0.5 pt, NQ 2 pt, YM 4 pt, RTY 0.3 pt.
Also, for comparison, the same LAST-HOUR rule cannot be built on SPY 1h bars (14:30/15:30 bars), so SPY is shown with
its last half hour (15:30 bar) as in round 22.
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
COST = {"ES=F": 0.5, "NQ=F": 2.0, "YM=F": 4.0, "RTY=F": 0.3}


def sh(v):
    return v.mean() / v.std() * np.sqrt(252) if len(v) > 10 and v.std() > 0 else float("nan")


print("Futures, last hour of the cash session, fade the day's move so far. net bp/day after cost")
for sym, cost in COST.items():
    d = yf.download(sym, period="730d", interval="1h", progress=False, auto_adjust=False)
    if d is None or len(d) < 500:
        print(f"{sym}: no data"); continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna(); idx = d.index.tz_convert("America/New_York")
    O, C = d["Open"].values, d["Close"].values
    bar15 = {}
    for i, ts in enumerate(idx):
        if ts.hour == 15 and ts.minute == 0 and ts.weekday() < 5:
            bar15[ts.date()] = i
    days = sorted(bar15)
    r = []; signal_size = []
    for k in range(1, len(days)):
        i, ip = bar15[days[k]], bar15[days[k - 1]]
        if (days[k] - days[k - 1]).days > 4:
            continue
        prev = C[ip]; s = np.sign(O[i] - prev)
        if s == 0:
            continue
        g = -s * (C[i] - O[i]) / O[i] * 1e4
        r.append(g - cost / O[i] * 1e4); signal_size.append(abs(O[i] / prev - 1))
    r = np.array(r); h = len(r) // 2; ss = np.array(signal_size)
    big = r[ss > 0.005]
    print(f"  {sym:5s} n={len(r)} net {r.mean():+.2f}bp (sd {r.std():.1f}) Sharpe {sh(r):+.2f} | 1st half {sh(r[:h]):+.2f} "
          f"| 2nd half {sh(r[h:]):+.2f} | day move >0.5%: {big.mean():+.2f}bp (n={len(big)}) | R/yr (1R=1sd) {r.mean()/r.std()*252:+.1f}")
