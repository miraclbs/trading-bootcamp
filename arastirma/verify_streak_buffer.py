"""Prop roundtable claim (Words of Rizdom ps5In64-2So): "If you give yourself only five losing trades before you blow
the account, you're likely to blow the account." Exact probability of at least one run of >= k consecutive losses
in n trades (iid, win rate WR), by dynamic programming. Used to size the trailing-drawdown buffer in R units."""
import sys
import numpy as np
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def p_run(n, k, q):  # q = loss prob; P(at least one run of >=k losses in n trials)
    # state: current run length 0..k-1 ; absorbing 'hit'
    s = np.zeros(k); s[0] = 1.0; hit = 0.0
    for _ in range(n):
        new = np.zeros(k)
        new[0] = s.sum() * (1 - q)
        new[1:] = s[:-1] * q
        hit += s[-1] * q
        s = new
    return hit

print("P(at least one losing streak of >= k trades) | rows: win rate, cols: k ; n = number of trades")
for n in (40, 100, 250):
    print(f"\nn = {n} trades")
    print("  WR   " + "".join(f"  k={k:<3d}" for k in (3, 5, 7, 10, 12)))
    for wr in (0.35, 0.45, 0.55, 0.65, 0.75):
        print(f"  {wr:.0%}  " + "".join(f"  {p_run(n, k, 1 - wr):5.0%}" for k in (3, 5, 7, 10, 12)))
