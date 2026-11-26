"""Jerry Parker (Meb Faber Show TjkdsSHW6oQ): 'Trading indices with systematic trend following is a huge mistake ...
trading the individual names is way more diversification, it improves the drawdown and the risk profile.'
Test: 12-month time-series momentum (long if price > 12 months ago, else short), monthly rebalance, inverse-vol
sizing with a 5% vol floor, 5 bp turnover cost, 2005+.
  A) SPY alone          B) 4 equity index ETFs (SPY QQQ IWM DIA)
  C) 30 US large caps (equal risk)   D) 30 large caps, LONG-ONLY version (flat instead of short)
Report Sharpe, maxDD (after scaling each to 10% vol), correlation with SPY buy & hold.
Caveat: today's large caps -> survivorship bias (helps long side)."""
import sys
import numpy as np
import pandas as pd
import yfinance as yf
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
STK = ("AAPL MSFT JNJ PG KO PEP XOM CVX JPM BAC WFC GE IBM INTC CSCO ORCL WMT HD MCD DIS MRK PFE T VZ MMM CAT BA HON "
       "UNH AMGN").split()
syms = ["SPY", "QQQ", "IWM", "DIA"] + STK
px = {}
for s in syms:
    d = yf.download(s, start="2003-06-01", interval="1d", progress=False, auto_adjust=True)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    c = d["Close"].dropna(); c.index = (c.index.tz_localize(None) if c.index.tz is not None else c.index).normalize()
    px[s] = c[~c.index.duplicated()]
P = pd.DataFrame(px).sort_index().ffill(limit=5)
R = P.pct_change(fill_method=None).clip(-0.4, 0.4)

def tsmom(cols, long_only=False, lb=252, floor=0.05):
    vol = R[cols].rolling(60).std() * np.sqrt(252)
    sig = np.sign(P[cols] / P[cols].shift(lb) - 1)
    if long_only: sig = sig.clip(lower=0)
    me = P.index.to_series().groupby(P.index.to_period("M")).max().values
    W = pd.DataFrame(np.nan, index=P.index, columns=cols)
    for dt in me:
        n = sig.loc[dt].notna().sum()
        if n: W.loc[dt] = sig.loc[dt] * (0.10 / np.maximum(vol.loc[dt], floor)) / n
    W = W.ffill().fillna(0.0)
    net = (W.shift(1) * R[cols]).sum(axis=1) - 0.0005 * W.diff().abs().sum(axis=1)
    return net[net.index >= "2005-01-01"]

def rep(lab, r):
    r = r * (0.10 / (r.std() * np.sqrt(252)))
    eq = (1 + r).cumprod(); mdd = (1 - eq / eq.cummax()).max()
    sh = r.mean() / r.std() * np.sqrt(252); sh2 = r[r.index >= "2015"].mean() / r[r.index >= "2015"].std() * np.sqrt(252)
    c = np.corrcoef(r.values, R["SPY"].reindex(r.index).fillna(0).values)[0, 1]
    print(f"  {lab:34s}: Sharpe {sh:+.2f} (2015+ {sh2:+.2f}) | maxDD at 10% vol {mdd:.0%} | corr with SPY {c:+.2f}")

print("12-month TSMOM, 2005+, each scaled to 10% vol")
rep("A) SPY alone", tsmom(["SPY"]))
rep("B) 4 index ETFs", tsmom(["SPY", "QQQ", "IWM", "DIA"]))
rep("C) 30 large caps long/short", tsmom(STK))
rep("D) 30 large caps long-only", tsmom(STK, long_only=True))
rep("   SPY buy & hold (reference)", R["SPY"][R.index >= "2005"])
