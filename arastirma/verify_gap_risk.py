"""Round 50: Lance Breitstein, "16 Years of Swing Trading Lessons in 12 Minutes" (bZ7-iBaI_Xw).
Claims checked:
 (L2/L9) "Going from intraday to swing you must cut size more than the stop-distance ratio, because of gap risk:
          a stock doesn't trade politely through your stop... you can wake up at 42 with a stop at 48";
          "shorting small caps overnight is the most dangerous (buyouts, gaps of hundreds of percent)".
 (L3/L4) "Technical analysis is fractal: a good intraday setup is almost always a good daily setup; the same
          breakout / capitulation ideas work across time frames."
Part A: risk 1R = k*ATR14 below/above the close; how often does the NEXT open gap THROUGH the stop, and how big is
        the loss then (in R)? Weekday nights vs weekends; large caps vs volatile small caps vs futures/FX.
        Prop angle: with 1% risk per position, how often does one overnight/weekend gap cost more than 3% / 5%
        (FTMO 1-Step / 2-Step daily limits; Swing accounts may hold over the weekend)?
Part B: the SAME two rules on 5m / 1h / 1d bars (SPY, QQQ, GLD, EURUSD): (i) 20-bar breakout, hold 10 bars;
        (ii) 'capitulation' = 3 down closes totalling > 2 ATR, buy, hold 5 bars. Forward return in ATR units minus
        the unconditional same-side forward return (drift-matched baseline). Round-trip cost shown in ATR units.
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def load(sym, interval="1d", period=None, start=None):
    kw = {"interval": interval, "progress": False, "auto_adjust": True}
    if period:
        kw["period"] = period
    else:
        kw["start"] = start
    d = yf.download(sym, **kw)
    if d is None or len(d) == 0:
        return None
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna()
    return d[(d["High"] > 0) & (d["Low"] > 0)]


def atr(H, L, C, n=14):
    tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    tr[0] = H[0] - L[0]
    return pd.Series(tr).rolling(n).mean().to_numpy(copy=True)


GROUPS = {"LARGE CAP": "AAPL MSFT AMZN JPM XOM JNJ PG KO WMT CSCO INTC PFE".split(),
          "VOLATILE SMALL/MID": "PLUG RIOT MARA GME AMC FCEL SAVA OCGN NVAX CLOV BLNK SPWR".split(),
          "FUT/FX/INDEX": "ES=F NQ=F GC=F CL=F EURUSD=X GBPUSD=X USDJPY=X SPY".split()}

print("PART A: next-open gap THROUGH a stop placed k*ATR14 from the close (daily, 2010+)")
print("  cells: P(gap through stop) | mean loss in R when it happens | worst 0.5% outcome (R) | worst ever (R)")
for g, syms in GROUPS.items():
    rows = {}
    for s in syms:
        d = load(s, start="2009-06-01")
        if d is None or len(d) < 500:
            continue
        d = d[d.index >= "2010-01-01"] if len(d[d.index >= "2010-01-01"]) > 300 else d
        O, H, L, C = (d[c].values for c in ("Open", "High", "Low", "Close"))
        a = atr(H, L, C); a[a <= 0] = np.nan
        wk = np.r_[False, (d.index[1:] - d.index[:-1]).days >= 3]  # True if the next bar comes after a 3+ day gap
        for k in (1.0, 2.0):
            for side in (1, -1):
                for night in ("weekday", "weekend"):
                    m = ~np.isnan(a[:-1])
                    m &= (wk[1:] if night == "weekend" else ~wk[1:])
                    r = side * (O[1:] - C[:-1]) / (k * a[:-1])  # open move in R; stop hit at open if r <= -1
                    r = r[m]; r = r[np.isfinite(r)]
                    rows.setdefault((k, side, night), []).append(r)
    print(f"\n  === {g} ===")
    for (k, side, night), lst in sorted(rows.items(), key=lambda x: (x[0][0], -x[0][1], x[0][2])):
        r = np.concatenate(lst)
        hit = r <= -1
        print(f"   stop {k:.0f} ATR {'LONG ' if side == 1 else 'SHORT'} {night:8s}: n={len(r):6d} | "
              f"P {hit.mean():6.2%} | mean loss {r[hit].mean() if hit.any() else float('nan'):+6.2f}R | "
              f"0.5% {np.percentile(r, 0.5):+6.2f}R | worst {r.min():+7.2f}R")

print("\n  Prop angle (1% risk per position, stop 1 ATR): probability that ONE position's open gap alone loses")
print("  more than 3% / 5% of the account (FTMO 1-Step / 2-Step daily limit), per overnight/weekend hold")
for g, syms in GROUPS.items():
    allr = []
    for s in syms:
        d = load(s, start="2009-06-01")
        if d is None or len(d) < 500:
            continue
        O, H, L, C = (d[c].values for c in ("Open", "High", "Low", "Close")); a = atr(H, L, C); a[a <= 0] = np.nan
        for side in (1, -1):
            r = side * (O[1:] - C[:-1]) / a[:-1]
            allr.append(r[np.isfinite(r) & (a[:-1] > 0)])
    r = np.concatenate(allr)
    print(f"   {g:20s}: P(gap loss > 3R) {np.mean(r < -3):.3%} | P(> 5R) {np.mean(r < -5):.3%} | "
          f"i.e. once every ~{1 / max(np.mean(r < -3), 1e-9):,.0f} holds (>3R)")

print("\nPART B: same rule, different bar sizes ('fractal' claim). Excess fwd return in ATR units vs same-side baseline")
TF = {"5m (60d)": ("5m", "60d"), "1h (730d)": ("1h", "730d"), "1d (2005+)": ("1d", None)}
COST = {"SPY": 0.02, "QQQ": 0.02, "GLD": 0.02, "EURUSD=X": 0.00010}  # rough round trip (spread + fees), price units
for s in COST:
    print(f"\n  === {s} ===")
    for lab, (iv, per) in TF.items():
        d = load(s, iv, period=per) if per else load(s, iv, start="2005-01-01")
        if d is None or len(d) < 300:
            print(f"   {lab}: no data"); continue
        O, H, L, C = (d[c].values for c in ("Open", "High", "Low", "Close")); a = atr(H, L, C); a[a <= 0] = np.nan
        n = len(C); out = []
        # (i) breakout: close above prior 20-bar high, hold 10 bars
        hi20 = pd.Series(H).shift(1).rolling(20).max().values
        fwd10 = np.full(n, np.nan); fwd10[:-10] = (C[10:] - C[:-10])
        sig = (C > hi20) & ~np.isnan(a)
        base = np.nanmean(fwd10 / a)
        x = (fwd10 / a)[sig & ~np.isnan(fwd10)]
        out.append(("breakout hold 10", x.mean() - base, x.std() / np.sqrt(max(len(x), 1)), len(x)))
        # (ii) capitulation: 3 down closes, total drop > 2 ATR, buy and hold 5 bars
        fwd5 = np.full(n, np.nan); fwd5[:-5] = (C[5:] - C[:-5])
        dn = (C < np.roll(C, 1)) & (np.roll(C, 1) < np.roll(C, 2)) & (np.roll(C, 2) < np.roll(C, 3))
        drop = (np.roll(C, 3) - C) > 2 * a
        sig2 = dn & drop & ~np.isnan(a); sig2[:3] = False
        base5 = np.nanmean(fwd5 / a)
        y = (fwd5 / a)[sig2 & ~np.isnan(fwd5)]
        out.append(("capitulation buy hold 5", y.mean() - base5, y.std() / np.sqrt(max(len(y), 1)), len(y)))
        cost = COST[s] / np.nanmedian(a)
        cells = " | ".join(f"{nm}: {m:+.3f} ATR (se {se:.3f}, n={k})" for nm, m, se, k in out)
        print(f"   {lab:11s} cost≈{cost:.3f} ATR | {cells}")
