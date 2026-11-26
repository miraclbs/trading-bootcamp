"""Round 17: the daily 'first pullback after momentum' edge (verify_pullback.py) on 1-HOUR bars, with COSTS.
yfinance 1h history: last ~730 days. Same rules scaled to bars: momentum = close outside EMA20 +/- 2.25*ATR20 (1h);
first touch of PREVIOUS bar's EMA20 3..20 bars later; fill at min(open, EMA20[p-1]) (long) / max (short);
stop 1 ATR, target 2R, time exit 20 bars. Baseline: random trend-state bar (close > EMA20 and EMA20 rising for long),
same exits. Costs in R: round-trip cost (spread + slippage + commission, in price units) / ATR.
Groups and assumed round-trip costs (conservative retail):
  US index ETFs  : $0.02 per share round trip
  Index futures  : ES 0.5 pt, NQ 2 pt, YM 4 pt, RTY 0.3 pt (=2 ticks + commission approx)
  FX majors      : 1.2 pips round trip (0.00012; JPY 0.012)
  Gold futures   : 0.4 $ round trip
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GROUPS = {
    "INDEX ETF": {s: 0.02 for s in ("SPY", "QQQ", "IWM", "DIA")},
    "INDEX FUT": {"ES=F": 0.5, "NQ=F": 2.0, "YM=F": 4.0, "RTY=F": 0.3},
    "FX": {"EURUSD=X": 0.00012, "GBPUSD=X": 0.00012, "AUDUSD=X": 0.00012, "USDJPY=X": 0.012,
           "USDCAD=X": 0.00012, "USDCHF=X": 0.00012},
    "GOLD": {"GC=F": 0.4},
}


def ema(x, n):
    a = 2 / (n + 1)
    out = np.empty_like(x); out[0] = x[0]
    for i in range(1, len(x)):
        out[i] = a * x[i] + (1 - a) * out[i - 1]
    return out


def trade(Hh, L, C, t, fill, side, a, k=2.0, maxd=20):
    stop, tgt = fill - side * a, fill + side * k * a
    if side * (C[t] - stop) <= 0:
        return -1.0
    for j in range(t + 1, min(t + 1 + maxd, len(C))):
        if (side == 1 and L[j] <= stop) or (side == -1 and Hh[j] >= stop):
            return -1.0
        if (side == 1 and Hh[j] >= tgt) or (side == -1 and L[j] <= tgt):
            return k
    return side * (C[min(t + maxd, len(C) - 1)] - fill) / a


MAXCOST = 0.25
print("Trades skipped when round-trip cost > 25% of ATR (untradeable). 1h bars, last ~2 years. R per trade gross and net of round-trip cost. Pullback vs random trend-state bar.")
for g, syms in GROUPS.items():
    pb, pb_net, base, base_net, sides, costR = [], [], [], [], [], []
    skipped = [0]
    halves = []
    for sym, cost in syms.items():
        d = yf.download(sym, period="730d", interval="1h", progress=False, auto_adjust=True)
        if d is None or len(d) < 500:
            print(f"  skip {sym}"); continue
        if hasattr(d.columns, "levels"):
            d.columns = d.columns.get_level_values(0)
        d = d.dropna()
        d = d[(d["High"] > 0) & (d["Low"] > 0) & (d["High"] >= d["Low"])]
        O, Hh, L, C = (d[c].values for c in ("Open", "High", "Low", "Close"))
        T = len(C); mid = T // 2
        tr = np.maximum(Hh - L, np.maximum(abs(Hh - np.roll(C, 1)), abs(L - np.roll(C, 1))))
        atr = np.convolve(tr, np.ones(20) / 20, mode="full")[:T]
        e = ema(C, 20)
        rng = np.random.default_rng(sum(map(ord, sym)))
        last_m = {1: -99, -1: -99}
        for t in range(30, T - 21):
            a = atr[t - 1]
            if a <= 0 or cost / a > MAXCOST:     # untradeable: round-trip cost > 25% of the 1-ATR stop
                skipped[0] += 1
                continue
            for side in (1, -1):
                if side * (C[t] - e[t]) > 0 and side * (e[t] - e[t - 5]) > 0 and rng.random() < 0.1:
                    r = trade(Hh, L, C, t, C[t], side, a)
                    base.append(r); base_net.append(r - cost / a)
                band = e[t] + side * 2.25 * atr[t]
                if side * (C[t] - band) <= 0 or t - last_m[side] < 20:
                    continue
                last_m[side] = t
                for p in range(t + 3, min(t + 21, T - 21)):
                    if side * (C[p - 1] - (e[p - 1] - side * 2.25 * atr[p - 1])) < 0:
                        break
                    lvl = e[p - 1]
                    if not ((L[p] <= lvl) if side == 1 else (Hh[p] >= lvl)):
                        continue
                    fill = min(O[p], lvl) if side == 1 else max(O[p], lvl)
                    ap = atr[p - 1]
                    if ap <= 0 or cost / ap > MAXCOST:
                        break
                    r = trade(Hh, L, C, p, fill, side, ap)
                    pb.append(r); pb_net.append(r - cost / ap); sides.append(side); costR.append(cost / ap)
                    halves.append(0 if p < mid else 1)
                    break
    pb, pb_net, base, base_net, sides, halves = map(np.array, (pb, pb_net, base, base_net, sides, halves))
    se = pb.std() / np.sqrt(len(pb)) if len(pb) else np.nan
    print(f"\n{g}: pullback n={len(pb)} gross {pb.mean():+.3f}R (se {se:.3f}) net {pb_net.mean():+.3f}R "
          f"| cost avg {np.mean(costR):.3f}R median {np.median(costR):.3f}R | untradeable bars skipped {skipped[0]}")
    print(f"   long {pb_net[sides == 1].mean():+.3f} (n={np.sum(sides == 1)}) | short {pb_net[sides == -1].mean():+.3f} "
          f"(n={np.sum(sides == -1)}) | 1st half {pb_net[halves == 0].mean():+.3f} | 2nd half {pb_net[halves == 1].mean():+.3f}")
    print(f"   baseline random trend bar: n={len(base)} gross {np.mean(base):+.3f}R net {np.mean(base_net):+.3f}R "
          f"-> pullback minus baseline (net) {pb_net.mean() - np.mean(base_net):+.3f}R")
