"""Round 20: the only edge that replicated out of sample (first pullback to EMA20 after a Keltner momentum thrust,
LONG side, equity index ETFs; verify_pullback.py) run as a real PORTFOLIO and as an FTMO-style CHALLENGE.
Symbols: 9 index ETFs + 11 country ETFs (highly correlated: same-day signals = one bet). Daily, 2005+.
Trade: fill at min(open, EMA20[p-1]); stop 1 ATR; target 2R; 20-day time exit; cost 0.02R per trade.
Daily mark-to-market of open trades (close to close) so the daily-loss rule can be checked on closes.
Baseline: the SAME number of trades per symbol taken on random trend-state days (close > EMA20, EMA20 rising),
same exits -> what the edge adds in prop terms.
Portfolio: risk r% of equity at entry; open-risk CAP = 3 x r (Brandt's composite-risk idea); signals beyond the cap
are skipped.
Challenge (FTMO-like, static): start at the first trading day of each month 2005-2025; target +10%; fail if equity
<= 90% of start or a day's close-to-close loss >= 5% of start; 365 calendar-day limit (FTMO has none, so 'timeout'
is reported separately). Risk is r% of the INITIAL balance (static sizing).
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SYMS = "SPY QQQ IWM DIA EEM EFA EWJ EWG MDY EWU EWC EWA EWH EWT EWY EWW EWS EWL EWQ EWI".split()
COST = 0.02


def ema(x, n):
    a = 2 / (n + 1); out = np.empty_like(x); out[0] = x[0]
    for i in range(1, len(x)):
        out[i] = a * x[i] + (1 - a) * out[i - 1]
    return out


def path(O, Hh, L, C, t, fill, a, k=2.0, maxd=20):
    """daily R increments from fill day t to exit; returns list of (index, dR)"""
    stop, tgt = fill - a, fill + k * a
    inc = []
    if C[t] <= stop:
        return [(t, -1.0)]
    inc.append((t, (C[t] - fill) / a)); prev = C[t]
    for j in range(t + 1, min(t + 1 + maxd, len(C))):
        if O[j] <= stop:
            inc.append((j, (O[j] - prev) / a)); return inc
        if L[j] <= stop:
            inc.append((j, (stop - prev) / a)); return inc
        if Hh[j] >= tgt:
            inc.append((j, (max(O[j], tgt) if O[j] > tgt else tgt) / a - prev / a)); return inc
        inc.append((j, (C[j] - prev) / a)); prev = C[j]
    return inc


trades = {"pullback": [], "random": []}   # each: (entry_date, [(date, dR)...])
for sym in SYMS:
    d = yf.download(sym, start="2004-01-01", interval="1d", progress=False, auto_adjust=True)
    if d is None or len(d) < 400:
        continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna(); d = d[(d["High"] > 0) & (d["Low"] > 0)]
    O, Hh, L, C = (d[c].values for c in ("Open", "High", "Low", "Close"))
    dates = d.index; yr = dates.year.values; T = len(C)
    tr = np.maximum(Hh - L, np.maximum(abs(Hh - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = np.convolve(tr, np.ones(20) / 20, mode="full")[:T]
    e = ema(C, 20)
    last_m = -99; npb = 0; cand = []
    for t in range(30, T - 21):
        if yr[t] < 2005 or atr[t - 1] <= 0:
            continue
        if C[t] > e[t] and e[t] > e[t - 5]:
            cand.append(t)
        if C[t] <= e[t] + 2.25 * atr[t] or t - last_m < 20:
            continue
        last_m = t
        for p in range(t + 3, min(t + 21, T - 21)):
            if C[p - 1] < e[p - 1] - 2.25 * atr[p - 1]:
                break
            lvl = e[p - 1]
            if L[p] > lvl:
                continue
            fill = min(O[p], lvl)
            inc = path(O, Hh, L, C, p, fill, atr[p - 1])
            trades["pullback"].append((dates[p], [(dates[j], r) for j, r in inc])); npb += 1
            break
    rng = np.random.default_rng(sum(map(ord, sym)))
    for t in rng.choice(cand, size=min(npb, len(cand)), replace=False):
        inc = path(O, Hh, L, C, t, C[t], atr[t - 1])
        trades["random"].append((dates[t], [(dates[j], r) for j, r in inc]))

master = pd.DatetimeIndex(sorted({dt for v in trades.values() for _, inc in v for dt, _ in inc} |
                                 {e for v in trades.values() for e, _ in v}))
pos = {dt: i for i, dt in enumerate(master)}


def compile_trades(tl):
    out = []
    for ent, inc in tl:
        idx = np.array([pos[dt] for dt, _ in inc]); dr = np.array([r for _, r in inc])
        dr[-1] -= COST
        out.append((pos[ent], idx, dr))
    out.sort(key=lambda x: x[0])
    return out


def simulate(ct, r, start=0, end=None, static=False, cap=3.0, challenge=False):
    end = len(master) if end is None else end
    eq = 1.0; open_tr = []; entries = {}
    for k, (ei, idx, dr) in enumerate(ct):
        if start <= ei < end:
            entries.setdefault(ei, []).append(k)
    curve = []; peak = 1.0; mdd = 0.0; taken = []; skipped = 0
    for day in range(start, end):
        base = 1.0 if static else eq
        for k in entries.get(day, []):
            open_risk = sum(x[1] for x in open_tr)
            amt = r * base
            if open_risk + amt <= cap * r * base + 1e-12:
                open_tr.append([k, amt, 0]); taken.append(k)
            else:
                skipped += 1
        pnl = 0.0; keep = []
        for tr_ in open_tr:
            k, amt, ptr = tr_
            ei, idx, dr = ct[k]
            while ptr < len(idx) and idx[ptr] == day:
                pnl += amt * dr[ptr]; ptr += 1
            tr_[2] = ptr
            if ptr < len(idx):
                keep.append(tr_)
        open_tr = keep
        eq += pnl
        if challenge:
            if eq >= 1.10:
                return "pass", day - start
            if eq <= 0.90 or pnl <= -0.05:
                return "fail", day - start
            if (master[day] - master[start]).days > 365:
                return "timeout", day - start
        peak = max(peak, eq); mdd = max(mdd, 1 - eq / peak); curve.append(eq)
    if challenge:
        return "timeout", end - start
    return np.array(curve), mdd, taken, skipped


print(f"trades: pullback {len(trades['pullback'])}, random baseline {len(trades['random'])}; "
      f"{master[0].date()} .. {master[-1].date()}")
years = (master[-1] - master[0]).days / 365.25
month_starts = [i for i in range(1, len(master)) if master[i].month != master[i - 1].month and master[i].year <= 2025]
for name in ("pullback", "random"):
    ct = compile_trades(trades[name])
    print(f"\n=== {name} ===  avg net R/trade {np.mean([dr.sum() for _, _, dr in ct]):+.3f}")
    for r in (0.005, 0.01, 0.02):
        curve, mdd, taken, skipped = simulate(ct, r)
        cagr = curve[-1] ** (1 / years) - 1
        tR = np.array([ct[k][2].sum() for k in taken])
        c2, m2, t2, s2 = simulate(ct, r, cap=1000)
        print(f"  [diag r={r:.1%}] taken {len(taken)} skipped {skipped} | avg R taken {tR.mean():+.3f} | "
              f"no-cap: CAGR {c2[-1]**(1/years)-1:+.1%} maxDD {m2:.1%}")
        res = [simulate(ct, r, start=s, static=True, challenge=True) for s in month_starts]
        outc = np.array([x[0] for x in res]); days = np.array([x[1] for x in res])
        p_pass = np.mean(outc == "pass"); p_fail = np.mean(outc == "fail"); p_to = np.mean(outc == "timeout")
        med = np.median(days[outc == "pass"]) if p_pass > 0 else float("nan")
        print(f"  risk {r:.1%}: CAGR {cagr:+.1%} maxDD {mdd:.1%} | challenge (n={len(res)} starts): "
              f"pass {p_pass:.0%} fail {p_fail:.0%} timeout(1y) {p_to:.0%} | median trading days to pass {med:.0f}")
