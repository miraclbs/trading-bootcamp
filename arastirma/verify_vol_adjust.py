"""Round 30: Rob Carver on Top Traders Unplugged #386 "Position sizing when markets break" (OVh3f8hmchA).
Claims tested:
 (1) Continuous volatility adjustment (cutting contracts as vol rises) kept Carver's silver loss small in the
     late-Jan 2026 silver crash; a CTA without vol adjustment gave back most of its month (+72% -> +27%).
     -> Compare 12m TSMOM variants: A monthly vol-scaled (our baseline), B daily vol-scaled (continuous, 10%
        buffer), C fixed shares from entry (size by vol at entry, then never resized: position grows in a
        parabolic move), D fixed shares with equal notional (no vol sizing at all).
        Report Sharpe, maxDD, worst day measured in the portfolio's own daily std, share of days < -4 std,
        kurtosis, and the FTMO-like 2-step pass / fail at equal realised vol.
 (2) "Volatility is quite predictable (next month vs last month R^2 ~0.35), correlation less (~0.2-0.25), means
     not at all." -> per-asset monthly regressions, averaged.
Universe = verify_tsmom.py (19 ETF/FX, daily, 2005+). Costs 5 bp x turnover.
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
cols = list(P.columns)
N = len(cols)
TARGET, FLOOR = 0.10, 0.05
vol60 = R.rolling(60).std() * np.sqrt(252)
vol20 = R.rolling(20).std() * np.sqrt(252)            # faster estimate for daily re-scaling
sig = np.sign(P / P.shift(252) - 1)
month_end = set(P.index.to_series().groupby(P.index.to_period("M")).max().values)


def run(variant):
    W = pd.DataFrame(0.0, index=P.index, columns=cols)
    w = pd.Series(0.0, index=cols)
    entry_px = pd.Series(np.nan, index=cols)
    entry_w = pd.Series(0.0, index=cols)
    cur_sig = pd.Series(0.0, index=cols)
    for dt in P.index:
        s_today = sig.loc[dt].fillna(0.0)
        if variant == "A":                                    # monthly vol-scaled rebalance
            if dt in month_end:
                w = s_today * (TARGET / np.maximum(vol60.loc[dt].fillna(np.inf), FLOOR)) / N
        elif variant == "B":                                  # signal monthly, size re-scaled daily (10% buffer)
            if dt in month_end:
                cur_sig = s_today
            v = np.maximum(np.maximum(vol20.loc[dt], vol60.loc[dt]).fillna(np.inf), FLOOR)
            ideal = cur_sig * (TARGET / v) / N
            move = (ideal - w).abs() > 0.10 * ideal.abs()
            w = w.where(~move, ideal)
        else:                                                 # C / D: fixed shares from entry
            if dt in month_end:
                for c in cols:
                    if s_today[c] != cur_sig[c]:              # new position only when the sign flips
                        cur_sig[c] = s_today[c]
                        entry_px[c] = P.at[dt, c]
                        if variant == "C":
                            sz = TARGET / max(vol60.at[dt, c], FLOOR) if not np.isnan(vol60.at[dt, c]) else 0.0
                        else:                                 # D: equal notional, sized so avg vol ~ A
                            sz = 1.0
                        entry_w[c] = s_today[c] * sz / N
            w = entry_w * (P.loc[dt] / entry_px).fillna(1.0)  # notional drifts with price
        W.loc[dt] = w
    gross = (W.shift(1) * R).sum(axis=1)
    net = gross - 0.0005 * W.diff().abs().sum(axis=1)
    return net[net.index >= "2005-01-01"], W


def stats(r):
    a = r.mean() * 252; v = r.std() * np.sqrt(252)
    eq = (1 + r).cumprod(); mdd = (1 - eq / eq.cummax()).max()
    z = (r - r.mean()) / r.std()
    return a, v, a / v, mdd, z.min(), (z < -4).mean() * 1e4, r.kurt()


def challenge_path(r, ann_vol):
    scale = ann_vol / (r.std() * np.sqrt(252)); x = (r * scale).values; idx = r.index
    starts = [i for i in range(1, len(idx)) if idx[i].month != idx[i - 1].month and idx[i].year <= 2023]
    out = []
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
    o = np.array(out)
    return np.mean(o == "pass"), np.mean(o == "fail")


print("(1) 12-month TSMOM, 19 markets, 2005+. Variants differ ONLY in how size is managed after the signal.")
print("    ann.ret / vol / Sharpe / maxDD | worst day (in own daily std) | days < -4 std per 10k | kurtosis")
res = {}
names = {"A": "A monthly vol-scaled", "B": "B daily vol-scaled ", "C": "C fixed shares, vol at entry",
         "D": "D fixed shares, equal notional"}
for v in "ABCD":
    r, W = run(v)
    res[v] = (r, W)
    a, vv, sh, mdd, wz, n4, k = stats(r)
    print(f"  {names[v]:32s}: {a:+.1%} / {vv:.1%} / {sh:+.2f} / {mdd:.0%} | {wz:+.1f} | {n4:.0f} | {k:.1f}")
print("\n    Same at equal realised vol (each path scaled to 10% annual): maxDD and worst day")
for v in "ABCD":
    r = res[v][0]; r10 = r * (0.10 / (r.std() * np.sqrt(252)))
    eq = (1 + r10).cumprod()
    roll = r10.rolling(21).std() * np.sqrt(252)
    print(f"  {names[v]:32s}: maxDD {(1 - eq / eq.cummax()).max():.0%} | worst day {r10.min():+.2%} | "
          f"worst 5d {r10.rolling(5).sum().min():+.1%} | realised 1m vol 95th pct {roll.quantile(.95):.0%}")
print("\n    FTMO-like 2-step at 8% annual vol (pass / fail):")
for v in "ABCD":
    p, f = challenge_path(res[v][0], 0.08)
    print(f"  {names[v]:32s}: pass {p:.0%} fail {f:.0%}")

print("\n    Silver episode (SLV), Jan-Feb 2026: SLV daily moves and each variant's SLV P&L (bp of capital)")
slv = R["SLV"]
win = (slv.index >= "2026-01-02") & (slv.index <= "2026-02-27")
big = slv[win].abs().sort_values(ascending=False).head(5)
print("  largest SLV days:", ", ".join(f"{d.date()} {slv[d]:+.1%}" for d in big.index))
for v in "ABCD":
    W = res[v][1]
    pnl = (W["SLV"].shift(1) * slv)[win]
    jan = pnl[pnl.index < "2026-02-01"]
    print(f"  {names[v]:32s}: SLV weight on 2026-01-02 {W['SLV'].get(pd.Timestamp('2026-01-02'), np.nan):+.2f}, "
          f"on worst day-1 {W['SLV'].shift(1)[slv[win].idxmin()]:+.2f} | Jan P&L {jan.sum()*1e4:+.0f} bp, "
          f"worst day {pnl.min()*1e4:+.0f} bp, Jan peak-to-end {((jan.cumsum().max() - jan.sum()))*1e4:.0f} bp")

print("\n(2) Predictability, per asset, averaged (R^2 of next month on last month):")
mv = R.groupby(R.index.to_period("M")).std() * np.sqrt(252)
mr = R.groupby(R.index.to_period("M")).sum()
r2v, r2m, r2lv = [], [], []
for c in cols:
    x = mv[c].dropna()
    if len(x) > 60:
        r2v.append(np.corrcoef(x.values[:-1], x.values[1:])[0, 1] ** 2)
        lx = np.log(x[x > 0]); r2lv.append(np.corrcoef(lx.values[:-1], lx.values[1:])[0, 1] ** 2)
    y = mr[c].dropna()
    if len(y) > 60:
        r2m.append(np.corrcoef(y.values[:-1], y.values[1:])[0, 1] ** 2)
print(f"  monthly volatility : mean R^2 {np.mean(r2v):.2f} (log vol {np.mean(r2lv):.2f}); range {min(r2v):.2f}-{max(r2v):.2f}")
print(f"  monthly return     : mean R^2 {np.mean(r2m):.3f}")
mc = {}
for per, g in R.groupby(R.index.to_period("M")):
    if len(g) >= 15:
        mc[per] = g.corr()
pers = sorted(mc)
r2c = []
for i, a in enumerate(cols):
    for b in cols[i + 1:]:
        s = pd.Series([mc[p].at[a, b] for p in pers]).dropna()
        if len(s) > 60:
            r2c.append(np.corrcoef(s.values[:-1], s.values[1:])[0, 1] ** 2)
print(f"  monthly pairwise correlation: mean R^2 {np.mean(r2c):.2f} over {len(r2c)} pairs")
# 6-month correlation windows (Carver's suggested look-back)
h = R.groupby([R.index.year, (R.index.month - 1) // 6]).corr()
keys = sorted(set((a, b) for a, b, _ in h.index))
r2c6 = []
for i, a in enumerate(cols):
    for b in cols[i + 1:]:
        s = pd.Series([h.loc[(k[0], k[1], a), b] for k in keys]).dropna()
        if len(s) > 15:
            r2c6.append(np.corrcoef(s.values[:-1], s.values[1:])[0, 1] ** 2)
print(f"  half-year pairwise correlation: mean R^2 {np.mean(r2c6):.2f}")
