"""Round 25: can DIVERSIFICATION across uncorrelated markets reach the prop yardstick (>= 10-15 R/yr, 09 §2)?
Sleeves built only from rules this knowledge base found positive per trade:
  EQ   : Connors RSI(2) long on SPY, QQQ (stop 2 ATR, exit close > SMA5 / 10 days)       [12, round 24]
  CMD  : 20-day close breakout long/short on commodity ETFs, Brandt 3-day trailing stop    [03, rounds 17-18]
  RATES: same breakout on TLT, IEF, GLD, 10-day-low trailing stop
  FX   : same breakout on 6 major pairs, 10-day-low trailing stop
Initial stop 1 ATR for breakout sleeves (1R = 1 ATR); 1R = 2 ATR for RSI(2). Gaps fill at the open. One open trade
per symbol. Cost 0.02 R per trade (FX 0.05 R). 2009+.
Portfolio: risk r per trade (of equity; static for challenges); open-risk caps: 2r per sleeve, 6r total.
Outputs: per-sleeve trades/yr, mean R, R/yr; monthly-R correlations between sleeves; portfolio CAGR / maxDD; FTMO-like
2-step challenge (phase 1 +10%, phase 2 +5%, -10% max loss per phase, -5% day, 365-day limit per phase).
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SLEEVES = {
    "EQ": ("rsi2", ["SPY", "QQQ"], 0.02),
    "CMD": ("brk_B", ["GLD", "SLV", "USO", "DBA", "DBC", "CPER", "PPLT", "UNG"], 0.02),
    "RATES": ("brk_C", ["TLT", "IEF"], 0.02),
    "FX": ("brk_C", ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X", "USDCHF=X"], 0.05),
}
# GLD is in CMD; keep RATES = bonds only to avoid duplicate gold exposure


def rsi(c, n=2):
    d = np.diff(c, prepend=c[0]); up = np.where(d > 0, d, 0.0); dn = np.where(d < 0, -d, 0.0)
    au = np.zeros_like(c); ad = np.zeros_like(c); au[n] = up[1:n + 1].mean(); ad[n] = dn[1:n + 1].mean()
    for i in range(n + 1, len(c)):
        au[i] = (au[i - 1] * (n - 1) + up[i]) / n; ad[i] = (ad[i - 1] * (n - 1) + dn[i]) / n
    rs = np.divide(au, ad, out=np.full_like(au, np.inf), where=ad > 0)
    return 100 - 100 / (1 + rs)


def path_rsi2(O, L, C, s5, t, R):
    e = C[t]; stop = e - R; inc = []; prev = e
    for j in range(t + 1, min(t + 11, len(C))):
        if O[j] <= stop: inc.append((j, (O[j] - prev) / R)); return inc
        if L[j] <= stop: inc.append((j, (stop - prev) / R)); return inc
        inc.append((j, (C[j] - prev) / R)); prev = C[j]
        if C[j] > s5[j]: return inc
    return inc


def path_trail(O, Hh, L, C, t, side, a, method, maxd=120):
    E = C[t]; stop = E - side * a; hd = t; inc = []; prev = E
    for j in range(t + 1, min(t + 1 + maxd, len(C))):
        if side == 1:
            if O[j] <= stop: inc.append((j, (O[j] - prev) / a)); return inc
            if L[j] <= stop: inc.append((j, (stop - prev) / a)); return inc
        else:
            if O[j] >= stop: inc.append((j, -(O[j] - prev) / a)); return inc
            if Hh[j] >= stop: inc.append((j, -(stop - prev) / a)); return inc
        inc.append((j, side * (C[j] - prev) / a)); prev = C[j]
        if method == "B":
            if side == 1:
                if Hh[j] > Hh[hd]: hd = j
                elif C[j] < L[hd]: stop = max(stop, L[j] - 0.01 * a)
            else:
                if L[j] < L[hd]: hd = j
                elif C[j] > Hh[hd]: stop = min(stop, Hh[j] + 0.01 * a)
        elif j - t >= 2:
            lo = max(t + 1, j - 9)
            stop = max(stop, L[lo:j + 1].min()) if side == 1 else min(stop, Hh[lo:j + 1].max())
    return inc


trades = []   # (sleeve, entry_date, [(date, dR)])
for sl, (kind, syms, cost) in SLEEVES.items():
    for sym in syms:
        d = yf.download(sym, start="2007-01-01", interval="1d", progress=False, auto_adjust=True)
        if d is None or len(d) < 500:
            print("skip", sym); continue
        if hasattr(d.columns, "levels"):
            d.columns = d.columns.get_level_values(0)
        d = d.dropna(); d = d[(d["High"] > 0) & (d["Low"] > 0) & (d["High"] >= d["Low"])]
        O, Hh, L, C = (d[c].values for c in ("Open", "High", "Low", "Close"))
        dates = d.index.tz_localize(None) if d.index.tz is not None else d.index
        dates = dates.normalize(); yr = dates.year.values; T = len(C)
        tr = np.maximum(Hh - L, np.maximum(abs(Hh - np.roll(C, 1)), abs(L - np.roll(C, 1))))
        atr = np.convolve(tr, np.ones(14) / 14, mode="full")[:T]
        s200 = np.convolve(C, np.ones(200) / 200, mode="full")[:T]
        s5 = np.convolve(C, np.ones(5) / 5, mode="full")[:T]
        r2 = rsi(C)
        t = 205
        while t < T - 2:
            if yr[t] < 2009 or atr[t] <= 0:
                t += 1; continue
            inc = None
            if kind == "rsi2":
                if C[t] > s200[t] and r2[t] < 10:
                    inc = path_rsi2(O, L, C, s5, t, 2 * atr[t])
            else:
                hi, lo = Hh[t - 20:t].max(), L[t - 20:t].min()
                side = 1 if C[t] > hi else (-1 if C[t] < lo else 0)
                if side:
                    inc = path_trail(O, Hh, L, C, t, side, atr[t], kind[-1])
            if inc:
                inc = [(dates[j], r) for j, r in inc]
                inc[-1] = (inc[-1][0], inc[-1][1] - cost)
                trades.append((sl, dates[t], inc))
                t = d.index.get_loc(d.index[[k for k in range(T) if dates[k] == inc[-1][0]][0]]) + 1
            else:
                t += 1

master = pd.DatetimeIndex(sorted({dt for _, _, inc in trades for dt, _ in inc} | {e for _, e, _ in trades}))
pos = {dt: i for i, dt in enumerate(master)}
ct = []
for sl, ent, inc in trades:
    ct.append((sl, pos[ent], np.array([pos[dt] for dt, _ in inc]), np.array([r for _, r in inc])))
ct.sort(key=lambda x: x[1])
years = (master[-1] - master[0]).days / 365.25

print(f"2009+ ({master[0].date()}..{master[-1].date()}), {len(ct)} trades")
monthly = {}
for sl in SLEEVES:
    v = np.array([dr.sum() for s, _, _, dr in ct if s == sl])
    print(f"  {sl:5s}: {len(v)} trades ({len(v)/years:.0f}/yr) mean {v.mean():+.3f}R (se {v.std()/np.sqrt(len(v)):.3f}) "
          f"-> {v.sum()/years:+.1f} R/yr (all signals, before caps)")
    m = pd.Series(0.0, index=pd.period_range(master[0], master[-1], freq="M"))
    for s, ei, idx, dr in ct:
        if s == sl:
            for k, r in zip(idx, dr):
                m[master[k].to_period("M")] += r
    monthly[sl] = m
mc = pd.DataFrame(monthly).corr()
print("  monthly R correlation between sleeves:\n" + mc.round(2).to_string())


def simulate(r, start=0, static=False, target=None, floor=None, maxdays=None, sleeves=None):
    eq = 1.0; open_tr = []; entries = {}
    for k, (s, ei, idx, dr) in enumerate(ct):
        if ei >= start and (sleeves is None or s in sleeves):
            entries.setdefault(ei, []).append(k)
    peak = 1.0; mdd = 0.0; taken = 0
    for day in range(start, len(master)):
        base = 1.0 if static else eq
        for k in entries.get(day, []):
            s = ct[k][0]
            tot = sum(x[1] for x in open_tr); sl_open = sum(x[1] for x in open_tr if ct[x[0]][0] == s)
            if tot + r * base <= 6 * r * base + 1e-12 and sl_open + r * base <= 2 * r * base + 1e-12:
                open_tr.append([k, r * base, 0]); taken += 1
        pnl = 0.0; keep = []
        for tr_ in open_tr:
            k, amt, ptr = tr_; _, ei, idx, dr = ct[k]
            while ptr < len(idx) and idx[ptr] == day:
                pnl += amt * dr[ptr]; ptr += 1
            tr_[2] = ptr
            if ptr < len(idx): keep.append(tr_)
        open_tr = keep; eq += pnl
        if target is not None:
            if eq >= target: return "pass", day
            if eq <= floor or pnl <= -0.05: return "fail", day
            if (master[day] - master[start]).days > maxdays: return "timeout", day
        peak = max(peak, eq); mdd = max(mdd, 1 - eq / peak)
    if target is not None: return "timeout", len(master)
    return eq, mdd, taken


MAXD = int(sys.argv[2]) if len(sys.argv) > 2 else 365
DAYS = []


def challenge(r, s, sleeves=None):
    o1, d1 = simulate(r, s, True, 1.10, 0.90, MAXD, sleeves)
    if o1 != "pass" or d1 + 1 >= len(master): return o1
    o2, d2 = simulate(r, d1 + 1, True, 1.05, 0.90, MAXD, sleeves)
    if o2 == "pass": DAYS.append((master[d2] - master[s]).days)
    return o2


starts = [i for i in range(1, len(master)) if master[i].month != master[i - 1].month and master[i].year <= (2025 if MAXD <= 365 else 2023)]
SETS = ((("EQ only", {"EQ"}), ("CMD only", {"CMD"}), ("ALL 4 sleeves", None)), (0.005, 0.01, 0.02))
if len(sys.argv) > 1 and sys.argv[1] == "eqcmd":
    SETS = ((("EQ+CMD", {"EQ", "CMD"}), ("CMD only", {"CMD"})), (0.0025, 0.005, 0.0075))
for label, sls in SETS[0]:
    for r in SETS[1]:
        eq, mdd, tk = simulate(r, sleeves=sls)
        o = np.array([challenge(r, s, sls) for s in starts])
        print(f"{label:14s} risk {r:.1%}: CAGR {eq**(1/years)-1:+.1%} maxDD {mdd:.1%} taken {tk} ({tk/years:.0f}/yr) | "
              f"2-step: pass {np.mean(o=='pass'):.0%} fail {np.mean(o=='fail'):.0%} timeout {np.mean(o=='timeout'):.0%}"
              f" | median calendar days to pass both {np.median(DAYS) if DAYS else float('nan'):.0f}")
        DAYS.clear()
