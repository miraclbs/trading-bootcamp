"""Test dynamic risk rules from Kimmel's 'Top 5 prop traders' video vs fixed risk.
FTMO-style phase 1: +10% target, -10% static max loss, base risk 1% of initial.
Rules:
 fixed      : always 1%
 halve_dd   : (Kyle) below starting balance -> 0.5%; at/above start -> 1%
 halve_loss : (Kyle variant) after each loss halve (min 0.25%), after a win reset to 1%
 cut_after4 : (Dan Chong) after >=4 consecutive losses -> 0.5% until back to starting balance
 double_win : (Kyle 'if you win you can double') above start -> 2%, below start -> 0.5%
"""
import random
import statistics

random.seed(21)


def run(wr, rr, rule, max_trades=300):
    eq, streak = 0.0, 0  # equity in % of initial
    risk = 1.0
    for t in range(1, max_trades + 1):
        if rule == "fixed":
            risk = 1.0
        elif rule == "halve_dd":
            risk = 0.5 if eq < 0 else 1.0
        elif rule == "cut_after4":
            if streak >= 4:
                risk = 0.5
            elif eq >= 0:
                risk = 1.0
        elif rule == "double_win":
            risk = 2.0 if eq > 0 else (0.5 if eq < 0 else 1.0)
        win = random.random() < wr
        eq += risk * rr if win else -risk
        if rule == "halve_loss":
            risk = 1.0 if win else max(0.25, risk / 2)
        streak = 0 if win else streak + 1
        if eq <= -10:
            return False, t
        if eq >= 10:
            return True, t
    return None, max_trades


rules = ["fixed", "halve_dd", "halve_loss", "cut_after4", "double_win"]
for wr, rr in ((0.30, 3.0), (0.40, 2.0), (0.55, 1.2), (0.33, 2.0)):
    print(f"\n== WR {wr:.0%} RR {rr} (EV {wr*rr-(1-wr):+.2f}R), phase 1 +10/-10, 300-trade cap ==")
    for rule in rules:
        res = [run(wr, rr, rule) for _ in range(30_000)]
        p = sum(1 for r, _ in res if r) / len(res)
        f = sum(1 for r, _ in res if r is False) / len(res)
        tp = [t for r, t in res if r]
        print(f" {rule:11s}: pass {p:.1%} | fail {f:.1%} | timeout {1-p-f:.1%} | "
              f"median trades to pass {statistics.median(tp):.0f}")
