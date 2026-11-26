"""Calibrate industry prop statistics against expectancy.
Industry (FPFX survey of 10 firms, ~300k accounts, Titans of Tomorrow ucF91qWKYBE): 14% pass to funded, 7% get a payout.
Blueberry Funded CEO (Diamant Trades PwPT-ETipm8): 2-step pass ~12%, 30% of those get a payout.
Model: FTMO-like 2-step at 1% risk per trade: phase 1 +10R before -10R, phase 2 +5R before -10R (no time limit,
daily limit ignored - rarely binding at 1%). Trades: +2R with prob p, -1R otherwise, EV per trade = 3p - 1.
Question: what per-trade expectancy reproduces the industry pass rate?  Also: at 2% and 3% risk."""
import sys
import numpy as np
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(3)

def p_reach(target, loss, ev, n=20000, maxtr=3000):
    p = (1 + ev) / 3
    wins = 0
    for _ in range(n):
        x = 0.0
        for _ in range(maxtr):
            x += 2.0 if rng.random() < p else -1.0
            if x >= target: wins += 1; break
            if x <= -loss: break
    return wins / n

print("2-step pass probability (phase1 x phase2) by per-trade EV (R) and risk per trade")
print("  EV/trade |  1% risk (10R/10R, 5R/10R) |  2% risk (5R/5R, 2.5R/5R) |  3% risk")
for ev in (-0.2, -0.1, -0.05, 0.0, 0.05, 0.1, 0.2):
    row = []
    for r in (1, 2, 3):
        t1, t2, L = 10 / r, 5 / r, 10 / r
        row.append(p_reach(t1, L, ev, n=6000) * p_reach(t2, L, ev, n=6000))
    print(f"  {ev:+.2f}     |  {row[0]:6.1%}                     |  {row[1]:6.1%}                    |  {row[2]:6.1%}")
