"""Round 24: SWING candidates for prop (industry data: consistent payout traders hold 1-3 days, don't overtrade).
Two published, evidence-based effects, tested OUT OF SAMPLE after publication:
 A Connors RSI(2) (Connors & Alvarez, 'Short Term Trading Strategies That Work', 2008): long when close > SMA200 and
   RSI(2) < 10; buy at the close; exit at the close when close > SMA5 (max 10 days). Pre-2009 = in-sample era,
   2009+ = after publication.
 B Overnight drift (Cooper, Cliff & Gulen 2008; Kelly & Clark 2011): buy the close, sell the next open, every day.
   Compared with the intraday leg (open -> close).
Units: % return and R where 1R = ATR14 at entry (a hypothetical 1-ATR stop distance). Prop yardstick: R per year.
Costs: 1 bp per round trip (ETF, liquid) for A; 1 bp per round trip for B (two trades per day).
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SYMS = ("SPY", "QQQ", "IWM", "DIA", "EFA", "EWJ", "EWG", "EWU")


def rsi(c, n=2):
    d = np.diff(c, prepend=c[0])
    up = np.where(d > 0, d, 0.0); dn = np.where(d < 0, -d, 0.0)
    au = np.zeros_like(c); ad = np.zeros_like(c)
    au[n] = up[1:n + 1].mean(); ad[n] = dn[1:n + 1].mean()
    for i in range(n + 1, len(c)):
        au[i] = (au[i - 1] * (n - 1) + up[i]) / n
        ad[i] = (ad[i - 1] * (n - 1) + dn[i]) / n
    rs = np.divide(au, ad, out=np.full_like(au, np.inf), where=ad > 0)
    return 100 - 100 / (1 + rs)


print("A) Connors RSI(2) long. per-trade net % / R (1R = ATR14), trades per year, hold days, R/yr per symbol")
allA = {"pre2009": [], "post2009": []}
for sym in SYMS:
    d = yf.download(sym, start="1993-01-01", interval="1d", progress=False, auto_adjust=True)
    if d is None or len(d) < 600:
        continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna()
    O, Hh, L, C = (d[c].values for c in ("Open", "High", "Low", "Close"))
    yr = d.index.year.values; T = len(C)
    tr = np.maximum(Hh - L, np.maximum(abs(Hh - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = np.convolve(tr, np.ones(14) / 14, mode="full")[:T]
    s200 = np.convolve(C, np.ones(200) / 200, mode="full")[:T]
    s5 = np.convolve(C, np.ones(5) / 5, mode="full")[:T]
    r2 = rsi(C)
    res = {"pre2009": [], "post2009": []}; holds = []
    t = 205
    while t < T - 11:
        if C[t] > s200[t] and r2[t] < 10:
            e = C[t]; a = atr[t]
            for j in range(t + 1, min(t + 11, T)):
                if C[j] > s5[j] or j == t + 10:
                    break
            pct = (C[j] / e - 1) * 100 - 0.01
            R = (C[j] - e) / a - 0.0001 * e / a
            key = "pre2009" if yr[t] < 2009 else "post2009"
            res[key].append((pct, R)); holds.append(j - t)
            t = j + 1
        else:
            t += 1
    line = f"  {sym:4s}"
    for key in res:
        v = np.array(res[key]) if res[key] else np.zeros((0, 2))
        yrs = (np.sum(yr < 2009) if key == "pre2009" else np.sum(yr >= 2009)) / 252
        allA[key].extend(res[key])
        if len(v):
            line += (f" | {key}: n={len(v)} ({len(v)/yrs:.1f}/yr) avg {v[:,0].mean():+.2f}% / {v[:,1].mean():+.2f}R "
                     f"win {np.mean(v[:,0] > 0):.0%} R/yr {v[:,1].sum()/yrs:+.1f}")
    line += f" | avg hold {np.mean(holds):.1f}d"
    print(line)
for key in allA:
    v = np.array(allA[key])
    print(f"  pooled {key}: n={len(v)} avg {v[:,0].mean():+.2f}% (se {v[:,0].std()/np.sqrt(len(v)):.2f}) "
          f"{v[:,1].mean():+.3f}R (se {v[:,1].std()/np.sqrt(len(v)):.3f}) win {np.mean(v[:,0] > 0):.0%}")

print("\nB) Overnight (close -> next open) vs intraday (open -> close). annualised return, Sharpe, by era. 1bp cost")
for sym in ("SPY", "QQQ", "IWM", "DIA"):
    d = yf.download(sym, start="1993-01-01", interval="1d", progress=False, auto_adjust=True)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna()
    O, C = d["Open"].values, d["Close"].values
    yr = d.index.year.values[1:]
    on = np.log(O[1:] / C[:-1]) - 0.0001
    intr = np.log(C[1:] / O[1:])
    line = f"  {sym:4s}"
    for lab, m in (("<=2008", yr <= 2008), ("2009-2017", (yr >= 2009) & (yr <= 2017)), ("2018+", yr >= 2018)):
        a, b = on[m], intr[m]
        line += (f" | {lab}: overnight {a.mean()*252*100:+.1f}%/yr Sh {a.mean()/a.std()*np.sqrt(252):+.2f}, "
                 f"intraday {b.mean()*252*100:+.1f}%/yr Sh {b.mean()/b.std()*np.sqrt(252):+.2f}")
    print(line)
