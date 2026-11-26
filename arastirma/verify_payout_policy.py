"""Round 33: payout policy on a funded prop account.
Sources: Kimmel Trading "How I received 200+ Payouts" (90ozA2Ts4FU): "lock in a small payout as soon as possible
(it refunds the fee), then rotate; even if you are not profitable you can make money from prop firms".
NinjaTrader Prop (GVdkt_EI26Q) / Phidias (N3bpg-Hiqos): after a payout the balance drops while the drawdown floor
may stay; many futures firms keep a non-withdrawable buffer.
Questions:
 (1) Does the payout threshold (withdraw at +0.5% / +2% / +5%) change expected total payouts per funded account?
     Theory for a driftless walk with a static floor and balance reset after each payout: expected total withdrawn
     = the buffer (optional stopping), whatever the threshold. With negative drift, earlier withdrawal should help.
 (2) How much does the account type matter: A) FTMO-like static -10% from initial, payout resets balance to start;
     B) futures-like end-of-day trailing 5% that locks at start+0.2%, only profit above start+5.2% withdrawable.
 (3) Net EV per challenge attempt (fee 540 for 100k, refunded with the first payout, FTMO-like 2-step pass needed).
Trades: RR 2 fixed, win prob p = (1+e)/3 so expected R per trade = e (after costs). 1 trade per day, payout check
every 10 trades (~2 weeks). Horizon: 500 trades (~2 years) on the funded account. 20,000 paths per cell.
"""
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(33)
NP, HORIZON, K, SPLIT, FEE, SIZE = 20000, 500, 2.0, 0.80, 540.0, 100_000


def outcomes(e, r, n):
    p = (1 + e) / (1 + K)
    return np.where(rng.random((NP, n)) < p, K * r, -r)


def pass_rate(e, r):
    """FTMO-like 2-step: +10% then +5%, -10% static, -5% daily (1 trade/day so a single loss never breaches daily)."""
    x = outcomes(e, r, 1500)
    ok = np.ones(NP, bool)
    for tgt in (0.10, 0.05):
        eq = np.zeros(NP); done = np.zeros(NP, bool); res = np.zeros(NP, bool)
        for t in range(750):
            act = ok & ~done
            if not act.any():
                break
            eq = np.where(act, eq + x[:, t + (0 if tgt == 0.10 else 750)], eq)
            hit = act & (eq >= tgt); die = act & (eq <= -0.10)
            res |= hit; done |= hit | die
        ok &= res
    return ok.mean()


def funded(e, r, model, thr):
    x = outcomes(e, r, HORIZON)
    bal = np.zeros(NP); alive = np.ones(NP, bool); paid = np.zeros(NP); npay = np.zeros(NP)
    peak_eod = np.zeros(NP); floor = np.full(NP, -0.10 if model == "A" else -0.05)
    life = np.full(NP, HORIZON)
    for t in range(HORIZON):
        bal = np.where(alive, bal + x[:, t], bal)
        if model == "B":                                      # end-of-day trailing, locks at +0.2%
            peak_eod = np.where(alive, np.maximum(peak_eod, bal), peak_eod)
            floor = np.where(alive, np.minimum(np.maximum(floor, peak_eod - 0.05), 0.002), floor)
        dead = alive & (bal <= floor)
        life[dead] = t + 1; alive &= ~dead
        if (t + 1) % 10 == 0:
            if model == "A":
                can = alive & (bal >= thr)
                paid += np.where(can, bal * SPLIT, 0); npay += can; bal = np.where(can, 0.0, bal)
            else:
                can = alive & (bal >= 0.052 + thr)
                paid += np.where(can, (bal - 0.052) * SPLIT, 0); npay += can; bal = np.where(can, 0.052, bal)
    return paid * SIZE, npay, life


print("Funded-account payouts per account (100k, 80% split, RR 2, 1 trade/day, 500-trade horizon)")
print("model A = static -10%, balance reset after payout | B = EOD trailing 5% locking at +0.2%, 5.2% buffer kept")
print(f"{'edge R':>7s} {'risk':>5s} {'model':>5s} {'thr':>5s} | mean payouts $ | P(>=1 payout) | median payouts n | "
      f"median life (trades) || pass 2-step | net EV per attempt $")
for e in (-0.10, -0.05, 0.0, 0.10):
    for r in (0.005, 0.01, 0.02):
        pr = pass_rate(e, r)
        for model, thr in (("A", 0.005), ("A", 0.02), ("A", 0.05), ("B", 0.005)):
            paid, npay, life = funded(e, r, model, thr)
            first = npay >= 1
            ev = pr * (paid.mean() + FEE * first.mean()) - FEE
            print(f"{e:+7.2f} {r:5.1%} {model:>5s} {thr:5.1%} | {paid.mean():14,.0f} | {first.mean():13.0%} | "
                  f"{np.median(npay):16.0f} | {np.median(life):20.0f} || {pr:11.0%} | {ev:+,.0f}")
    print()


def funded_b(e, r, dd, thr=0.005):
    """model B with a chosen trailing size dd (buffer dd+0.2%), to separate 'trailing' from 'smaller buffer'"""
    x = outcomes(e, r, HORIZON)
    bal = np.zeros(NP); alive = np.ones(NP, bool); paid = np.zeros(NP); npay = np.zeros(NP)
    peak = np.zeros(NP); floor = np.full(NP, -dd)
    for t in range(HORIZON):
        bal = np.where(alive, bal + x[:, t], bal)
        peak = np.where(alive, np.maximum(peak, bal), peak)
        floor = np.where(alive, np.minimum(np.maximum(floor, peak - dd), 0.002), floor)
        alive &= ~(bal <= floor)
        if (t + 1) % 10 == 0:
            can = alive & (bal >= dd + 0.002 + thr)
            paid += np.where(can, (bal - dd - 0.002) * SPLIT, 0); npay += can
            bal = np.where(can, dd + 0.002, bal)
    return paid * SIZE, npay


print("Separating trailing vs buffer size (risk 1%, thr 0.5%): mean payouts $ / P(>=1 payout)")
for e in (0.0, 0.10):
    pa, na, _ = funded(e, 0.01, "A", 0.005)
    p5, n5 = funded_b(e, 0.01, 0.05); p10, n10 = funded_b(e, 0.01, 0.10)
    print(f"  edge {e:+.2f}: A static 10% {pa.mean():,.0f} / {np.mean(na >= 1):.0%} | B trailing 10% {p10.mean():,.0f} / "
          f"{np.mean(n10 >= 1):.0%} | B trailing 5% {p5.mean():,.0f} / {np.mean(n5 >= 1):.0%}")
