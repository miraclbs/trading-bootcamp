"""Optimal risk per trade for a 2-phase FTMO-style challenge INCLUDING the funded phase.
Resolves the Photon Trading ("go aggressive, pass 3x faster") vs SharpeEdge ("too much leverage kills funded EV") conflict.

Model (per trader-year, 120 trades = ~10 trades/month, as in Photon's example):
- Challenge: Phase 1 +10%, Phase 2 +5%, max loss 10% static from initial, daily loss 5%.
- Fee $500 for 100k; refunded with first payout. On failure: buy a new challenge.
- Funded: same risk; every 10 trades (≈monthly) withdraw 80% of profit above 100k (balance reset to 100k).
  Account lost if equity <= 90k -> buy a new challenge.
- Risk is % of INITIAL balance (fixed $), trades are i.i.d. win/loss with fixed RR.
"""
import random

random.seed(5)
INIT, FEE, SPLIT = 100_000, 500, 0.80


def trader_year(wr, rr, risk_pct, trades=120, trades_per_day=1):
    risk = INIT * risk_pct
    fees = payouts = 0.0
    state, bal, day_start, n_in_day, since_payout, paid_once = "p1", INIT, INIT, 0, 0, False
    fees += FEE
    for _ in range(trades):
        if n_in_day == 0:
            day_start = bal
        bal += risk * rr if random.random() < wr else -risk
        n_in_day = (n_in_day + 1) % trades_per_day
        breached = bal <= INIT * 0.90 + 1e-9 or (day_start - bal) >= INIT * 0.05 - 1e-9
        if state in ("p1", "p2"):
            if breached:
                fees += FEE
                state, bal, n_in_day = "p1", INIT, 0
                continue
            target = 0.10 if state == "p1" else 0.05
            if bal >= INIT * (1 + target) - 1e-9:
                state = "p2" if state == "p1" else "funded"
                bal, n_in_day, since_payout = INIT, 0, 0
        else:  # funded
            if breached:
                fees += FEE
                state, bal, n_in_day = "p1", INIT, 0
                continue
            since_payout += 1
            if since_payout >= 10 and bal > INIT:
                payouts += (bal - INIT) * SPLIT
                if not paid_once:
                    payouts += FEE  # refund
                    paid_once = True
                bal, since_payout = INIT, 0
    return payouts - fees, fees, payouts


def summarize(wr, rr, label, tpd=1, trials=6000):
    print(f"\n== {label}: WR {wr:.0%} RR {rr} (EV {wr*rr-(1-wr):+.2f}R), {tpd} trade/day ==")
    print(" risk | mean net/yr | median net | P(net<0) | avg fees | avg payouts")
    for r in (0.0025, 0.005, 0.01, 0.015, 0.02, 0.03, 0.05):
        res = [trader_year(wr, rr, r, trades_per_day=tpd) for _ in range(trials)]
        nets = sorted(x[0] for x in res)
        mean = sum(nets) / trials
        neg = sum(1 for x in nets if x < 0) / trials
        fees = sum(x[1] for x in res) / trials
        pays = sum(x[2] for x in res) / trials
        print(f" {r:5.2%} | {mean:11,.0f} | {nets[trials//2]:10,.0f} | {neg:7.1%} | {fees:8,.0f} | {pays:10,.0f}")


summarize(0.40, 2.0, "Good edge (Photon example)")
summarize(0.35, 2.0, "Backtest WR overestimated by 5pts (live reality)")
summarize(0.333, 2.0, "Zero edge")
summarize(0.40, 2.0, "Good edge but 2 trades/day (daily 5% limit bites)", tpd=2)
