"""Round 46: Peter Brandt's own breakout rules (Chat With Traders, bIi6YzPt9bE):
 "a horizontal pattern (rectangle / right-angle triangle) that lasts 8 to 14 weeks, contained within ~15% of price;
  14-day ADX under 12, close to 10 (compression); breakout = 50% of a 30-day ATR beyond the boundary (buy-stop);
  manage with an 8-day moving average (stay while price holds above it)". He also says: "There is no edge in a
  rectangle... my edge comes from risk management, emotional management and process."
Mechanical approximation, daily 2005+, no costs:
  box = high/low of the previous 60 trading days (~12 weeks); width <= 15% of price; ADX(14) at signal < 15 (strict
  version < 12); entry stop at box high + 0.5*ATR30 (mirror for shorts); initial stop at the breakout day's low
  (Brandt's 'last day rule'), min 0.5 ATR; exit on a close below the 8-day SMA (long) or stop, max 120 days.
Variants: A full rules; B no ADX filter; C no width filter; D plain 60-day breakout (no filters); E random entry
day/direction with the same stop/exit. Report mean R, win rate, n, per group (commodity futures, FX, index ETFs).
"""
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GROUPS = {"COMMOD FUT": "GC=F SI=F CL=F NG=F HG=F ZC=F ZS=F ZW=F KC=F SB=F CT=F LE=F".split(),
          "FX": "EURUSD=X GBPUSD=X USDJPY=X AUDUSD=X USDCAD=X USDCHF=X NZDUSD=X".split(),
          "INDEX ETF": "SPY QQQ IWM DIA EFA EEM EWJ EWG".split()}


def adx(H, L, C, n=14):
    up = np.diff(H, prepend=H[0]); dn = -np.diff(L, prepend=L[0])
    pdm = np.where((up > dn) & (up > 0), up, 0.0); mdm = np.where((dn > up) & (dn > 0), dn, 0.0)
    tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    s = lambda x: pd.Series(x).ewm(alpha=1 / n, adjust=False).mean().values
    atr = s(tr); pdi = 100 * s(pdm) / atr; mdi = 100 * s(mdm) / atr
    dx = 100 * abs(pdi - mdi) / np.maximum(pdi + mdi, 1e-9)
    return s(dx)


def run_trade(O, H, L, C, sma8, t, side, entry, a):
    """entered intraday on day t at 'entry'; initial stop = breakout day's extreme; exit on close beyond SMA8"""
    stop = L[t] if side == 1 else H[t]
    if side * (entry - stop) < 0.5 * a:
        stop = entry - side * 0.5 * a
    risk = abs(entry - stop)
    if side * (C[t] - stop) <= 0:
        return -1.0
    for j in range(t + 1, min(t + 121, len(C))):
        if (side == 1 and L[j] <= stop) or (side == -1 and H[j] >= stop):
            px = min(O[j], stop) if side == 1 else max(O[j], stop)
            return side * (px - entry) / risk
        if side * (C[j] - sma8[j]) < 0:
            return side * (C[j] - entry) / risk
    j = min(t + 120, len(C) - 1)
    return side * (C[j] - entry) / risk


