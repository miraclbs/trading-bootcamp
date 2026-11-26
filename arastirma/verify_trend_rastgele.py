"""Kullanıcının sorusu: "Nereden açarsam açayım şansım %50 mi? Trend yukarıyken rastgele long, aşağıyken rastgele short
açınca 1:2, 1:1 ve 0,5:1 oranlarında sonuç ne olur? Trendi 1 saatlik, 4 saatlik ve günlükte; girişi 15 dakikalık,
1 saatlik ve 4 saatlikte dene."

Kurgu:
- Trend: trend zaman diliminde EMA20 > EMA50 ise yukarı, altındaysa aşağı. Yalnız giriş anına kadar kapanmış mumlarla.
- Giriş: giriş zaman diliminde rastgele seçilen bir mumun kapanışı (piyasa başına zaman dilimi başına 1.500 an). Giriş,
  sonraki 1m mumunun açılışı. Stop 1 ATR(14) (giriş zaman dilimi), hedef RR × ATR. Stop ve hedef 1m mumlarla kontrol
  edilir; aynı dakikada ikisi görülürse stop. Fiyat stopun ötesinde açılırsa çıkış açılıştan. 60 mum içinde biri
  gelmezse son kapanıştan çıkış. Maliyet: akademinin piyasa maliyeti (FX gerçek spread, altın 0,35 $, BTC %0,0325/yön).
- "Trend yönünde": girişin yönü trend. "Rastgele yön": aynı anlarda long ve short sonucunun ortalaması (yazı-turanın
  beklenen değeri; aynı anlar kullanıldığı için fark yalnız yön seçiminden gelir).
- Piyasalar: BTCUSD (2017+), XAUUSD (2021+), EURUSD, GBPUSD, USDJPY (2020+). Hepsi birlikte ve piyasa piyasa.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BACKEND = Path(r"C:\Users\mimi\Desktop\btc-order\backend")
sys.path.insert(0, str(BACKEND))
from app.akademi import senaryo, veri  # noqa: E402
from app.akademi.sonuc import M1, maliyet_fiyat  # noqa: E402

SEMBOLLER = ["BTCUSD", "XAUUSD", "EURUSD", "GBPUSD", "USDJPY"]
GIRIS_TF = ["15m", "1H", "4H"]
TREND_TF = ["1H", "4H", "1D"]
RR = [2.0, 1.0, 0.5]
N, TUT, TOHUM = 1500, 60, 5


def cikis(m1: M1, i0: int, i1: int, y: int, giris: float, stop: float, hedef: float) -> float:
    h, l, o = m1.h[i0:i1], m1.l[i0:i1], m1.o[i0:i1]
    st = (l <= stop) if y > 0 else (h >= stop)
    hd = (h >= hedef) if y > 0 else (l <= hedef)
    js = int(np.argmax(st)) if st.any() else None
    jh = int(np.argmax(hd)) if hd.any() else None
    if js is not None and (jh is None or js <= jh):
        return float(min(o[js], stop)) if y > 0 else float(max(o[js], stop))
    if jh is not None:
        return float(max(o[jh], hedef)) if y > 0 else float(min(o[jh], hedef))
    return float(m1.c[i1 - 1])


def calistir() -> pd.DataFrame:
    rng = np.random.default_rng(TOHUM)
    satir = []
    for s in SEMBOLLER:
        sb = veri.ayar(None)["semboller"][s]
        m1 = M1.df(veri.m1_oku(s, cfg=None))
        trend = {}
        for ttf in TREND_TF:
            dt = veri.tf_oku(s, ttf, None)
            c = dt["close"].to_numpy(float)
            trend[ttf] = (dt["close_ts"].to_numpy("int64"), np.sign(senaryo.ema(c, 20) - senaryo.ema(c, 50)))
        for gtf in GIRIS_TF:
            d = veri.tf_oku(s, gtf, None).reset_index(drop=True)
            d = d[(d.ts >= m1.ts[0]) & (d.close_ts <= m1.ts[-1])].reset_index(drop=True)
            A = senaryo.atr(d)
            ts, kts = d["ts"].to_numpy("int64"), d["close_ts"].to_numpy("int64")
            aday = np.arange(300, len(d) - TUT - 1)
            aday = aday[[(np.diff(ts[i:i + TUT + 1]).max() <= 72 * 3_600_000) for i in aday]] if len(aday) < 400_000 else aday
            secilen = rng.choice(aday, min(N, len(aday)), replace=False)
            for e in secilen:
                i0 = int(np.searchsorted(m1.ts, kts[e], "left"))
                i1 = int(np.searchsorted(m1.ts, kts[e + TUT], "left"))
                if i1 - i0 < 10 or not A[e] > 0:
                    continue
                giris, risk = float(m1.o[i0]), float(A[e])
                mal_r = maliyet_fiyat(sb["maliyet"], giris, float(m1.sp[i0]), float(m1.sp[i0])) / risk
                sonuc = {}
                for y in (1, -1):
                    for rr in RR:
                        cx = cikis(m1, i0, i1, y, giris, giris - y * risk, giris + y * rr * risk)
                        sonuc[(y, rr)] = (cx - giris) * y / risk - mal_r
                for ttf in TREND_TF:
                    tk, tsg = trend[ttf]
                    j = int(np.searchsorted(tk, kts[e], "right")) - 1
                    if j < 60 or tsg[j] == 0:
                        continue
                    y = int(tsg[j])
                    for rr in RR:
                        satir.append({"sembol": s, "giris_tf": gtf, "trend_tf": ttf, "rr": rr, "yon": y,
                                      "trend_r": sonuc[(y, rr)], "rastgele_r": (sonuc[(1, rr)] + sonuc[(-1, rr)]) / 2,
                                      "long_r": sonuc[(1, rr)], "short_r": sonuc[(-1, rr)], "maliyet_r": mal_r})
        print(f"{s} tamam", flush=True)
    return pd.DataFrame(satir)


def tablo(df: pd.DataFrame, baslik: str) -> None:
    print(f"\n=== {baslik} ===")
    print(f"{'trend':>5} {'giriş':>5} {'RR':>4} | {'n':>5} | {'trend yönü: isabet / R':>24} | {'rastgele yön: isabet / R':>25} | {'fark (se)':>14} | başa baş")
    for (ttf, gtf, rr), g in df.groupby(["trend_tf", "giris_tf", "rr"], sort=False):
        n = len(g)
        fark = g.trend_r - g.rastgele_r
        isabet_t = (g.trend_r > 0).mean()
        isabet_r = ((g.long_r > 0).mean() + (g.short_r > 0).mean()) / 2
        print(f"{ttf:>5} {gtf:>5} {rr:>4} | {n:>5} | {isabet_t:>9.1%} / {g.trend_r.mean():+.3f}R | {isabet_r:>10.1%} / {g.rastgele_r.mean():+.3f}R | "
              f"{fark.mean():+.3f} ({fark.std(ddof=1) / np.sqrt(n):.3f}) | {1 / (1 + rr):.0%}")


if __name__ == "__main__":
    df = calistir()
    df.to_parquet(Path(__file__).with_name("verify_trend_rastgele_veri.parquet"), index=False)
    df["trend_tf"] = pd.Categorical(df.trend_tf, TREND_TF)
    df["giris_tf"] = pd.Categorical(df.giris_tf, GIRIS_TF)
    df = df.sort_values(["trend_tf", "giris_tf", "rr"], ascending=[True, True, False])
    tablo(df, "5 piyasa birlikte")
    print("\nOrtalama maliyet (R), giriş zaman dilimine göre:", df.groupby("giris_tf", observed=True).maliyet_r.mean().round(3).to_dict())
    print("\nPiyasa piyasa, trend 4H / giriş 1H / RR 2:")
    g = df[(df.trend_tf == "4H") & (df.giris_tf == "1H") & (df.rr == 2.0)]
    for s, x in g.groupby("sembol"):
        print(f"  {s}: n={len(x)}, trend {x.trend_r.mean():+.3f}R, rastgele {x.rastgele_r.mean():+.3f}R, sadece long {x.long_r.mean():+.3f}R, sadece short {x.short_r.mean():+.3f}R")
    print("\nTrend yönündeki işlemlerde long ve short ayrı (RR 2, bütün kombinasyonlar):")
    for y, x in df[df.rr == 2.0].groupby("yon"):
        print(f"  {'long' if y > 0 else 'short'}: n={len(x)}, {x.trend_r.mean():+.3f}R")
