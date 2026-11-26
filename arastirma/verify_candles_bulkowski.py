"""Bulkowski candlestick 'top 5' as quoted by Financial Wisdom (4Lx-NnMOpWs): three-line strike (bullish, '84%'),
three black crows (bearish, '78%'), evening star (bearish, '72%'), abandoned baby bullish ('70%'), two black gapping
(bearish continuation, '68%'). Bulkowski's rate = direction of the BREAKOUT: price closes beyond the pattern's high
(bullish) or low (bearish) first. That is not a profit rate.
Hypothesis: much of the rate is GEOMETRY. If the last candle closes near the top of the pattern's range, the close is
already close to the upper breakout level, so it is likely to cross it first.
Test: daily, 2005+, 30 US large caps + 10 ETFs. For every day compute the pattern range (min low / max high of the
pattern bars) and where the close sits in it (location 0..1). Baseline = P(first breakout in the predicted direction)
for ALL days with the same location bin. Also forward 10-day return (ATR units, minus the symbol's drift, signed).
Definitions (mechanical approximations of Bulkowski's):
  3-line strike bull : 3 black candles with lower lows, then a candle that opens below the prior close and closes above
                       the HIGH of the first black candle. Prior 10-day decline.
  3 black crows      : 3 black candles, each close lower, each open inside prior body, first one near 20d high.
  evening star       : tall white (body > 0.6 ATR) making a 20d high; small body (< 0.25 ATR) whose body is above the
                       white body; black candle closing below the midpoint of the white body.
  2 black gapping    : uptrend (close > 50SMA), gap down (high < prior low), then 2 black candles, 2nd closes lower.
  abandoned baby bull: downtrend, gap down to a doji (body < 0.1 range) whose high < prior low, then gap up (low > doji high).
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SYMS = ("AAPL MSFT JNJ PG KO PEP XOM CVX JPM BAC WFC GE IBM INTC CSCO ORCL WMT HD MCD DIS MRK PFE T VZ MMM CAT BA HON "
        "UNH AMGN SPY QQQ IWM DIA XLE XLF XLK GLD TLT EEM").split()
NEW = ("AMZN NVDA GOOGL COST NKE SBUX LOW TGT UPS FDX LMT RTX DE ADBE TXN QCOM NEE DUK SO MO CL KMB GIS ABT TMO MDT "
       "BMY LLY AXP GS XLV XLY XLP XLI XLU XLB SMH EFA EWJ MDY").split()
if len(sys.argv) > 1 and sys.argv[1] == "new":
    SYMS = NEW
BINS = np.linspace(0, 1, 11)


def first_break(C, t, hi, lo, maxd=60):
    for j in range(t + 1, min(t + 1 + maxd, len(C))):
        if C[j] > hi:
            return 1
        if C[j] < lo:
            return -1
    return 0


pat = {k: {"brk": [], "fwd": [], "loc": []} for k in ("3-line strike bull", "3 black crows", "evening star",
                                                     "2 black gapping", "abandoned baby bull")}
pred = {"3-line strike bull": 1, "3 black crows": -1, "evening star": -1, "2 black gapping": -1, "abandoned baby bull": 1}
nbars = {"3-line strike bull": 4, "3 black crows": 3, "evening star": 3, "2 black gapping": 3, "abandoned baby bull": 3}
base = {n: {"brk": [], "loc": []} for n in (3, 4)}

for sym in SYMS:
    d = yf.download(sym, start="2004-01-01", interval="1d", progress=False, auto_adjust=True)
    if d is None or len(d) < 500:
        continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna(); d = d[(d["High"] > 0) & (d["Low"] > 0) & (d["High"] >= d["Low"])]
    O, Hh, L, C = (d[c].values for c in ("Open", "High", "Low", "Close"))
    yr = d.index.year.values; T = len(C)
    tr = np.maximum(Hh - L, np.maximum(abs(Hh - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = np.convolve(tr, np.ones(14) / 14, mode="full")[:T]
    sma50 = np.convolve(C, np.ones(50) / 50, mode="full")[:T]
    drift = np.nanmean([(C[t + 10] - C[t]) / atr[t] for t in range(60, T - 10)])
    rng = np.random.default_rng(sum(map(ord, sym)))
    blk = C < O; wht = C > O; body = np.abs(C - O)
    for t in range(60, T - 61):
        if yr[t] < 2005 or atr[t] <= 0:
            continue
        a = atr[t]
        fwd = (C[t + 10] - C[t]) / a - drift
        # baseline sample (1 in 4 days), for 3- and 4-bar windows
        if rng.random() < 0.25:
            for n in (3, 4):
                hi, lo = Hh[t - n + 1:t + 1].max(), L[t - n + 1:t + 1].min()
                if hi > lo:
                    base[n]["loc"].append((C[t] - lo) / (hi - lo)); base[n]["brk"].append(first_break(C, t, hi, lo))
        hits = []
        if (blk[t - 3] and blk[t - 2] and blk[t - 1] and L[t - 2] < L[t - 3] and L[t - 1] < L[t - 2]
                and O[t] < C[t - 1] and C[t] > Hh[t - 3] and C[t - 3] < C[t - 13]):
            hits.append("3-line strike bull")
        if (blk[t - 2] and blk[t - 1] and blk[t] and C[t - 1] < C[t - 2] and C[t] < C[t - 1]
                and C[t - 2] < O[t - 1] < O[t - 2] and C[t - 1] < O[t] < O[t - 1]
                and Hh[t - 2] >= 0.98 * Hh[t - 21:t - 1].max()):
            hits.append("3 black crows")
        if (wht[t - 2] and body[t - 2] > 0.6 * a and Hh[t - 2] >= Hh[t - 22:t - 2].max()
                and body[t - 1] < 0.25 * a and min(O[t - 1], C[t - 1]) > C[t - 2]
                and blk[t] and C[t] < (O[t - 2] + C[t - 2]) / 2):
            hits.append("evening star")
        if (C[t - 3] > sma50[t - 3] and Hh[t - 2] < L[t - 3] and blk[t - 2] and blk[t - 1] and blk[t]
                and C[t] < C[t - 1]):
            hits.append("2 black gapping")
        rg = Hh[t - 1] - L[t - 1]
        if (C[t - 2] < sma50[t - 2] and rg > 0 and body[t - 1] < 0.1 * rg and Hh[t - 1] < L[t - 2] and L[t] > Hh[t - 1]):
            hits.append("abandoned baby bull")
        for k in hits:
            n = nbars[k]
            hi, lo = Hh[t - n + 1:t + 1].max(), L[t - n + 1:t + 1].min()
            if hi <= lo:
                continue
            pat[k]["loc"].append((C[t] - lo) / (hi - lo))
            pat[k]["brk"].append(first_break(C, t, hi, lo))
            pat[k]["fwd"].append(pred[k] * fwd)

print("Breakout-direction rate: pattern vs baseline days with the SAME close location in the pattern range.")
for k, v in pat.items():
    brk = np.array(v["brk"]); loc = np.array(v["loc"]); fw = np.array(v["fwd"])
    if len(brk) < 5:
        print(f"\n{k}: n={len(brk)} (too few)"); continue
    p = pred[k]; n = nbars[k]
    rate = np.mean(brk == p)
    bl = np.array(base[n]["loc"]); bb = np.array(base[n]["brk"])
    # location-matched baseline rate
    idx = np.clip(np.digitize(loc, BINS) - 1, 0, 9)
    bidx = np.clip(np.digitize(bl, BINS) - 1, 0, 9)
    exp = np.mean([np.mean(bb[bidx == i] == p) for i in idx])
    raw_base = np.mean(bb == p)
    print(f"\n{k} (n={len(brk)}, avg close location {loc.mean():.2f})")
    print(f"  breaks in predicted direction: {rate:.0%} | all-days baseline {raw_base:.0%} | "
          f"LOCATION-MATCHED baseline {exp:.0%} | pattern minus matched {100*(rate-exp):+.0f} pts "
          f"(se ~{100*np.sqrt(rate*(1-rate)/len(brk)):.0f})")
    print(f"  fwd 10d return in predicted direction, drift-adjusted: {fw.mean():+.3f} ATR (se {fw.std()/np.sqrt(len(fw)):.3f})")
