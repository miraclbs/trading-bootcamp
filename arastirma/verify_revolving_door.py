"""Round 53: Waqar Asim, "I interviewed EVERY prop firm millionaire" (8FXbZRS4Gq4) - the 'revolving door strategy':
 - stagger 5 funded accounts by week (copy-traded), lock a payout at +3%, 'bin' accounts in drawdown and bring in
   fresh ones that are 1% from passing phase 2; "even a break-even trader can profit: winning periods amplified,
   losing periods minimised";
 - in evaluations risk the max daily loss (4-4.5%) on a single trade to pass in 1-2 trades;
 - millionaires spent $200-400k on evaluations; fee:payout used to be 1:10, now 1:3-1:4.
Model (FTMO-like 100k 2-Step): phase 1 +10%, phase 2 +5%, static -10%, daily -5% (from day start), fee $540
(refund ignored), funded: risk 1%/trade, RR 2 binary, payout of all profit when >= +3% (balance resets), split 80%.
 Part 1: value of a funded account started at P&L 0 vs at -3% -> is 'binning and refreshing' worth the cost of a new
         funded account? Edge cases: iid EV -0.10R / 0 / +0.10R per trade, and a zero-mean REGIME model
         (EV +0.3R or -0.3R, switching with prob 3% per trade, so streaks exist).
 Part 2: evaluation policy: 1% risk vs 4.5% risk (one trade per day) -> P(pass both phases), cost per funded account.
 Part 3: expected payouts per $ of fees for each combination.
Note: staggering/copy-trading changes only WHEN each account is exposed; by linearity of expectation it cannot change
the mean of the sum unless decisions condition on P&L (binning, lock-in), which Part 1 isolates.
"""
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(53)
K = 2.0
SPLIT = 0.80
FEE = 540.0


def ev_matrix(kind, sims, n):
    """per-trade EV, shape (n, sims)"""
    if kind == "regime":
        s = np.where(rng.random(sims) < 0.5, 1.0, -1.0)
        out = np.empty((n, sims))
        for i in range(n):
            s = np.where(rng.random(sims) < 0.03, -s, s)
            out[i] = 0.3 * s
        return out
    return np.full((n, sims), float(kind))


def funded_value(kind, start, bin_at=None, sims=20000, n=1500):
    """expected trader payouts ($) from a 100k funded account starting at P&L 'start' (fraction)."""
    e = ev_matrix(kind, sims, n)
    pnl = np.full(sims, start); pay = np.zeros(sims); alive = np.ones(sims, bool)
    for i in range(n):
        p = (1 + e[i]) / (1 + K)
        step = 0.01 * np.where(rng.random(sims) < p, K, -1.0)
        pnl = np.where(alive, pnl + step, pnl)
        dead = pnl <= -0.10 + 1e-12
        if bin_at is not None:
            dead |= pnl <= bin_at + 1e-12
        alive &= ~dead
        hit = alive & (pnl >= 0.03 - 1e-12)
        pay += np.where(hit, pnl * 100000 * SPLIT, 0.0)
        pnl = np.where(hit, 0.0, pnl)
        if not alive.any():
            break
    return pay.mean()


def evaluation(kind, risk, sims=20000, max_days=400):
    """P(pass phase 1 (+10%) then phase 2 (+5%)); one trade per day, so a single loss < 5% never breaches the
    daily limit; breach at -10% static. Unfinished after max_days per phase counts as a fail."""
    e = ev_matrix(kind, sims, 2 * max_days)
    ok = np.ones(sims, bool); idx = 0
    for target in (0.10, 0.05):
        pnl = np.zeros(sims); state = np.zeros(sims, int)  # 0 running, 1 passed, -1 failed
        for _d in range(max_days):
            p = (1 + e[idx]) / (1 + K); idx += 1
            run = state == 0
            pnl = np.where(run, pnl + risk * np.where(rng.random(sims) < p, K, -1.0), pnl)
            state = np.where(run & (pnl >= target - 1e-12), 1, state)
            state = np.where(run & (pnl <= -0.10 + 1e-12), -1, state)
            if not (state == 0).any():
                break
        ok &= state == 1
    return ok.mean()


KINDS = [(-0.10, "iid -0.10R"), (0.0, "iid 0"), (0.10, "iid +0.10R"), ("regime", "regime 0 (±0.3R streaks)")]
print("PART 1: funded account value (trader's expected payouts, $, 100k, split 80%, payout at +3%)")
print("   edge                    | V(start 0) | V(start -3%) | refresh value V(0)-V(-3%) | V(0) if binning at -3%")
vals = {}
for k, lab in KINDS:
    v0 = funded_value(k, 0.0); v3 = funded_value(k, -0.03); vb = funded_value(k, 0.0, bin_at=-0.03)
    vals[lab] = (v0, vb)
    print(f"   {lab:24s} | {v0:9,.0f} | {v3:11,.0f} | {v0 - v3:24,.0f} | {vb:9,.0f}")

print("\nPART 2: evaluation policy -> P(pass phase 1 + 2), cost per funded account = fee / P(pass)")
print("   edge                    | 1% risk: P / cost | 4.5% risk (max daily on one trade): P / cost")
costs = {}
for k, lab in KINDS:
    cells = []
    for r in (0.01, 0.045):
        pp = evaluation(k, r)
        costs[(lab, r)] = FEE / max(pp, 1e-9)
        cells.append(f"{pp:5.1%} / ${FEE / max(pp, 1e-9):,.0f}")
    print(f"   {lab:24s} | " + " | ".join(cells))

print("\nPART 3: net value per funded account = V - cost to get funded, and payout per $1 of fees")
print("   edge                    | eval risk | hold to breach: net / payout per $ fee | bin at -3%: net / per $ fee")
for k, lab in KINDS:
    v0, vb = vals[lab]
    for r in (0.01, 0.045):
        c = costs[(lab, r)]
        # binning at -3% means more accounts are needed: each funded account yields vb, but the bin happens
        # before breach, so the per-account value is vb (measured), cost per account the same
        print(f"   {lab:24s} | {r:8.1%} | {v0 - c:+9,.0f} / {v0 / c:5.2f} | {vb - c:+9,.0f} / {vb / c:5.2f}")
