"""RSI-2 endeks dışında ve satış yönünde çalışır mı? (kullanıcının sorusu, 2026-11-27)

Kural (Connors, verify_rsi2_timesplit.py ile aynı):
  ALIŞ : kapanış > SMA200 ve RSI(2) < 10 → kapanışta al; ilk kapanış > SMA5'te çık (en çok 10 gün).
  SATIŞ: kapanış < SMA200 ve RSI(2) > 90 → kapanışta sat; ilk kapanış < SMA5'te çık (en çok 10 gün). (aynanın tersi)
Kıyas: her işlem için aynı sembolde, aynı 5 yıllık dönemde, aynı rejimde (alışta SMA200 üstü, satışta altı) rastgele
5 gün, aynı süre tutulmuş, aynı yönde. Birim: girişteki ATR(14) (R). Maliyet yok (fark ölçüsünde iki tarafa da
benzer düşer; tutma ~3 gün).
Gruplar: endeks (kıyas), emtia ETF'leri, kripto, ABD büyük 10 + sağlık, BIST 100 ve Türk enerji hisseleri, pariteler.
Ek: sinyallerin S&P 500 (SPY) sinyalleriyle aynı günlere düşme payı ve 2015+ günlük getiri korelasyonu.
Veri: Yahoo Finance günlük (auto_adjust). Çıktı: verify_rsi2_genis_sonuc.txt.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GRUP = {
    "Endeks (kıyas)": "SPY QQQ IWM DIA EWG EWJ EWU",
    "Emtia": "GLD SLV USO",
    "Kripto": "BTC-USD ETH-USD",
    "ABD büyük 10": "NVDA AAPL MSFT AMZN GOOGL META TSLA AVGO JPM BRK-B",
    "Sağlık": "XLV UNH JNJ LLY",
    "Türkiye": "XU100.IS TUPRS.IS AKSEN.IS ENJSA.IS ZOREN.IS ODAS.IS",
    "Parite": "EURUSD=X GBPUSD=X USDJPY=X",
}
AD = {"GLD": "altın", "SLV": "gümüş", "USO": "petrol", "XLV": "sağlık sektörü", "XU100.IS": "BIST 100", "TUPRS.IS": "Tüpraş",
      "AKSEN.IS": "Aksa Enerji", "ENJSA.IS": "Enerjisa", "ZOREN.IS": "Zorlu Enerji", "ODAS.IS": "Odaş", "EWG": "Almanya",
      "EWJ": "Japonya", "EWU": "İngiltere"}


def rsi(c, n=2):
    d = np.diff(c, prepend=c[0]); up = np.clip(d, 0, None); dn = np.clip(-d, 0, None)
    au = np.zeros_like(c); ad = np.zeros_like(c)
    for i in range(1, len(c)):
        au[i] = au[i - 1] + (up[i] - au[i - 1]) / n; ad[i] = ad[i - 1] + (dn[i] - ad[i - 1]) / n
    return 100 - 100 / (1 + au / np.where(ad == 0, 1e-12, ad))


def yukle(s):
    d = yf.download(s, start="2003-01-01", interval="1d", progress=False, auto_adjust=True)
    if d is None or len(d) < 400:
        return None
    if hasattr(d.columns, "levels"):
        d.columns = d.columns.get_level_values(0)
    d = d.dropna()
    return d[(d.High > 0) & (d.Low > 0) & (d.Close > 0)]


def islemler(s, d):
    H, L, C = (d[c].to_numpy(float) for c in ("High", "Low", "Close")); yr = d.index.year.to_numpy()
    tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)), abs(L - np.roll(C, 1))))
    atr = pd.Series(tr).rolling(14).mean().to_numpy()
    sma200 = pd.Series(C).rolling(200).mean().to_numpy(); sma5 = pd.Series(C).rolling(5).mean().to_numpy()
    r2 = rsi(C); T = len(C); rng = np.random.default_rng(sum(map(ord, s)))
    out = []
    for yon in (1, -1):
        rejim = np.array([t for t in range(201, T - 11) if (C[t] - sma200[t]) * yon > 0])
        if len(rejim) < 50:
            continue
        t = 201
        while t < T - 11:
            if (C[t] - sma200[t]) * yon > 0 and (r2[t] < 10 if yon == 1 else r2[t] > 90):
                h = 1
                while h < 10 and (C[t + h] - sma5[t + h]) * yon <= 0:
                    h += 1
                R = yon * (C[t + h] - C[t]) / atr[t]
                ayni = rejim[(yr[rejim] // 5 == yr[t] // 5)]
                sec = rng.choice(ayni if len(ayni) else rejim, 5)
                bR = np.mean([yon * (C[u + h] - C[u]) / atr[u] for u in sec])
                out.append((s, yon, d.index[t], yr[t], R, bR))
                t += h + 1
            else:
                t += 1
    return out


def main():
    satir, getiri = [], {}
    for g, semboller in GRUP.items():
        for s in semboller.split():
            d = yukle(s)
            if d is None:
                print(f"  {s}: veri yok"); continue
            satir += [(g,) + x for x in islemler(s, d)]
            getiri[s] = d.Close.pct_change()
    A = pd.DataFrame(satir, columns=["grup", "sembol", "yon", "tarih", "yil", "R", "taban"])
    A["fark"] = A.R - A.taban
    A["donem"] = np.where(A.yil < 2015, "2015 öncesi", "2015+")
    cikti = []
    yaz = cikti.append

    def ozet(x):
        f = x.fark
        return pd.Series(dict(n=len(x), RSI2=x.R.mean(), rastgele=x.taban.mean(), fark=f.mean(),
                              se=f.std(ddof=1) / np.sqrt(len(x)) if len(x) > 1 else np.nan, isabet=(x.R > 0).mean()))
    pd.set_option("display.width", 220); pd.set_option("display.max_rows", 300)
    yaz("RSI-2, gruplar × yön × dönem (R = ATR; fark = RSI-2 − aynı dönem/rejim/yön rastgele; se = standart hata)")
    G = A.groupby(["grup", "yon", "donem"]).apply(ozet, include_groups=False).round(3)
    yaz(G.to_string())
    yaz("\nSembol başına, 2015+ (fark ve se)")
    S = A[A.yil >= 2015].groupby(["grup", "sembol", "yon"]).apply(ozet, include_groups=False).round(3)
    S.index = S.index.set_levels([[f"{x} ({AD[x]})" if x in AD else x for x in S.index.levels[1]]], level=[1])
    yaz(S.to_string())
    # aynı gün: SPY alış sinyalinden ±1 gün içinde düşen alış sinyali payı
    spy = set(A[(A.sembol == "SPY") & (A.yon == 1)].tarih.dt.normalize())
    spy |= {t + pd.Timedelta(days=k) for t in spy for k in (-1, 1)}
    yaz("\nAlış sinyallerinin SPY alış sinyaliyle aynı günlere (±1 gün) düşme payı, 2015+")
    B = A[(A.yon == 1) & (A.yil >= 2015)]
    for g, x in B.groupby("grup"):
        yaz(f"  {g:16s} {x.tarih.dt.normalize().isin(spy).mean():.0%}  ({len(x)} sinyal)")
    R = pd.DataFrame(getiri).loc["2015":]
    kor = R.corr()["SPY"].drop("SPY")
    yaz("\nGünlük getiri korelasyonu, SPY ile (2015+): " + ", ".join(f"{AD.get(k, k)} {v:+.2f}" for k, v in kor.sort_values().items()))
    metin = "\n".join(cikti)
    print(metin)
    Path(__file__).with_name("verify_rsi2_genis_sonuc.txt").write_text(metin, encoding="utf-8")


if __name__ == "__main__":
    main()
