"""CHoCH + geri test (akademi "donus" dedektörü), bütün sinyaller ve 10 bağlam filtresinin 1-3'lü bütün birleşimleri.

Kullanıcının isteği: "Her dönemi çek, hangi dönemde hangisi en iyi söyle, her kombinasyonu dene." Önceden yazılan kurgu:
- Sinyaller: 5 piyasa (BTC, altın, EUR/USD, GBP/USD, USD/JPY), 1H ve 4H, verinin tamamı (bankadaki örneklem değil).
  Her sinyalin ders kitabı işlemi (stop geri test ucunun 0,2 ATR ötesi, hedef 2R, en çok 60 mum) 1m ile, maliyet dahil.
- Filtreler (karar anına kadar kapanmış mumlarla):
  ust_trend   bir üst TF'de EMA20/EMA50 sırası işlem yönüyle: uyumlu / ters
  supurme     CHoCH öncesi uç, önceki onaylı swing ucunu fitille aşıp gerisinde kapandı: var / yok
  ema_testi   geri test EMA20'ye değdi: evet / hayır
  rsi_gunluk  son kapanmış günlük RSI(14), işlem yönüne çevrilmiş (short'ta 100 − RSI): <40 / 40-60 / >60
  adx_4h      son kapanmış 4H ADX(14): <20 / 20-30 / >30
  hacim       giriş TF'de karar mumunun hacmi ÷ önceki 20 mum ortalaması: <0,8 / 0,8-1,5 / >1,5 (FX'te hacim verisi yok)
  ema200      günlük kapanış EMA200'ün işlem yönündeki tarafında mı: lehine / aleyhine
  vol_rejim   giriş TF'de ATR14 ÷ ATR100: <0,8 / 0,8-1,2 / >1,2
  seans       karar anı UTC: Asya / Londra / New York / Geç saat
  gun         haftanın günü (UTC)
- Kombinasyon: farklı filtrelerin 1, 2 ve 3 koşulunun bütün birleşimleri.
- Dönemler: (a) yıl yıl; (b) seç = karar anı < 2023, doğrula = 2023, sına = 2024-2026.
  Seçim ölçütü: seçim döneminde n ≥ 40 ve t ≥ 3. Geçme: doğrulamada ve sınavda ortalama > 0, ikisinin birleşiminde t ≥ 2.
- Şans makinesi: sonuçlar (R) aynı yıl ve aynı piyasa içinde karıştırılır, aynı seçim ve geçme kuralı uygulanır (20 tekrar).
"""
import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BACKEND = Path(r"C:\Users\mimi\Desktop\btc-order\backend")
sys.path.insert(0, str(BACKEND))
from app.akademi import senaryo, veri  # noqa: E402
from app.akademi.sonuc import M1, simule  # noqa: E402

SEMBOLLER = ["BTCUSD", "XAUUSD", "EURUSD", "GBPUSD", "USDJPY"]
UST = {"1H": "4H", "4H": "1D"}
FILTRELER = ["ust_trend", "supurme", "ema_testi", "rsi_gunluk", "adx_4h", "hacim", "ema200", "vol_rejim", "seans", "gun"]
GUNLER = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]


def rsi(c, n=14):
    d = np.diff(c, prepend=c[0])
    up = pd.Series(np.maximum(d, 0)).ewm(alpha=1 / n, adjust=False).mean()
    dn = pd.Series(np.maximum(-d, 0)).ewm(alpha=1 / n, adjust=False).mean()
    return (100 - 100 / (1 + up / dn.replace(0, np.nan))).to_numpy()


def adx(h, l, c, n=14):
    tr = np.maximum(h - l, np.maximum(np.abs(h - np.r_[c[0], c[:-1]]), np.abs(l - np.r_[c[0], c[:-1]])))
    up, dn = np.diff(h, prepend=h[0]), -np.diff(l, prepend=l[0])
    pdm, mdm = np.where((up > dn) & (up > 0), up, 0.0), np.where((dn > up) & (dn > 0), dn, 0.0)
    r = lambda x: pd.Series(x).ewm(alpha=1 / n, adjust=False).mean().to_numpy()   # noqa: E731
    ta = r(tr)
    pdi, mdi = 100 * r(pdm) / ta, 100 * r(mdm) / ta
    return r(100 * np.abs(pdi - mdi) / np.maximum(pdi + mdi, 1e-12))


def asof(kapanis, deger, t):
    j = int(np.searchsorted(kapanis, t, side="right")) - 1
    return deger[j] if j >= 0 else np.nan


