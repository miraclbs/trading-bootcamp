"""Peter Brandt (TraderLion, R1sNTB2Vh7w): "Trade identification is maybe 5-10% of a trader's edge; trade and risk
management is where the game is played." + his 3-DAY TRAILING STOP rule (ChartWizards -WaAMAEAjOs, from 'Diary of a
Professional Commodity Trader'): identify the HIGH DAY of the move; when a later day CLOSES below the low of the high
day, move the stop to just below the low of that day; repeat on every new high day (mirror for shorts).
Test (daily, 2005+, no costs), entries x exits:
  Entries: (1) 20-day close breakout (proxy for a classical-pattern breakout), long and short;
           (2) RANDOM day, random direction (same number of trades, roughly).
  Exits (all with initial stop 1 ATR below entry, gaps filled at the open):
           A fixed target 2R, 20-day time exit
           B Brandt 3-day trailing stop, no target, max 120 days
           C 10-day-low trailing stop, no target, max 120 days
Metrics: mean R (se), profit factor, worst loss R, Pareto = share of trades (largest winners) that make 80% of net
profit. Groups: INDEX ETFs, COMMODITY ETFs, FX majors.
Also: how unusual is Brandt's '19 losers out of 20' streak (Aug 2022) for a ~55% win-rate trader?
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GROUPS = {
    "INDEX": "SPY QQQ IWM DIA EFA EEM EWJ EWG".split(),
    "COMMOD": "GLD SLV USO UNG DBA DBC PPLT PALL CPER CORN WEAT SOYB".split(),
    "FX": "EURUSD=X GBPUSD=X USDJPY=X AUDUSD=X USDCAD=X USDCHF=X NZDUSD=X".split(),
}
N = 20


def run_exit(O, Hh, L, C, t, side, a, method):
    E = C[t]
    stop = E - side * a
    hd = t                      # high-day index (low-day for shorts)
    maxd = 20 if method == "A" else 120
    for j in range(t + 1, min(t + 1 + maxd, len(C))):
        # stop check with gap
        if side == 1:
            if O[j] <= stop:
                return (O[j] - E) / a
            if L[j] <= stop:
                return (stop - E) / a
            if method == "A" and Hh[j] >= E + 2 * a:
                return 2.0
        else:
            if O[j] >= stop:
                return (E - O[j]) / a
            if Hh[j] >= stop:
                return (E - stop) / a
            if method == "A" and L[j] <= E - 2 * a:
                return 2.0
        # trailing updates after the day closes
        if method == "B":
            if side == 1:
                if Hh[j] > Hh[hd]:
                    hd = j
                elif C[j] < L[hd]:
                    stop = max(stop, L[j] - 0.01 * a)
            else:
                if L[j] < L[hd]:
                    hd = j
                elif C[j] > Hh[hd]:
                    stop = min(stop, Hh[j] + 0.01 * a)
        elif method == "C" and j - t >= 2:
            lo = max(t + 1, j - 9)
            stop = max(stop, L[lo:j + 1].min()) if side == 1 else min(stop, Hh[lo:j + 1].max())
    j = min(t + maxd, len(C) - 1)
    return side * (C[j] - E) / a


def stats(r):
    r = np.array(r)
    if len(r) < 10:
        return "n/a"
    gp, gl = r[r > 0].sum(), -r[r < 0].sum()
    pf = gp / gl if gl > 0 else np.inf
    net = r.sum()
    if net > 0:
        w = np.sort(r[r > 0])[::-1]
        k = np.searchsorted(np.cumsum(w), 0.8 * net) + 1
        par = f"{k / len(r):.0%}"
    else:
        par = "-"
    return (f"n={len(r):5d} avg {r.mean():+.3f}R (se {r.std()/np.sqrt(len(r)):.3f}) PF {pf:.2f} "
            f"worst {r.min():+.1f}R top-trades-for-80%-of-net {par}")


for g, syms in GROUPS.items():
    res = {(e, m): [] for e in ("breakout", "random") for m in "ABC"}
    for sym in syms:
        d = yf.download(sym, start="2004-01-01", interval="1d", progress=False, auto_adjust=True)
        if d is None or len(d) < 300:
            continue
        if hasattr(d.columns, "levels"):
            d.columns = d.columns.get_level_values(0)
        d = d.dropna()
        d = d[(d["High"] > 0) & (d["Low"] > 0)]
        O, Hh, L, C = (d[c].values for c in ("Open", "High", "Low", "Close"))
        yr = d.index.year.values
        tr = np.maximum(Hh - L, np.maximum(abs(Hh - np.roll(C, 1)), abs(L - np.roll(C, 1))))
        atr = np.convolve(tr, np.ones(14) / 14, mode="full")[:len(tr)]
        rng = np.random.default_rng(sum(map(ord, sym)))
        last = -99
        for t in range(N + 15, len(C) - 2):
            if yr[t] < 2005 or atr[t] <= 0:
                continue
            a = atr[t]
            hi, lo = Hh[t - N:t].max(), L[t - N:t].min()
            side = 1 if C[t] > hi else (-1 if C[t] < lo else 0)
            if side and t - last >= 10:
                last = t
                for m in "ABC":
                    res[("breakout", m)].append(run_exit(O, Hh, L, C, t, side, a, m))
            if rng.random() < 0.03:
                s = 1 if rng.random() < 0.5 else -1
                for m in "ABC":
                    res[("random", m)].append(run_exit(O, Hh, L, C, t, s, a, m))
    print(f"\n=== {g} ===")
    for e in ("breakout", "random"):
        for m, lab in (("A", "fixed 2R/20d"), ("B", "Brandt 3-day trail"), ("C", "10-day-low trail")):
            print(f"  {e:8s} | {lab:18s} | {stats(res[(e, m)])}")

# streak check
rng = np.random.default_rng(1)
print("\nP(at least one 20-trade window with >= 19 losers) for iid trades:")
for wr in (0.50, 0.55):
    for ntr in (1000, 3000):
        hits = 0
        for _ in range(4000):
            loss = (rng.random(ntr) > wr).astype(int)
            w = np.convolve(loss, np.ones(20, dtype=int), mode="valid")
            hits += (w >= 19).any()
        print(f"  WR {wr:.0%}, {ntr} trades: {hits / 4000:.2%}")
