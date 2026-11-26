"""Verify Mulham 'Math of Winning in Prop Firms' claims and extend 09 with trailing drawdown.
Account: 50k futures-style: target +3000 (6%), max loss 2000 (4%).
Drawdown types: static / intraday-trailing (trails peak equity) / EOD-trailing (trails peak end-of-day balance).
Trailing stops trailing once the floor reaches the starting balance (common futures-prop rule).
Strategies have EQUAL expectancy (+0.15R) but different win rate / payoff (variance).
"""
import random

random.seed(11)
START, TARGET, MAXLOSS = 50_000, 3_000, 2_000


def run(wr, rr, risk, dd_type, trades_per_day=3, max_days=60, trials=20_000):
    passed = 0
    for _ in range(trials):
        bal = START
        peak_eq = START
        peak_eod = START
        floor = START - MAXLOSS
        done = False
        for _day in range(max_days):
            for _ in range(trades_per_day):
                bal += risk * rr if random.random() < wr else -risk
                if dd_type == "intraday":
                    peak_eq = max(peak_eq, bal)
                    floor = min(START, max(floor, peak_eq - MAXLOSS))
                if bal <= floor:
                    done = True
                    break
                if bal >= START + TARGET:
                    passed += 1
                    done = True
                    break
            if done:
                break
            if dd_type == "eod":
                peak_eod = max(peak_eod, bal)
                floor = min(START, max(floor, peak_eod - MAXLOSS))
        # timeout counts as not passed
    return passed / trials


EV = 0.15
strategies = {
    "A WR65 (low var)": (0.65, (EV + 0.35) / 0.65),
    "B WR55 (mid var)": (0.55, (EV + 0.45) / 0.55),
    "C WR35 (high var)": (0.35, (EV + 0.65) / 0.35),
}
print("== Equal EV (+0.15R), 50k: +3000 target / -2000 max loss ==")
for risk in (250, 500, 1000):
    print(f"-- risk ${risk} per trade ({risk/START:.1%} of account, {MAXLOSS/risk:.0f}R of room)")
    for name, (wr, rr) in strategies.items():
        row = [f"{dd}: {run(wr, rr, risk, dd):.1%}" for dd in ("static", "eod", "intraday")]
        print(f"   {name} RR {rr:.2f} | " + " | ".join(row))

print("\n== Zero-edge 50% 1:1 (theory: P = 2000/5000 = 40% static, no time limit) ==")
for risk in (250, 500, 1000):
    print(f"risk ${risk}: static {run(0.5, 1.0, risk, 'static', max_days=400):.1%}")

print("\n== Negative edge 40% 1:1: bigger risk -> higher pass chance (gambling) ==")
for risk in (250, 500, 1000):
    print(f"risk ${risk}: static {run(0.4, 1.0, risk, 'static'):.1%}")

print("\n== Exact-4-trade-group all losses: (1-WR)^4 ==")
for wr in (0.45, 0.55, 0.65):
    print(f"WR {wr:.0%}: {(1-wr)**4:.1%}")

print("\n== Economics: Mulham example ==")
fee, n, payouts, payout_amt = 150, 100, 6, 2000
print(f"{n} x ${fee} = ${fee*n}, payouts {payouts} x ${payout_amt} = ${payouts*payout_amt}, "
      f"net ${payouts*payout_amt - fee*n} (per challenge ${(payouts*payout_amt - fee*n)/n:.0f})")
