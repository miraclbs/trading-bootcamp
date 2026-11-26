"""Round 26: Clenow's benchmark (Top Traders Unplugged grIHdA5pMhE): '12-month return rule' - long if price is above
its level 12 months ago, short otherwise, on a broad diversified universe with volatility position sizing.
Academic name: time-series momentum (Moskowitz, Ooi & Pedersen 2012). 'If you can't beat this model, you might have a
problem.' Also tests Jerry Parker's point (Real Vision B894C3Z6Pq0) that SHORT look-backs stopped working from the
late 1990s and longer ones are needed (compare 1-month and 3-month look-backs).
Universe (ETF/FX proxies, daily 2005+): equities SPY EFA EEM EWJ | bonds TLT IEF | commodities GLD SLV USO DBA DBC
CPER UNG | FX EURUSD GBPUSD USDJPY AUDUSD USDCAD USDCHF (spot, no carry).
Monthly rebalance. Weight_i = sign(lookback return) * (target_asset_vol / max(sigma_60d, vol_floor)) / N.
Vol floor (Clenow/Parker lesson after the 2015 CHF peg removal) = 5% annualised. Cost 5 bp x turnover.
Portfolio scaled to ~10% annual vol ex ante (each asset 10%/sqrt-ish of N ignored -> report realised vol, then
rescale for the prop test).
Prop test: FTMO-like 2-step on the daily portfolio path scaled to a chosen annual vol (static, % of start).
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
UNIV = {"EQ": ["SPY", "EFA", "EEM", "EWJ"], "BOND": ["TLT", "IEF"],
        "CMD": ["GLD", "SLV", "USO", "DBA", "DBC", "CPER", "UNG"],
        "FX": ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X", "USDCHF=X"]}
px = {}
for cls, syms in UNIV.items():
    for s in syms:
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
cls_of = {s: c for c, ss in UNIV.items() for s in ss if s in P.columns}


def tsmom(lookback_days, subset=None, target=0.10, floor=0.05):
    cols = [c for c in P.columns if subset is None or cls_of[c] in subset]
    vol = R[cols].rolling(60).std() * np.sqrt(252)
    sig = np.sign(P[cols] / P[cols].shift(lookback_days) - 1)
    month_end = P.index.to_series().groupby(P.index.to_period("M")).max().values
    W = pd.DataFrame(np.nan, index=P.index, columns=cols)
    for dt in month_end:
        if dt not in W.index:
            continue
        n = sig.loc[dt].notna().sum()
        if n == 0:
            continue
        W.loc[dt] = sig.loc[dt] * (target / np.maximum(vol.loc[dt], floor)) / n
    W = W.ffill().fillna(0.0)
    gross = (W.shift(1) * R[cols]).sum(axis=1)
    turnover = W.diff().abs().sum(axis=1)
    net = gross - 0.0005 * turnover
    return net[net.index >= "2005-01-01"]


LOOKS = (20, 40, 80, 160, 320)


def sharpe(r):
    return r.mean() / r.std() * np.sqrt(252) if r.std() > 0 else np.nan


# ---- Round 29: Rob Carver's claims (Desire To TRADE lMY9n1c3tFU) ----
# (1) 'Going from one market to 100 markets raises risk-adjusted performance by a factor of nearly five.'
print("(1) Diversification: 12-month TSMOM Sharpe, single assets vs portfolio (2005+, 5bp turnover cost)")
singles = {c: sharpe(tsmom(252, None if False else None) if False else tsmom_single(c)) for c in []} if False else {}
cols = list(P.columns)
def tsmom_cols(cols, lb=252, mode="sign"):
    vol = R[cols].rolling(60).std() * np.sqrt(252)
    if mode == "sign":
        f = np.sign(P[cols] / P[cols].shift(lb) - 1)
    else:   # Carver-style continuous breakout forecast averaged over several look-backs, in [-1, 1]
        fs = []
        for n in LOOKS:
            hi = P[cols].rolling(n).max(); lo = P[cols].rolling(n).min(); mid = (hi + lo) / 2
            fs.append(((P[cols] - mid) / (hi - lo).replace(0, np.nan)).clip(-0.5, 0.5) * 2)
        f = sum(fs) / len(fs)
    W = pd.DataFrame(np.nan, index=P.index, columns=cols)
    me = P.index.to_series().groupby(P.index.to_period("M")).max().values if mode == "sign" else P.index
    if mode == "sign":
        for dt in me:
            n = f.loc[dt].notna().sum()
            if n: W.loc[dt] = f.loc[dt] * (0.10 / np.maximum(vol.loc[dt], 0.05)) / n
        W = W.ffill()
    else:
        n = f.notna().sum(axis=1).replace(0, np.nan)
        W = f.mul(0.10 / np.maximum(vol, 0.05)).div(n, axis=0)
        W = W.where(W.index.to_series().dt.dayofweek.eq(4)).ffill()   # weekly rebalance (Fridays)
    W = W.fillna(0.0)
    turn = W.diff().abs().sum(axis=1)
    net = (W.shift(1) * R[cols]).sum(axis=1) - 0.0005 * turn
    net = net[net.index >= "2005-01-01"]
    return net, turn[turn.index >= "2005-01-01"].mean() * 252
single_sh = {c: sharpe(tsmom_cols([c])[0]) for c in cols}
s = pd.Series(single_sh).sort_values()
print("  single-asset Sharpes:", " ".join(f"{k.replace('=X','')} {v:+.2f}" for k, v in s.items()))
port, _ = tsmom_cols(cols)
print(f"  average single-asset Sharpe {s.mean():+.2f} (median {s.median():+.2f}) | equal-risk portfolio of {len(cols)}: {sharpe(port):+.2f} "
      f"-> ratio {sharpe(port)/s.mean():.1f}x")
rng = np.random.default_rng(0)
print(f'  markets with data: {len(cols)}')
for k in (1, 3, 5, 10, len(cols)):
    v = [sharpe(tsmom_cols(list(rng.choice(cols, k, replace=False)))[0]) for _ in range(12 if k < len(cols) else 1)]
    print(f"  random subsets of {k:2d} markets: mean portfolio Sharpe {np.nanmean(v):+.2f}")

# (2) continuous breakout forecast vs binary sign
print("\n(2) Signal shape (all 19 markets): binary 12-month sign (monthly) vs Carver-style continuous breakout (weekly)")
for mode in ("sign", "cont"):
    r, t = tsmom_cols(cols, mode=mode)
    print(f"  {mode:5s}: Sharpe 2005+ {sharpe(r):+.2f} | 2015+ {sharpe(r[r.index >= '2015']):+.2f} | annual turnover {t:.1f}x")

# (3) 'don't cherry-pick markets': is the dispersion of single-asset Sharpes larger than noise?
yrs = (port.index[-1] - port.index[0]).days / 365.25
print(f"\n(3) Standard error of a single-asset Sharpe over {yrs:.0f} years ~ {1/np.sqrt(yrs):.2f}. "
      f"Observed std of single-asset Sharpes: {s.std():.2f}.")

print("\n(2b) Same continuous forecast, LONG look-backs only (separating signal shape from look-back length):")
for looks in ((160, 320), (250,), (320,)):
    LOOKS = looks
    r, t = tsmom_cols(cols, mode="cont")
    print(f"  continuous, look-backs {looks}: Sharpe 2005+ {sharpe(r):+.2f} | 2015+ {sharpe(r[r.index >= '2015']):+.2f} | turnover {t:.1f}x")
