"""Round 44: Trader Dante, "A Blueprint For Trading Success" (Uzq1jgNKuBc): "Open drive lower [the market makes a
concerted move one way off the open and after the first 30 minutes the open is the high]... we know there is an 80%
probability that the open drive is going to fail and price is going to trade one tick above the open drive high."
(His stat is for Bund futures; we test liquid US ETFs/futures.)
Definition (5m bars, regular session 09:30-16:00 ET, ~60 days): open drive DOWN if the open is the high of the first
30 minutes (no bar trades above open + 0.02%) and the 10:00 close is at least 0.25% below the open; mirror for UP.
Outcome: does price trade beyond the first-30-minute extreme (= open +/- tolerance) later in the session?
Baseline: time-of-day bootstrap (synthetic days from same-slot bars, starting at the real open), same definition.
Also reported: share of all days that qualify.
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(44)
SYMS = ["SPY", "QQQ", "IWM", "DIA", "GLD", "TLT", "XLF", "XLE", "ES=F", "NQ=F", "ZN=F", "GC=F", "CL=F"]


def classify(day):
    o = day[0, 0]; f30 = day[:6]; rest = day[6:]
    if f30[:, 1].max() <= o * 1.0002 and f30[-1, 3] <= o * (1 - 0.0025):
        ext = f30[:, 1].max(); return -1, (rest[:, 1] > ext).any()
    if f30[:, 2].min() >= o * (1 - 0.0002) and f30[-1, 3] >= o * (1 + 0.0025):
        ext = f30[:, 2].min(); return 1, (rest[:, 2] < ext).any()
    return 0, False


tot = np.zeros(3); totb = np.zeros(3)
print("Open drive (first 30 min) -> does price later trade beyond the open-drive extreme? real vs bootstrap")
for s in SYMS:
    d = yf.download(s, period="60d", interval="5m", progress=False, auto_adjust=False, prepost=False)
    if d is None or len(d) < 500:
        continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d[["Open", "High", "Low", "Close"]].dropna()
    d.index = d.index.tz_convert("America/New_York"); d = d.between_time("09:30", "15:55")
    days = [g.values for _, g in d.groupby(d.index.date) if len(g) == 78]
    if len(days) < 20:
        continue
    arr = np.stack(days); prevc = np.concatenate([arr[:, :1, 0], arr[:, :-1, 3]], axis=1)
    rel = arr / prevc[:, :, None]
    n = fail = 0; bn = bf = 0.0
    for i in range(len(days)):
        side, f = classify(arr[i]); n += side != 0; fail += side != 0 and f
        for _ in range(40):
            pick = rng.integers(0, len(days), 78); bars = rel[pick, np.arange(78)]
            out = np.empty((78, 4)); c = arr[i, 0, 0] / bars[0, 0]
            for j in range(78):
                out[j] = bars[j] * c; c = out[j, 3]
            sd, ff = classify(out); bn += (sd != 0) / 40; bf += (sd != 0 and ff) / 40
    tot += [len(days), n, fail]; totb += [len(days), bn, bf]
    print(f"  {s:5s}: days {len(days)} | open drives {n:2d} | later traded beyond extreme {fail:2d} "
          f"({fail / max(n, 1):.0%}) | bootstrap: drives/day {bn / len(days):.0%}, failure {bf / max(bn, 1e-9):.0%}")
print(f"\nPOOLED: {tot[1]:.0f} open drives on {tot[0]:.0f} days ({tot[1] / tot[0]:.0%}; bootstrap {totb[1] / totb[0]:.0%}) | "
      f"'failure' (price trades beyond the open-drive extreme later) {tot[2] / tot[1]:.0%} (bootstrap {totb[2] / totb[1]:.0%})")


# --- larger sample: first-HOUR open drive on 1h bars (~2 years), ETFs (09:30 bar = first hour) ---
print("\nFirst-hour version, 1h bars ~2y: open is the high (low) of the first hour and the 10:30 close is >= 0.4% away")
tn = tf = 0; tb = tbf = 0.0
for s in ["SPY", "QQQ", "IWM", "DIA", "GLD", "TLT", "XLF", "XLE", "EFA", "EEM"]:
    d = yf.download(s, period="730d", interval="1h", progress=False, auto_adjust=False)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d[["Open", "High", "Low", "Close"]].dropna(); d.index = d.index.tz_convert("America/New_York")
    days = [g.values for _, g in d.groupby(d.index.date) if len(g) == 7]
    arr = np.stack(days); prevc = np.concatenate([arr[:, :1, 0], arr[:, :-1, 3]], axis=1); rel = arr / prevc[:, :, None]

    def cls1h(day):
        o = day[0, 0]; f = day[0]; rest = day[1:]
        if f[1] <= o * 1.0002 and f[3] <= o * 0.996:
            return 1, (rest[:, 1] > f[1]).any()
        if f[2] >= o * 0.9998 and f[3] >= o * 1.004:
            return 1, (rest[:, 2] < f[2]).any()
        return 0, False
    n = fl = 0; bn = bf = 0.0
    for i in range(len(days)):
        a, b = cls1h(arr[i]); n += a; fl += a and b
        for _ in range(40):
            pick = rng.integers(0, len(days), 7); bars = rel[pick, np.arange(7)]
            out = np.empty((7, 4)); c = arr[i, 0, 0] / bars[0, 0]
            for j in range(7):
                out[j] = bars[j] * c; c = out[j, 3]
            a2, b2 = cls1h(out); bn += a2 / 40; bf += (a2 and b2) / 40
    tn += n; tf += fl; tb += bn; tbf += bf
    print(f"  {s:4s}: days {len(days)} | first-hour drives {n:3d} | later beyond extreme {fl / max(n, 1):.0%} | bootstrap {bf / max(bn, 1e-9):.0%}")
print(f"POOLED 1h: {tn} drives | 'failure' {tf / tn:.0%} (bootstrap {tbf / tb:.0%})")
