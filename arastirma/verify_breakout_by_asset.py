"""Grimes (Chat With Traders ep.115): "buying 20-day highs / shorting 20-day lows makes a little money in commodities
and loses money in stocks -> the claim that the same tools work in every market is a lie of traditional TA;
on the daily timeframe stocks mean-revert more than commodities."
Test, daily data 2005+, three asset groups (no costs):
  STOCKS : 30 US large caps (survivorship bias: today's large caps -> biased toward long-side success)
  COMMOD : commodity ETFs (GLD SLV USO UNG DBA DBC PPLT PALL UGA CPER CORN WEAT SOYB)  [roll yield included]
  FX     : 7 major pairs (yfinance =X)
(1) Donchian stop-and-reverse: +1 after close > prior 20d high, -1 after close < prior 20d low, hold until opposite.
    Daily P&L in ATR units = pos[t-1] * (C[t]-C[t-1]) / ATR14[t-1].  Report annualised mean (ATR units/yr), Sharpe.
(2) Long-only version (+1 / flat) for stocks, to separate drift from trend.
(3) Event study: forward 20d return (ATR units) after a close-breakout of the 20d high / low, minus the symbol's
    unconditional 20d forward return (drift), signed in trade direction.
Usage: python verify_breakout_by_asset.py
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GROUPS = {
    "STOCKS": ("AAPL MSFT JNJ PG KO PEP XOM CVX JPM BAC WFC GE IBM INTC CSCO ORCL WMT HD MCD DIS MRK PFE T VZ MMM "
               "CAT BA HON UNH AMGN").split(),
    "COMMOD": "GLD SLV USO UNG DBA DBC PPLT PALL UGA CPER CORN WEAT SOYB".split(),
    "FX": "EURUSD=X GBPUSD=X USDJPY=X AUDUSD=X USDCAD=X USDCHF=X NZDUSD=X".split(),
}
N = 20


def load(sym):
    d = yf.download(sym, start="2004-01-01", interval="1d", progress=False, auto_adjust=True)
    if d is None or len(d) < 300:
        return None
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna()
    d = d[(d["High"] > 0) & (d["Low"] > 0)]
    return d


res = {}
for g, syms in GROUPS.items():
    daily, daily_lo, yrs, ev, n_sym, bh = [], [], [], [], 0, []
    for sym in syms:
        d = load(sym)
        if d is None:
            print(f"  skip {sym}"); continue
        n_sym += 1
        Hh, L, C = d["High"].values, d["Low"].values, d["Close"].values
        yr = d.index.year.values
        tr = np.maximum(Hh - L, np.maximum(abs(Hh - np.roll(C, 1)), abs(L - np.roll(C, 1))))
        atr = np.convolve(tr, np.ones(14) / 14, mode="full")[:len(tr)]
        pos = 0
        hi = np.array([Hh[max(0, t - N):t].max() if t >= N else np.nan for t in range(len(C))])
        lo = np.array([L[max(0, t - N):t].min() if t >= N else np.nan for t in range(len(C))])
        fwd = np.full(len(C), np.nan)
        fwd[:-N] = (C[N:] - C[:-N])
        start = N + 15
        valid = [t for t in range(start, len(C) - N) if yr[t] >= 2005 and atr[t - 1] > 0]
        drift = np.nanmean([fwd[t] / atr[t - 1] for t in valid])
        posL = 0
        for t in range(start, len(C)):
            a = atr[t - 1]
            if a <= 0 or not np.isfinite(hi[t]):
                continue
            if yr[t] >= 2005:
                r = (C[t] - C[t - 1]) / a
                daily.append(pos * r); daily_lo.append(posL * r); yrs.append(yr[t]); bh.append(r)
            # signal at close t -> position from t+1
            if C[t] > hi[t]:
                if pos != 1 and yr[t] >= 2005 and t < len(C) - N:
                    ev.append(fwd[t] / a - drift)
                pos = 1; posL = 1
            elif C[t] < lo[t]:
                if pos != -1 and yr[t] >= 2005 and t < len(C) - N:
                    ev.append(-(fwd[t] / a - drift))
                pos = -1; posL = 0
    res[g] = (np.array(daily), np.array(daily_lo), np.array(yrs), np.array(ev), n_sym, np.array(bh))


def stats(x):
    if len(x) < 50:
        return "n/a"
    m, s = x.mean(), x.std()
    return f"{m*252:+6.2f} ATR/yr  Sharpe {m/s*np.sqrt(252) if s > 0 else 0:+.2f}"


print(f"Donchian {N}-day stop-and-reverse, daily 2005+, no costs. P&L in ATR units per symbol-year (pooled)")
for g, (dl, dlo, y, ev, n, bh) in res.items():
    print(f"\n{g} ({n} symbols, {len(dl)} symbol-days)")
    print(f"  long/short SAR      : all {stats(dl)} | 2005-14 {stats(dl[y < 2015])} | 2015+ {stats(dl[y >= 2015])}")
    print(f"  long-only (flat)    : all {stats(dlo)} | 2005-14 {stats(dlo[y < 2015])} | 2015+ {stats(dlo[y >= 2015])}")
    print(f"  buy & hold (ref)    : all {stats(bh)} | 2005-14 {stats(bh[y < 2015])} | 2015+ {stats(bh[y >= 2015])}")
    if len(ev):
        print(f"  event: fwd 20d after first breakout in new direction, drift-adjusted, signed: "
              f"n={len(ev)} mean {ev.mean():+.3f} ATR (se {ev.std()/np.sqrt(len(ev)):.3f})")
