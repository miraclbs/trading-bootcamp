"""Round 51: Lance Breitstein, "Why Small Account Trading Challenges Are BS" (LbSn-awZmm4).
Claims: "an influencer turns $2,000 into $50,000 (25x) -> you think you can too; to go viral they must take oversized
risk / leverage / home-run swings; a responsible 20% return doesn't go viral; the challenge teaches gambling".
Questions:
 (1) What per-trade risk does a 25x run within ~1 year (250 trades) require, with and without an edge?
 (2) How many of 1,000 zero-edge attempters 'succeed' at 25x (survivorship: the ones you see on YouTube)?
 (3) What does the same per-trade risk do inside a prop account (FTMO 2-Step: -5% daily, -10% total)?
Model: RR 2 binary trades, EV per trade e (R), risk f of CURRENT equity (compounding), ruin = equity < 10% of start.
"""
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(51)
K = 2.0


def run(f, e, n_trades=250, sims=20000, target=25.0, ruin=0.10):
    p = (1 + e) / (1 + K)
    win = rng.random((sims, n_trades)) < p
    mult = np.where(win, 1 + f * K, 1 - f)
    eq = np.cumprod(mult, axis=1)
    hit_t = np.where((eq >= target).any(1), (eq >= target).argmax(1), n_trades + 1)
    ruin_t = np.where((eq <= ruin).any(1), (eq <= ruin).argmax(1), n_trades + 1)
    success = hit_t < ruin_t
    ruined = ruin_t < hit_t
    final = eq[:, -1]
    return success.mean(), ruined.mean(), np.median(final), np.mean(final < 1)


print("(1)+(2) 250 trades (~1 year), RR 2, compounding risk f of equity. Success = 25x before falling to 10%")
print("   EV/trade |  risk f | P(25x)  | P(ruin <10%) | median final | P(final < start)")
for e in (0.0, 0.10, 0.20):
    for f in (0.01, 0.03, 0.05, 0.10, 0.20, 0.33):
        s, r, med, lose = run(f, e)
        print(f"   {e:+.2f}R   | {f:6.0%} | {s:6.2%} | {r:11.1%} | {med:10.2f}x | {lose:6.1%}")
    print()

print("   Zero-edge attempters needed per visible 25x 'success' at 20% risk: "
      f"~{1 / max(run(0.20, 0.0)[0], 1e-9):.0f}; at 33% risk: ~{1 / max(run(0.33, 0.0)[0], 1e-9):.0f}")

print("\n(3) The same risk per trade inside a prop account (FTMO 2-Step style: target +10%, -5% daily, -10% total,")
print("    2 trades/day, fixed risk of initial balance). P(pass) / P(breach), 2,000 trading days cap")
for e in (0.0, 0.20):
    for f in (0.01, 0.05, 0.10, 0.20):
        p = (1 + e) / (1 + K)
        passed = breached = 0
        for _ in range(20000):
            bal = 1.0
            for day in range(2000):
                start = bal
                for _t in range(2):
                    bal += f * (K if rng.random() < p else -1.0)
                    if bal <= start - 0.05 or bal <= 0.90 or bal >= 1.10:
                        break
                if bal <= start - 0.05 or bal <= 0.90:
                    breached += 1; break
                if bal >= 1.10:
                    passed += 1; break
        print(f"   EV {e:+.2f}R, risk {f:4.0%}: pass {passed / 20000:5.1%} | breach {breached / 20000:5.1%}")
