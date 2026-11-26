"""Round 35: FTMO Scaling Plan (ftmo.com/en/scaling-plan, read 2026-11-22):
 "Minimum of 4 months trading ... At least 10% net simulated profit above the starting balance, generated within the
  prior 4 months ... At least 2 processed Rewards within that same 4-month period ... Positive account balance at the
  time of scale-up" -> "Increase your FTMO Account size by 25% every 4 months", 90% split (2-Step), cap $2M.
Question: does the scaling plan change the best funded-account risk for a trader WITH an edge? 10% per 4 months is
~30% a year - a high bar.
Model: funded 100k, RR 2, win prob (1+e)/3, 1 trade/day, risk = % of CURRENT account size. Payout every 10 trades if
profit >= 0.5% (withdraw 80%/90% of profit, balance reset). Static max loss 10% of current size. Review every 84
trades (~4 months): if P&L generated in the window >= 10% of size, >= 2 payouts in the window and balance >= start ->
size += 25k (25% of the initial 100k), split 90%. Horizon 750 trades (~3 years), 20,000 paths.
"""
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(35)
NP, T, K, S0 = 20000, 750, 2.0, 100_000


def run(e, r, scaling=True):
    win = rng.random((NP, T)) < (1 + e) / (1 + K)
    size = np.full(NP, float(S0)); bal = np.zeros(NP); alive = np.ones(NP, bool)
    paid = np.zeros(NP); split = np.full(NP, 0.8); win_pnl = np.zeros(NP); win_pay = np.zeros(NP); ups = np.zeros(NP)
    life = np.full(NP, T)
    for t in range(T):
        pnl = np.where(win[:, t], K * r, -r) * size
        bal = np.where(alive, bal + pnl, bal); win_pnl += np.where(alive, pnl, 0)
        dead = alive & (bal <= -0.10 * size); life[dead] = t + 1; alive &= ~dead
        if (t + 1) % 10 == 0:
            can = alive & (bal >= 0.005 * size)
            paid += np.where(can, bal * split, 0); win_pay += can; bal = np.where(can, 0.0, bal)
        if scaling and (t + 1) % 84 == 0:
            ok = alive & (win_pnl >= 0.10 * size) & (win_pay >= 2) & (bal >= 0)
            size = np.where(ok, np.minimum(size + 0.25 * S0, 2_000_000), size); split = np.where(ok, 0.9, split)
            ups += ok; bal = np.where(ok, 0.0, bal)
            win_pnl[:] = 0; win_pay[:] = 0
    return paid, ups, size, life


print("Funded account over ~3 years (750 trades). mean payouts $ | P(>=1 scale-up) | mean scale-ups | "
      "mean final size | P(alive at end)  [no-scaling mean payouts]")
for e in (0.0, 0.10, 0.20, 0.30):
    print(f"\nedge {e:+.2f}R")
    for r in (0.005, 0.01, 0.015, 0.02):
        paid, ups, size, life = run(e, r, True)
        paid0, _, _, _ = run(e, r, False)
        print(f"  risk {r:4.1%}: {paid.mean():9,.0f} | {np.mean(ups >= 1):4.0%} | {ups.mean():4.1f} | "
              f"{size.mean():9,.0f} | {np.mean(life == T):4.0%}   [{paid0.mean():9,.0f}]")


def run_cushion(e, r, keep):
    """no scaling; at each payout withdraw only profit ABOVE a kept cushion 'keep' (fraction of size)"""
    win = rng.random((NP, T)) < (1 + e) / (1 + K)
    bal = np.zeros(NP); alive = np.ones(NP, bool); paid = np.zeros(NP); life = np.full(NP, T)
    for t in range(T):
        bal = np.where(alive, bal + np.where(win[:, t], K * r, -r), bal)
        dead = alive & (bal <= -0.10); life[dead] = t + 1; alive &= ~dead
        if (t + 1) % 10 == 0:
            can = alive & (bal >= keep + 0.005)
            paid += np.where(can, (bal - keep) * 0.8 * S0, 0); bal = np.where(can, keep, bal)
    return paid, life


print("\nPayout policy: keep a cushion of profit in the account (no scaling, 3 years). mean payouts $ / P(alive)")
for e in (0.0, 0.10, 0.20):
    for r in (0.005, 0.01):
        cells = []
        for keep in (0.0, 0.03, 0.05, 0.10):
            p, l = run_cushion(e, r, keep)
            cells.append(f"keep {keep:3.0%}: {p.mean():8,.0f} / {np.mean(l == T):3.0%}")
        print(f"  edge {e:+.2f} risk {r:.1%} | " + " | ".join(cells))
