"""Round 32: Rob Carver, "In The Money by Zerodha" podcast #04 (p0znNV4oWe8). Claims tested:
 (A) "There are about a hundred ways of identifying trends and they all do the same thing; they are highly
     correlated. The simplest - price change over the last N days - performs very close to an EWMA crossover.
     Adding more trend rules moves Sharpe by a few hundredths at most." Also: trend works on horizons of weeks to a
     year; fast trends are noise.
     -> 19 ETF/FX markets (as verify_tsmom.py), 2005+. Rules: EWMAC 8/32, 16/64, 32/128, 64/256 (sign), N-day return
        sign (20, 63, 126, 252), Donchian position (20, 55, 120 day: long above mid-channel), and the equal-weight
        average of all. Positions vol-scaled (60d, 5% floor), weekly rebalance, 5 bp cost.
 (B) "Max drawdown is a terrible metric: exposed to outliers, poor sampling error, and it scales with time. Look at
     the bootstrapped distribution for the horizon you care about."
     -> Block bootstrap (20-day blocks) of the 12m TSMOM daily returns at 8% annual vol: distribution of max
        drawdown over 1, 2, 5 and 20 years vs the single historical figure. Prop reading: P(maxDD > 10%) by horizon.
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(32)
SYMS = ["SPY", "EFA", "EEM", "EWJ", "TLT", "IEF", "GLD", "SLV", "USO", "DBA", "DBC", "CPER", "UNG",
        "EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X", "USDCHF=X"]
px = {}
for s in SYMS:
    d = yf.download(s, start="2003-06-01", interval="1d", progress=False, auto_adjust=True)
    if d is None or len(d) < 500:
        continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    c = d["Close"].dropna()
    c.index = (c.index.tz_localize(None) if c.index.tz is not None else c.index).normalize()
    px[s] = c[~c.index.duplicated()]
P = pd.DataFrame(px).sort_index().ffill(limit=5)
R = P.pct_change(fill_method=None).clip(-0.25, 0.25)
N = P.shape[1]
vol = (R.rolling(60).std() * np.sqrt(252)).clip(lower=0.05)
week_end = P.index.to_series().groupby(P.index.to_period("W")).max().values


def ewma(x, span):
    return x.ewm(span=span, adjust=False).mean()


rules = {}
for f, s in ((8, 32), (16, 64), (32, 128), (64, 256)):
    rules[f"EWMAC {f}/{s}"] = np.sign(ewma(P, f) - ewma(P, s))
for n in (20, 63, 126, 252):
    rules[f"{n}-day return"] = np.sign(P / P.shift(n) - 1)
for n in (20, 55, 120):
    hi = P.rolling(n).max(); lo = P.rolling(n).min()
    rules[f"Donchian {n}"] = np.sign(P - (hi + lo) / 2)


def backtest(sig):
    w = sig * (0.10 / vol) / N
    W = pd.DataFrame(np.nan, index=P.index, columns=P.columns)
    W.loc[week_end] = w.loc[week_end]
    W = W.ffill().fillna(0.0)
    net = (W.shift(1) * R).sum(axis=1) - 0.0005 * W.diff().abs().sum(axis=1)
    return net[net.index >= "2005-01-01"]


def sharpe(r):
    return r.mean() / r.std() * np.sqrt(252)


res = {k: backtest(v) for k, v in rules.items()}
res["AVERAGE of all 11"] = backtest(sum(rules.values()) / len(rules))
print("(A) Trend rules on 19 markets, vol-scaled, weekly rebalance, 5 bp costs, 2005+")
print(f"  {'rule':20s} Sharpe 2005+ | 2015+ | corr with EWMAC 16/64 | corr with 252-day return")
for k, r in res.items():
    print(f"  {k:20s} {sharpe(r):+.2f}      | {sharpe(r[r.index >= '2015']):+.2f} | "
          f"{np.corrcoef(r, res['EWMAC 16/64'])[0, 1]:+.2f}                 | {np.corrcoef(r, res['252-day return'])[0, 1]:+.2f}")
M = pd.DataFrame({k: v for k, v in res.items() if k != "AVERAGE of all 11"}).corr()
iu = np.triu_indices(len(M), 1)
print(f"  average pairwise P&L correlation among the 11 rules: {M.values[iu].mean():.2f} "
      f"(min {M.values[iu].min():.2f}, max {M.values[iu].max():.2f})")
slow = [k for k in M.index if k not in ("EWMAC 8/32", "20-day return", "Donchian 20")]
Ms = M.loc[slow, slow].values; ius = np.triu_indices(len(slow), 1)
print(f"  ... among the 8 rules slower than ~1 month: {Ms[ius].mean():.2f}")

print("\n(B) Max drawdown sampling: 12m TSMOM (252-day return rule) scaled to 8% annual vol, 20-day block bootstrap")
r = res["252-day return"]; r = r * (0.08 / (r.std() * np.sqrt(252)))
eq = (1 + r).cumprod()
print(f"  historical: {len(r) / 252:.0f} years, Sharpe {sharpe(r):.2f}, single max drawdown {(1 - eq / eq.cummax()).max():.1%}")
x = r.values; B = 20; nb = len(x) // B
for yrs in (1, 2, 5, 20):
    L = yrs * 252; mdds = []
    for _ in range(4000):
        idx = np.concatenate([np.arange(s, s + B) for s in rng.integers(0, len(x) - B, L // B + 1)])[:L]
        e = np.cumprod(1 + x[idx]); mdds.append((1 - e / np.maximum.accumulate(e)).max())
    q = np.percentile(mdds, [5, 25, 50, 75, 95])
    print(f"  {yrs:2d}-year window: max DD percentiles 5/25/50/75/95 = "
          + " / ".join(f"{v:.1%}" for v in q) + f" | P(maxDD > 10%) = {np.mean(np.array(mdds) > 0.10):.0%}")
