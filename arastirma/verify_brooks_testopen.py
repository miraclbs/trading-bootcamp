"""Sensitivity of Brooks' claim D ('any rally in the middle third of the day has a 60-70% chance to come back and
test the open later', on trading-range days). 1h bars ~2 years. Move at the 12:30 bar close measured in units of the
20-day average daily range (ADR). Also a pure random-walk check of the same conditional probability."""
import sys
import numpy as np
import yfinance as yf
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
THR = (0.05, 0.1, 0.2, 0.3, 0.5)
out = {t: [] for t in THR}
for sym in ("SPY", "QQQ", "IWM", "DIA"):
    d = yf.download(sym, period="730d", interval="1h", progress=False, auto_adjust=False, prepost=False)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna(); idx = d.index.tz_convert("America/New_York")
    O, Hh, L, C = (d[c].values for c in ("Open", "High", "Low", "Close"))
    days = {}
    for i, ts in enumerate(idx):
        if (9, 30) <= (ts.hour, ts.minute) and ts.hour < 16:
            days.setdefault(ts.date(), []).append(i)
    info = [(b, O[b[0]], Hh[b].max() - L[b].min()) for _, b in sorted(days.items()) if len(b) == 7]
    rng_hist = []
    for b, op, r in info:
        if len(rng_hist) >= 5:
            adr = np.mean(rng_hist[-20:])
            j = b[3]
            move = C[j] - op
            later = b[4:]
            for t in THR:
                if abs(move) >= t * adr:
                    touched = L[later].min() <= op if move > 0 else Hh[later].max() >= op
                    out[t].append(touched)
        rng_hist.append(r)
print("P(price returns to the day's open after 12:30 | move from open at 12:30 >= thr x ADR), 4 index ETFs pooled")
for t in THR:
    v = np.array(out[t]); print(f"  thr {t:.2f} ADR: {v.mean():.0%} (n={len(v)})")
# random walk with 390 one-minute steps, 'hourly' checkpoint at minute 180
rng = np.random.default_rng(0)
paths = rng.normal(0, 1, (20000, 390)).cumsum(1)
adr = (paths.max(1) - paths.min(1)).mean()
m = paths[:, 239]   # 12:30 bar closes at 13:30 = minute 240; 150 minutes remain
print("Random walk (same question):")
for t in THR:
    sel = np.abs(m) >= t * adr
    later = paths[sel, 240:]
    mm = m[sel]
    touched = np.where(mm > 0, later.min(1) <= 0, later.max(1) >= 0)
    print(f"  thr {t:.2f} ADR: {touched.mean():.0%} (n={sel.sum()})")
