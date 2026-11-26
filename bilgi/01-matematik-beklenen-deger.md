# 01 — Trading Matematiği: Beklenen Değer, Başa Baş, Örneklem

> Güven seviyesi: **YÜKSEK** — formüller standart; rakamlar `arastirma/verify_math.py` ile Monte Carlo/binom hesabıyla bağımsız doğrulandı.
> Kaynaklar: AlgoCoinism "Trading'de Gerçekten Kazanmanın Matematiği" (UNwwqKk2OT0), Tradeciety RR makalesi, Adam Grimes (kanıta dayalı yaklaşım).

## 1. Beklenen değer (EV / expectancy) — tek önemli sayı

```
EV (R cinsinden) = WR × ortalama_kazanç_R − (1 − WR) × ortalama_kayıp_R
```

- **R** = bir işlemde riske edilen tutar (giriş → stop mesafesi × lot). 1R = "bu işlem stop olursa kaybedeceğim para".
- Sonuçları her zaman **R cinsinden** kaydet; dolar/yüzde değil. Böylece farklı lot/hesap boyutları karşılaştırılabilir.

| Sistem | WR | Hedef | EV / işlem |
|---|---|---|---|
| A | %15 | 8R | 0.15×8 − 0.85×1 = **+0.35R** |
| B | %55 | 3R | 1.65 − 0.45 = **+1.20R** (gerçekçi değil, örnek) |
| C | %70 | 1R | 0.70 − 0.30 = **+0.40R** |
| D | %30 | 6R | 1.80 − 0.70 = **+1.10R** |
| E | %40 | 2R | 0.80 − 0.60 = **+0.20R** (gerçekçi iyi sistem) |

**Ders:** Ne kazanma oranı tek başına ne de RR tek başına önemli. Avantajı ikisinin **birleşimi** yaratır. %15 WR'lı sistem %70 WR'lı sistem kadar kâr edebilir.

## 2. Başa baş kazanma oranı

```
Gereken WR = 1 / (1 + RR)
```

| RR | 0.5 | 1 | 1.5 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|
| Başa baş WR | %66.7 | %50 | %40 | %33.3 | %25 | %20 | %16.7 |

⚠️ Bu tablo **maliyetsizdir**. Spread + komisyon + slippage başa baş WR'ı yukarı iter. Özellikle küçük stoplu scalp işlemlerde maliyet 1R'nin %10-20'si olabilir → "kağıt üstünde kârlı, gerçekte zararlı" sistem.

## 3. RR ↔ WR takası (piyasanın doğası)

- Hedef uzaklaştıkça fiyatın oraya ulaşma sıklığı düşer → WR düşer. Bu senin hatan değil, fizik.
- **"Hem yüksek WR hem yüksek RR" veren sistem arayışı** traderların en çok takıldığı yer. Gerçekçi tatlı bölge: **%40–55 WR, 1.5–3R**.
- 1:10, 1:15 RR gösteren sosyal medya ekran görüntüleri: genelde 9 kaybın 1 kazancın gösterildiği seçilmiş örnekler (hayatta kalan yanlılığı).
- **Uç örnek: "ilk kârlı kapanışta çık"** (Meb Faber; test 12'de). Rastgele girişlerle isabet %96, ama ortalama -0,05R, çünkü en kötü %1'lik işlemler -11,8R. İsabeti istediğin kadar yükseltebilirsin. Bedeli, nadir ama devasa kayıplardır.

## 4. Örneklem büyüklüğü — kısa vadede sonuç hiçbir şey söylemez

WR %40, 2R sistemde (EV +0.2R, yani **gerçekten kârlı**) zararda bitirme ihtimali (binom, doğrulandı):

| İşlem sayısı | Zararda olma ihtimali |
|---|---|
| 20 | **%25** |
| 100 | %9 |
| 300 | %0.7 |

**Ders:** 20-30 işlemle bir sistemi "çalışmıyor" diye atmak, kârlı bir sistemi atmak olabilir. Tersi de geçerli: 20 işlemlik şanslı seri hiçbir şey kanıtlamaz.

> Tradeciety "30-50 işlem yeterli" diyor — **abartılı**. 30-50 işlem kaba bir ilk eleme için iyi; istatistiksel güven için **100+**, tercihen 200-300.

## 5. Kayıp serileri kaçınılmazdır

100 işlem içinde en az bir kez **k ardışık kayıp** görme ihtimali (simülasyon, 40k deneme):

| WR | 5'li seri | 7'li seri | 10'lu seri |
|---|---|---|---|
| %40 | %97.6 | **%69.6** | %20.5 |
| %50 | %81.6 | %31.8 | %4.5 |
| %60 | %45.8 | %8.6 | %0.6 |

**Ders:** %40 WR'lı bir sistemle 7'li kayıp serisi "sistem bozuldu" sinyali değil, **normal**. Risk/işlem bunu kaldıracak kadar küçük olmalı.

**Yüksek isabette de seri olur** (Trader Dante, NDkE6RHke9U; `arastirma/verify_dante_drift.py` A bölümü). %65 isabetle 50 işlemde en az bir kez k ardışık kayıp: 3'lü %78, 4'lü **%38,5**, 5'li **%15**, 6'lı %5,4. Dante'nin tablosundaki "4'lü seri %50'nin üstünde, 5'li 5'te 1'in üstünde" rakamları ~1,3 kat abartılı, ama ders aynı: seriye önceden plan yap (boyutu küçült, kenara çekil ya da avantaja güvenip devam et). Seri sırasında karar verme.

## 6. Kumarbaz yanılgısı

Her işlem bağımsızdır. 4 kayıptan sonra 5. işlemin kazanma ihtimali artmaz. "Artık sıra kazanmada" diye lot büyütmek = klasik hesap patlatma yolu.

## 7. Kelly kriteri (bilgi amaçlı — kullanma)

```
f* = WR − (1 − WR) / RR
```
WR %40 / 2R → tam Kelly %10/işlem. **Asla tam Kelly kullanma**: WR/RR tahminlerin hatalıdır, Kelly bu hataya çok duyarlıdır ve %10 riskte (aşağıya bak) çöküş neredeyse kesin. Pratikte Kelly'nin 1/10 – 1/20'si (%0.5–1) kullanılır.

## 8. Tek cümlelik özet

> Senin işin tahmin etmek değil, **pozitif EV'li bir süreci yeterince küçük riskle yeterince çok kez uygulamak**.

İlgili: [02-risk-pozisyon-boyutu.md](02-risk-pozisyon-boyutu.md), [10-backtest-ve-istatistik.md](10-backtest-ve-istatistik.md)
