"""FTMO 2 aşamalı (10K): "tek işlemde geç" ile küçük riskli sürekli işlem karşılaştırması.

Kurallar: toplam limit −%10 (başlangıçtan), günlük limit −%5 (gün başından), hedef 1. aşama +%10, 2. aşama +%5.
İşlem sonucu yalnız stop (−1R) ya da hedef (+RR R); maliyet R cinsinden düşülür.
Avantaj e = işlem başı net beklenti (R). İsabet p, e'den çözülür: p·RR − (1−p) − maliyet = e.
  A "Tek atış": %4,9 risk (günlük limitin hemen altı), hedefi tam aşama hedefine ayarla. Kayıpta kalan payla bir atış
    daha (gerekli RR büyür). Bu, 'Spark' tipi videolardaki yöntemin FTMO uyarlaması.
  B "Küçük risk": işlem başı r (%0,5 ya da %1), RR 2, günde en çok 2 işlem, sınırsız süre (en çok 3.000 işlem).
"""
import numpy as np

rng = np.random.default_rng(11)
YOL = 40_000


def p_bul(e, rr, maliyet):
    return min(max((e + 1 + maliyet) / (rr + 1), 0.0), 1.0)


def tek_atis(hedef_pct, e, maliyet=0.03, risk=4.9):
    """İki atışa kadar: her atışta riski %4,9, hedef kalan mesafe kadar. Toplam limit −%10."""
    bakiye = np.full(YOL, 100.0)
    bitti = np.zeros(YOL, bool)
    gecti = np.zeros(YOL, bool)
    for _ in range(2):
        aktif = ~bitti
        kalan_hedef = 100 + hedef_pct - bakiye
        rr = kalan_hedef / risk
        p = np.array([p_bul(e, x, maliyet) for x in rr])
        kazan = rng.random(YOL) < p
        bakiye = np.where(aktif & kazan, bakiye + risk * rr - maliyet * risk, np.where(aktif, bakiye - risk - maliyet * risk, bakiye))
        gecti |= aktif & kazan
        bitti |= aktif & kazan
        # ikinci kayıptan sonra ya da toplam limite değince bitti
        bitti |= bakiye <= 90.0 + 1e-9
    return gecti.mean()


def kucuk_risk(hedef_pct, e, risk, rr=2.0, maliyet=0.05, gunde=2, en_cok=3000):
    p = p_bul(e, rr, maliyet)
    bakiye = np.full(YOL, 100.0)
    sonuc = np.zeros(YOL, int)   # 1 geçti, -1 kaldı
    for i in range(en_cok):
        aktif = sonuc == 0
        if not aktif.any():
            break
        if i % gunde == 0:
            gun_bas = bakiye.copy()
        kazan = rng.random(YOL) < p
        degis = np.where(kazan, risk * rr, -risk) - maliyet * risk
        bakiye = np.where(aktif, bakiye + degis, bakiye)
        sonuc = np.where(aktif & (bakiye >= 100 + hedef_pct), 1, sonuc)
        sonuc = np.where(aktif & ((bakiye <= 90.0) | (bakiye <= gun_bas - 5.0)), -1, sonuc)
    return (sonuc == 1).mean()


if __name__ == "__main__":
    print("Geçme olasılıkları (1. aşama / iki aşama birden)")
    print(f"{'Avantaj (R)':>12} | {'Tek atış %4,9':>16} | {'%1 risk, RR 2':>16} | {'%0,5 risk, RR 2':>16}")
    for e in (-0.05, 0.0, 0.1, 0.2):
        a1, a2 = tek_atis(10, e), tek_atis(5, e)
        b1, b2 = kucuk_risk(10, e, 1.0), kucuk_risk(5, e, 1.0)
        c1, c2 = kucuk_risk(10, e, 0.5), kucuk_risk(5, e, 0.5)
        print(f"{e:>+12.2f} | {a1:6.1%} / {a1 * a2:6.1%} | {b1:6.1%} / {b1 * b2:6.1%} | {c1:6.1%} / {c1 * c2:6.1%}")
