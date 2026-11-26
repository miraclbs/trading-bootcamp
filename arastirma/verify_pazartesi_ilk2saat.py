import sys, numpy as np, pandas as pd, yfinance as yf
sys.stdout.reconfigure(encoding="utf-8")
for sym in ["SPY","QQQ"]:
    d = yf.download(sym, start="2000-01-01", end="2026-11-26", interval="1d", auto_adjust=False, progress=False)
    d.columns = [c[0] if isinstance(c, tuple) else c for c in d.columns]
    d["rng"] = (d.High - d.Low) / d.Open * 100
    d["oc"] = (d.Close - d.Open).abs() / d.Open * 100
    d["wd"] = d.index.day_of_week
    for per, sub in [("2000-2026", d), ("2020-2026", d[d.index >= "2020-01-01"])]:
        g = sub.groupby("wd")[["rng","oc"]].median()
        others = sub[sub.wd != 0].rng
        mon = sub[sub.wd == 0].rng
        # Welch t on log range
        a, b = np.log(mon), np.log(others)
        t = (a.mean()-b.mean())/np.sqrt(a.var()/len(a)+b.var()/len(b))
        print(f"{sym} {per} medyan gün içi aralık % (Pzt..Cum):", " ".join(f"{x:.2f}" for x in g.rng), f"| Pzt/diğer log-fark t={t:.1f}")
    h = yf.download(sym, period="729d", interval="1h", auto_adjust=False, progress=False)
    h.columns = [c[0] if isinstance(c, tuple) else c for c in h.columns]
    h.index = h.index.tz_convert("America/New_York")
    h = h[(h.index.time >= pd.Timestamp("09:30").time()) & (h.index.time < pd.Timestamp("16:00").time())]
    h["r"] = np.log(h.Close / h.Open)
    h["rng"] = (h.High - h.Low) / h.Open
    h["hr"] = h.index.strftime("%H:%M")
    s_abs = h.groupby("hr").r.apply(lambda x: x.abs().sum()); s_var = h.groupby("hr").r.apply(lambda x: (x**2).sum())
    s_rng = h.groupby("hr").rng.sum()
    print(f"{sym} 1h ({h.index[0].date()}..{h.index[-1].date()}) saat payları:")
    for k in s_abs.index:
        print(f"   {k}  |getiri| %{100*s_abs[k]/s_abs.sum():.1f}  varyans %{100*s_var[k]/s_var.sum():.1f}  aralık %{100*s_rng[k]/s_rng.sum():.1f}")
    first2 = [k for k in s_abs.index if k in ("09:30","10:30")]
    print(f"   İLK 2 SAAT (09:30-11:30, seans süresinin %31'i): |getiri| %{100*s_abs[first2].sum()/s_abs.sum():.0f}, varyans %{100*s_var[first2].sum()/s_var.sum():.0f}, aralık %{100*s_rng[first2].sum()/s_rng.sum():.0f}")
