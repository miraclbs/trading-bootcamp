"""Round 3 checks.
(A) Wilksey: WR30 / RR3 (EV +0.2R), phase 1 +10% / max loss 10% static. Risk 1% vs 2%:
    claimed pass 77% / 63%, avg trades to pass ~30 (median 22) vs ~10.
(B) Kimmel 'normal' formula: risk = (MaxDD/2)/trades_per_week -> failing needs ~2 weeks of all losses.
    Check P(fail) for FTMO 10% DD, 5 trades/week (risk 1%) for WR 30/40/50% at the strategy's RR,
    plus expected time to pass.
"""
import random
import statistics

random.seed(9)


def phase(wr, rr, target_r, dd_r, max_trades=2000):
    """Return (passed, trades) for target/dd in R units (static)."""
    eq = 0.0
    for t in range(1, max_trades + 1):
        eq += rr if random.random() < wr else -1
        if eq <= -dd_r:
            return False, t
        if eq >= target_r:
            return True, t
    return False, max_trades


def report(label, wr, rr, target_r, dd_r, trials=40_000):
    res = [phase(wr, rr, target_r, dd_r) for _ in range(trials)]
    passed = [t for p, t in res if p]
    p = len(passed) / trials
    print(f"{label}: pass {p:.1%} | trades-to-pass mean {statistics.mean(passed):.1f}, "
          f"median {statistics.median(passed):.0f}")


print("== (A) Wilksey WR30 RR3, +10% / -10% ==")
report("risk 1% (10R/10R)", 0.30, 3.0, 10, 10)
report("risk 2% (5R/5R) ", 0.30, 3.0, 5, 5)
print("theory expected trades (drift only) at 1%: 10/0.2 = 50")

print("\n== (B) Kimmel normal: FTMO 10% DD, 5 trades/week -> risk 1% (10R room), target 10R ==")
for wr, rr in ((0.30, 3.0), (0.40, 2.0), (0.50, 1.5), (0.55, 1.2)):
    report(f"WR{wr:.0%} RR{rr} (EV {wr*rr-(1-wr):+.2f}R)", wr, rr, 10, 10)
