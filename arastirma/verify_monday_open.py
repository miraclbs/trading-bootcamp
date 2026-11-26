"""Round 40: Trader Dante, "Performing a weekly trading review" (sI-2VJo47xA): "the market has a high probability of
returning to test the Monday open price once Monday has closed, and it usually happens on a Tuesday - you can test
that for yourself."
Test: for every day d, after day d closes, does price trade back through day d's OPEN within the next 4 trading days
(for Monday: Tue-Fri)? Compare Monday with the other weekdays (the baseline), overall and within buckets of the
distance between the close and the open (|C-O| / ATR14) - a small Monday body is trivially retested.
Also: share of the retests that happen on the very next day (Tuesday for Monday).
Daily data via yfinance. Crypto trades 7 days, so "next 4 days" = 4 calendar days there.
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SYMS = {"BTC-USD": "2017-01-01", "ETH-USD": "2018-01-01", "SPY": "2005-01-01", "QQQ": "2005-01-01",
        "GLD": "2005-01-01", "EURUSD=X": "2005-01-01", "GBPUSD=X": "2005-01-01", "GC=F": "2005-01-01"}
NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
BUCKETS = ((0, 0.5), (0.5, 1.0), (1.0, 99))


def analyse(sym, start):
    d = yf.download(sym, start=start, interval="1d", progress=False, auto_adjust=False)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna()
    O, H, L, C = (d[c].values for c in ("Open", "High", "Low", "Close")); wd = d.index.dayofweek.values
    tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = np.convolve(tr, np.ones(14) / 14, mode="full")[:len(tr)]
    rows = []
    for t in range(20, len(C) - 4):
        if C[t] == O[t] or atr[t] <= 0:
            continue
        up = C[t] > O[t]
        hits = [(L[t + j] <= O[t]) if up else (H[t + j] >= O[t]) for j in range(1, 5)]
        rows.append((wd[t], abs(C[t] - O[t]) / atr[t], any(hits), hits[0]))
    return np.array(rows, dtype=float)


print("P(open of day d is traded through again within the next 4 days | after day d's close)")
print("  symbol    | Mon (next-day share) | other weekdays | Mon - others | by |C-O|/ATR bucket: Mon vs others")
for s, st in SYMS.items():
    A = analyse(s, st)
    mon = A[A[:, 0] == 0]; oth = A[A[:, 0] != 0]
    cells = []
    for lo, hi in BUCKETS:
        m = mon[(mon[:, 1] >= lo) & (mon[:, 1] < hi)]; o = oth[(oth[:, 1] >= lo) & (oth[:, 1] < hi)]
        cells.append(f"{lo:.1f}-{hi if hi < 99 else 'inf'}: {m[:, 2].mean():.0%} vs {o[:, 2].mean():.0%} (n={len(m)})")
    nxt = mon[mon[:, 2] == 1][:, 3].mean()
    se = np.sqrt(mon[:, 2].var() / len(mon) + oth[:, 2].var() / len(oth))
    print(f"  {s:9s} | {mon[:, 2].mean():.0%} ({nxt:.0%}) | {oth[:, 2].mean():.0%} | "
          f"{mon[:, 2].mean() - oth[:, 2].mean():+.1%} (se {se:.1%}) | " + " | ".join(cells))
    per_day = " ".join(f"{NAMES[int(w)]} {A[A[:, 0] == w][:, 2].mean():.0%}" for w in sorted(set(A[:, 0].astype(int))))
    print(f"             all weekdays: {per_day}")
