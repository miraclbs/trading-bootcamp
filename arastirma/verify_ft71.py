"""Round 54: Futures Trader 71, Chat With Traders ep. 82 (woT6d7xUtOs).
 (A) "An impulsive move = a large bar, expansion of range on expansion of volume. After it pulls back and forms a flag,
     78% of the time in the S&P minis it retests that first high." -> compare with a distance-matched random baseline.
 (B) "Regressive risk: daily loss limit $3,000 with 10 lots; at 1/3 of the limit -> 6 lots, at 1/2 -> 5 lots,
     at 3/4 -> 2 lots until the limit. I want to hit my daily loss limit with the minimum size possible. The goal is
     not to make the money back, it is to find alignment with the market."
Test A: ES=F and NQ=F, 1h (730 days) and 5m (60 days). Impulse bar: range >= 2x the 20-bar average range AND volume >=
 2x the 20-bar average volume, closing in its top 30% (mirror for down). Then wait (<= 6 bars) for the first pullback
 bar (a lower low than the previous bar for up impulses); from that bar's close, does price retest the impulse high
 within 12 bars? Baseline: random bars with the SAME distance to a level above (in ATR units), same window.
Test B: per day up to 6 trades, RR 2 binary outcomes, base risk 0.75% of a 100k account, personal daily stop 3%
 (FTMO 1-Step daily limit 3%; for 2-Step 5% it would be a self-imposed stop). Flat vs regressive sizing.
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(71)

print("(A) Retest of the impulse extreme after the first pullback, within 12 bars")
for sym in ("ES=F", "NQ=F"):
    for iv, per in (("1h", "730d"), ("5m", "60d")):
        d = yf.download(sym, period=per, interval=iv, progress=False, auto_adjust=True)
        if hasattr(d.columns, "levels"):
            d.columns = d.columns.get_level_values(0)
        d = d.dropna(); d = d[d["Volume"] > 0]
        O, H, L, C, V = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
        rngs = H - L
        ar = pd.Series(rngs).shift(1).rolling(20).mean().to_numpy()
        av = pd.Series(V).shift(1).rolling(20).mean().to_numpy()
        hits, dists = [], []
        n = len(C)
        for t in range(25, n - 20):
            if np.isnan(ar[t]) or rngs[t] < 2 * ar[t] or V[t] < 2 * av[t]:
                continue
            pos = (C[t] - L[t]) / max(rngs[t], 1e-9)
            for side in (1, -1):
                if (side == 1 and pos < 0.7) or (side == -1 and pos > 0.3):
                    continue
                ext = H[t] if side == 1 else L[t]
                for k in range(t + 1, min(t + 7, n - 13)):
                    pull = L[k] < L[k - 1] if side == 1 else H[k] > H[k - 1]
                    if pull:
                        dist = side * (ext - C[k]) / ar[t]
                        if dist <= 0:
                            break
                        fut = H[k + 1:k + 13].max() if side == 1 else L[k + 1:k + 13].min()
                        hits.append(side * (fut - ext) >= 0); dists.append(dist)
                        break
        if len(hits) < 15:
            print(f"   {sym} {iv}: n={len(hits)} (too few)"); continue
        # baseline: random bars, level at the same distance (in units of the 20-bar average range) above/below close
        base = []
        for dist in dists:
            for _ in range(30):
                t = rng.integers(25, n - 13); side = 1 if rng.random() < 0.5 else -1
                if np.isnan(ar[t]):
                    continue
                lvl = C[t] + side * dist * ar[t]
                fut = H[t + 1:t + 13].max() if side == 1 else L[t + 1:t + 13].min()
                base.append(side * (fut - lvl) >= 0)
        h = np.array(hits)
        print(f"   {sym:5s} {iv:3s}: impulse events n={len(h):4d} | retest {h.mean():.0%} (se {h.std() / np.sqrt(len(h)):.0%}) "
              f"| distance-matched random {np.mean(base):.0%} | median distance {np.median(dists):.2f} avg ranges")

print("\n(B) Regressive vs flat intraday sizing (100k, up to 6 trades/day, RR 2, personal daily stop -3%)")
print("   EV/trade | sizing      | mean day | P(day hits -3%) | 5th pct day | P(pass +10% before -10%, 2-Step static)")
for e in (-0.10, 0.0, 0.10, 0.20):
    p = (1 + e) / 3
    for mode in ("flat", "regressive"):
        days = []
        for _ in range(40000):
            pnl = 0.0
            for _t in range(6):
                if mode == "flat":
                    r = 0.0075
                else:
                    frac = -pnl / 0.03
                    r = 0.0075 * (1.0 if frac < 1 / 3 else 0.6 if frac < 0.5 else 0.5 if frac < 0.75 else 0.2)
                r = min(r, 0.03 + pnl) if pnl - r < -0.03 else r  # never risk beyond the remaining daily stop
                if r <= 1e-9:
                    break
                pnl += r * 2 if rng.random() < p else -r
                if pnl <= -0.03 + 1e-12:
                    break
            days.append(pnl)
        days = np.array(days)
        # challenge: draw days until +10% or -10%
        passed = 0
        for _ in range(4000):
            eq = 0.0
            while -0.10 < eq < 0.10:
                eq += days[rng.integers(len(days))]
            passed += eq >= 0.10
        print(f"   {e:+.2f}R   | {mode:11s} | {days.mean():+.3%} | {np.mean(days <= -0.03 + 1e-9):14.1%} | "
              f"{np.percentile(days, 5):+.2%} | {passed / 4000:.1%}")
