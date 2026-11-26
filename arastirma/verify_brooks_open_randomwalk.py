"""Random-walk baseline for Brooks' opening claims (Grimes-style check).
78 five-minute bars, each bar = 30 Gaussian sub-steps (so bars have intrabar high/low).
"""
import random
random.seed(1)
CHECKS = (1, 7, 12, 18, 24)
N, SUB, T = 78, 30, 20000
formed = {k: 0 for k in CHECKS}
brk = held = 0
for _ in range(T):
    p = 0.0
    highs, lows = [], []
    for _b in range(N):
        h = l = p
        for _s in range(SUB):
            p += random.gauss(0, 1)
            h = max(h, p); l = min(l, p)
        highs.append(h); lows.append(l)
    hi = max(range(N), key=lambda i: highs[i]); lo = min(range(N), key=lambda i: lows[i])
    fe = min(hi, lo)
    for k in CHECKS:
        if fe < k:
            formed[k] += 1
    h18, l18 = max(highs[:18]), min(lows[:18])
    up = next((i for i in range(18, N) if highs[i] > h18), None)
    dn = next((i for i in range(18, N) if lows[i] < l18), None)
    if up is None and dn is None:
        continue
    brk += 1
    if dn is None or (up is not None and up < dn):
        held += int(min(lows[up:]) >= l18)
    else:
        held += int(max(highs[dn:]) <= h18)
print("RANDOM WALK | P(high or low of day already set) " + " | ".join(f"bar {k}: {formed[k]/T:.0%}" for k in CHECKS))
print(f"RANDOM WALK | 18-bar range broken {brk/T:.0%} of days; opposite extreme held after first break {held/brk:.0%}")
