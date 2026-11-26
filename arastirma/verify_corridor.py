"""Round 38: Syndicate001 "16.8% Pass. 1 in 3 Get Paid. The Prop Firm Math Nobody Shows You" (-BF_X7tSkQY).
Claims (50k futures evaluation, target +3,000, max loss 2,000; zero-edge 1:1 strategy, $300 risk, 2 trades/day):
 (a) random-walk corridor ceiling: P(target first) = 2000/5000 = 40%; with lumpy trades ~38%
 (b) end-of-day trailing max loss -> ~25%
 (c) + costs of 3% of risk per trade -> ~15% ("Topstep's real 16.8% = a zero-edge strategy paying normal costs")
 (d) geometry sweep (zero edge, $300 risk): without costs ~27% flat (trailing case); with 3% costs high win rate /
     tight target collapses (<5%) while low win rate / big target holds >20%.
Trailing model: floor = max(start-2000, highest END-OF-DAY balance - 2000), stops trailing at start (+0) as Topstep's
MLL locks at the starting balance. Paths: 40,000 per cell, up to 400 trading days.
"""
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(38)
N, DAYS, TPD = 40000, 400, 2


def run(win_rr, risk=300.0, cost_frac=0.0, trailing=False, edge=0.0):
    k = win_rr; p = (1 + edge) / (1 + k)              # zero gross edge when edge = 0
    bal = np.zeros(N); floor = np.full(N, -2000.0); alive = np.ones(N, bool); passed = np.zeros(N, bool)
    peak_eod = np.zeros(N); trades = np.zeros(N)
    for d in range(DAYS):
        for _ in range(TPD):
            w = rng.random(N) < p
            pnl = np.where(w, k * risk, -risk) - cost_frac * risk
            bal = np.where(alive, bal + pnl, bal); trades += alive
            hit = alive & (bal >= 3000); die = alive & (bal <= floor)
            passed |= hit; alive &= ~(hit | die)
        if trailing:
            peak_eod = np.where(alive, np.maximum(peak_eod, bal), peak_eod)
            floor = np.where(alive, np.minimum(np.maximum(floor, peak_eod - 2000), 0.0), floor)
        if not alive.any():
            break
    return passed.mean(), np.median(trades)


print("Zero-edge 1:1, $300 risk, 2 trades/day, target +3000, max loss 2000")
for lab, kw in (("static, no cost", {}), ("EOD trailing, no cost", {"trailing": True}),
                ("EOD trailing + 3% cost", {"trailing": True, "cost_frac": 0.03})):
    p, t = run(1.0, **kw)
    print(f"  {lab:24s}: pass {p:.1%} (median trades {t:.0f})")
print("\nGeometry sweep (zero edge, $300 risk, EOD trailing): pass without cost / with 3% cost")
for k in (0.25, 0.33, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0):
    p0, _ = run(k, trailing=True); p1, t1 = run(k, trailing=True, cost_frac=0.03)
    print(f"  target {k:4.2f}R (win rate {1 / (1 + k):3.0%}): {p0:5.1%} / {p1:5.1%}  (median trades with cost {t1:.0f})")
print("\nRisk size ('a seventh of the drawdown' = ~$285): EOD trailing + 3% cost, 1:1")
for risk in (100, 200, 285, 400, 600):
    p, t = run(1.0, risk=risk, trailing=True, cost_frac=0.03)
    print(f"  risk ${risk:3d}: pass {p:.1%}, median trades {t:.0f}")
print("\nWith a small real edge (+3 win-rate points at 1:1 = +0.06R gross), EOD trailing + 3% cost, $285 risk")
for e in (0.0, 0.06, 0.10, 0.20):
    p, t = run(1.0, risk=285, trailing=True, cost_frac=0.03, edge=e)
    print(f"  gross edge {e:+.2f}R: pass {p:.1%}, median trades {t:.0f}")
