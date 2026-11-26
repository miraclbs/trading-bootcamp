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


def stats(r):
    a = r.mean() * 252; v = r.std() * np.sqrt(252)
    eq = (1 + r).cumprod(); mdd = (1 - eq / eq.cummax()).max()
    return a, v, a / v if v > 0 else np.nan, mdd


def challenge_path(r, ann_vol):
    """2-step pass rate on the daily path, scaled to ann_vol, static % of start, monthly starts"""
    scale = ann_vol / (r.std() * np.sqrt(252)); x = (r * scale).values; idx = r.index
    starts = [i for i in range(1, len(idx)) if idx[i].month != idx[i - 1].month and idx[i].year <= 2023]
    out = []; days = []
    for s in starts:
        res = None; i = s
        for target in (0.10, 0.05):
            eq = 0.0; t0 = i
            while i < len(x):
                eq += x[i]
                if x[i] <= -0.05 or eq <= -0.10: res = "fail"; break
                if eq >= target: break
                if (idx[i] - idx[t0]).days > 1095: res = "timeout"; break
                i += 1
            if res: break
            if i >= len(x): res = "timeout"; break
            i += 1
        out.append(res or "pass")
        if res is None: days.append((idx[min(i, len(idx) - 1)] - idx[s]).days)
    o = np.array(out)
    return np.mean(o == "pass"), np.mean(o == "fail"), (np.median(days) if days else np.nan)




# ---- Round 27: blend 12-month TSMOM with SPY buy & hold, equal RISK weights, prop test ----
r12 = tsmom(252)
spy = R["SPY"].reindex(r12.index).fillna(0.0)
ts = r12 * (0.10 / (r12.std() * np.sqrt(252)))          # TSMOM scaled to 10% vol
sp = spy * (0.10 / (spy.std() * np.sqrt(252)))           # SPY scaled to 10% vol (ex post, illustrative)
print("Blends (each leg scaled to 10% vol ex post; weights are risk weights). 2005+")
for w in (0.0, 0.3, 0.5, 0.7, 1.0):
    b = w * sp + (1 - w) * ts
    a, v, sh, mdd = stats(b)
    a2, v2, sh2, mdd2 = stats(b[b.index >= "2015"])
    print(f"  SPY weight {w:.0%}: return {a:+.1%} vol {v:.1%} Sharpe {sh:+.2f} maxDD {mdd:.0%} | 2015+ Sharpe {sh2:+.2f} maxDD {mdd2:.0%}")
print("\nProp test, 2-step FTMO-like (no time limit approximated by 3 years per phase), path scaled to annual vol:")
for w in (0.0, 0.5):
    b = w * sp + (1 - w) * ts
    for av in (0.06, 0.08):
        p, f, md = challenge_path(b, av)
        print(f"  SPY weight {w:.0%}, ann vol {av:.0%}: pass {p:.0%} fail {f:.0%} | median days {md:.0f}")
