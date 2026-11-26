"""Round 22: INTRADAY MOMENTUM as a prop candidate (Gao, Han, Li & Zhou, 'Market Intraday Momentum', JFE 2018:
the first half-hour return incl. overnight predicts the last half-hour return of SPY).
yfinance 1h bars (~730 days) -> bars 9:30, 10:30, ..., 14:30 (60 min) and 15:30 (30 min, the LAST HALF HOUR).
  P1: sign(prev close -> 10:30 close)  [overnight + first hour]  -> trade the last half hour (15:30 open -> close)
  P2: sign(open -> 13:30 close)        [midday position]          -> trade 13:30 -> 16:00
  P3: sign(prev close -> 15:30 open)   [whole day so far]          -> trade the last half hour
Metrics per symbol and pooled: mean signed return in bps, t-stat, hit rate, net of a round-trip cost ($0.02/share),
annualised Sharpe of the one-trade-per-day strategy, and 'R per year if 1R = 1 stdev of the trade' = mean/std * 252
(the prop yardstick from 09 §2: need >= 10-15R/yr).
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SYMS = ("SPY", "QQQ", "IWM", "DIA", "XLK", "XLF", "SMH", "XLE", "GLD", "TLT")
COSTUSD = 0.02

rows = {"P1": [], "P2": [], "P3": []}
print("1h bars ~2 years. signed return of the target window, bps; net = after $0.02/share round trip")
for sym in SYMS:
    d = yf.download(sym, period="730d", interval="1h", progress=False, auto_adjust=False, prepost=False)
    if d is None or len(d) < 500:
        print(f"{sym}: no data"); continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna(); idx = d.index.tz_convert("America/New_York")
    O, C = d["Open"].values, d["Close"].values
    days = {}
    for i, ts in enumerate(idx):
        if (9, 30) <= (ts.hour, ts.minute) and ts.hour < 16:
            days.setdefault(ts.date(), []).append(i)
    dl = [k for k in sorted(days) if len(days[k]) == 7 and idx[days[k][0]].hour == 9 and idx[days[k][6]].hour == 15]
    res = {"P1": [], "P2": [], "P3": []}; prev_close = None
    for k in dl:
        b = days[k]
        op = O[b[0]]
        if prev_close is not None:
            px_last_open = O[b[6]]; px_close = C[b[6]]
            cost_bps = 2 * 0 + COSTUSD / px_close * 1e4
            s1 = np.sign(C[b[0]] - prev_close)
            r_last = (px_close - px_last_open) / px_last_open * 1e4
            if s1 != 0:
                res["P1"].append((s1 * r_last, cost_bps))
            s2 = np.sign(C[b[3]] - op)
            r_aft = (px_close - C[b[3]]) / C[b[3]] * 1e4
            if s2 != 0:
                res["P2"].append((s2 * r_aft, cost_bps))
            s3 = np.sign(px_last_open - prev_close)
            if s3 != 0:
                res["P3"].append((s3 * r_last, cost_bps))
        prev_close = C[b[6]]
    line = f"{sym:4s} days={len(dl)}"
    for key in res:
        v = np.array(res[key]); g = v[:, 0]; n = g - v[:, 1]
        rows[key].append((sym, g, n))
        t = g.mean() / (g.std() / np.sqrt(len(g)))
        sh = n.mean() / n.std() * np.sqrt(252)
        line += f" | {key}: gross {g.mean():+.2f}bp (t {t:+.1f}) hit {np.mean(g > 0):.0%} net {n.mean():+.2f}bp Sharpe {sh:+.2f}"
    print(line)

print("\nPooled (equal weight across symbols; index ETFs are highly correlated, so the pooled t-stat is optimistic):")
for key in rows:
    g = np.concatenate([x[1] for x in rows[key]]); n = np.concatenate([x[2] for x in rows[key]])
    spy = [x for x in rows[key] if x[0] == "SPY"][0][2]
    print(f"  {key}: gross {g.mean():+.2f}bp (t {g.mean()/(g.std()/np.sqrt(len(g))):+.1f}) | net {n.mean():+.2f}bp | "
          f"SPY alone: Sharpe {spy.mean()/spy.std()*np.sqrt(252):+.2f}, R/yr (1R = 1 sd) {spy.mean()/spy.std()*252:+.1f}")
