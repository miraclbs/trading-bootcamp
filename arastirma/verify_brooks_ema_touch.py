"""Round 37: Al Brooks, "Live Trades Series: Scaling in to avoid loss" (N5c6TsF2W-s). Claims (Emini, 5-min chart,
20-bar EMA of the day-session chart):
 (1) "In 35 years I have never seen a day that opened above the moving average and went all day without touching it
     ... 99.99% chance we touch the moving average, 99.95% chance of at least three bars with lows below it."
 (2) "Once it touches the moving average and you get a bull bar, 80% chance of a test of the high of the day."
Data: yfinance 5m bars, last ~60 days, regular session 09:30-16:00 ET (78 bars), EMA20 computed on the continuous
RTH series (carries over from the prior day, like a day-session chart). Mirror for days opening below the EMA.
Baseline: time-of-day bootstrap (each simulated day takes, for each 5-minute slot, a random real bar from the same
slot) -> same intraday volatility profile, no dependence. 50 reps.
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(37)
SYMS = ["SPY", "QQQ", "IWM", "DIA", "AAPL", "MSFT", "NVDA", "AMZN", "META", "XLF", "XLE", "GLD", "TLT"]


def ema_series(x, n=20, seed=None):
    a = 2 / (n + 1); out = np.empty_like(x); out[0] = x[0] if seed is None else seed
    for i in range(1, len(x)):
        out[i] = a * x[i] + (1 - a) * out[i - 1]
    return out


def measures(days, prev_close_ema):
    """days: list of (78,4) arrays O,H,L,C (absolute); ema state carried in"""
    n_open_above = n_never = n_3below = 0; n_touch_bull = n_test_high = 0
    for (a, e0) in zip(days, prev_close_ema):
        C = a[:, 3]; e = ema_series(C, seed=e0)
        e_prev = np.concatenate([[e0], e[:-1]])
        side = 1 if a[0, 0] > e0 else -1
        if side == 1:
            n_open_above += 1
            touched = a[:, 2] <= e_prev
            n_never += not touched.any(); n_3below += (a[:, 2] < e_prev).sum() >= 3
            if touched.any():
                k = np.argmax(touched); hi = a[:k + 1, 1].max()
                for j in range(k + 1, 77):
                    if a[j, 3] > a[j, 0]:                      # first bull bar after the touch
                        n_touch_bull += 1; n_test_high += (a[j + 1:, 1] >= hi).any(); break
    return n_open_above, n_never, n_3below, n_touch_bull, n_test_high


print("Days opening ABOVE the 5-min EMA20: share that never touch it / have >=3 bars below / after touch+bull bar, "
      "test of the high")
tot = np.zeros(5); totb = np.zeros(5)
for s in SYMS:
    d = yf.download(s, period="60d", interval="5m", progress=False, auto_adjust=False, prepost=False)
    if d is None or len(d) < 500:
        print(s, "no data"); continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d[["Open", "High", "Low", "Close"]].dropna()
    d.index = d.index.tz_convert("America/New_York")
    d = d.between_time("09:30", "15:55")
    full = [g.values for _, g in d.groupby(d.index.date) if len(g) == 78]
    if len(full) < 20:
        print(s, "too few full days"); continue
    closes = np.concatenate([x[:, 3] for x in full]); e_all = ema_series(closes)
    e0 = [e_all[i * 78 - 1] if i > 0 else full[0][0, 3] for i in range(len(full))]
    real = measures(full[1:], e0[1:])
    # bootstrap: same slot, random day; returns relative to each bar's previous close
    arr = np.stack(full); prevc = np.concatenate([arr[:, :1, 0], arr[:, :-1, 3]], axis=1)
    rel = arr / prevc[:, :, None]
    base = np.zeros(5)
    for _ in range(50):
        sims = []
        start = arr[1:, 0, 0]
        for i in range(len(full) - 1):
            pick = rng.integers(0, len(full), 78); bars = rel[pick, np.arange(78)]
            c = np.empty(79); c[0] = arr[i, -1, 3] if i < len(arr) else start[i]
            out = np.empty((78, 4))
            for j in range(78):
                out[j] = bars[j] * c[j]; c[j + 1] = out[j, 3]
            sims.append(out)
        base += np.array(measures(sims, e0[1:]))
    base /= 50
    tot += real; totb += base
    print(f"  {s:5s} days={len(full) - 1:3d} | open above {real[0]:3d} | never touch {real[1]:2d} ({real[1] / max(real[0], 1):4.0%}; "
          f"base {base[1] / max(base[0], 1):4.0%}) | >=3 below {real[2] / max(real[0], 1):4.0%} (base {base[2] / max(base[0], 1):4.0%}) | "
          f"high test after touch+bull {real[4] / max(real[3], 1):4.0%} (base {base[4] / max(base[3], 1):4.0%})")
print(f"\nPOOLED: open-above days {tot[0]:.0f} | never touch {tot[1]:.0f} = {tot[1] / tot[0]:.1%} (bootstrap {totb[1] / totb[0]:.1%}) | "
      f">=3 bars below {tot[2] / tot[0]:.1%} (bootstrap {totb[2] / totb[0]:.1%}) | test of high after touch + bull bar "
      f"{tot[4] / tot[3]:.0%} (bootstrap {totb[4] / totb[3]:.0%})")
