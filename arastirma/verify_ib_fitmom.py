"""Fit Mom Trader, "my trading strategy is boring, but it made me $100,000 in 2 months" (LfSeAMzKjwM) testi.

İddia: "Initial balance benim ekmek teknem", "en iyi setup'ım ~%70 kazanıyor", NQ ve altın. Kurallar videodan:
  IB = New York 9:30-10:30 tepe/dip, IB orta = %50.
  TC  (trend devamı): IB yukarı trendliyse fiyat IB ortasına geri çekilir, reddedilir → long, hedef IB tepesi,
      stop son swing dibinin altı. Aşağı için tersi.
  FA  (failed auction): IB dışına çıkar, tutunamaz, içeri kapanır → IB ortasına doğru işlem, stop swing ucunun ötesi.
  ASYA: 18:00-20:00 ET aralığı; 20:00'den sonra uç süpürülüp içeri kapanırsa ters yöne işlem (hedef aralık ortası / 2R).
Kurallar sonuçlar görülmeden sabitlendi (2026-11-27):
  - Veri: HistData 1m bid. NAS100 = NSXUSD (veri_nq_indir.py), XAUUSD = spot altın (gosterge_lab/altin_spot.py).
    Saat New York (yaz saati dahil). 2020 → 2026-11.
  - Onay: 5 dakikalık mum kapanışı (9:30'a hizalı). Girişler 10:30-14:59 (son saat yok: videoda "power hour kötü").
    Açık işlem en geç 15:59 kapanışında kapanır. Asya: girişler 20:00-01:59, çıkış en geç 02:59.
  - TC yön: IB kapanışı > IB orta VE > IB açılışı → yukarı (tersi aşağı), yoksa işlem yok.
    TC-onay: IB ortasına ilk dokunan 5m mumdan sonraki 6 mum içinde ortanın üstünde kapanan boğa mumu → kapanışta giriş,
      stop = dokunuştan girişe kadarki en dip − 1 tick, hedef = IB tepesi.
    TC-limit: ilk dokunuşta IB ortasından limit giriş, hedef IB tepesi, stop = RR 1/2/3 verecek mesafe.
  - FA: IB dibinin altına inen ilk 5m mumdan sonra IB dibinin üstünde kapanan ilk 5m mum → kapanışta long,
    stop = kırılımdaki en dip − 1 tick, hedef = IB orta. Tepe için tersi. Gün başına her uçta en fazla bir işlem.
  - Swing stopu IB aralığının %10'undan darsa %10'a genişletilir (yoksa milimetrik stoplar R'yi anlamsızlaştırır).
  - Aynı 1m mumda hem stop hem hedef → kayıp (muhafazakâr). Stop boşlukla geçilirse açılıştan dolum.
  - Maliyet (gidiş-dönüş): NQ 0,5 puan, altın 0,25 $ (iyimser futures maliyeti). R'ye çevrilir.
  - Kıyas (şans makinesi): her işlem için aynı gün, aynı giriş penceresinde 20 rastgele dakika; aynı yön, aynı stop ve
    hedef mesafesi. Fark = setup'ın seviyeden/zamanlamadan gelen avantajı. İkinci kıyas: rastgele gün (mesafeler o günün
    IB aralığına ölçeklenir) → gün seçimi (IB yönü) dahil toplam avantaj.
Kullanım: python verify_ib_fitmom.py  → verify_ib_fitmom_sonuc.txt
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = Path(__file__).resolve().parent
SRC = {"NAS100": (B / "veri_nq" / "m1", 0.25, 0.5), "XAUUSD": (B / "veri_altin" / "m1", 0.1, 0.25)}
K = 20
RNG = np.random.default_rng(20261127)
MIN_STOP_FRAC = 0.10
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(s)


def yukle(sym):
    d = pd.concat([pd.read_parquet(f) for f in sorted(SRC[sym][0].glob("*.parquet"))], ignore_index=True)
    d = d.drop_duplicates("ts").sort_values("ts").reset_index(drop=True)
    t = pd.to_datetime(d.ts, unit="ms", utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
    d["dt"] = t
    return d


def seanslar(d, kayma_saat, bas_dk, uzunluk, min_bar):
    """Seans listesi: (tarih, dakika ofseti, o, h, l, c). kayma: seans başı gece yarısına gelsin diye saat kaydırma."""
    t = d.dt + pd.Timedelta(hours=kayma_saat)
    dk = (t.dt.hour * 60 + t.dt.minute).to_numpy() - bas_dk
    tarih = t.dt.normalize().to_numpy()
    sec = (dk >= 0) & (dk < uzunluk)
    o, h, l, c = (d[k].to_numpy()[sec] for k in ("open", "high", "low", "close"))
    dk, tarih = dk[sec], tarih[sec]
    sinir = np.flatnonzero(np.diff(tarih.astype("int64"))) + 1
    out = []
    for a, b in zip(np.r_[0, sinir], np.r_[sinir, len(dk)]):
        if b - a < min_bar:
            continue
        out.append((pd.Timestamp(tarih[a]), dk[a:b], o[a:b], h[a:b], l[a:b], c[a:b]))
    return out


def bes_dk(dk, o, h, l, c, lo, hi):
    """dk ∈ [lo, hi) aralığındaki 1m mumlardan 5m mumlar: (o, h, l, c, son 1m konumu)."""
    idx = np.flatnonzero((dk >= lo) & (dk < hi))
    if len(idx) == 0:
        return None
    kova = dk[idx] // 5
    _, bas = np.unique(kova, return_index=True)
    bit = np.r_[bas[1:], len(idx)] - 1
    return (o[idx[bas]], np.maximum.reduceat(h[idx], bas), np.minimum.reduceat(l[idx], bas), c[idx[bit]], idx[bit])


def sim(o, h, l, c, s, e, yon, giris, stop, hedef):
    """1m konum s..e. Döner: (kâr fiyat birimi, sonuç: 1 hedef, -1 stop, 0 süre)."""
    if s > e:
        return (c[e] - giris) * yon, 0
    hh, ll = h[s:e + 1], l[s:e + 1]
    if yon == 1:
        vs, vt = ll <= stop, hh >= hedef
    else:
        vs, vt = hh >= stop, ll <= hedef
    i_s = np.argmax(vs) if vs.any() else 10**9
    i_t = np.argmax(vt) if vt.any() else 10**9
    if i_s == 10**9 and i_t == 10**9:
        return (c[e] - giris) * yon, 0
    if i_s <= i_t:
        acilis = o[s + i_s]
        dolum = min(acilis, stop) if yon == 1 else max(acilis, stop)
        return (dolum - giris) * yon, -1
    return (hedef - giris) * yon, 1


def islem(gun, yon, poz, giris, stop, hedef, cikis_poz, ilk_bar_stop=False):
    """Giriş poz'daki mumun kapanışında (ya da limitle poz mumunda); sim poz+1'den."""
    dk, o, h, l, c = gun
    if ilk_bar_stop and ((yon == 1 and l[poz] <= stop) or (yon == -1 and h[poz] >= stop)):
        return (stop - giris) * yon, -1
    return sim(o, h, l, c, poz + 1, cikis_poz, yon, giris, stop, hedef)


def kayit(liste, tarih, yon, giris, stop, hedef, sonuc, rg, gun_i, pencere):
    pnl, kod = sonuc
    b = abs(giris - stop)
    liste.append(dict(tarih=tarih, yil=tarih.year, yon=yon, a=abs(hedef - giris), b=b, pnl=pnl, kod=kod,
                      rg=rg, gun_i=gun_i, pencere=pencere))


def stop_ayarla(giris, stop, yon, rg):
    if abs(giris - stop) < MIN_STOP_FRAC * rg:
        stop = giris - yon * MIN_STOP_FRAC * rg
    return stop


def rth_setuplari(ss, tick):
    """ss: seanslar (9:30 başlangıç, 390 dk). Setup başına işlem listesi."""
    S = {k: [] for k in ("TC-onay", "TC-limit RR1", "TC-limit RR2", "TC-limit RR3", "FA", "FA ≤30dk")}
    for gi, (tarih, dk, o, h, l, c) in enumerate(ss):
        ib = dk < 60
        if ib.sum() < 50 or (dk >= 60).sum() < 250:
            continue
        H, L = h[ib].max(), l[ib].min()
        M, rg = (H + L) / 2, H - L
        if rg <= 0:
            continue
        ib_ac, ib_kp = o[ib][0], c[ib][-1]
        cikis = len(dk) - 1
        pen = np.flatnonzero((dk >= 60) & (dk < 330))
        if len(pen) == 0:
            continue
        gun = (dk, o, h, l, c)
        b5 = bes_dk(dk, o, h, l, c, 60, 330)
        if b5 is None:
            continue
        O5, H5, L5, C5, P5 = b5
        # --- TC
        yon = 1 if (ib_kp > M and ib_kp > ib_ac) else -1 if (ib_kp < M and ib_kp < ib_ac) else 0
        if yon:
            hedef = H if yon == 1 else L
            dokun = (L5 <= M) if yon == 1 else (H5 >= M)
            if dokun.any():
                j = int(np.argmax(dokun))
                # limit: dokunulan ilk 1m mum
                m1 = (l[pen] <= M) if yon == 1 else (h[pen] >= M)
                p1 = pen[int(np.argmax(m1))]
                giris_l = M if (yon == 1 and o[p1] >= M) or (yon == -1 and o[p1] <= M) else o[p1]
                for rr in (1, 2, 3):
                    st = giris_l - yon * abs(hedef - giris_l) / rr
                    if abs(hedef - giris_l) > 0:
                        kayit(S[f"TC-limit RR{rr}"], tarih, yon, giris_l, st, hedef,
                              islem(gun, yon, p1, giris_l, st, hedef, cikis, ilk_bar_stop=True), rg, gi, pen)
                # onay
                for k in range(j, min(j + 6, len(C5))):
                    ok = (C5[k] > M and C5[k] > O5[k]) if yon == 1 else (C5[k] < M and C5[k] < O5[k])
                    if ok:
                        giris = C5[k]
                        uc = L5[j:k + 1].min() - tick if yon == 1 else H5[j:k + 1].max() + tick
                        st = stop_ayarla(giris, uc, yon, rg)
                        if (hedef - giris) * yon > 0:
                            kayit(S["TC-onay"], tarih, yon, giris, st, hedef,
                                  islem(gun, yon, P5[k], giris, st, hedef, cikis), rg, gi, pen)
                        break
        # --- FA (iki uç bağımsız)
        for yon_fa, kir, geri in ((1, L5 < L, C5 > L), (-1, H5 > H, C5 < H)):
            if not kir.any():
                continue
            b0 = int(np.argmax(kir))
            sonra = np.flatnonzero(geri[b0:])
            if len(sonra) == 0:
                continue
            b1 = b0 + int(sonra[0])
            giris = C5[b1]
            uc = L5[b0:b1 + 1].min() - tick if yon_fa == 1 else H5[b0:b1 + 1].max() + tick
            st = stop_ayarla(giris, uc, yon_fa, rg)
            if (M - giris) * yon_fa <= 0:
                continue
            sonuc = islem(gun, yon_fa, P5[b1], giris, st, M, cikis)
            kayit(S["FA"], tarih, yon_fa, giris, st, M, sonuc, rg, gi, pen)
            if b1 - b0 <= 6:
                kayit(S["FA ≤30dk"], tarih, yon_fa, giris, st, M, sonuc, rg, gi, pen)
    return S


def asya_setuplari(ss, tick):
    """ss: 18:00 başlangıçlı seanslar (540 dk). Aralık 0-119, girişler 120-479."""
    S = {k: [] for k in ("ASYA FA→orta", "ASYA FA→2R")}
    for gi, (tarih, dk, o, h, l, c) in enumerate(ss):
        ar = dk < 120
        if ar.sum() < 90 or (dk >= 120).sum() < 300:
            continue
        H, L = h[ar].max(), l[ar].min()
        M, rg = (H + L) / 2, H - L
        if rg <= 0:
            continue
        cikis = len(dk) - 1
        pen = np.flatnonzero((dk >= 120) & (dk < 480))
        b5 = bes_dk(dk, o, h, l, c, 120, 480)
        if b5 is None or len(pen) == 0:
            continue
        O5, H5, L5, C5, P5 = b5
        gun = (dk, o, h, l, c)
        for yon, kir, geri in ((1, L5 < L, C5 > L), (-1, H5 > H, C5 < H)):
            if not kir.any():
                continue
            b0 = int(np.argmax(kir))
            sonra = np.flatnonzero(geri[b0:])
            if len(sonra) == 0:
                continue
            b1 = b0 + int(sonra[0])
            giris = C5[b1]
            uc = L5[b0:b1 + 1].min() - tick if yon == 1 else H5[b0:b1 + 1].max() + tick
            st = stop_ayarla(giris, uc, yon, rg)
            if (M - giris) * yon > 0:
                kayit(S["ASYA FA→orta"], tarih, yon, giris, st, M,
                      islem(gun, yon, P5[b1], giris, st, M, cikis), rg, gi, pen)
            h2 = giris + yon * 2 * abs(giris - st)
            kayit(S["ASYA FA→2R"], tarih, yon, giris, st, h2,
                  islem(gun, yon, P5[b1], giris, st, h2, cikis), rg, gi, pen)
    return S


def sans(ss, tr, ayni_gun):
    """Her işlem için K rastgele giriş, aynı yön ve mesafe. Döner: işlem başına ortalama brüt R."""
    out = np.empty(len(tr))
    for n, t in enumerate(tr):
        rs = []
        for _ in range(K):
            if ayni_gun:
                gi, olcek, pen = t["gun_i"], 1.0, t["pencere"]
            else:
                gi = int(RNG.integers(len(ss)))
                dk_r, h_r, l_r = ss[gi][1], ss[gi][3], ss[gi][4]
                ilk = dk_r < (60 if t["pencere_tip"] == "rth" else 120)
                if ilk.sum() == 0:
                    continue
                rg_r = h_r[ilk].max() - l_r[ilk].min()
                if rg_r <= 0:
                    continue
                olcek = rg_r / t["rg"]
                lo, hi = (60, 330) if t["pencere_tip"] == "rth" else (120, 480)
                pen = np.flatnonzero((dk_r >= lo) & (dk_r < hi))
                if len(pen) == 0:
                    continue
            _, dk, o, h, l, c = ss[gi]
            p = int(pen[RNG.integers(len(pen))])
            a, b = t["a"] * olcek, t["b"] * olcek
            g = c[p]
            pnl, _ = sim(o, h, l, c, p + 1, len(dk) - 1, t["yon"], g, g - t["yon"] * b, g + t["yon"] * a)
            rs.append(pnl / b)
        out[n] = np.mean(rs) if rs else np.nan
    return out


def tstat(x):
    x = x[np.isfinite(x)]
    return (x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 else np.nan


def rapor(sym, ad, tr, ss, maliyet, tip):
    if len(tr) < 20:
        say(f"  {ad:14s} n={len(tr)} (az)")
        return None
    for t in tr:
        t["pencere_tip"] = tip
    df = pd.DataFrame([{k: v for k, v in t.items() if k != "pencere"} for t in tr])
    R = (df.pnl / df.b).to_numpy()
    Rn = R - maliyet / df.b.to_numpy()
    kaz = (df.kod == 1).mean()
    bas = (df.b / (df.a + df.b)).mean()      # rastgele yürüyüşte hedefe önce varma olasılığı
    s1 = sans(ss, tr, True)
    s2 = sans(ss, tr, False)
    d1 = R - s1
    yil = df.assign(Rn=Rn).groupby("yil").Rn.mean()
    yillik_n = len(df) / max(1, df.tarih.dt.year.nunique())
    say(f"  {ad:14s} n={len(df):5d} ({yillik_n:4.0f}/yıl) kazanma %{100*kaz:4.1f} (hedef/stop başa baş ≈%{100*bas:4.1f}, "
        f"süre çıkışı %{100*(df.kod==0).mean():3.0f}) ort. hedef/stop {np.median(df.a/df.b):.2f}R")
    say(f"  {'':14s} brüt {R.mean():+.3f}R (t {tstat(R):+.1f}) | net {Rn.mean():+.3f}R (t {tstat(Rn):+.1f}, maliyet "
        f"{np.mean(maliyet/df.b):.3f}R) | aynı gün şans {np.nanmean(s1):+.3f}R → fark {np.nanmean(d1):+.3f} (t {tstat(d1):+.1f})"
        f" | rastgele gün şans {np.nanmean(s2):+.3f}R")
    say(f"  {'':14s} yıllara göre net R: " + "  ".join(f"{y}:{v:+.2f}" for y, v in yil.items()))
    return dict(sym=sym, ad=ad, n=len(df), kaz=kaz, bas=bas, brut=R.mean(), net=Rn.mean(), t_net=tstat(Rn),
                sans1=np.nanmean(s1), fark=np.nanmean(d1), t_fark=tstat(d1), sans2=np.nanmean(s2))


def main():
    ozet = []
    say("Fit Mom Trader IB/Asya testi (LfSeAMzKjwM). 1m HistData, NY saati, 2020-2026.")
    say("R = stop mesafesi. 'Aynı gün şans' = aynı gün rastgele dakikada aynı yön/stop/hedef. Fark t ≥ 2 → setup kanıtı.")
    for sym, (_, tick, maliyet) in SRC.items():
        d = yukle(sym)
        # saat hizası kontrolü: 9:30'da oynaklık sıçraması olmalı
        r = d.close.pct_change().abs()
        hm = d.dt.dt.hour * 60 + d.dt.dt.minute
        sira = [r[hm == m].mean() * 1e4 for m in range(565, 576)]
        say("")
        say(f"=== {sym}: {d.dt.iloc[0]:%Y-%m-%d} → {d.dt.iloc[-1]:%Y-%m-%d}, {len(d):,} 1m mum. "
            f"Ort. |1m getiri| (bp) 9:25-9:35: " + " ".join(f"{x:.1f}" for x in sira))
        rth = seanslar(d, 0, 570, 390, 300)
        asya = seanslar(d, 6, 0, 540, 400)
        say(f"  RTH seansı {len(rth)}, Asya seansı {len(asya)}")
        for ad, tr in rth_setuplari(rth, tick).items():
            x = rapor(sym, ad, tr, rth, maliyet, "rth")
            if x:
                ozet.append(x)
        for ad, tr in asya_setuplari(asya, tick).items():
            x = rapor(sym, ad, tr, asya, maliyet, "asya")
            if x:
                ozet.append(x)
    say("")
    say("ÖZET (net R, şansa göre fark):")
    for x in ozet:
        say(f"  {x['sym']:7s} {x['ad']:14s} n={x['n']:5d} kazanma %{100*x['kaz']:4.1f} (başa baş %{100*x['bas']:4.1f}) "
            f"net {x['net']:+.3f}R (t {x['t_net']:+.1f}) | şansa göre {x['fark']:+.3f}R (t {x['t_fark']:+.1f})")
    (B / "verify_ib_fitmom_sonuc.txt").write_text("\n".join(OUT), encoding="utf-8")


if __name__ == "__main__":
    main()
