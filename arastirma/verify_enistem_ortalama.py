"""Kullanıcının eniştesinin yöntemi: bir coin seç, düştükçe eşit parçalarla daha fazla al, fiyat ortalamanın biraz üstüne
çıkınca hepsini sat, yeniden başla ("ortalama düşürme" + küçük kâr hedefi).

Veri: btc-order akademi deposundaki BTCUSD 4 saatlik mumlar (2017-08 → bugün). Maliyet: işlem başına %0,1 (spot).
Hesap 10.000 $, her alım 1.000 $ (hesabın %10'u, kaldıraçsız), en çok 10 alım (hesap tamamen yatırılır).
Alım: son alımdan `adim` kadar aşağıda limit emir. Satış: ortalama maliyetin `kar` kadar üstünde limit emir.
Ölçülenler: döngü sayısı, kazanan döngü oranı, toplam getiri, en derin açık zarar (varlık değeri), en uzun "takılı" süre;
ve FTMO kuralları (başlangıçtan -%10 ya da gün başına göre -%5, mum içi dipten varlık değeriyle) ilk ne zaman ihlal edilir.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BACKEND = Path(r"C:\Users\mimi\Desktop\btc-order\backend")   # BTC mumları masanın 1m deposundan üretilir
HESAP, PARCA, EN_COK, MALIYET = 10_000.0, 1_000.0, 10, 0.001


def calistir(d: pd.DataFrame, adim: float, kar: float) -> dict:
    nakit, adet, maliyet_top, son_alim = HESAP, 0.0, 0.0, None
    dongu_kar, dongu_bas, en_uzun, n_alim = [], None, 0, 0
    tepe_varlik, en_derin = HESAP, 0.0
    ftmo_ihlal, gun, gun_bas_varlik = None, None, HESAP
    ts = pd.to_datetime(d.ts, unit="ms", utc=True)

    def al(fiyat, t):
        nonlocal nakit, adet, maliyet_top, son_alim, n_alim, dongu_bas
        nakit -= PARCA
        adet += PARCA * (1 - MALIYET) / fiyat
        maliyet_top += PARCA
        son_alim, n_alim = fiyat, n_alim + 1
        if dongu_bas is None:
            dongu_bas = t

    o, h, l, c = (d[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    al(o[0], ts.iloc[0])
    for i in range(len(d)):
        t = ts.iloc[i]
        if gun != t.date():   # gün başı varlığı (UTC gün; FTMO CE(S)T gece yarısı, yaklaşık)
            gun, gun_bas_varlik = t.date(), nakit + adet * o[i]
        # aşağıda kademeli alımlar
        while n_alim < EN_COK and l[i] <= son_alim * (1 - adim):
            al(son_alim * (1 - adim), t)
        varlik_dip = nakit + adet * l[i]
        en_derin = max(en_derin, 1 - varlik_dip / tepe_varlik)
        if ftmo_ihlal is None and (varlik_dip <= HESAP * 0.9 or varlik_dip - gun_bas_varlik <= -HESAP * 0.05):
            ftmo_ihlal = t
        # satış: ortalama maliyetin kar% üstü
        ort = maliyet_top / (adet / (1 - MALIYET))
        if adet > 0 and h[i] >= ort * (1 + kar):
            sat = ort * (1 + kar)
            gelir = adet * sat * (1 - MALIYET)
            dongu_kar.append(gelir - maliyet_top)
            en_uzun = max(en_uzun, (t - dongu_bas).days)
            nakit += gelir
            adet, maliyet_top, n_alim, son_alim, dongu_bas = 0.0, 0.0, 0, None, None
            al(c[i], t)
        tepe_varlik = max(tepe_varlik, nakit + adet * c[i])
    son = nakit + adet * c[-1]
    acik_gun = (ts.iloc[-1] - dongu_bas).days if dongu_bas is not None else 0
    k = np.array(dongu_kar)
    return {"adim": adim, "kar": kar, "dongu": len(k), "kazanan_%": round(100 * float((k > 0).mean()), 1) if len(k) else None,
            "kapanan_kar_$": round(float(k.sum())), "son_varlik_$": round(son), "acik_alim": n_alim, "acik_dongu_gun": acik_gun,
            "en_derin_acik_zarar_%": round(100 * en_derin, 1), "en_uzun_dongu_gun": max(en_uzun, acik_gun),
            "ftmo_ilk_ihlal": str(ftmo_ihlal.date()) if ftmo_ihlal is not None else "yok"}


if __name__ == "__main__":
    sys.path.insert(0, str(BACKEND))
    from app.akademi import veri
    d = veri.tf_oku("BTCUSD", "4H", None).sort_values("ts").reset_index(drop=True)
    print(f"BTCUSD 4H: {pd.to_datetime(d.ts.iloc[0], unit='ms').date()} → {pd.to_datetime(d.ts.iloc[-1], unit='ms').date()}, al-tut: "
          f"{d.close.iloc[-1] / d.open.iloc[0]:.1f}x")
    for adim, kar in ((0.03, 0.015), (0.05, 0.02), (0.08, 0.03)):
        print(calistir(d, adim, kar))
    # dönem dönem: her yılın başında yeniden başlayan hesap
    print("\nYıl başında yeni 10.000 $ ile (adım %5, kâr %2):")
    for yil in range(2018, 2026):
        g = d[pd.to_datetime(d.ts, unit="ms").dt.year == yil].reset_index(drop=True)
        r = calistir(g, 0.05, 0.02)
        print(yil, {k: r[k] for k in ("dongu", "kazanan_%", "son_varlik_$", "en_derin_acik_zarar_%", "acik_alim", "ftmo_ilk_ihlal")})