def sinyaller() -> pd.DataFrame:
    a = veri.ayar(None)
    s_ = a["senaryo"]
    satir = []
    for s in SEMBOLLER:
        sb = a["semboller"][s]
        m1 = M1.df(veri.m1_oku(s, cfg=None))
        gun = veri.tf_oku(s, "1D", None)
        gc = gun["close"].to_numpy(float)
        g_kap = gun["close_ts"].to_numpy("int64")
        g_rsi, g_e200 = rsi(gc), senaryo.ema(gc, 200)
        h4 = veri.tf_oku(s, "4H", None)
        h4_kap, h4_adx = h4["close_ts"].to_numpy("int64"), adx(*(h4[k].to_numpy(float) for k in ("high", "low", "close")))
        for tf in ("1H", "4H"):
            d = veri.tf_oku(s, tf, None).reset_index(drop=True)
            d = d[(d.ts >= m1.ts[0]) & (d.close_ts <= m1.ts[-1])].reset_index(drop=True)
            ts, kap = d["ts"].to_numpy("int64"), d["close_ts"].to_numpy("int64")
            h, l, c, v = (d[k].to_numpy(float) for k in ("high", "low", "close", "volume"))
            A14 = senaryo.atr(d)
            A100 = senaryo.atr(d, 100)
            e20 = senaryo.ema(c, 20)
            st_t, st_d = senaryo.swinglar(h, l, s_["pivot"])
            ut = veri.tf_oku(s, UST[tf], None)
            u_kap = ut["close_ts"].to_numpy("int64")
            uc = ut["close"].to_numpy(float)
            u_sira = np.sign(senaryo.ema(uc, 20) - senaryo.ema(uc, 50))
            vort = pd.Series(v).shift(1).rolling(20).mean().to_numpy()
            olaylar = [e for e in senaryo.tespit(d, a, tf, s) if e["tur"] == "donus"]
            for e in olaylar:
                t, y = e["t"], e["yon"]
                if t + s_["gelecek_mum"] >= len(d) or np.diff(ts[max(0, t - 160):t + s_["gelecek_mum"] + 1]).max() > 72 * 3_600_000:
                    continue
                r = simule(m1, int(kap[t]), int(kap[t + s_["gelecek_mum"]]), y, e["stop"], e["hedef"], sb["maliyet"])
                if r is None:
                    continue
                isr = {lab: idx for idx, _, lab in e["isaret"]}
                i_uc = isr.get("son tepe" if y < 0 else "son dip")
                i_test = isr.get("geri test tepesi" if y < 0 else "geri test dibi")
                supurme = False
                if i_uc is not None and i_uc > 10:
                    bay = st_t if y < 0 else st_d
                    aday = np.flatnonzero(bay[: max(0, i_uc - 3)])
                    aday = aday[aday + 3 <= i_uc]
                    if len(aday):
                        j = int(aday[-1])
                        supurme = (h[i_uc] > h[j] and c[i_uc] < h[j]) if y < 0 else (l[i_uc] < l[j] and c[i_uc] > l[j])
                ema_t = i_test is not None and ((h[i_test] >= e20[i_test]) if y < 0 else (l[i_test] <= e20[i_test]))
                ust = asof(u_kap, u_sira, kap[t])
                rg = asof(g_kap, g_rsi, kap[t])
                rg = 100 - rg if y < 0 else rg
                ad = asof(h4_kap, h4_adx, kap[t])
                gk, ge = asof(g_kap, gc, kap[t]), asof(g_kap, g_e200, kap[t])
                hv = v[t] / vort[t] if vort[t] and vort[t] > 0 else np.nan
                vr = A14[t] / A100[t] if A100[t] > 0 else np.nan
                saat = pd.Timestamp(int(kap[t]), unit="ms", tz="UTC")
                satir.append({
                    "sembol": s, "tf": tf, "yon": y, "karar_t": int(kap[t]), "yil": saat.year, "r": r["r_net"],
                    "ust_trend": "uyumlu" if ust == y else "ters",
                    "supurme": "var" if supurme else "yok",
                    "ema_testi": "evet" if ema_t else "hayır",
                    "rsi_gunluk": None if np.isnan(rg) else "<40" if rg < 40 else "40-60" if rg <= 60 else ">60",
                    "adx_4h": None if np.isnan(ad) else "<20" if ad < 20 else "20-30" if ad <= 30 else ">30",
                    "hacim": None if np.isnan(hv) else "<0,8" if hv < 0.8 else "0,8-1,5" if hv <= 1.5 else ">1,5",
                    "ema200": None if np.isnan(ge) else ("lehine" if (gk - ge) * y > 0 else "aleyhine"),
                    "vol_rejim": None if np.isnan(vr) else "<0,8" if vr < 0.8 else "0,8-1,2" if vr <= 1.2 else ">1,2",
                    "seans": "Asya" if saat.hour < 7 else "Londra" if saat.hour < 12 else "New York" if saat.hour < 20 else "Geç saat",
                    "gun": GUNLER[saat.dayofweek],
                })
        print(f"{s}: {sum(1 for x in satir if x['sembol'] == s)} sinyal", flush=True)
    return pd.DataFrame(satir)


def kosullar(df: pd.DataFrame) -> list[tuple]:
    return [(f, v) for f in FILTRELER for v in sorted(df[f].dropna().unique())]


def kombinasyonlar(df: pd.DataFrame) -> list[tuple]:
    k = kosullar(df)
    out = []
    for n in (1, 2, 3):
        for kom in itertools.combinations(k, n):
            if len({f for f, _ in kom}) == n:
                out.append(kom)
    return out


def maske(df, kom):
    m = np.ones(len(df), bool)
    for f, v in kom:
        m &= (df[f] == v).to_numpy()
    return m


