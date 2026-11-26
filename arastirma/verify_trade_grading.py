"""Round 48: Lance Breitstein, "My Trade Grading System (A,B,C,D)" (ubofAZwgd4w): grade every setup before entry,
size up A trades (best trades of the day/month), normal size B, a fraction for C, pass on D; "after a few months,
compare your grades to your results; if your A trades outperform, size more aggressively".
Questions:
 (1) How many A-graded trades do you need before 'A beats B' is statistically real? RR 2 trades (sd ~1.4-1.5R).
 (2) What does grade-based sizing do to results if the grades are informative / uninformative / inversely related
     (Brandt: "my expectations of a trade are probably inversely correlated with the outcomes")?
Model: 200 trades/yr, 15% A, 65% B, 20% C. B trades EV +0.10R (RR 2). Sizes A 2x, B 1x, C 0.5x (risk 1% x size).
"""
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(48)
K = 2.0


def draw(ev, n):
    p = (1 + ev) / (1 + K)
    return np.where(rng.random(n) < p, K, -1.0)


print("(1) Power: probability that a one-sided t-test (5%) shows A > B, B EV +0.10R, A EV +0.10+delta")
print("    n_A trades |  delta +0.15R |  +0.30R |  +0.50R")
for nA in (20, 50, 100, 200, 400):
    cells = []
    for delta in (0.15, 0.30, 0.50):
        hits = 0
        for _ in range(2000):
            a = draw(0.10 + delta, nA); b = draw(0.10, nA * 4)
            se = np.sqrt(a.var(ddof=1) / nA + b.var(ddof=1) / len(b))
            hits += (a.mean() - b.mean()) / se > 1.645
        cells.append(f"{hits / 2000:6.0%}")
    print(f"    {nA:10d} | " + " | ".join(cells))

print("\n(2) One year (200 trades), risk 1% x size (A 2x, B 1x, C 0.5x) vs flat 1%: mean return / 5th pct / "
      "median max drawdown")
SCEN = {"informative (A +0.40, C 0.00)": (0.40, 0.10, 0.00),
        "uninformative (all +0.10)": (0.10, 0.10, 0.10),
        "inverse (A -0.10, C +0.30; Brandt's warning)": (-0.10, 0.10, 0.30)}
for lab, (ea, eb, ec) in SCEN.items():
    out = {"graded": [], "flat": []}
    for _ in range(4000):
        g = rng.choice(3, 200, p=[0.15, 0.65, 0.20])
        ev = np.array([ea, eb, ec])[g]
        p = (1 + ev) / (1 + K); r = np.where(rng.random(200) < p, K, -1.0)
        for mode, size in (("graded", np.array([2.0, 1.0, 0.5])[g]), ("flat", np.ones(200))):
            pnl = r * size * 0.01
            eq = np.cumprod(1 + pnl); mdd = (1 - eq / np.maximum.accumulate(eq)).max()
            out[mode].append((eq[-1] - 1, mdd))
    cells = []
    for mode in ("graded", "flat"):
        a = np.array(out[mode])
        cells.append(f"{mode}: {a[:, 0].mean():+.1%} / {np.percentile(a[:, 0], 5):+.1%} / DD {np.median(a[:, 1]):.1%}")
    print(f"  {lab:44s} | " + " | ".join(cells))
