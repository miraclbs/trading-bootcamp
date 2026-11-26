"""Test Al Brooks' opening-range claims on real intraday data (5-min bars, US regular session).
Claims (Emini, 81 five-minute bars/day):
  P(high or low of day already formed) by bar 1 ~20-30%, bar 7 ~50%, bar 12 ~70%, bar 18 ~90%.
  After a breakout of the 18-bar range, ~90% the opposite extreme of that range holds for the rest of the day.
Data: yfinance 5-min, last ~60 days (Yahoo limit), symbols SPY, QQQ, IWM (RTH only).
"""
import sys

import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CHECKS = (1, 7, 12, 18, 24)

for sym in ("SPY", "QQQ", "IWM"):
    df = yf.download(sym, period="60d", interval="5m", prepost=False, progress=False, auto_adjust=False)
    if df.empty:
        print(sym, "no data")
        continue
    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)
    df = df.tz_convert("America/New_York").between_time("09:30", "15:55")
    days = [g for _, g in df.groupby(df.index.date) if len(g) >= 75]
    n = len(days)
    formed = {k: 0 for k in CHECKS}
    brk_total = brk_held = 0
    for g in days:
        hi_idx = g["High"].values.argmax()
        lo_idx = g["Low"].values.argmin()
        first_extreme = min(hi_idx, lo_idx)  # bar index (0-based) when the first of the two extremes printed
        for k in CHECKS:
            if first_extreme < k:
                formed[k] += 1
        # 18-bar range breakout test
        h18 = g["High"].values[:18].max()
        l18 = g["Low"].values[:18].min()
        rest = g.iloc[18:]
        up_break = (rest["High"].values > h18)
        dn_break = (rest["Low"].values < l18)
        first_up = up_break.argmax() if up_break.any() else None
        first_dn = dn_break.argmax() if dn_break.any() else None
        if first_up is None and first_dn is None:
            continue
        brk_total += 1
        if first_dn is None or (first_up is not None and first_up < first_dn):
            # broke up first: does the 18-bar low hold for rest of day?
            brk_held += int(rest["Low"].values[first_up:].min() >= l18)
        else:
            brk_held += int(rest["High"].values[first_dn:].max() <= h18)
    row = " | ".join(f"bar {k}: {formed[k]/n:.0%}" for k in CHECKS)
    print(f"{sym}: {n} days | P(high or low of day already set) {row}")
    print(f"      18-bar range broken on {brk_total}/{n} days; opposite extreme held after first break: "
          f"{brk_held}/{brk_total} = {brk_held/max(brk_total,1):.0%}")
