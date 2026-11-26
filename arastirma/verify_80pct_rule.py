"""Round 41: Market Profile "80% rule" (auction market theory, as used by Trader Dante-style traders): if the market
OPENS outside the prior day's value area and then trades back inside it for two consecutive 30-minute periods, there
is an ~80% chance it traverses the value area to the opposite edge the same day.
Data: yfinance 5-minute bars, ~60 days, regular session. Prior-day volume profile: each 5m bar's volume spread evenly
over its high-low range in 0.02%-of-price bins; POC = max bin; value area = 70% of volume expanding from the POC.
"Inside for a 30-min period" = that half hour's close is inside the VA (a common simplification).
Baselines: (a) unconditional: all open-outside days, does price reach the opposite VA edge after 10:30?
(b) time-of-day bootstrap of the same days (synthetic paths from same-slot bars, starting at the real open, same
prior VA) -> the rule's hit rate when there is no dependence. 30 reps.
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(41)
SYMS = ["SPY", "QQQ", "IWM", "DIA", "GLD", "TLT", "XLF", "XLE", "AAPL", "MSFT", "AMZN", "NVDA"]


def value_area(day):
    lo, hi = day[:, 2].min(), day[:, 1].max()
    step = day[0, 3] * 0.0002; edges = np.arange(lo, hi + step, step)
    vol = np.zeros(len(edges))
    for o, h, l, c, v in day:
        i0, i1 = np.searchsorted(edges, l), np.searchsorted(edges, h)
        i1 = max(i1, i0 + 1); vol[i0:i1] += v / (i1 - i0)
    poc = int(np.argmax(vol)); tot = vol.sum(); a = b = poc; s = vol[poc]
    while s < 0.7 * tot and (a > 0 or b < len(vol) - 1):
        up = vol[b + 1] if b < len(vol) - 1 else -1; dn = vol[a - 1] if a > 0 else -1
        if up >= dn: b += 1; s += up
        else: a -= 1; s += dn
    return edges[a], edges[min(b + 1, len(edges) - 1)]


def rule(day, val, vah):
    """day: (78,4) O,H,L,C. returns (opened_outside, triggered, traversed, reached_opposite_unconditional)"""
    o = day[0, 0]
    if val <= o <= vah:
        return 0, 0, 0, 0
    side = 1 if o > vah else -1                         # 1 = opened above -> target VAL
    target = val if side == 1 else vah
    halves = day.reshape(13, 6, 4)
    closes = halves[:, -1, 3]
    inside = (closes >= val) & (closes <= vah)
    trig = None
    for k in range(1, 13):
        if inside[k - 1] and inside[k]:
            trig = k; break
    uncond = (day[12:, 2].min() <= target) if side == 1 else (day[12:, 1].max() >= target)
    if trig is None:
        return 1, 0, 0, int(uncond)
    rest = day[(trig + 1) * 6:]
    if len(rest) == 0:
        return 1, 1, 0, int(uncond)
    hit = (rest[:, 2].min() <= target) if side == 1 else (rest[:, 1].max() >= target)
    return 1, 1, int(hit), int(uncond)


tot = np.zeros(4); totb = np.zeros(4)
print("Market Profile 80% rule, 5-minute data (~60 days). counts: opened outside VA / rule triggered / traversed")
for s in SYMS:
    d = yf.download(s, period="60d", interval="5m", progress=False, auto_adjust=False, prepost=False)
    if d is None or len(d) < 500:
        continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d[["Open", "High", "Low", "Close", "Volume"]].dropna()
    d.index = d.index.tz_convert("America/New_York"); d = d.between_time("09:30", "15:55")
    days = [g.values for _, g in d.groupby(d.index.date) if len(g) == 78]
    if len(days) < 20:
        continue
    arr = np.stack([x[:, :4] for x in days]); prevc = np.concatenate([arr[:, :1, 0], arr[:, :-1, 3]], axis=1)
    rel = arr / prevc[:, :, None]
    res = np.zeros(4); base = np.zeros(4)
    for i in range(1, len(days)):
        val, vah = value_area(days[i - 1])
        res += np.array(rule(arr[i], val, vah))
        for _ in range(30):
            pick = rng.integers(0, len(days), 78); bars = rel[pick, np.arange(78)]
            c = arr[i, 0, 0]; out = np.empty((78, 4))
            first = bars[0].copy(); first[0] = 1.0                   # start exactly at the real open
            for j in range(78):
                b = first if j == 0 else bars[j]
                out[j] = b * (c if j else arr[i, 0, 0] / bars[0][0] * bars[0][0]); c = out[j, 3]
            out[0, 0] = arr[i, 0, 0]
            base += np.array(rule(out, val, vah)) / 30
    tot += res; totb += base
    print(f"  {s:5s}: outside {res[0]:3.0f} | triggered {res[1]:3.0f} | traversed {res[2]:3.0f} "
          f"({res[2] / max(res[1], 1):.0%}; bootstrap {base[2] / max(base[1], 1e-9):.0%}) | "
          f"unconditional opposite-edge {res[3] / max(res[0], 1):.0%}")
print(f"\nPOOLED: open outside {tot[0]:.0f} | triggered {tot[1]:.0f} ({tot[1] / tot[0]:.0%}) | traversed after trigger "
      f"{tot[2] / tot[1]:.0%} (bootstrap {totb[2] / totb[1]:.0%}) | unconditional opposite edge on open-outside days "
      f"{tot[3] / tot[0]:.0%} (bootstrap {totb[3] / totb[0]:.0%})")
