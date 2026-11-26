"""Kullanıcının kurulumu: CHoCH + geri test (akademi dedektörü "donus"), filtrelerle.

Veri: btc-order akademi senaryo bankası (senaryolar.parquet), tur == "donus": 5 piyasa (BTC, altın, EUR/USD, GBP/USD,
USD/JPY), 1H ve 4H, ders kitabı işleminin 1m mumlarla maliyet sonrası sonucu (kitap_r). Bütün özellikler yalnız karar
anına kadar bilinen mumlarla hesaplanır:
  ust_trend   bir üst zaman diliminde (1H→4H, 4H→1D) EMA20 ile EMA50'nin sıralaması işlem yönüyle aynı mı
  supurme     CHoCH'tan önceki uç (short'ta son tepe), ondan önceki onaylı swing ucunu fitille aşıp onun gerisinde
              kapandı mı (kullanıcının örneğindeki "son tepeye fitil atıp longları patlatmış")
  ema_testi   geri test EMA20'ye değdi mi (yoksa yalnız kırılan seviyeye mi)
  guclu_tetik tetik mumunun gövdesi aralığının ≥ %50'si ve kapanışı işlem yönündeki uca yakın (son %30)
  seans       karar anının UTC saati
Ölçüt (önceden yazıldı): bir filtre ancak (1) grubun ortalaması maliyetten sonra > 0, (2) "donus hepsi"nden ≥ 2 standart
hata iyi ve (3) 2023 öncesi ve sonrası iki dönemde de > 0 ise "aday" sayılır. Çok sayıda bölme yapıldığı için tek bir
"aday" şans olabilir (yaklaşık 20 karşılaştırmada ~1 sahte isabet beklenir).
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BACKEND = Path(r"C:\Users\mimi\Desktop\btc-order\backend")
sys.path.insert(0, str(BACKEND))
from app.akademi import senaryo, veri  # noqa: E402

UST = {"1H": "4H", "4H": "1D"}
YIL_BOLME = pd.Timestamp("2023-01-01", tz="UTC").value // 10**6


def ozellikler(b: pd.DataFrame) -> pd.DataFrame:
    satir = []
    onbellek: dict = {}

    def tf(sembol, t):
        k = (sembol, t)
        if k not in onbellek:
            d = veri.tf_oku(sembol, t, None).reset_index(drop=True)
            onbellek[k] = (d, senaryo.ema(d["close"].to_numpy(float), 20), senaryo.ema(d["close"].to_numpy(float), 50),
                           senaryo.swinglar(d["high"].to_numpy(float), d["low"].to_numpy(float), 3))
        return onbellek[k]

    for s in b.itertuples():
        d, e20, _, (st_t, st_d) = tf(s.sembol, s.tf)
        du, u20, u50, _ = tf(s.sembol, UST[s.tf])
        ts = d["ts"].to_numpy("int64")
        h, l, o, c = (d[k].to_numpy(float) for k in ("high", "low", "open", "close"))
        n = json.loads(s.notlar)
        isr = {y: t for t, _, y in n["isaret"]}
        y = int(s.yon)
        t_uc = isr.get("son tepe" if y < 0 else "son dip")
        t_test = isr.get("geri test tepesi" if y < 0 else "geri test dibi")
        i_k = int(np.searchsorted(ts, s.ts))
        i_uc = int(np.searchsorted(ts, t_uc)) if t_uc else None
        i_test = int(np.searchsorted(ts, t_test)) if t_test else None
        # üst zaman dilimi trendi (karar anına kadar kapanmış üst mumlar)
        j = int(np.searchsorted(du["close_ts"].to_numpy("int64"), s.karar_t, side="right")) - 1
        ust = int(np.sign(u20[j] - u50[j])) if j >= 50 else 0
        # süpürme: uçtan önceki onaylı swing (uçtan en az 3 mum önce onaylanmış)
        supurme = False
        if i_uc is not None and i_uc > 10:
            bayrak = st_t if y < 0 else st_d
            aday = np.flatnonzero(bayrak[: max(0, i_uc - 3)])
            aday = aday[aday + 3 <= i_uc]
            if len(aday):
                jj = int(aday[-1])
                if y < 0:
                    supurme = bool(h[i_uc] > h[jj] and c[i_uc] < h[jj])
                else:
                    supurme = bool(l[i_uc] < l[jj] and c[i_uc] > l[jj])
        ema_testi = bool(i_test is not None and ((h[i_test] >= e20[i_test]) if y < 0 else (l[i_test] <= e20[i_test])))
        aralik = max(h[i_k] - l[i_k], 1e-12)
        govde = abs(c[i_k] - o[i_k]) / aralik
        uc_yakin = ((c[i_k] - l[i_k]) / aralik <= 0.3) if y < 0 else ((h[i_k] - c[i_k]) / aralik <= 0.3)
        saat = pd.Timestamp(s.karar_t, unit="ms", tz="UTC").hour
        satir.append({"id": s.id, "sembol": s.sembol, "tf": s.tf, "yon": y, "r": s.kitap_r, "donem": "2023+" if s.karar_t >= YIL_BOLME else "2023 öncesi",
                      "ust_trend": "uyumlu" if ust == y else "ters" if ust else "belirsiz", "supurme": "var" if supurme else "yok",
                      "ema_testi": "evet" if ema_testi else "hayır", "guclu_tetik": "evet" if (govde >= 0.5 and uc_yakin) else "hayır",
                      "seans": "Asya" if saat < 7 else "Londra" if saat < 12 else "New York" if saat < 20 else "Geç saat"})
    return pd.DataFrame(satir)


def ozet(g: pd.Series) -> dict:
    r = g.dropna()
    return {"n": len(r), "ort": round(r.mean(), 3), "se": round(r.std(ddof=1) / np.sqrt(len(r)), 3) if len(r) > 1 else np.nan,
            "isabet": round((r > 0).mean(), 3)}


if __name__ == "__main__":
    b = pd.read_parquet(r"C:\Users\mimi\Desktop\btc-order\data\akademi\senaryolar.parquet")
    b = b[(b.tur == "donus") & b.kitap_r.notna()].reset_index(drop=True)
    f = ozellikler(b)
    hepsi = ozet(f.r)
    print("Hepsi:", hepsi, "| aynı stop/RR rastgele giriş (banka özeti): -0.029")
    sonuc = []
    for kol in ("ust_trend", "supurme", "ema_testi", "guclu_tetik", "seans", "tf", "sembol", "yon"):
        for deger, g in f.groupby(kol):
            o = ozet(g.r)
            d1, d2 = (g[g.donem == p].r.mean() for p in ("2023 öncesi", "2023+"))
            fark_se = (o["ort"] - hepsi["ort"]) / o["se"] if o["se"] and o["se"] > 0 else 0
            aday = o["ort"] > 0 and fark_se >= 2 and d1 > 0 and d2 > 0
            sonuc.append({"filtre": kol, "deger": deger, **o, "2023_once": round(d1, 3), "2023_sonra": round(d2, 3), "aday": aday})
    # kullanıcının kombinasyonu: üst trend uyumlu + süpürme var (+ EMA testi)
    for ad, m in (("uyumlu + süpürme", (f.ust_trend == "uyumlu") & (f.supurme == "var")),
                  ("uyumlu + süpürme + EMA testi", (f.ust_trend == "uyumlu") & (f.supurme == "var") & (f.ema_testi == "evet")),
                  ("ters + süpürme (kullanıcının altın örneği gibi)", (f.ust_trend == "ters") & (f.supurme == "var")),
                  ("uyumlu + güçlü tetik", (f.ust_trend == "uyumlu") & (f.guclu_tetik == "evet"))):
        g = f[m]
        o = ozet(g.r)
        d1, d2 = (g[g.donem == p].r.mean() for p in ("2023 öncesi", "2023+"))
        sonuc.append({"filtre": "kombinasyon", "deger": ad, **o, "2023_once": round(d1, 3), "2023_sonra": round(d2, 3),
                      "aday": bool(o["ort"] > 0 and d1 > 0 and d2 > 0 and o["se"] and (o["ort"] - hepsi["ort"]) / o["se"] >= 2)})
    tablo = pd.DataFrame(sonuc)
    with pd.option_context("display.width", 200, "display.max_rows", 100):
        print(tablo.to_string(index=False))


def kirilim(f: pd.DataFrame) -> None:
    """Aday kombinasyonun sağlamlığı: yön, sembol, zaman dilimi ve yıl kırılımı."""
    m = (f.ust_trend == "uyumlu") & (f.supurme == "var") & (f.ema_testi == "evet")
    g = f[m].copy()
    g["yil"] = pd.to_datetime(g.id.str.split("-").str[-1].astype("int64"), unit="ms").dt.year
    for kol in ("yon", "sembol", "tf", "yil"):
        print(f"\n[{kol}]")
        for deger, x in g.groupby(kol):
            o = ozet(x.r)
            print(f"  {deger}: n={o['n']}, ort={o['ort']:+.3f}, se={o['se']}, isabet={o['isabet']}")
    # bootstrap: rastgele 318'lik donus alt kümelerinin ortalaması bu kadar yüksek olur mu?
    rng = np.random.default_rng(1)
    ort = np.array([f.r.sample(len(g), random_state=int(rng.integers(1e9))).mean() for _ in range(5000)])
    print(f"\nRastgele {len(g)}'lik donus alt kümesi ortalaması ≥ {g.r.mean():.3f} olma oranı: {(ort >= g.r.mean()).mean():.4f}")


if __name__ == "__main__":
    kirilim(f)
