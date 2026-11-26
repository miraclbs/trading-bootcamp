"""Round 52: Jeff Holden (SMB Capital), Chat With Traders (UWDFkMaJXNw):
 "Dynamic risk allocation: A+ = 80% of the daily stop, A = 30%, B = 15%, C = 5%. When you know you have a positive
  expectancy, increase your bet; when you don't understand it, massively decrease." He also warns: "a lot of times we
  get really slippery with our identification of what an A+ is" and "don't even think about a risk bump for 3 months;
  successful traders needed ~4 months of consistency first".
Prop translation: personal daily stop = 2% of the account (well inside FTMO's 5%) -> A+ 1.6%, A 0.6%, B 0.3%, C 0.1%.
Mix per 250 trades/yr: A+ 5%, A 15%, B 40%, C 40%. RR 2 binary outcomes. Compare with flat risk that has the SAME
average risk per trade (0.36%). Scenarios for the grades:
  informative  : A+ +0.50R, A +0.30R, B +0.10R, C 0.00R
  uninformative: all +0.10R (grades carry no information)
  slippery A+  : A+ -0.10R (mis-identified, e.g. 'first red day' taken too early), A +0.30, B +0.10, C 0.00
Metrics over 1 year: mean return, 5th percentile, P(max DD > 10%), P(reach +10% before -10%) (2-Step phase proxy).
"""
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(152)
K = 2.0
MIX = np.array([0.05, 0.15, 0.40, 0.40])
RISK = np.array([0.016, 0.006, 0.003, 0.001])
FLAT = float((MIX * RISK).sum())
SCEN = {"informative": [0.50, 0.30, 0.10, 0.00], "uninformative": [0.10, 0.10, 0.10, 0.10],
        "slippery A+": [-0.10, 0.30, 0.10, 0.00]}

print(f"Flat risk with the same average: {FLAT:.2%} per trade")
print("scenario       | sizing | mean yr | 5th pct | P(maxDD>10%) | P(+10% before -10%)")
for lab, ev in SCEN.items():
    ev = np.array(ev)
    for mode in ("SMB", "flat"):
        rets, dd10, passed = [], 0, 0
        for _ in range(20000):
            g = rng.choice(4, 250, p=MIX)
            p = (1 + ev[g]) / (1 + K)
            r = np.where(rng.random(250) < p, K, -1.0)
            size = RISK[g] if mode == "SMB" else np.full(250, FLAT)
            eq = np.cumsum(r * size)
            peak = np.maximum.accumulate(np.r_[0.0, eq])[1:]
            dd10 += (peak - eq).max() > 0.10
            hit_up = np.argmax(eq >= 0.10) if (eq >= 0.10).any() else 10**9
            hit_dn = np.argmax(eq <= -0.10) if (eq <= -0.10).any() else 10**9
            passed += hit_up < hit_dn
            rets.append(eq[-1])
        rets = np.array(rets)
        print(f"{lab:14s} | {mode:6s} | {rets.mean():+6.1%} | {np.percentile(rets, 5):+6.1%} | {dd10 / 20000:11.1%} | "
              f"{passed / 20000:6.1%}")
