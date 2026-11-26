"""Round 39: FTMO 1-Step vs 2-Step challenge (rules read 2026-11-22 from ftmo.com/en/trading-objectives/):
 2-Step: phase 1 +10%, phase 2 +5%, max daily loss 5%, max loss 10% STATIC (from initial).
 1-Step: one phase +10%, max daily loss 3%, max loss 10% END-OF-DAY TRAILING: limit = highest 00:00 balance (or
         initial if higher) - 10% of initial, "can only increase, never decrease" (no cap at the initial balance);
         Consistency (orders from 12 Oct 2026): best day <= 50% of total profit - not a breach, you keep trading until
         it is met.
Model: RR 2, win prob (1+e)/3 -> e R per trade after costs; risk % of initial; 1 or 2 trades per day; daily loss
measured from the day's start balance (closed trades only, no intra-trade drawdown -> optimistic); no time limit
(cap 600 trading days). 30,000 paths per cell.
Theory check: driftless walk, target a before a drawdown of d from the running max -> P = exp(-a/d) = 37% (vs 50%
for a static floor at the same distance) - ignoring the daily limit and discreteness.
"""
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(39)
N, DAYS, K = 30000, 600, 2.0


def phase(e, r, tpd, target, daily, trailing, consistency):
    p = (1 + e) / (1 + K)
    eq = np.zeros(N); floor = np.full(N, -0.10); alive = np.ones(N, bool); passed = np.zeros(N, bool)
    peak_eod = np.zeros(N); best_day = np.zeros(N); days = np.full(N, DAYS)
    for d in range(DAYS):
        start = eq.copy()
        for _ in range(tpd):
            pnl = np.where(rng.random(N) < p, K * r, -r)
            eq = np.where(alive, eq + pnl, eq)
            die = alive & ((eq <= floor) | (start - eq >= daily - 1e-12))
            alive &= ~die
        day_pnl = eq - start
        best_day = np.where(alive, np.maximum(best_day, day_pnl), best_day)
        ok_cons = (best_day <= 0.5 * eq) if consistency else True
        hit = alive & (eq >= target) & ok_cons
        passed |= hit; days[hit] = d + 1; alive &= ~hit
        if trailing:
            peak_eod = np.where(alive, np.maximum(peak_eod, eq), peak_eod)
            floor = np.where(alive, np.maximum(floor, peak_eod - 0.10), floor)
        if not alive.any():
            break
    return passed, days


def two_step(e, r, tpd):
    a, d1 = phase(e, r, tpd, 0.10, 0.05, False, False)
    b, d2 = phase(e, r, tpd, 0.05, 0.05, False, False)
    ok = a & b
    return ok.mean(), np.median((d1 + d2)[ok]) if ok.any() else np.nan


def one_step(e, r, tpd, consistency=True):
    ok, d = phase(e, r, tpd, 0.10, 0.03, True, consistency)
    return ok.mean(), np.median(d[ok]) if ok.any() else np.nan


print("Pass rate (median trading days to pass). RR 2. 2-Step = both phases; 1-Step with consistency rule")
for tpd in (1, 2):
    print(f"\n{tpd} trade(s) per day")
    print("  edge R | risk  | 2-Step            | 1-Step            | 1-Step w/o consistency")
    for e in (-0.10, 0.0, 0.10, 0.20):
        for r in (0.005, 0.01, 0.015):
            p2, d2 = two_step(e, r, tpd); p1, d1 = one_step(e, r, tpd); p1n, _ = one_step(e, r, tpd, False)
            print(f"  {e:+.2f}  | {r:4.1%} | {p2:5.1%} ({d2:4.0f}d)    | {p1:5.1%} ({d1:4.0f}d)    | {p1n:5.1%}")