def ist(r):
    n = len(r)
    if n < 2:
        return n, np.nan, np.nan
    m, s = r.mean(), r.std(ddof=1)
    return n, m, m / (s / np.sqrt(n)) if s > 0 else np.nan


def tarama(df: pd.DataFrame, r: np.ndarray, komlar: list, maskeler: list) -> dict:
    sec, dog, sin = df.karar_t < pd.Timestamp("2023-01-01", tz="UTC").value // 10**6, df.yil == 2023, df.yil >= 2024
    sec, dog, sin = sec.to_numpy(), dog.to_numpy(), sin.to_numpy()
    secilen, gecen = [], []
    for kom, m in zip(komlar, maskeler):
        n, ort, t = ist(r[m & sec])
        if n >= 40 and t >= 3:
            n2, o2, _ = ist(r[m & dog])
            n3, o3, _ = ist(r[m & sin])
            nb, ob, tb = ist(r[m & (dog | sin)])
            kayit = {"kom": " + ".join(f"{f}={v}" for f, v in kom), "n_sec": n, "ort_sec": ort, "t_sec": t,
                     "n_2023": n2, "ort_2023": o2, "n_2024_26": n3, "ort_2024_26": o3, "t_sonra": tb}
            secilen.append(kayit)
            if (o2 or -1) > 0 and (o3 or -1) > 0 and (tb or 0) >= 2:
                gecen.append(kayit)
    return {"secilen": secilen, "gecen": gecen}


if __name__ == "__main__":
    yol = Path(__file__).with_name("verify_choch_kombinasyon_sinyal.parquet")
    df = pd.read_parquet(yol) if yol.exists() else sinyaller()
    df.to_parquet(yol, index=False)
    r = df.r.to_numpy(float)
    komlar = kombinasyonlar(df)
    maskeler = [maske(df, k) for k in komlar]
    print(f"\nToplam sinyal: {len(df)}, ortalama {r.mean():+.3f}R | kombinasyon sayısı: {len(komlar)}")
    print("Yıllara göre sinyal ve ortalama:", df.groupby("yil").r.agg(["count", "mean"]).round(3).to_dict("index"))

    # (a) her yıl en iyi kombinasyon ve ertesi yıl ne yaptı
    print("\n=== Her yılın en iyisi (n ≥ 25) ve ertesi yıl ===")
    yillar = sorted(df.yil.unique())
    kalicilik = []
    for yil in yillar[:-1]:
        my, ms = (df.yil == yil).to_numpy(), (df.yil == yil + 1).to_numpy()
        en = None
        for kom, m in zip(komlar, maskeler):
            n, ort, t = ist(r[m & my])
            if n >= 25 and (en is None or ort > en[1]):
                en = (kom, ort, n, t, m)
        if en:
            n2, o2, _ = ist(r[en[4] & ms])
            kalicilik.append(o2)
            print(f"{yil}: {' + '.join(f'{f}={v}' for f, v in en[0])} | {yil}: {en[1]:+.2f}R (n={en[2]}) → {yil + 1}: {o2:+.2f}R (n={n2})")
    print(f"Yılın en iyisinin ertesi yıl ortalaması: {np.nanmean(kalicilik):+.3f}R | o yılların bütün sinyalleri: {r[df.yil.isin(yillar[1:]).to_numpy()].mean():+.3f}R")

    # (b) seç / doğrula / sına + şans makinesi
    g = tarama(df, r, komlar, maskeler)
    print(f"\n=== Seç (<2023) / doğrula (2023) / sına (2024-26) ===\nSeçilen (n ≥ 40, t ≥ 3): {len(g['secilen'])} | geçen: {len(g['gecen'])}")
    for k in sorted(g["secilen"], key=lambda x: -x["t_sec"])[:15]:
        print(f"  {k['kom']}: seç {k['ort_sec']:+.2f}R (n={k['n_sec']}, t={k['t_sec']:.1f}) | 2023 {k['ort_2023']:+.2f}R (n={k['n_2023']}) | 2024-26 {k['ort_2024_26']:+.2f}R (n={k['n_2024_26']})")
    print("Geçenler:")
    for k in g["gecen"]:
        print(f"  {k['kom']}: seç {k['ort_sec']:+.2f} (n={k['n_sec']}) | 2023 {k['ort_2023']:+.2f} (n={k['n_2023']}) | 2024-26 {k['ort_2024_26']:+.2f} (n={k['n_2024_26']}), sonrası t={k['t_sonra']:.1f}")
    rng = np.random.default_rng(3)
    sans = []
    for _ in range(20):
        rk = r.copy()
        for _, idx in df.groupby(["yil", "sembol"]).indices.items():
            rk[idx] = rk[idx][rng.permutation(len(idx))]
        gs = tarama(df, rk, komlar, maskeler)
        sans.append((len(gs["secilen"]), len(gs["gecen"])))
    s = np.array(sans)
    print(f"Şans makinesi (20 tekrar): seçilen ortalama {s[:, 0].mean():.1f}, geçen ortalama {s[:, 1].mean():.2f} (en çok {s[:, 1].max()})")
