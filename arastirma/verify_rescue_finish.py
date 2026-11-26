"""Round 52: Saul Lokier (CEO, The5ers), Titans of Tomorrow (dFZgmVGUmlM):
 "A funny pattern: when traders go into drawdown they take one very large trade (risk-wise) -> daily or max loss.
  Same near the target: 2% away, they take a large trade, they want it quick -> they go down. Traders that keep a
  consistent lot size / risk perform better and get payouts."
Question: does switching to a big 'rescue' or 'finish' trade change P(pass)? Theory (Dubins-Savage): in a
favourable game timid play maximises P(reaching the target); in an unfavourable game BOLD play does. So the answer
should depend on the trader's edge.
Model: 2-Step style phase (target +10%, max loss -10% static, daily loss -5% from day-start balance), RR 2 binary
trades, 2 trades/day, base risk 1% of initial. Variants:
  constant   : always 1%
  rescue     : when equity <= -6%, the next trade risks 3%
  finish     : when within 2% of target, the next trade risks 3% ("they take a large trade, they want it quick")
  both       : rescue + finish
  'tilt'     : after 2 losses in a row, double risk until a win (inconsistent lot size)
EV per trade: -0.10R (typical after costs), 0, +0.10R, +0.20R. 20,000 runs, 1,000-day cap.
"""
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(52)
K = 2.0


def phase(e, mode, sims=20000):
    p = (1 + e) / (1 + K)
    passed = 0; trades_used = []
    for _ in range(sims):
        bal = 0.0; n = 0; streak = 0; done = False; tilt_mult = 1.0
        for _day in range(1000):
            day_start = bal
            for _t in range(2):
                r = 0.01 * tilt_mult if mode == "tilt" else 0.01
                if mode in ("rescue", "both") and bal <= -0.06:
                    r = 0.03
                if mode in ("finish", "both") and 0.10 - bal <= 0.02:
                    r = 0.03  # a large trade to finish quickly (CEO: "they want it quick")
                # cannot risk beyond the remaining daily allowance in a single trade? -> traders often do; keep it
                win = rng.random() < p
                bal += r * K if win else -r
                n += 1
                if mode == "tilt":
                    streak = 0 if win else streak + 1
                    tilt_mult = 1.0 if win else (2.0 if streak >= 2 else tilt_mult)
                if bal >= 0.10 - 1e-12:
                    passed += 1; done = True; break
                if bal <= -0.10 or bal <= day_start - 0.05:
                    done = True; break
            if done:
                break
        trades_used.append(n)
    return passed / sims, np.median(trades_used)


print("P(pass) by behaviour and edge (2-Step phase: +10% target, -10% static, -5% daily, RR 2, 2 trades/day)")
print("   EV/trade | constant 1% | rescue (3% at -6%) | finish (3% when <=2% from target) | both | tilt (2x after 2 losses)")
for e in (-0.10, 0.0, 0.10, 0.20):
    cells = []
    for mode in ("constant", "rescue", "finish", "both", "tilt"):
        pp, med = phase(e, mode)
        cells.append(f"{pp:6.1%}")
    print(f"   {e:+.2f}R   | " + " | ".join(cells))
