"""Round 14: out-of-sample check of the Wyckoff ST result (verify_secondary_test.py) on NEW symbols,
plus a test of the volume filter itself.
Same definitions as verify_secondary_test.py:
  Climax: decline background (10d ret <= -1.5 ATR, close within 5% of 20d low) + vol >= 2x 20d avg + range >= 1.2 ATR.
  Retest window: 3..15 days after climax; abort if low < climax_low - 1 ATR.
  'ST low-vol'   : low within +-0.5 ATR of climax low, vol < 0.7x climax vol, range < climax range, close > climax low
  'retest any'   : FIRST day in window with low within +-0.5 ATR of climax low and close > climax low (no volume/range
                   filter)  -> isolates the value of the low-volume condition
  'retest hi-vol': first such day with vol >= 0.7x climax vol (opposite of Wyckoff's ST requirement)
Trade: long at close; stop = min(climax low, day low) - 0.1 ATR; target 2R; 20-day time exit. No costs.
Baselines: buy climax close; random decline-background day (1 in 8 sampled; stop = 20d low - 0.1 ATR).
Usage: python verify_secondary_test2.py [new|orig|all]
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ORIG = ("SPY", "QQQ", "IWM", "DIA", "GLD", "TLT", "XLE", "XLF", "EEM")
NEW = ("XLK", "XLV", "XLY", "XLP", "XLI", "XLU", "XLB", "SLV", "USO", "EFA", "EWJ", "EWZ", "FXI", "SMH", "IEF",
       "EWG", "EWU", "MDY")
which = sys.argv[1] if len(sys.argv) > 1 else "new"
SYMS = {"new": NEW, "orig": ORIG, "all": ORIG + NEW}[which]
START_YEAR = 2005


def trade(C, Hh, L, t, entry, stop, k=2.0, maxd=20):
    R = entry - stop
    if R <= 0:
        return None
    for j in range(t + 1, min(t + 1 + maxd, len(C))):
        if L[j] <= stop:
            return -1.0
        if Hh[j] >= entry + k * R:
            return k
    j = min(t + maxd, len(C) - 1)
    return (C[j] - entry) / R


KEYS = ("buy climax close", "random decline day", "retest any", "retest hi-vol", "ST low-vol (all)",
        "  ST no undercut", "  spring undercut")
out = {k: [] for k in KEYS}
years = {k: [] for k in KEYS}
per_sym = {}


def add(k, r, y):
    if r is not None:
        out[k].append(r); years[k].append(y)


for sym in SYMS:
    d = yf.download(sym, start="2004-06-01", interval="1d", progress=False, auto_adjust=True)
    if d is None or len(d) < 100:
        print(f"skip {sym}: no data"); continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna()
    O, Hh, L, C, V = (d[c].values for c in ("Open", "High", "Low", "Close", "Volume"))
    yr = d.index.year.values
    tr = np.maximum(Hh - L, np.maximum(abs(Hh - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = np.convolve(tr, np.ones(14) / 14, mode="full")[:len(tr)]
    vavg = np.convolve(V, np.ones(20) / 20, mode="full")[:len(V)]
    last_c = -99
    rng_seed = np.random.default_rng(sum(map(ord, sym)))
    st_sym = []
    for t in range(25, len(C) - 21):
        if yr[t] < START_YEAR:
            continue
        a = atr[t - 1]
        if a <= 0 or vavg[t - 1] <= 0:
            continue
        decline = (C[t] - C[t - 10]) <= -1.5 * a and C[t] <= L[t - 19:t + 1].min() * 1.05
        if not decline:
            continue
        if rng_seed.random() < 0.125:
            add("random decline day", trade(C, Hh, L, t, C[t], L[t - 19:t + 1].min() - 0.1 * a), yr[t])
        climax = V[t] >= 2.0 * vavg[t - 1] and (Hh[t] - L[t]) >= 1.2 * a
        if not climax or t - last_c <= 15:
            continue
        last_c = t
        cl, cv, cr = L[t], V[t], Hh[t] - L[t]
        add("buy climax close", trade(C, Hh, L, t, C[t], cl - 0.1 * a), yr[t])
        got_any = got_hi = got_st = False
        for s in range(t + 3, min(t + 16, len(C) - 21)):
            if L[s] < cl - 1.0 * a:
                break
            near = abs(L[s] - cl) <= 0.5 * a and C[s] > cl
            if not near:
                continue
            r = trade(C, Hh, L, s, C[s], min(cl, L[s]) - 0.1 * a)
            if not got_any:
                add("retest any", r, yr[s]); got_any = True
            if not got_hi and V[s] >= 0.7 * cv:
                add("retest hi-vol", r, yr[s]); got_hi = True
            if not got_st and V[s] < 0.7 * cv and (Hh[s] - L[s]) < cr:
                add("ST low-vol (all)", r, yr[s])
                add("  spring undercut" if L[s] < cl else "  ST no undercut", r, yr[s])
                if r is not None:
                    st_sym.append(r)
                got_st = True
            if got_any and got_hi and got_st:
                break
    per_sym[sym] = st_sym

print(f"Symbols ({which}): {' '.join(SYMS)}  | daily {START_YEAR}+ | long, 2R target, 20d time exit, no costs")
for k in KEYS:
    v = np.array(out[k]); y = np.array(years[k])
    if len(v) == 0:
        print(f"{k:20s}: n=0"); continue
    a1 = v[y < 2015]; a2 = v[y >= 2015]
    print(f"{k:20s}: n={len(v):5d} avg {v.mean():+.3f}R (se {v.std()/np.sqrt(len(v)):.3f}) | 2R hit {np.mean(v==2.0):.0%} "
          f"stop {np.mean(v==-1.0):.0%} | 2005-14 {a1.mean() if len(a1) else float('nan'):+.2f} (n={len(a1)}) "
          f"| 2015+ {a2.mean() if len(a2) else float('nan'):+.2f} (n={len(a2)})")

# difference tests (Welch t)
def diff(k1, k2):
    a, b = np.array(out[k1]), np.array(out[k2])
    if len(a) < 2 or len(b) < 2:
        return
    dm = a.mean() - b.mean()
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    print(f"  {k1.strip():18s} - {k2.strip():18s}: {dm:+.3f}R  (t = {dm/se:+.2f})")

print("\nDifferences:")
diff("ST low-vol (all)", "random decline day")
diff("ST low-vol (all)", "buy climax close")
diff("ST low-vol (all)", "retest hi-vol")
diff("retest any", "random decline day")
diff("buy climax close", "random decline day")

print("\nST low-vol avg by symbol (n):")
print("  " + " | ".join(f"{s} {np.mean(v):+.2f}({len(v)})" for s, v in per_sym.items() if len(v)))
pos = sum(1 for v in per_sym.values() if len(v) and np.mean(v) > 0)
tot = sum(1 for v in per_sym.values() if len(v))
print(f"  symbols with positive ST avg: {pos}/{tot}")
