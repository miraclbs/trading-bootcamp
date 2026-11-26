"""Round 18: is the round-17 result ('in commodities, trailing exits make random-direction entries profitable')
robust? Per symbol, per period, and on continuous FUTURES with a roll-gap filter.
Exit rules identical to verify_brandt_exits.py (initial stop 1 ATR; B = Brandt 3-day trail; C = 10-day-low trail;
A = fixed 2R/20d). Entries: random day (p=0.05), random direction. Many seeds averaged to reduce sampling noise.
Futures from yfinance are back-adjusted? NO - they are spliced front months, so roll days show artificial gaps.
Filter: drop any trade whose holding window contains a day with |open - prior close| > 3 ATR (likely roll gap) and
report how many were dropped.
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ETF = "GLD SLV USO UNG DBA DBC PPLT PALL CPER CORN WEAT SOYB".split()
FUT = "GC=F SI=F CL=F NG=F HG=F ZC=F ZS=F ZW=F KC=F SB=F CT=F LE=F".split()


def run_exit(O, Hh, L, C, t, side, a, method, gapflag):
    E = C[t]; stop = E - side * a; hd = t
    maxd = 20 if method == "A" else 120
    for j in range(t + 1, min(t + 1 + maxd, len(C))):
        if gapflag[j]:
            return None
        if side == 1:
            if O[j] <= stop: return (O[j] - E) / a
            if L[j] <= stop: return (stop - E) / a
            if method == "A" and Hh[j] >= E + 2 * a: return 2.0
        else:
            if O[j] >= stop: return (E - O[j]) / a
            if Hh[j] >= stop: return (E - stop) / a
            if method == "A" and L[j] <= E - 2 * a: return 2.0
        if method == "B":
            if side == 1:
                if Hh[j] > Hh[hd]: hd = j
                elif C[j] < L[hd]: stop = max(stop, L[j] - 0.01 * a)
            else:
                if L[j] < L[hd]: hd = j
                elif C[j] > Hh[hd]: stop = min(stop, Hh[j] + 0.01 * a)
        elif method == "C" and j - t >= 2:
            lo = max(t + 1, j - 9)
            stop = max(stop, L[lo:j + 1].min()) if side == 1 else min(stop, Hh[lo:j + 1].max())
    return side * (C[min(t + maxd, len(C) - 1)] - E) / a


def evaluate(syms, label, gapfilter):
    print(f"\n=== {label} === random-direction entries, mean R per trade; per symbol: A fixed2R | B Brandt3d | C 10dLow")
    allr = {m: {"h1": [], "h2": []} for m in "ABC"}
    better = {"B": 0, "C": 0}; nsym = 0; dropped = 0; total = 0
    for sym in syms:
        d = yf.download(sym, start="2004-01-01", interval="1d", progress=False, auto_adjust=True)
        if d is None or len(d) < 500:
            print(f"  skip {sym}"); continue
        if hasattr(d.columns, "levels"):
            d.columns = d.columns.get_level_values(0)
        d = d.dropna(); d = d[(d["High"] > 0) & (d["Low"] > 0) & (d["High"] >= d["Low"])]
        O, Hh, L, C = (d[c].values for c in ("Open", "High", "Low", "Close"))
        yr = d.index.year.values
        tr = np.maximum(Hh - L, np.maximum(abs(Hh - np.roll(C, 1)), abs(L - np.roll(C, 1))))
        atr = np.convolve(tr, np.ones(14) / 14, mode="full")[:len(tr)]
        gap = np.zeros(len(C), dtype=bool)
        if gapfilter:
            gap[1:] = np.abs(O[1:] - C[:-1]) > 3 * atr[:-1]
        res = {m: [] for m in "ABC"}; yrs = []
        for seed in range(5):
            rng = np.random.default_rng(seed * 1000 + sum(map(ord, sym)))
            for t in range(35, len(C) - 2):
                if yr[t] < 2005 or atr[t] <= 0 or rng.random() >= 0.05:
                    continue
                s = 1 if rng.random() < 0.5 else -1
                out = [run_exit(O, Hh, L, C, t, s, atr[t], m, gap) for m in "ABC"]
                total += 1
                if any(o is None for o in out):
                    dropped += 1; continue
                for m, o in zip("ABC", out):
                    res[m].append(o)
                yrs.append(yr[t])
        yrs = np.array(yrs)
        means = {m: np.mean(res[m]) for m in "ABC"}
        nsym += 1
        for m in "BC":
            better[m] += means[m] > means["A"]
        for m in "ABC":
            r = np.array(res[m]); allr[m]["h1"].extend(r[yrs < 2015]); allr[m]["h2"].extend(r[yrs >= 2015])
        print(f"  {sym:6s} n={len(res['A']):4d} | A {means['A']:+.3f} | B {means['B']:+.3f} | C {means['C']:+.3f}")
    for m, lab in (("A", "fixed 2R"), ("B", "Brandt 3-day"), ("C", "10-day low")):
        h1, h2 = np.array(allr[m]["h1"]), np.array(allr[m]["h2"])
        allv = np.concatenate([h1, h2])
        print(f"  pooled {lab:12s}: all {allv.mean():+.3f} (se {allv.std()/np.sqrt(len(allv)):.3f}) | "
              f"2005-14 {h1.mean():+.3f} | 2015+ {h2.mean():+.3f}")
    print(f"  symbols where trailing beats fixed: Brandt {better['B']}/{nsym}, 10-day {better['C']}/{nsym}"
          + (f" | trades dropped for roll gaps: {dropped}/{total}" if gapfilter else ""))


evaluate(ETF, "COMMODITY ETFs", gapfilter=False)
evaluate(FUT, "COMMODITY FUTURES (continuous, roll-gap filter 3 ATR)", gapfilter=True)
