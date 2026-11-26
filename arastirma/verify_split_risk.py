"""Round 34: "Risk more on the challenge, be conservative on the funded account" (Kimmel 90ozA2Ts4FU; a common prop
tip). Also checks FTMO's blog claim (ftmo.com/en/blog/how-to-use-monte-carlo-simulations-to-pass-the-ftmo-challenge,
2026-07-31): "reducing your risk per trade from 2% to 0.5% or 1% can dramatically increase your probability of
passing... for instance, from 15% to 85%" - which edge would that require?
Model: FTMO-like 2-step (+10%, +5%, -10% static, -5% daily), fee 540 for 100k refunded with the first payout,
funded: -10% static, every 10 trades withdraw 80% of profit if >= +0.5% (balance reset). Account lost -> buy a new
challenge. 1 trade/day, 250 trades per trader-year, RR 2, win prob (1+e)/3 => e R per trade after costs.
Risk is % of initial balance, separately for the challenge (rc) and the funded account (rf). 20,000 trader-years.
"""
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(34)
NP, T, K, SPLIT, FEE, SIZE = 20000, 250, 2.0, 0.80, 540.0, 100_000


def year(e, rc, rf):
    p = (1 + e) / (1 + K)
    win = rng.random((NP, T)) < p
    state = np.zeros(NP, int); eq = np.zeros(NP); fees = np.full(NP, FEE); paid = np.zeros(NP)
    refunded = np.zeros(NP, bool); since = np.zeros(NP, int); funded_days = np.zeros(NP)
    for t in range(T):
        r = np.where(state < 2, rc, rf)
        eq += np.where(win[:, t], K * r, -r)
        lost = (eq <= -0.10) | (r >= 0.05) & ~win[:, t]
        # challenge phases
        p1 = (state == 0) & ~lost & (eq >= 0.10); p2 = (state == 1) & ~lost & (eq >= 0.05)
        state = np.where(p1, 1, state); state = np.where(p2, 2, state)
        eq = np.where(p1 | p2, 0.0, eq); since = np.where(p2, 0, since)
        # funded payouts
        f = state == 2
        funded_days += f & ~lost
        since = np.where(f, since + 1, since)
        can = f & ~lost & (since % 10 == 0) & (eq >= 0.005)
        paid += np.where(can, eq * SPLIT * SIZE, 0)
        fees -= np.where(can & ~refunded, FEE, 0); refunded |= can
        eq = np.where(can, 0.0, eq)
        # breach -> new challenge
        fees += np.where(lost, FEE, 0); refunded = np.where(lost, False, refunded)
        state = np.where(lost, 0, state); eq = np.where(lost, 0.0, eq)
    net = paid - fees
    return net, funded_days


def pass_rate(e, r, n=20000):
    p = (1 + e) / (1 + K)
    x = np.where(rng.random((n, 3000)) < p, K * r, -r)
    ok = np.ones(n, bool); start = np.zeros(n, int)
    for tgt in (0.10, 0.05):
        eq = np.zeros(n); res = np.zeros(n, bool); done = np.zeros(n, bool)
        for t in range(1500):
            col = x[:, t + (0 if tgt == 0.10 else 1500)]
            act = ok & ~done; eq = np.where(act, eq + col, eq)
            hit = act & (eq >= tgt); die = act & ((eq <= -0.10) | ((r >= 0.05) & (col < 0)))
            res |= hit; done |= hit | die
        ok &= res
    return ok.mean()


print("FTMO blog check: 2-step pass rate (no time limit) by edge and risk")
print("  edge R  | 0.5%  1.0%  2.0%  3.0%")
for e in (-0.10, 0.0, 0.10, 0.20, 0.30):
    print(f"  {e:+.2f}   | " + "  ".join(f"{pass_rate(e, r):4.0%}" for r in (0.005, 0.01, 0.02, 0.03)))

print("\nTrader-year net $ (payouts - fees), mean / median / P(net<0) / funded days, by challenge risk rc x funded risk rf")
for e in (-0.10, 0.0, 0.10, 0.20):
    print(f"\nedge {e:+.2f}R per trade")
    print("   rc \\ rf  |" + "|".join(f"{'rf ' + format(rf, '.1%'):^34s}" for rf in (0.005, 0.01, 0.02)))
    for rc in (0.005, 0.01, 0.02, 0.03):
        cells = []
        for rf in (0.005, 0.01, 0.02):
            net, fd = year(e, rc, rf)
            cells.append(f" {net.mean():+7,.0f} / {np.median(net):+7,.0f} / {np.mean(net < 0):3.0%} / {fd.mean():3.0f}d ")
        print(f"   rc {rc:4.1%} |" + "|".join(cells))
