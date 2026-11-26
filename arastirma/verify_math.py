"""Verify statistical claims from the AlgoCoinism 'matematik' video."""
import math
import random

random.seed(42)


def binom_cdf(k, n, p):
    return sum(math.comb(n, i) * p**i * (1 - p)**(n - i) for i in range(0, k + 1))


print("== P(net loss) for WR=40%, RR=2 (EV=+0.2R) ==")
for n in (20, 100, 300):
    # net = 2W - (n-W) = 3W - n < 0  -> W < n/3
    kmax = math.ceil(n / 3) - 1
    print(f"n={n}: P(loss)={binom_cdf(kmax, n, 0.4):.3f}")


def p_streak(n, q, k, trials=200_000):
    hit = 0
    for _ in range(trials):
        run = 0
        for _ in range(n):
            if random.random() < q:
                run += 1
                if run >= k:
                    hit += 1
                    break
            else:
                run = 0
    return hit / trials


print("\n== P(at least one run of >=k losses in 100 trades), loss prob q ==")
for wr in (0.4, 0.5, 0.6):
    for k in (5, 7, 10):
        print(f"WR={wr:.0%} k={k}: {p_streak(100, 1 - wr, k, 40_000):.3f}")


def p_halve(risk, wr=0.4, rr=2.0, n=500, trials=20_000):
    """Fixed-fractional risk; probability equity ever touches <=50% of start."""
    hit = 0
    for _ in range(trials):
        eq = 1.0
        for _ in range(n):
            if random.random() < wr:
                eq *= 1 + risk * rr
            else:
                eq *= 1 - risk
            if eq <= 0.5:
                hit += 1
                break
    return hit / trials


print("\n== P(50% drawdown from start within 500 trades), WR=40% RR=2 ==")
for r in (0.005, 0.01, 0.02, 0.05, 0.10):
    print(f"risk={r:.1%}: {p_halve(r):.3f}")

print("\n== Max drawdown distribution (peak-to-trough), WR=40% RR=2, 500 trades ==")
for r in (0.005, 0.01, 0.02):
    dds = []
    for _ in range(5000):
        eq, peak, mdd = 1.0, 1.0, 0.0
        for _ in range(500):
            eq *= (1 + r * 2) if random.random() < 0.4 else (1 - r)
            peak = max(peak, eq)
            mdd = max(mdd, 1 - eq / peak)
        dds.append(mdd)
    dds.sort()
    print(f"risk={r:.1%}: median MDD={dds[2500]:.1%}, 95th pct={dds[4750]:.1%}")

print("\n== Recovery needed after loss ==")
for l in (0.1, 0.2, 0.3, 0.5, 0.65, 0.8):
    print(f"loss {l:.0%} -> need +{l/(1-l):.1%}")

print("\n== 10 consecutive losses ==")
for r in (0.01, 0.02, 0.05, 0.10):
    print(f"risk {r:.0%}: drawdown {1-(1-r)**10:.1%}")

print("\n== Breakeven WR = 1/(1+RR) ==")
for rr in (0.5, 1, 1.5, 2, 3, 4, 5):
    print(f"RR {rr}: {1/(1+rr):.1%}")

print("\n== Kelly fraction f* = WR - (1-WR)/RR ==")
for wr, rr in ((0.4, 2), (0.55, 1), (0.5, 2), (0.35, 3)):
    print(f"WR {wr:.0%} RR {rr}: full Kelly {wr-(1-wr)/rr:.1%}, half {0.5*(wr-(1-wr)/rr):.1%}")
