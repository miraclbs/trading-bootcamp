"""Round 53: Trader Dante, "What Everyone Should Know About Trading Financial Markets" (NDkE6RHke9U).
 (A) "With a 65% strike rate, in 50 trades you have over a 50% chance of 4 losers in a row and over a 1 in 5 chance
     of 5 losers in a row."
 (B) "Levels are way more likely to hold if the market moves into them aggressively than if it drifts into them
     ('the drift of death') - completely counterintuitive, test it yourself." (outside Asia hours)
Test B: 1h bars (730 days), FX + futures. Level = previous calendar day's low (support) / high (resistance).
 First touch of the day, approached from the right side. Approach speed = distance travelled over the 4 bars before
 the touch, in ATR(14, 1h). Outcome: from the level, does price reach 1 ATR in the 'hold' direction before 1 ATR
 through the level (within 24 bars)? Compare speed terciles. Control: the same procedure on RANDOM pseudo-levels at a
 similar distance from the prior close (separates a level effect from a generic 'fast moves mean-revert' effect).
 Asian hours (00-06 UTC) excluded, as Dante suggests.
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(53)

# ---- A: streak probabilities
print("(A) P(at least k losers in a row within 50 trades), win rate 65% (exact via simulation, 200k runs)")
L = rng.random((200000, 50)) >= 0.65
for k in (3, 4, 5, 6):
    run = np.zeros(200000, int); best = np.zeros(200000, int)
    for i in range(50):
        run = np.where(L[:, i], run + 1, 0); best = np.maximum(best, run)
    print(f"   k={k}: {np.mean(best >= k):.1%}")

# ---- B: approach speed into prior-day levels
SYMS = "EURUSD=X GBPUSD=X USDJPY=X AUDUSD=X GC=F CL=F ES=F NQ=F".split()
events = {"real": [], "random": []}
for s in SYMS:
    d = yf.download(s, period="730d", interval="1h", progress=False, auto_adjust=True)
    if d is None or len(d) < 2000:
        continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna()
    idx = d.index.tz_convert("UTC") if d.index.tz is not None else d.index.tz_localize("UTC")
    O, H, Lo, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    tr = np.maximum(H - Lo, np.maximum(abs(H - np.roll(C, 1)), abs(Lo - np.roll(C, 1))))
    atr = pd.Series(tr).rolling(14).mean().to_numpy()
    days = pd.Series(idx.date)
    hours = idx.hour
    uniq = days.unique()
    pos = {dd: np.where(days.values == dd)[0] for dd in uniq}
    for j in range(1, len(uniq)):
        prev, cur = pos[uniq[j - 1]], pos[uniq[j]]
        if len(prev) < 10 or len(cur) < 10:
            continue
        pdl, pdh, pclose = Lo[prev].min(), H[prev].max(), C[prev[-1]]
        rngp = pdh - pdl
        if rngp <= 0:
            continue
        lv = {"real": [(pdl, 1), (pdh, -1)]}
        off = rng.uniform(0.3, 1.2, 2) * rngp
        lv["random"] = [(pclose - off[0], 1), (pclose + off[1], -1)]
        for kind, levels in lv.items():
            for level, side in levels:  # side +1 = support (expect bounce up), -1 = resistance
                for t in cur:
                    if t < 20 or t + 25 >= len(C) or np.isnan(atr[t - 1]):
                        continue
                    touched = Lo[t] <= level if side == 1 else H[t] >= level
                    if not touched:
                        continue
                    if side * (C[t - 1] - level) <= 0 or 0 <= hours[t] < 6:
                        break  # first touch only; skip if approached from the wrong side or in Asia
                    a = atr[t - 1]
                    speed = side * (C[t - 5] - level) / a  # how far price travelled toward the level in 4 bars
                    up, dn = level + side * 1.0 * a, level - side * 1.0 * a
                    out = None
                    for k in range(t, t + 25):
                        through = Lo[k] <= dn if side == 1 else H[k] >= dn
                        held = H[k] >= up if side == 1 else Lo[k] <= up
                        if k == t:
                            held = held and side * (C[t] - level) > 0  # touch bar: count hold only if it closed back
                        if through:
                            out = 0; break
                        if held:
                            out = 1; break
                    if out is not None:
                        events[kind].append((speed, out, s))
                    break

print("\n(B) Hold rate (1 ATR away from the level before 1 ATR through it), by approach speed tercile")
for kind in ("real", "random"):
    ev = np.array([(sp, o) for sp, o, _ in events[kind]])
    q1, q2 = np.quantile(ev[:, 0], [1 / 3, 2 / 3])
    cells = []
    for lab, m in (("slow (drift)", ev[:, 0] <= q1), ("medium", (ev[:, 0] > q1) & (ev[:, 0] <= q2)),
                   ("fast", ev[:, 0] > q2)):
        r = ev[m, 1]
        cells.append(f"{lab}: {r.mean():.1%} (se {r.std() / np.sqrt(len(r)):.1%}, n={len(r)})")
    print(f"   {kind:6s} levels | " + " | ".join(cells) + f" | speed cut-offs {q1:.2f}/{q2:.2f} ATR")
print("\n   per symbol, real levels: fast minus slow hold rate")
for s in SYMS:
    ev = np.array([(sp, o) for sp, o, ss in events["real"] if ss == s])
    if len(ev) < 60:
        continue
    q1, q2 = np.quantile(ev[:, 0], [1 / 3, 2 / 3])
    print(f"   {s:9s}: slow {ev[ev[:, 0] <= q1, 1].mean():.0%} | fast {ev[ev[:, 0] > q2, 1].mean():.0%} | n={len(ev)}")
