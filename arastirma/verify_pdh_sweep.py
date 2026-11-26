"""Test the 'sweep of previous day high/low' (failed breakout) setup on real data.
Setup (short side; long is mirrored at PDL):
  - Price trades above the previous RTH day's high (PDH) during today's RTH session.
  - Entry: close of the FIRST bar that closes back below PDH after the sweep.
  - Stop: highest high since the sweep started (the sweep extreme).
  - Targets: 1R and 2R. If neither hit by session end -> exit at last close (R multiple).
  - Same-bar ambiguity: stop assumed first (conservative).
Random-walk baseline (no edge, no time limit): P(1R before -1R)=50%, P(2R before -1R)=33%.
Data: yfinance, 1h bars ~2 years and 5m bars ~60 days, RTH only. NO costs included.
"""
import sys

import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def load(sym, interval, period):
    df = yf.download(sym, period=period, interval=interval, prepost=False, progress=False, auto_adjust=False)
    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)
    df = df.tz_convert("America/New_York").between_time("09:30", "15:59")
    return [g for _, g in df.groupby(df.index.date)]


def simulate(days, k):
    res = []  # list of R outcomes
    hits = {"win": 0, "loss": 0, "eod": 0}
    for i in range(1, len(days)):
        prev, g = days[i - 1], days[i]
        pdh, pdl = prev["High"].max(), prev["Low"].min()
        H, L, C = g["High"].values, g["Low"].values, g["Close"].values
        for side in ("short", "long"):
            swept, ext, entry_i = False, None, None
            for j in range(len(g)):
                if side == "short":
                    if H[j] > pdh:
                        swept = True
                        ext = H[j] if ext is None else max(ext, H[j])
                    if swept and C[j] < pdh:
                        entry_i = j
                        break
                else:
                    if L[j] < pdl:
                        swept = True
                        ext = L[j] if ext is None else min(ext, L[j])
                    if swept and C[j] > pdl:
                        entry_i = j
                        break
            if entry_i is None or entry_i == len(g) - 1:
                continue
            entry = C[entry_i]
            R = (ext - entry) if side == "short" else (entry - ext)
            if R <= entry * 0.0003:  # skip degenerate tiny-risk signals
                continue
            out = None
            for j in range(entry_i + 1, len(g)):
                if side == "short":
                    if H[j] >= ext:
                        out = -1.0; hits["loss"] += 1; break
                    if L[j] <= entry - k * R:
                        out = float(k); hits["win"] += 1; break
                else:
                    if L[j] <= ext:
                        out = -1.0; hits["loss"] += 1; break
                    if H[j] >= entry + k * R:
                        out = float(k); hits["win"] += 1; break
            if out is None:
                last = C[-1]
                out = ((entry - last) / R) if side == "short" else ((last - entry) / R)
                hits["eod"] += 1
            res.append(out)
    return res, hits


for interval, period in (("1h", "730d"), ("5m", "60d")):
    print(f"\n===== {interval} bars, {period} =====")
    for sym in ("SPY", "QQQ", "IWM"):
        days = load(sym, interval, period)
        for k in (1, 2):
            res, hits = simulate(days, k)
            n = len(res)
            if n == 0:
                print(f"{sym} k={k}: no signals"); continue
            decided = hits["win"] + hits["loss"]
            wr = hits["win"] / decided if decided else 0
            ev = sum(res) / n
            base = 0.5 if k == 1 else 1 / 3
            print(f"{sym} target {k}R: N={n} (days {len(days)}) | win {hits['win']} loss {hits['loss']} eod {hits['eod']} "
                  f"| WR(decided) {wr:.0%} vs random {base:.0%} | avg R/trade {ev:+.2f}")