for g, syms in GROUPS.items():
    res = {k: [] for k in "ABCDE"}
    for s in syms:
        d = yf.download(s, start="2004-01-01", interval="1d", progress=False, auto_adjust=True)
        if d is None or len(d) < 500:
            continue
        if hasattr(d.columns, "levels"):
            d.columns = d.columns.get_level_values(0)
        d = d.dropna(); d = d[(d["High"] > 0) & (d["Low"] > 0)]
        O, H, L, C = (d[c].values for c in ("Open", "High", "Low", "Close")); yr = d.index.year.values
        tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)), abs(L - np.roll(C, 1))))
        atr30 = pd.Series(tr).rolling(30).mean().values; ad = adx(H, L, C)
        sma8 = pd.Series(C).rolling(8).mean().values
        rng = np.random.default_rng(sum(map(ord, s)))
        busy = {k: -1 for k in "ABCD"}
        for t in range(70, len(C) - 2):
            if yr[t] < 2005 or np.isnan(atr30[t - 1]):
                continue
            hi = H[t - 60:t].max(); lo = L[t - 60:t].min(); a = atr30[t - 1]
            width_ok = (hi - lo) / C[t - 1] <= 0.15
            adx_ok = ad[t - 1] < 15
            for side, lvl in ((1, hi + 0.5 * a), (-1, lo - 0.5 * a)):
                trig = H[t] >= lvl if side == 1 else L[t] <= lvl
                if not trig:
                    continue
                entry = max(O[t], lvl) if side == 1 else min(O[t], lvl)
                for k, ok in (("A", width_ok and adx_ok), ("B", width_ok), ("C", adx_ok), ("D", True)):
                    if ok and t > busy[k]:
                        res[k].append(run_trade(O, H, L, C, sma8, t, side, entry, a)); busy[k] = t + 10
            if rng.random() < 0.02:
                side = 1 if rng.random() < 0.5 else -1
                res["E"].append(run_trade(O, H, L, C, sma8, t, side, O[t], atr30[t - 1]))
    print(f"\n=== {g} (daily 2005+, no costs; exit: close beyond 8-day SMA or stop) ===")
    labels = {"A": "A full Brandt rules (width<=15%, ADX<15)", "B": "B no ADX filter", "C": "C no width filter",
              "D": "D plain 60-day breakout + 0.5 ATR", "E": "E random entry, same exits"}
    for k in "ABCDE":
        r = np.array(res[k])
        if len(r) == 0:
            print(f"  {labels[k]:42s}: n=0"); continue
        print(f"  {labels[k]:42s}: n={len(r):4d} | mean {r.mean():+.3f}R (se {r.std() / np.sqrt(len(r)):.3f}) | "
              f"win {np.mean(r > 0):.0%} | top 15% share of gross gains {np.sort(r)[::-1][:max(1, len(r) // 7)].sum() / max(r[r > 0].sum(), 1e-9):.0%}")


# --- robustness: commodity futures only, drop trades spanning a roll gap (> 3 ATR open-vs-prior-close), split by period ---
print(); print("Robustness (COMMOD FUT): roll-gap filtered, 2005-14 vs 2015+")
rob = {k: {"p1": [], "p2": []} for k in "ADE"}
for s in GROUPS["COMMOD FUT"]:
    d = yf.download(s, start="2004-01-01", interval="1d", progress=False, auto_adjust=True)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna(); d = d[(d["High"] > 0) & (d["Low"] > 0)]
    O, H, L, C = (d[c].values for c in ("Open", "High", "Low", "Close")); yr = d.index.year.values
    tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr30 = pd.Series(tr).rolling(30).mean().values; ad = adx(H, L, C); sma8 = pd.Series(C).rolling(8).mean().values
    gap = np.abs(O - np.roll(C, 1)) > 3 * np.nan_to_num(atr30, nan=np.inf)
    rng = np.random.default_rng(sum(map(ord, s))); busy = {k: -1 for k in "AD"}
    def ok_window(t):
        return not gap[t:min(t + 121, len(C))].any()
    for t in range(70, len(C) - 2):
        if yr[t] < 2005 or np.isnan(atr30[t - 1]):
            continue
        per = "p1" if yr[t] < 2015 else "p2"
        hi = H[t - 60:t].max(); lo = L[t - 60:t].min(); a = atr30[t - 1]
        full = (hi - lo) / C[t - 1] <= 0.15 and ad[t - 1] < 15
        for side, lvl in ((1, hi + 0.5 * a), (-1, lo - 0.5 * a)):
            if not (H[t] >= lvl if side == 1 else L[t] <= lvl) or not ok_window(t):
                continue
            entry = max(O[t], lvl) if side == 1 else min(O[t], lvl)
            for k, ok in (("A", full), ("D", True)):
                if ok and t > busy[k]:
                    rob[k][per].append(run_trade(O, H, L, C, sma8, t, side, entry, a)); busy[k] = t + 10
        if rng.random() < 0.02 and ok_window(t):
            sd = 1 if rng.random() < 0.5 else -1
            rob["E"][per].append(run_trade(O, H, L, C, sma8, t, sd, O[t], atr30[t - 1]))
for k, lab in (("A", "full Brandt rules"), ("D", "plain 60-day breakout"), ("E", "random entry")):
    cells = []
    for per, pl in (("p1", "2005-14"), ("p2", "2015+")):
        r = np.array(rob[k][per]); cells.append(f"{pl}: {r.mean():+.3f}R (se {r.std() / np.sqrt(len(r)):.3f}, n={len(r)})")
    print(f"  {lab:22s} | " + " | ".join(cells))
