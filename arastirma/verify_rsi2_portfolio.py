"""Round 24: Connors RSI(2) as a PROP candidate - same machinery as verify_pullback_portfolio.py (round 20).
Entry: close > SMA200 and RSI(2) < 10 -> buy the close. Exit: close > SMA5 (at the close) or after 10 days.
Protective stop 2 x ATR14 below entry (gap -> fill at the open). 1R = 2 ATR (the stop distance). Cost 0.02R/trade.
Universe: 8 equity index ETFs (highly correlated). 2009+ only (after publication). Open-risk cap = 3 x r.
Baseline: same count per symbol of RANDOM days with close > SMA200, same exits and stop.
Outputs: per-trade R, taken/skipped, CAGR, maxDD, FTMO-like 2-step challenge (static risk; phase 1 +10% then
phase 2 +5%, fail at -10% from start of phase or a -5% day; 365-day limit per phase).
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SYMS = ("SPY", "QQQ", "IWM", "DIA", "EFA", "EWJ", "EWG", "EWU")
COST = 0.02


def rsi(c, n=2):
    d = np.diff(c, prepend=c[0]); up = np.where(d > 0, d, 0.0); dn = np.where(d < 0, -d, 0.0)
    au = np.zeros_like(c); ad = np.zeros_like(c); au[n] = up[1:n + 1].mean(); ad[n] = dn[1:n + 1].mean()
    for i in range(n + 1, len(c)):
        au[i] = (au[i - 1] * (n - 1) + up[i]) / n; ad[i] = (ad[i - 1] * (n - 1) + dn[i]) / n
    rs = np.divide(au, ad, out=np.full_like(au, np.inf), where=ad > 0)
    return 100 - 100 / (1 + rs)


def path(O, L, C, s5, t, R):
    """daily R increments (1R = stop distance R in price) from entry at C[t]"""
    e = C[t]; stop = e - R; inc = []; prev = e
    for j in range(t + 1, min(t + 11, len(C))):
        if O[j] <= stop:
            inc.append((j, (O[j] - prev) / R)); return inc
        if L[j] <= stop:
            inc.append((j, (stop - prev) / R)); return inc
        inc.append((j, (C[j] - prev) / R)); prev = C[j]
        if C[j] > s5[j]:
            return inc
    return inc


trades = {"rsi2": [], "random": []}
for sym in SYMS:
    d = yf.download(sym, start="2007-01-01", interval="1d", progress=False, auto_adjust=True)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna()
    O, Hh, L, C = (d[c].values for c in ("Open", "High", "Low", "Close"))
    dates = d.index; yr = dates.year.values; T = len(C)
    tr = np.maximum(Hh - L, np.maximum(abs(Hh - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = np.convolve(tr, np.ones(14) / 14, mode="full")[:T]
    s200 = np.convolve(C, np.ones(200) / 200, mode="full")[:T]
    s5 = np.convolve(C, np.ones(5) / 5, mode="full")[:T]
    r2 = rsi(C)
    cand = [t for t in range(205, T - 11) if yr[t] >= 2009 and C[t] > s200[t]]
    n = 0; t = 205
    while t < T - 11:
        if yr[t] >= 2009 and C[t] > s200[t] and r2[t] < 10:
            inc = path(O, L, C, s5, t, 2 * atr[t])
            trades["rsi2"].append((dates[t], [(dates[j], r) for j, r in inc])); n += 1
            t = inc[-1][0] + 1
        else:
            t += 1
    rng = np.random.default_rng(sum(map(ord, sym)))
    for t in sorted(rng.choice(cand, size=min(n, len(cand)), replace=False)):
        inc = path(O, L, C, s5, t, 2 * atr[t])
        trades["random"].append((dates[t], [(dates[j], r) for j, r in inc]))

master = pd.DatetimeIndex(sorted({dt for v in trades.values() for _, inc in v for dt, _ in inc} |
                                 {e for v in trades.values() for e, _ in v}))
pos = {dt: i for i, dt in enumerate(master)}


def compile_trades(tl):
    out = []
    for ent, inc in tl:
        idx = np.array([pos[dt] for dt, _ in inc]); dr = np.array([r for _, r in inc]); dr[-1] -= COST
        out.append((pos[ent], idx, dr))
    out.sort(key=lambda x: x[0]); return out


def simulate(ct, r, start=0, end=None, static=False, cap=3.0, target=None, floor=None, maxdays=None):
    end = len(master) if end is None else end
    eq = 1.0; open_tr = []; entries = {}
    for k, (ei, idx, dr) in enumerate(ct):
        if start <= ei < end:
            entries.setdefault(ei, []).append(k)
    peak = 1.0; mdd = 0.0; taken = 0; skipped = 0
    for day in range(start, end):
        base = 1.0 if static else eq
        for k in entries.get(day, []):
            if sum(x[1] for x in open_tr) + r * base <= cap * r * base + 1e-12:
                open_tr.append([k, r * base, 0]); taken += 1
            else:
                skipped += 1
        pnl = 0.0; keep = []
        for tr_ in open_tr:
            k, amt, ptr = tr_; ei, idx, dr = ct[k]
            while ptr < len(idx) and idx[ptr] == day:
                pnl += amt * dr[ptr]; ptr += 1
            tr_[2] = ptr
            if ptr < len(idx):
                keep.append(tr_)
        open_tr = keep; eq += pnl
        if target is not None:
            if eq >= target: return "pass", day
            if eq <= floor or pnl <= -0.05: return "fail", day
            if (master[day] - master[start]).days > maxdays: return "timeout", day
        peak = max(peak, eq); mdd = max(mdd, 1 - eq / peak)
    if target is not None:
        return "timeout", end
    return eq, mdd, taken, skipped


def challenge(ct, r, s):
    o1, d1 = simulate(ct, r, start=s, static=True, target=1.10, floor=0.90, maxdays=365)
    if o1 != "pass" or d1 + 1 >= len(master):
        return o1
    o2, d2 = simulate(ct, r, start=d1 + 1, static=True, target=1.05, floor=0.90, maxdays=365)
    return "pass" if o2 == "pass" else ("fail" if o2 == "fail" else "timeout")


years = (master[-1] - master[0]).days / 365.25
starts = [i for i in range(1, len(master)) if master[i].month != master[i - 1].month and master[i].year <= 2025]
spy = yf.download("SPY", start=str(master[0].date()), interval="1d", progress=False, auto_adjust=True)["Close"].squeeze()
print(f"2009+ ({master[0].date()}..{master[-1].date()}). SPY buy&hold CAGR {(spy.iloc[-1]/spy.iloc[0])**(1/years)-1:+.1%}")
for name in ("rsi2", "random"):
    ct = compile_trades(trades[name])
    allR = np.array([dr.sum() for _, _, dr in ct])
    print(f"\n=== {name} === n={len(ct)} avg net {allR.mean():+.3f}R (se {allR.std()/np.sqrt(len(allR)):.3f}) win {np.mean(allR>0):.0%}")
    for r in (0.005, 0.01, 0.02):
        eq, mdd, tk, sk = simulate(ct, r)
        outc = np.array([challenge(ct, r, s) for s in starts])
        print(f"  risk {r:.1%}/trade (1R=2ATR): CAGR {eq**(1/years)-1:+.1%} maxDD {mdd:.1%} taken {tk} skipped {sk} | "
              f"2-step challenge (n={len(starts)}): pass {np.mean(outc=='pass'):.0%} fail {np.mean(outc=='fail'):.0%} "
              f"timeout {np.mean(outc=='timeout'):.0%}")
