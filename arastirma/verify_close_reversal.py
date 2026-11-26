"""Round 22 follow-up (post-hoc finding, treat as a HYPOTHESIS): last-half-hour REVERSAL of the day's move.
Signal at the 15:30 bar open: s = sign(price - previous close); trade -s from 15:30 open to 16:00 close.
Checks: two halves of the ~730-day sample, per symbol, stdev of the trade (for R/yr if 1R = 1 sd), and a stronger-
move filter (|day move| > 0.5% ). Cost: $0.02/share (ETF) round trip.
Mechanism candidate from the literature: Baltussen, Da, Lammers & Martens (JFE 2021) - intraday momentum is driven by
dealers' gamma hedging; when dealers are LONG gamma, hedging dampens moves and late-day reversals appear. The sign can
flip with the options-positioning regime, so this is regime-dependent by construction."""
import sys
import numpy as np
import yfinance as yf
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for sym in ("SPY", "QQQ", "IWM", "DIA", "XLK", "SMH"):
    d = yf.download(sym, period="730d", interval="1h", progress=False, auto_adjust=False, prepost=False)
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna(); idx = d.index.tz_convert("America/New_York")
    O, C = d["Open"].values, d["Close"].values
    days = {}
    for i, ts in enumerate(idx):
        if (9, 30) <= (ts.hour, ts.minute) and ts.hour < 16:
            days.setdefault(ts.date(), []).append(i)
    dl = [k for k in sorted(days) if len(days[k]) == 7 and idx[days[k][6]].hour == 15]
    r, rbig, cost = [], [], []; prev = None
    for k in dl:
        b = days[k]
        if prev is not None:
            s = np.sign(O[b[6]] - prev)
            x = -s * (C[b[6]] - O[b[6]]) / O[b[6]] * 1e4
            c = 0.02 / C[b[6]] * 1e4
            r.append(x - c); cost.append(c)
            if abs(O[b[6]] / prev - 1) > 0.005:
                rbig.append(x - c)
        prev = C[b[6]]
    r = np.array(r); h = len(r) // 2; rb = np.array(rbig)
    def sh(v): return v.mean() / v.std() * np.sqrt(252)
    print(f"{sym}: net {r.mean():+.2f}bp/day (sd {r.std():.1f}bp, cost {np.mean(cost):.2f}bp) Sharpe {sh(r):+.2f} | "
          f"1st half {r[:h].mean():+.2f}bp (Sharpe {sh(r[:h]):+.2f}) | 2nd half {r[h:].mean():+.2f}bp (Sharpe {sh(r[h:]):+.2f}) | "
          f"|move|>0.5%: {rb.mean():+.2f}bp n={len(rb)} | R/yr (1R=1sd) {r.mean()/r.std()*252:+.1f}")
