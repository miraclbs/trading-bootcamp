"""Round 50: Lance Breitstein, "The Claude Trading Trap Killing Your PnL" (Z9THivbJ2mI).
Claim: "Find your one biggest constraint. A trader makes +20K on his best setup and loses -12K everywhere else; I don't
give him a new setup, I cut the other trades... Feed your trades into a system that categorizes them by playbook:
maybe your three setups made +40K and everything outside the playbook lost -18K -> stop trading the garbage."
Question: how reliable is a one-quarter per-setup P&L split for that decision?
Model: 1 quarter = 100 trades, RR 2 binary outcomes (sd ~1.4R). Category A (playbook) 40 trades, B/C/D 20 each.
 World 1 'real problem': A +0.30R, B/C/D -0.15R each.     World 2 'no difference': all +0.05R.
 World 3 'mixed': A +0.30R, B +0.20R (good but new), C/D -0.15R.
Policies after quarter 1, applied to quarters 2-4: keep all / drop every category with negative Q1 sum (naive) /
 drop only if Q1 mean < 0 AND t < -1.0 (cautious) / oracle (drop the truly negative ones).
"""
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(50)
K = 2.0
N = {"A": 40, "B": 20, "C": 20, "D": 20}
WORLDS = {"1 real problem (A +0.30, rest -0.15)": {"A": 0.30, "B": -0.15, "C": -0.15, "D": -0.15},
          "2 no difference (all +0.05)": {"A": 0.05, "B": 0.05, "C": 0.05, "D": 0.05},
          "3 mixed (A +0.30, B +0.20, C/D -0.15)": {"A": 0.30, "B": 0.20, "C": -0.15, "D": -0.15}}


def draw(ev, n):
    p = (1 + ev) / (1 + K)
    return np.where(rng.random(n) < p, K, -1.0)


print("Quarters 2-4 total R (mean over 5000 sims) by policy, plus how often a category was dropped after Q1")
for wl, ev in WORLDS.items():
    tot = {"keep all": [], "naive (drop if Q1 sum<0)": [], "cautious (drop if t<-1)": [], "oracle": []}
    drops = {"naive": {c: 0 for c in N}, "cautious": {c: 0 for c in N}}
    pattern = 0
    for _ in range(5000):
        q1 = {c: draw(ev[c], N[c]) for c in N}
        later = {c: draw(ev[c], 3 * N[c]) for c in N}
        if q1["A"].sum() > 0 and sum(q1[c].sum() for c in "BCD") < 0:
            pattern += 1
        naive = {c for c in N if q1[c].sum() < 0}
        caut = {c for c in N if q1[c].mean() < 0 and q1[c].mean() / (q1[c].std(ddof=1) / np.sqrt(N[c])) < -1.0}
        orac = {c for c in N if ev[c] < 0}
        for c in naive:
            drops["naive"][c] += 1
        for c in caut:
            drops["cautious"][c] += 1
        for lab, dset in (("keep all", set()), ("naive (drop if Q1 sum<0)", naive),
                          ("cautious (drop if t<-1)", caut), ("oracle", orac)):
            tot[lab].append(sum(later[c].sum() for c in N if c not in dset))
    print(f"\n  World {wl}")
    print(f"    Q1 shows 'playbook A profitable, everything else losing': {pattern / 5000:.0%} of quarters")
    for lab, v in tot.items():
        v = np.array(v)
        print(f"    {lab:26s}: mean {v.mean():+6.1f}R | 5th pct {np.percentile(v, 5):+6.1f}R")
    for pol in ("naive", "cautious"):
        print(f"    {pol:8s} drop rate: " + " ".join(f"{c} {drops[pol][c] / 5000:.0%}" for c in N))
