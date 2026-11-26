# Generic mapping: annual Sharpe (after costs) and annual vol -> FTMO 2-step pass probability and time.
# Daily returns iid Student-t(df=4) scaled; static 10% max loss from initial balance; 5% daily loss
# measured from start-of-day balance (closed-day approximation); phase1 +10%, phase2 +5% (fresh account).
# Cap: 3 years (756 trading days) per phase. Also reports 1-step-like single +10% within 1 year.
import numpy as np
rng = np.random.default_rng(7)
N = 20000; T = 756; df = 4
tscale = np.sqrt(df/(df-2))
def run_phase(S, vol, target):
    mu = S*vol/252; sd = vol/np.sqrt(252)
    z = rng.standard_t(df, size=(N, T))/tscale
    r = mu + sd*z
    eq = np.cumprod(1+r, axis=1)
    prev = np.concatenate([np.ones((N,1)), eq[:, :-1]], axis=1)
    daily_breach = (eq - prev) <= -0.05          # loss >= 5% of initial (approx: initial=1)
    max_breach = eq <= 0.90
    fail = daily_breach | max_breach
    win = eq >= 1+target
    first_fail = np.where(fail.any(1), fail.argmax(1), T+1)
    first_win = np.where(win.any(1), win.argmax(1), T+1)
    passed = first_win < first_fail
    failed = first_fail < first_win
    days = np.where(passed, first_win+1, np.nan)
    return passed, failed, days
print("S   vol  | P(pass both) P(fail) P(open after 3y/phase) | median months to pass both | P(+10% within 12m, phase1 only)")
for S in [0.0, 0.3, 0.5, 0.8, 1.0, 1.5]:
    for vol in [0.05, 0.08, 0.10, 0.15, 0.20]:
        p1, f1, d1 = run_phase(S, vol, 0.10)
        p2, f2, d2 = run_phase(S, vol, 0.05)
        both = p1 & p2
        fail = f1 | (p1 & f2)
        tot = d1 + d2
        med = np.nanmedian(np.where(both, tot, np.nan))/21
        within12 = np.mean(p1 & (d1 <= 252))
        print(f"{S:.1f} {vol:.2f} | {both.mean():6.2f} {fail.mean():6.2f} {1-both.mean()-fail.mean():6.2f} | {med:6.1f} | {within12:5.2f}")
