"""Round 31: PipBack "Ex-Prop Firm Owner Tells You How to Pass an Evaluation (Data-based)" (WWulQ4Mi0fM).
The video compares PASSED vs BREACHED accounts of a CFD prop firm:
  22% pass phase 1 | passed 2.5-3 trades/day vs breached 8-9 | passed avg RR ~2.5 and 60-80% have win rate >= 50%
  | passed take ~9 days, breached 5-7 days | 70% of breached are scalpers.
Question: how much of this "winner profile" would appear even if NOBODY had skill (pure luck + risk choices)?
Population sim: traders with heterogeneous risk/trade, trades/day and TP:SL ratio. Each trade = +k*risk or -risk,
win prob p = (1+e)/(1+k) so the expected R per trade = e. Costs (spread/commission/slippage) = 0.05R per trade.
Scenario A: nobody has skill (e = -0.05 for all). Scenario B: 20% of traders have skill +0.20R (e = +0.15).
Phase 1 rules: +10% target, -10% static max loss (equity), -5% daily loss from the day's start balance,
30 calendar days (~22 trading days) like the classic FTMO-style challenge, and a no-limit variant (cap 250 days).
Report: pass rate, passed vs breached profile, and how informative passing is about skill.
"""
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(31)
N = 40000
RISKS = np.array([0.0025, 0.005, 0.01, 0.02, 0.03, 0.04])
FREQS = np.array([1, 2, 3, 5, 8, 10])
RRS = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
COST = 0.05


def simulate(skill_share, skill, max_days):
    risk = rng.choice(RISKS, N, p=[.05, .15, .30, .25, .15, .10])
    freq = rng.choice(FREQS, N, p=[.15, .20, .20, .20, .15, .10])
    k = rng.choice(RRS, N)
    skilled = rng.random(N) < skill_share
    e = np.where(skilled, skill, 0.0) - COST
    p = (1 + e) / (1 + k)
    eq = np.zeros(N); alive = np.ones(N, bool); res = np.full(N, "time", dtype=object)
    days = np.zeros(N); ntr = np.zeros(N); nwin = np.zeros(N)
    for d in range(max_days):
        start = eq.copy()
        for t in range(FREQS.max()):
            m = alive & (t < freq)
            if not m.any():
                break
            win = rng.random(N) < p
            pnl = np.where(win, k * risk, -risk)
            eq = np.where(m, eq + pnl, eq)
            ntr += m; nwin += m & win
            breach = m & ((eq <= -0.10) | (eq - start <= -0.05))
            passed = m & ~breach & (eq >= 0.10)
            res[breach] = "breach"; res[passed] = "pass"
            days[breach | passed] = d + 1
            alive &= ~(breach | passed)
        if not alive.any():
            break
    days[res == "time"] = max_days
    wr = np.divide(nwin, ntr, out=np.zeros(N), where=ntr > 0)
    real_r = np.divide(nwin * k - (ntr - nwin), ntr, out=np.zeros(N), where=ntr > 0)
    return dict(risk=risk, freq=freq, k=k, skilled=skilled, res=res, days=days, wr=wr, real_r=real_r)


def report(tag, s):
    res = s["res"]
    print(f"\n=== {tag} ===")
    print(f"  phase-1 pass {np.mean(res == 'pass'):.0%} | breach {np.mean(res == 'breach'):.0%} | "
          f"time-out {np.mean(res == 'time'):.0%}")
    print("  profile            passed    breached")
    for lab, key, fmt in (("trades/day", "freq", "{:.1f}"), ("risk/trade", "risk", "{:.2%}"),
                          ("planned RR (TP:SL)", "k", "{:.2f}"), ("days to end", "days", "{:.1f}"),
                          ("realised win rate", "wr", "{:.0%}"), ("realised R/trade", "real_r", "{:+.2f}")):
        a = s[key][res == "pass"].mean(); b = s[key][res == "breach"].mean()
        print(f"  {lab:18s} {fmt.format(a):>8s}  {fmt.format(b):>8s}")
    hi = (s["k"] >= 2.5) & (res == "pass")
    print(f"  passers with planned RR>=2.5: {np.mean(s['k'][res == 'pass'] >= 2.5):.0%}; of those, realised win rate >= 50%:"
          f" {np.mean(s['wr'][hi] >= 0.5):.0%}  (a 2.5R trader with no skill wins ~27% of trades)")
    print("  pass rate by risk/trade :", "  ".join(f"{r:.2%}:{np.mean(res[s['risk'] == r] == 'pass'):.0%}" for r in RISKS))
    print("  pass rate by trades/day :", "  ".join(f"{f}:{np.mean(res[s['freq'] == f] == 'pass'):.0%}" for f in FREQS))
    print("  pass rate by planned RR :", "  ".join(f"{k}:{np.mean(res[s['k'] == k] == 'pass'):.0%}" for k in RRS))
    if s["skilled"].any():
        print(f"  skilled share: population {s['skilled'].mean():.0%} -> among passers {s['skilled'][res == 'pass'].mean():.0%}"
              f" -> among breached {s['skilled'][res == 'breach'].mean():.0%}")
        for r in (0.005, 0.01, 0.04):
            m = s["risk"] == r
            print(f"    at risk {r:.1%}: skilled pass {np.mean(res[m & s['skilled']] == 'pass'):.0%} vs unskilled "
                  f"{np.mean(res[m & ~s['skilled']] == 'pass'):.0%}")


for max_days, lab in ((22, "30-day limit"), (250, "no time limit (cap 250 trading days)")):
    report(f"A: nobody has skill (-0.05R/trade after costs), {lab}", simulate(0.0, 0.0, max_days))
    report(f"B: 20% skilled (+0.15R/trade after costs), {lab}", simulate(0.2, 0.20, max_days))
