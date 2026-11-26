"""Round 58: last-half-hour reversal (README #32, verify_close_reversal.py, found post hoc on 2026-11-22).
Rule (unchanged): at the 15:30 ET bar open, s = sign(price - previous day's close); trade -s from the 15:30 open to the
16:00 close. Net of $0.02/share round-trip cost.
PART 1 (in-sample robustness, today): is the effect concentrated in a VIX regime (dealer-gamma mechanism, Baltussen et
 al. 2021 predicts reversals when dealers are long gamma, typically calm markets)? Share of positive months?
PART 2 (PRE-REGISTERED FORWARD TEST): only days on/after FORWARD_START are used.
 Revised on 2026-11-23, BEFORE any forward data was seen: the first version decided after 60 days, but with the in-sample
 effect (mean 1.77bp, sd 21.7bp) the expected t after 60 days is only 0.63, so a real effect would pass t >= 1 only
 36% of the time. Power by sample size (expected t / P(pass | real) / P(pass | none)):
   60 days 0.63 / 36% / 16% | 250 days 1.29 / 61% / 16% | 500 days 1.82 / 79% / 16%.
 Decision rules fixed in advance:
   INTERIM checks at >= 60 and >= 250 trading days: DROP only if SPY net t <= -1.0 (a real effect would be wrongly
     dropped at most ~5% of the time). Otherwise keep collecting.
   FINAL decision at >= 500 trading days (~Oct-Nov 2028): KEEP if SPY net mean > 0 with t >= 1.0 AND at least 2 of
     {SPY, QQQ, IWM} have a positive net mean; otherwise DROP (move README #32 to the myths list).
 No parameter may be changed after seeing forward data.
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
FORWARD_START = pd.Timestamp("2026-11-23")
SYMS = ("SPY", "QQQ", "IWM")


def daily_trades(sym):
    d = yf.download(sym, period="730d", interval="1h", progress=False, auto_adjust=False, prepost=False)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna(); idx = d.index.tz_convert("America/New_York")
    O, C = d["Open"].values, d["Close"].values
    days = {}
    for i, ts in enumerate(idx):
        if (9, 30) <= (ts.hour, ts.minute) and ts.hour < 16:
            days.setdefault(ts.date(), []).append(i)
    dl = [k for k in sorted(days) if len(days[k]) == 7 and idx[days[k][6]].hour == 15]
    out = []; prev = None
    for k in dl:
        b = days[k]
        if prev is not None:
            s = np.sign(O[b[6]] - prev)
            x = -s * (C[b[6]] - O[b[6]]) / O[b[6]] * 1e4 - 0.02 / C[b[6]] * 1e4
            out.append((pd.Timestamp(k), x))
        prev = C[b[6]]
    return pd.DataFrame(out, columns=["date", "bp"]).set_index("date")


vix = yf.download("^VIX", period="3y", interval="1d", progress=False, auto_adjust=True)
if hasattr(vix.columns, "levels"):
    vix.columns = vix.columns.get_level_values(0)
vix_prev = vix["Close"].shift(1); vix_prev.index = vix_prev.index.tz_localize(None).normalize()

print("PART 1: in-sample robustness (all available 1h history)")
for s in SYMS:
    t = daily_trades(s)
    t = t[t.index < FORWARD_START]
    t["vix"] = vix_prev.reindex(t.index).values
    t = t.dropna()
    q1, q2 = t.vix.quantile([1 / 3, 2 / 3])
    cells = []
    for lab, m in (("low VIX", t.vix <= q1), ("mid", (t.vix > q1) & (t.vix <= q2)), ("high VIX", t.vix > q2)):
        x = t.bp[m]
        cells.append(f"{lab}: {x.mean():+.2f}bp (t {x.mean() / x.std() * np.sqrt(len(x)):+.1f})")
    mon = t.bp.groupby(t.index.to_period("M")).mean()
    print(f"   {s}: {len(t)} days, mean {t.bp.mean():+.2f}bp | " + " | ".join(cells) +
          f" | positive months {np.mean(mon > 0):.0%} of {len(mon)} | VIX terciles {q1:.1f}/{q2:.1f}")

print(f"\nPART 2: forward test from {FORWARD_START.date()} (pre-registered rule in the docstring)")
res = {}
for s in SYMS:
    t = daily_trades(s)
    f = t[t.index >= FORWARD_START].bp
    if len(f) < 2:
        print(f"   {s}: {len(f)} forward days so far - run again after >= 60 trading days"); continue
    tstat = f.mean() / f.std() * np.sqrt(len(f))
    res[s] = (f.mean(), tstat, len(f))
    print(f"   {s}: n={len(f)} | net mean {f.mean():+.2f}bp | t {tstat:+.2f} | cumulative {f.sum():+.0f}bp")
if res and "SPY" in res:
    n_min = min(v[2] for v in res.values())
    spy_mean, spy_t, _ = res["SPY"]
    if n_min >= 500:
        keep = spy_mean > 0 and spy_t >= 1.0 and sum(v[0] > 0 for v in res.values()) >= 2
        print("   FINAL DECISION:", "KEEP the hypothesis" if keep else "DROP the hypothesis")
    elif n_min >= 60:
        print("   INTERIM CHECK:", "DROP (SPY t <= -1)" if spy_t <= -1.0 else
              f"continue collecting ({n_min} of 500 days; next check at 250, final at 500)")
    else:
        print(f"   {n_min} forward days - first interim check at 60")
