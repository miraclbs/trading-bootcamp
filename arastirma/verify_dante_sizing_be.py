"""Two claims from Trader Dante (Chat With Traders ep.39):
(1) "A trader had a positive-expectancy strategy but was losing money because he varied his size: bigger after a
    loss (revenge), tiny after two losses (scared), bigger on 'gut feel'. At fixed size he would have made money."
    Math check: if trades are iid, sizes chosen from PAST outcomes cannot flip the sign of the expected P&L
    (E[size*outcome] = E[size]*EV). So the story needs either (a) bad luck in a finite sample (variance), or
    (b) size correlated with trade QUALITY (revenge/gut-feel trades are worse). Simulate both.
(2) "There is no free trade": moving the stop to breakeven early. In a driftless random walk every stopping rule has
    EV 0 (optional stopping), so BE cannot help or hurt on average; with a real edge (drift) it cuts EV.
"""
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(7)

ONLY_BE = len(sys.argv) > 1 and sys.argv[1] == "be"
# ---------------- (1) sizing ----------------
N_TR, N_SIM = 200, 20000
WIN_R, WR = 1.3, 0.50          # EV = 0.5*1.3 - 0.5 = +0.15 R per lot
print("(1) Variable sizing on a +0.15R/lot strategy (WR 50%, win 1.3R), 200 trades, 20,000 runs")


def run(rule, revenge_wr=None, gut=False):
    tot = np.zeros(N_SIM); lots = np.zeros(N_SIM)
    for s in range(N_SIM):
        streak = 0; pnl = 0.0; L = 0.0
        for i in range(N_TR):
            if rule == "fixed":
                size, wr = 2, WR
            else:
                if streak == 0:
                    size, wr = 2, WR
                elif streak == 1:
                    size = 4; wr = revenge_wr if revenge_wr is not None else WR   # revenge trade
                else:
                    size, wr = 1, WR                                                # scared
                if gut and rng.random() < 0.25:                                     # 'gut feel' big bet
                    size = 5; wr = WR - 0.08 if revenge_wr is not None else WR
            win = rng.random() < wr
            r = WIN_R if win else -1.0
            pnl += size * r; L += size
            streak = 0 if win else streak + 1
        tot[s] = pnl; lots[s] = L
    return tot, lots


for name, kw in () if ONLY_BE else (("fixed 2 lots", dict(rule="fixed")),
                 ("Dante's pattern, same trade quality", dict(rule="var")),
                 ("Dante's pattern + gut-feel 5-lots, same quality", dict(rule="var", gut=True)),
                 ("revenge 4-lot trades WR 40%", dict(rule="var", revenge_wr=0.40)),
                 ("revenge WR 40% + gut-feel 5-lots WR 42%", dict(rule="var", revenge_wr=0.40, gut=True))):
    t, l = run(**kw)
    print(f"  {name:48s}: mean P&L {t.mean():+7.1f}R | per lot {t.sum()/l.sum():+.3f}R | P(loss after 200) {np.mean(t < 0):.1%}"
          f" | P&L sd {t.std():.0f}")

# ---------------- (2) breakeven stop ----------------
print("\n(2) Breakeven stop. Gaussian random walk, 1 step sd = 1, stop = 10 (1R), target = 20 (2R), 20,000 trades")


def be_sim(mu, be_at, n=20000, maxsteps=3000):
    out = np.empty(n); steps = np.empty(n); kind = np.full(n, 9)
    for k in range(n):
        x = 0.0; stop = -10.0; moved = False
        for j in range(1, maxsteps + 1):
            x += rng.normal(mu, 1.0)
            if be_at is not None and not moved and x >= be_at:
                stop = 0.0; moved = True
            if x <= stop:            # exit at the price actually reached (overshoot = slippage), keeps EV exact
                out[k] = x / 10; kind[k] = 0 if moved else -1; break
            if x >= 20:
                out[k] = x / 10; kind[k] = 2; break
        else:
            out[k] = x / 10
        steps[k] = j
    return out, steps, kind


for mu in (0.0, 0.01, 0.03):
    line = []
    for be in (None, 5.0, 10.0, 15.0):
        r, st, kd = be_sim(mu, be)
        lab = "no BE" if be is None else f"BE@+{be/10:.1f}R"
        line.append(f"{lab}: EV {r.mean():+.3f}R (se {r.std()/np.sqrt(len(r)):.3f}), {np.mean(kd == 2):.0%} full win, "
                    f"{np.mean(kd == 0):.0%} scratch, EV/100 steps {100*r.mean()/st.mean():+.3f}")
    print(f"  drift {mu:+.2f}/step:")
    for s in line:
        print("     " + s)
