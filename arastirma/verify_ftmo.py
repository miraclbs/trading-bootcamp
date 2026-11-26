"""(1) P(peak-to-trough DD >= 50%) to check video's wording.
(2) Prop-challenge pass probability: hit +target before -max_loss (static from start),
    with daily loss limit, for different risk-per-trade levels and edges.
"""
import random

random.seed(7)


def p_mdd50(risk, wr=0.4, rr=2.0, n=500, trials=10_000):
    hit = 0
    for _ in range(trials):
        eq = peak = 1.0
        for _ in range(n):
            eq *= (1 + risk * rr) if random.random() < wr else (1 - risk)
            peak = max(peak, eq)
            if eq / peak <= 0.5:
                hit += 1
                break
    return hit / trials


print("== P(peak-to-trough DD >= 50% within 500 trades), WR40 RR2 ==")
for r in (0.01, 0.02, 0.05, 0.10):
    print(f"risk {r:.0%}: {p_mdd50(r):.3f}")


def challenge(risk, wr, rr, target=0.10, max_loss=0.10, daily=0.05,
              trades_per_day=2, max_days=60, trials=20_000):
    """Fixed risk as % of INITIAL balance (how most prop traders size).
    Returns (pass, fail_maxloss, fail_daily, timeout)."""
    res = [0, 0, 0, 0]
    for _ in range(trials):
        bal = 1.0
        outcome = 3
        for _ in range(max_days):
            day_start = bal
            for _ in range(trades_per_day):
                bal += risk * rr if random.random() < wr else -risk
                if bal <= 1 - max_loss + 1e-12:
                    outcome = 1
                    break
                if day_start - bal >= daily - 1e-12:
                    outcome = 2
                    break
                if bal >= 1 + target - 1e-12:
                    outcome = 0
                    break
            if outcome != 3:
                break
        res[outcome] += 1
    return [x / trials for x in res]


print("\n== Prop challenge (+10% target, -10% max, -5% daily, 2 trades/day, 60 days) ==")
for wr, rr, label in ((0.40, 2.0, "edge +0.20R"), (0.35, 2.0, "edge +0.05R"),
                      (0.33, 2.0, "~breakeven -0.01R"), (0.55, 1.0, "edge +0.10R")):
    for r in (0.005, 0.01, 0.02, 0.03):
        p, fm, fd, to = challenge(r, wr, rr)
        print(f"{label:18s} WR{wr:.0%} RR{rr} risk {r:.1%}: pass {p:.1%} | "
              f"maxloss {fm:.1%} | daily {fd:.1%} | timeout {to:.1%}")
