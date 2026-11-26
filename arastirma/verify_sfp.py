"""Round 42: Trader Dante's Swing Failure Pattern (SFP, NrIXfv94Jgs): "the market breaks a prior swing high and
CLOSES BELOW it -> bearish (mirror for bullish). Traders get trapped, stops above swing points are liquidity.
You have to be picky; a lot of people trade every SFP." He shows it on the Bund, H1.
Test the UNFILTERED pattern (Dante's own baseline) on 1h data (~2 years): swing high = highest high of +-5 bars
(known 5 bars later); the most recent untaken swing high/low is the reference; SFP bar = trades through it and closes
back on the other side. Trade: enter at SFP bar close, stop 1 tick beyond the SFP bar extreme (min 0.25 ATR),
target 2R, time exit 48 bars. Baseline: random bars, same side, same stop distance in ATR, same exits.
Also: is the SFP better when the swing is 'longer' (deeper swing) - Dante's point that longer swings matter more.
No costs (1h FX costs ~0.10R per trade, 04 §5b).
"""
import sys

import numpy as np
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SYMS = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "ES=F", "NQ=F", "GC=F", "CL=F", "ZN=F", "BTC-USD"]
K = 5


def trade(H, L, C, t, side, stop, k=2.0, maxb=48):
    entry = C[t]; risk = abs(entry - stop)
    tgt = entry + side * k * risk
    for j in range(t + 1, min(t + 1 + maxb, len(C))):
        if (side == 1 and L[j] <= stop) or (side == -1 and H[j] >= stop):
            return -1.0
        if (side == 1 and H[j] >= tgt) or (side == -1 and L[j] <= tgt):
            return k
    j = min(t + maxb, len(C) - 1)
    return side * (C[j] - entry) / risk


pooled = {"sfp": [], "base": [], "sfp_deep": [], "sfp_shallow": []}
print("Unfiltered SFP, 1h, ~2y, 2R target / stop beyond SFP bar / 48 bars. mean R (win%) n | random baseline")
for s in SYMS:
    d = yf.download(s, period="730d", interval="1h", progress=False, auto_adjust=False)
    if d is None or len(d) < 1000:
        continue
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna()
    H, L, C = (d[c].values for c in ("High", "Low", "Close"))
    tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = np.convolve(tr, np.ones(24) / 24, mode="full")[:len(tr)]
    rng = np.random.default_rng(sum(map(ord, s)))
    res, base, deep, shallow = [], [], [], []
    sh = None; sl = None        # (level, index, swing depth in ATR)
    for t in range(2 * K + 30, len(C) - 49):
        i = t - K                # bar i becomes a confirmed swing at t
        if H[i] == H[i - K:i + K + 1].max():
            depth = (H[i] - L[i:t + 1].min()) / atr[i]
            sh = (H[i], i, depth)
        if L[i] == L[i - K:i + K + 1].min():
            depth = (H[i:t + 1].max() - L[i]) / atr[i]
            sl = (L[i], i, depth)
        a = atr[t]
        if a <= 0:
            continue
        for side, ref in ((-1, sh), (1, sl)):
            if ref is None:
                continue
            lvl = ref[0]
            broke = H[t] > lvl if side == -1 else L[t] < lvl
            if not broke:
                continue
            closed_back = C[t] < lvl if side == -1 else C[t] > lvl
            if closed_back:
                stop = (H[t] if side == -1 else L[t]) - side * 0.0
                if abs(C[t] - stop) < 0.25 * a:
                    stop = C[t] - side * 0.25 * a
                r = trade(H, L, C, t, side, stop)
                res.append(r); (deep if ref[2] >= 3 else shallow).append(r)
                u = rng.integers(60, len(C) - 49)
                dist = abs(C[t] - stop) / a
                base.append(trade(H, L, C, u, side, C[u] - side * dist * atr[u]))
            if side == -1: sh = None
            else: sl = None           # level is taken either way
    for k_, v in (("sfp", res), ("base", base), ("sfp_deep", deep), ("sfp_shallow", shallow)):
        pooled[k_] += v
    r = np.array(res); b = np.array(base)
    print(f"  {s:9s}: SFP {r.mean():+.3f} ({np.mean(r > 0):.0%}) n={len(r)} | base {b.mean():+.3f} ({np.mean(b > 0):.0%}) | "
          f"deep swing {np.mean(deep) if deep else np.nan:+.3f} n={len(deep)} | shallow {np.mean(shallow) if shallow else np.nan:+.3f}")
r = np.array(pooled["sfp"]); b = np.array(pooled["base"])
se = np.sqrt(r.var() / len(r) + b.var() / len(b))
print(f"\nPOOLED: SFP {r.mean():+.3f}R (win {np.mean(r > 0):.0%}, n={len(r)}) | random {b.mean():+.3f}R | diff {r.mean() - b.mean():+.3f} "
      f"(se {se:.3f}) | deep-swing SFP {np.mean(pooled['sfp_deep']):+.3f} (n={len(pooled['sfp_deep'])}) | shallow "
      f"{np.mean(pooled['sfp_shallow']):+.3f} (n={len(pooled['sfp_shallow'])})")
