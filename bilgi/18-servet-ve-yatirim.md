# 18 — Servet ve Yatırım: Sadece Yatırımla Zengin Olunur mu?

> Güven seviyesi: **YÜKSEK** (bileşik faiz matematiği, 150 yıllık ABD verisi, DMS/UBS yıllığı, SPIVA). **ORTA** (Türkiye'ye özgü vergi ve ürün ayrıntıları ◐, sık değişiyor).
> Hesaplar: `arastirma/verify_birikim.py` (çıktı: `arastirma/verify_birikim_sonuc.txt`). Tüm dolar rakamları **bugünün parasıyla (reel)**, vergi ve gider **hariç**.
> İşaretler: ✔ kaynakla veya hesapla doğrulandı · ◐ kısmen doğrulandı / belirsiz / değişken · ✘ desteklenmedi.
> Bu dosya eğitim amaçlıdır, kişisel yatırım tavsiyesi değildir.

## Özet

- **"Sadece yatırımla zengin olunur mu?"** Küçük bir birikimle **hayır**. Piyasa getirisi parayı zengin etmez, korur ve yavaşça büyütür. Uzun dönem reel getiri dünya hisselerinde yılda **~%5,2**, ABD'de **~%6,6** (1900'den bu yana) ✔. Servetin büyüklüğünü asıl belirleyen şey **ne kadar yatırdığın** (gelir × tasarruf oranı) ve **ne kadar süre** beklediğin.
- **"Maaş + yatırım yeterli mi?"** Finansal bağımsızlık için **evet, ama süre tasarruf oranına bağlı**. %5 reel getiri ve %4 çekimle: net gelirin **%10'unu** biriktiren ~51 yıl, **%20'sini** ~36 yıl, **%50'sini** ~16 yıl çalışır ✔ (§4b). Fidelity'nin 401(k) milyonerleri tam bu yolu izlemiş: ortalama ~59 yaş, ~25 yıl düzenli birikim, ~%17 tasarruf ◐.
- **"10 yılda ayda 300$ ile emekli olabilir miyim?"** **Hayır** ✘. %7 reel getiriyle 10 yıl sonunda ~**51.000$** birikir. %4 çekim kuralıyla bu ayda **~171$** eder. Ayda 1.000$ gelir için ~300.000$ gerekir. 300$/ay ile buna 10 yılda ulaşmak **yılda %40 reel getiri** ister. Bu, Buffett'ın 60 yıllık ortalamasının (~%20 nominal ◐) iki katı. Aynı 300$ ile %7 reelde 300.000$'a ulaşmak **~28 yıl** sürer. 10 yılda 1.000$/ay için ayda **~1.750-1.950$** yatırmak gerekir.
- **Süre riski azaltır ama sıfırlamaz.** 1871'den beri her ay başlayan 10 yıllık "ayda 300$" birikimlerinin **%11,5'i** yatırılan paranın altında (reel zararda) bitti. 1965'te başlayan biri 36.000$ yatırıp 22.500$ ile çıktı. 30 yıllık pencerelerin hiçbiri zararla bitmedi ✔ (§2c). Japonya'da Nikkei 1989 zirvesini ancak **34 yıl** sonra geçti ✔.
- **Kendi kendine zengin olanlar nasıl zenginleşiyor?** Çoğunlukla **şirket sahipliğiyle** (kurmak ya da erken ortak olmak) ve **yüksek gelirli beceriyle**. Forbes 400'ün **%71'i** kendi servetini yapmış ✔. Kaplan-Rauh'a göre listede kendi işini kuranların payı 1982-2011 arasında **%40'tan %69'a** çıktı ✔. ABD'nin en üst %0,1'lik gelir diliminde ana gelir kaynağı iş sahipliği. Yalnızca faiz, kira gibi sermaye gelirine dayananlar **%13'ün altında** ✔. Yatırım bu servetleri **korumuş ve büyütmüş**, yaratmamış.
- **Erken dönemde kaldıraç gelir ve tasarruf oranıdır, getiri sonra önemlenir.** 10 yılda getiriyi %5'ten %7'ye çıkarmak sonucu **%11** artırıyor, aylık katkıyı ikiye katlamak **%100**. 30 yılda ise aynı 2 puanlık getiri farkı **%43** fark yaratıyor ✔ (§1f).
- **Getiriyi masraf ve fazla işlem yer.** 2025'te ABD büyük şirket hisse fonlarının **%79'u**, 20 yılda **~%93'ü** S&P 500'ün gerisinde kaldı ✔. Yıllık %2 masraf, 30 yılda birikimi **~%30** küçültür (§3).
- **Türkiye:** 2015 sonunda yastık altında duran 100 TL'nin alım gücü 2025 sonunda **7,7 TL** (TÜİK TÜFE ile) ✔. Dolar nakit aynı 10 yılda TÜFE'yi toplamda yalnızca **~%13** geçti, yıllık sonucu **-%17 ile +%32** arasında savruldu. 2024-25'te TL mevduat dolardan iyiydi. Reel kazanç **üretken varlıktan** geliyor (§5).
- **Trading bir gelir planı değil, bir beceri deneyidir.** Sektör verisinde challenge alanların ~**%7'si** ödeme alıyor (09 §4h). Mantıklı plan: **iş ve gelir artışı + %20 ve üstü tasarruf + düşük maliyetli küresel endeks + küçük, sınırlı bir trading/prop bütçesi**. Geçimin için gereken para asla trading'e girmez (§6).

---

## 1. Bileşik faiz matematiği (✔ hesap, `verify_birikim.py` A-B)

**Varsayımlar**: Her ay sonu 300$ (bugünün doları). Getiri **reel**, yani enflasyon düşülmüş: %3 temkinli, %5 dengeli/küresel, %7 ABD hissesinin tarihsel ortalamasına yakın, %9 iyimser. Vergi ve gider yok. "Aylık gelir" = birikimin %4'ü (parantez içinde %3,5'i) / 12.

### 1a. Ayda 300$: birikim ve desteklediği aylık gelir

| Yıl | Yatırılan | %3 reel | %5 reel | %7 reel | %9 reel |
|---|---|---|---|---|---|
| 10 | 36.000 $ | 41.834 $ → **139 $** (122) | 46.309 $ → **154 $** (135) | 51.316 $ → **171 $** (150) | 56.916 $ → **190 $** (166) |
| 15 | 54.000 $ | 67.872 $ → 226 $ (198) | 79.447 $ → 265 $ (232) | 93.331 $ → 311 $ (272) | 109.992 $ → 367 $ (321) |
| 20 | 72.000 $ | 98.056 $ → 327 $ (286) | 121.741 $ → 406 $ (355) | 152.261 $ → 508 $ (444) | 191.656 $ → 639 $ (559) |
| 25 | 90.000 $ | 133.048 $ → 443 $ (388) | 175.720 $ → 586 $ (513) | 234.913 $ → 783 $ (685) | 317.306 $ → 1.058 $ (925) |
| 30 | 108.000 $ | 173.614 $ → 579 $ (506) | 244.613 $ → 815 $ (713) | 350.836 $ → **1.169 $** (1.023) | 510.634 $ → 1.702 $ (1.489) |

→ Ayda 300$ ile 30 yıl ve %7 reel getiriyle bile, bugünün parasıyla ayda **~1.000-1.170$**'lık bir gelire ulaşılıyor. Bu bir emeklilik tamamlayıcısı, zenginlik değil.

### 1b. Birikimin ne kadarı senin paran, ne kadarı getiri? (%7 reel)

| Süre | Yatırılan | Getiri | Yatırılanın birikimdeki payı |
|---|---|---|---|
| 10 yıl | 36.000 $ | 15.316 $ | **%70** |
| 20 yıl | 72.000 $ | 80.261 $ | %47 |
| 30 yıl | 108.000 $ | 242.836 $ | **%31** |

İlk 10 yılda servetin büyük kısmı **cebinden çıkan paradır**. Bileşik faiz ancak 20. yıldan sonra baskın hale geliyor.

### 1c. Katkıyı her yıl reel %5 artırmak (300$ ile başlayıp)

Maaş arttıkça katkıyı da artırmak (ör. her zamda) etkiyi ciddi şekilde büyütür:

| Süre | Sabit 300$ (%7) | Her yıl +%5 (%7) | Son yıldaki aylık katkı | Aylık gelir (%4): sabit → artan |
|---|---|---|---|---|
| 10 yıl | 51.316 $ | 62.816 $ | 465 $ | 171 $ → 209 $ |
| 20 yıl | 152.261 $ | 225.888 $ | 758 $ | 508 $ → 753 $ |
| 30 yıl | 350.836 $ | 611.026 $ | 1.235 $ | 1.169 $ → **2.037 $** |

(%5 reel getiride: 10 yılda 57.116 $, 20 yılda 186.073 $, 30 yılda 454.640 $.)

### 1d. Hedef aylık gelir için gereken aylık yatırım (bugünün parasıyla)

Gereken sermaye = aylık gelir × 12 / çekim oranı. %4 ile 1.000$/ay = **300.000 $**, 2.000$/ay = **600.000 $**.

| Hedef | Çekim | 10 yıl (%5 / %7) | 15 yıl | 20 yıl | 30 yıl |
|---|---|---|---|---|---|
| 1.000 $/ay | %4 | **1.943 / 1.754 $** | 1.133 / 964 $ | 739 / 591 $ | 368 / **257 $** |
| 2.000 $/ay | %4 | **3.887 / 3.508 $** | 2.266 / 1.929 $ | 1.479 / 1.182 $ | 736 / 513 $ |
| 1.000 $/ay | %3,5 | 2.221 / 2.004 $ | 1.295 / 1.102 $ | 845 / 676 $ | 420 / 293 $ |
| 2.000 $/ay | %3,5 | 4.442 / 4.009 $ | 2.589 / 2.204 $ | 1.690 / 1.351 $ | 841 / 586 $ |

Erken emeklilik 40-50 yıllık bir çekim dönemi demek. Bu durumda %4 yerine **%3-3,5** daha güvenli (§2d), yani alttaki iki satır daha gerçekçi.

### 1e. "10 yılda ayda 300$ ile emeklilik" testi: ✘ gerçekçi değil

| Soru | Cevap |
|---|---|
| 10 yıl sonra birikim (%5 / %7 reel) | 46.309 $ / 51.316 $ → ayda **154 $ / 171 $** (%4) |
| 300$/ay ile 10 yılda 300.000 $ (1.000$/ay) için gereken reel getiri | yılda **%40** |
| 300$/ay ile 10 yılda 600.000 $ (2.000$/ay) için gereken reel getiri | yılda **%54** |
| 300$/ay ile 300.000 $'a ulaşma süresi | %5'te **33 yıl**, %7'de **28 yıl** |
| 300$/ay ile 600.000 $'a ulaşma süresi | %5'te 45 yıl, %7'de 37 yıl |

Kıyas: Brandt'a göre 5 yıl boyunca yılda %30 bile "3 standart sapma" bir başarı (14 §3d). Berkshire Hathaway 1965-2024 arasında yılda ~%20 nominal büyüdü (◐ hafızadan). **10 yıl boyunca %40 reel** hiçbir gerçekçi planın varsayımı olamaz. Bunu vaat eden her ürün ya da kişi kırmızı bayraktır.

### 1f. Hangi kaldıraç daha güçlü: getiri mi, katkı mı?

| Senaryo | 10 yıl sonu | Fark |
|---|---|---|
| 300 $/ay, %5 reel | 46.309 $ | taban |
| 300 $/ay, **%7** reel (+2 puan getiri) | 51.316 $ | **+%11** |
| **600 $/ay**, %5 reel (katkı ×2) | 92.618 $ | **+%100** |
| 30 yılda: 300 $/ay %5 → %7 | 244.613 → 350.836 $ | +%43 |

→ ✔ **İlk yıllarda servet "ne kadar kazandığın ve biriktirdiğin" ile belirlenir.** Getiri optimizasyonu, yani "daha iyi hisse bulmak" ya da trading, küçük sermayede marjinal bir etki yaratıyor. Süre uzadıkça ve sermaye büyüdükçe getirinin ağırlığı artıyor.

---

## 2. Tarihsel getiriler ve riskler

### 2a. Uzun dönem reel getiriler (Dimson-Marsh-Staunton, UBS Global Investment Returns Yearbook) ✔

| Varlık | Dönem | Yıllık reel getiri |
|---|---|---|
| Dünya hisse senetleri | 1900-2024 | **%5,2** |
| Dünya tahvilleri | 1900-2024 | %1,7 |
| Dünya hazine bonoları | 1900-2024 | %0,5 |
| Dünya hisseleri, 21. yüzyıl | 2000-2024 | **%3,5** |
| ABD hisseleri | 1900-2025 | **%6,6** (nominal %9,8, enflasyon %2,9) |
| ABD tahvilleri / bonoları | 1900-2025 | %1,6 / %0,5 |
| Altın (USD) | 1900-2025 | **%1,3** (126 yılda reel 5,2 kat) |
| Altın, Bretton Woods sonrası | 1971-2025 | %4,7 (ABD), %5,8 (İngiltere) |

Yıllıktan diğer bulgular ✔:
- Hisseler, kesintisiz verisi olan **21 ülkenin hepsinde** en iyi varlık sınıfı oldu.
- Hisse ve tahviller birkaç kez **reel olarak %70'ten fazla** kaybetti, ama **60/40'lık bir karışım hiç %50'den fazla düşmedi**.
- **Altın enflasyona karşı güvenilir bir kalkan değil** ✘: enflasyonun %3'ü aştığı 28 yılın **13'ünde** altının getirisi negatif. Uzun vadede enflasyonu yeniyor, ama çok uzun düz dönemleri var.
- **Küresel çeşitlendirme**: kur riskinden korunulduğunda, 1974-2025 arasında piyasaların büyük çoğunluğunda yatırımcı yurt içi yerine küresel hisse tutarak daha iyi bir risk/getiri oranı elde etti.
- 1900-2025'te gelişmekte olan piyasalar yılda %6,9, gelişmiş piyasalar %8,5 getirdi (USD, nominal). "Büyüyen ekonomi = yüksek getiri" otomatik değil.

**Kendi kontrolümüz (Shiller verisi, S&P 500, temettü dahil)**: 1900-2023 reel yıllık **%6,60**, yani DMS'nin %6,6'sıyla birebir aynı ✔. 1871-2023 için %6,90.

### 2b. Kötü dönemler: uzun düz yıllar gerçek (Shiller, 1871-2023/06) ✔

**Yuvarlanan pencerelerde yıllık reel getiri (S&P 500, temettü dahil):**

| Pencere | En kötü | %5'lik dilim | Medyan | En iyi | Negatif biten pencere |
|---|---|---|---|---|---|
| 10 yıl | **-%5,9** (1999 başlangıç) | -%2,3 | %6,9 | %19,9 | **%11,3** |
| 20 yıl | -%0,2 (1901) | %1,8 | %6,7 | %13,6 | %0,1 |
| 30 yıl | %1,9 (1902) | %4,0 | %6,7 | %11,1 | %0 |

**Reel olarak "su altında" kalınan en uzun dönemler** (zirveden zirveye):

| Zirve → toparlanma | Süre | En dip |
|---|---|---|
| 2000/08 → 2013/05 | **12,7 yıl** | -%52 |
| 1973/01 → 1985/01 | **11,9 yıl** | -%50 |
| 1937/02 → 1945/04 | 8,1 yıl | -%48 |
| 1929/09 → 1936/11 | 7,2 yıl | **-%77** (en derin düşüş, 1932) |

- Ocak 2000'de S&P 500 alan biri, temettüler dahil, reel olarak ancak **Mart 2013'te** başa baş geldi.
- **Japonya**: Nikkei 225, 29 Aralık 1989'da 38.915,87'de kapandı. Bu seviyeyi ilk kez **22 Şubat 2024'te** geçti, yani **34 yıl 2 ay** sonra ✔. Bu fiyat endeksi, temettüyle toparlanma daha erken ama yine on yıllar sürdü. Tek ülkeye ve tek piyasaya bağlı kalmanın riski bu.
- Not: Shiller verisi aylık ortalama fiyat kullanıyor. Gün içi dipler (ör. 2009) burada görünenden biraz daha derin.

### 2c. Tarihte "ayda 300$" ne verdi? (her başlangıç ayı için, reel) ✔

| Süre (yatırılan) | En kötü | %10'luk dilim | **Medyan** | %90'lık dilim | En iyi | Reel zararla biten pencere |
|---|---|---|---|---|---|---|
| 10 yıl (36.000 $) | **22.517 $** (1965 başlangıç) | 34.550 $ | **52.258 $** | 74.496 $ | 150.723 $ (1919) | **%11,5** |
| 20 yıl (72.000 $) | 55.418 $ (1901) | 84.942 $ | **152.473 $** | 271.797 $ | 377.824 $ (1979) | %4,6 |
| 30 yıl (108.000 $) | 119.269 $ (1891) | 190.608 $ | **327.345 $** | 604.642 $ | 769.212 $ (1970) | %0 |

- Medyan, §1a'daki %7 varsayımıyla neredeyse aynı (10 yıl: 52k'ya karşı 51k; 20 yıl: 152k'ya karşı 152k). Tablo **gerçekçi**.
- Ama **dağılım çok geniş**. 30 yılda en kötü ile en iyi arasında 6 kat fark var. Hangi on yılda doğduğun, aylık gelirini ayda ~400$ ile ~2.500$ arasında değiştirebiliyor.
- Bu tablo **ABD'nin** sonucu. ABD 20. yüzyılın en başarılı piyasalarından biriydi (hayatta kalma yanlılığı). Tek ülke yerine küresel endeks bu riski azaltır (§2a).

### 2d. Güvenli çekim oranı (SWR) araştırması

| Çalışma | Bulgu | Not |
|---|---|---|
| **Bengen (1994)**, Journal of Financial Planning | 30 yıllık emeklilikte enflasyona endeksli **%4** başlangıç çekimi tarihteki en kötü dönemde de dayandı (ABD, hisse/tahvil karışımı) ✔ | 2006'da %4,5'e, 2025 kitabında (*A Richer Retirement*) 7 varlıklı portföyle **%4,7**'ye çıkardı ✔ |
| **Trinity çalışması** (Cooley, Hubbard, Walz 1998; veri 1926-1995) | %4 çekim, 30 yıl: başarı ~%95 (50/50), ~%98'e kadar (75/25) ◐ | Yıllık %1-2 fon masrafı başarıyı belirgin düşürüyor ◐ |
| **Pfau (2010)**, 17 ülke, 109 yıl | %4 kuralı yalnızca **4 ülkede** (ABD, Kanada, İsveç, Danimarka) "güvenli" kaldı ✔ | ABD verisi istisnai olabilir. İtalya'da başarısızlık %62,5, Fransa'da %42,5 ◐ |
| **Morningstar** (2025 / 2026 raporları) | 30 yıl ve %90 başarı için en yüksek güvenli başlangıç oranı **%3,7** (2025), **%3,9** (2026) ✔ | 35 yıllık süre için oran **%3,5**'e iniyor ✔ |

**Kendi testimiz** (Shiller ABD verisi, 30 yıl, aylık çekim, tahvil getirisi 10 yıllık faizden yaklaşık hesaplandı ◐):

| Portföy | %3 | %3,5 | %4 | %4,5 | %5 | Tarihin en kötü başlangıcında bile dayanan oran |
|---|---|---|---|---|---|---|
| %100 hisse | %100 | %100 | %98 | %93 | %83 | ~%3,1 (1929 zirvesinde emekli olan) |
| %60 hisse / %40 tahvil | %100 | %100 | %97 | %89 | %75 | ~%3,7 (1965-66'da emekli olan) |
| %50 / %50 | %100 | %100 | %96 | %86 | %69 | ~%3,7 |

→ ✔ **%4, 30 yıl için makul bir kural, garanti değil.** Erken emeklilik (40-50 yıl), yüksek fon masrafı ve ABD dışı piyasalar için **%3-3,5** daha temkinli. Bengen'in tarihsel en kötü durumu (%4,15 civarı ◐ hafızadan) bizim testten biraz yüksek. Sebebi büyük ihtimalle yıllık veri kullanması (takvim yılı başlangıcı 1929 Eylül zirvesini yakalamıyor) ve tahvil serisi farkı.

### 2e. Getiri sırası riski (sequence-of-returns) ✔

Aynı 30 yılın getirileri, **önce düz sonra ters sırada** uygulanıyor. Ortalama getiri iki durumda da aynı:

| Başlangıç | Çekim | Düz sıra (gerçek tarih) | Ters sıra |
|---|---|---|---|
| 1966 (yıllık reel %4,9) | %4 | **27,8. yılda para bitti** | Son bakiye ilk sermayenin 2,45 katı |
| 1966 | %5 | **18,2. yılda bitti** | 2,00 kat |
| 1929 (yıllık reel %6,6) | %4 | İlk sermayenin 0,20 katı kaldı | 4,51 kat |
| 1929 | %5 | **19,0. yılda bitti** | 3,94 kat |

→ Para biriktirirken kötü yıllar sorun değil, hatta ucuz alım fırsatı. **Çekim döneminin ilk yıllarındaki** kötü getiri ise kalıcı hasar bırakıyor. "Ortalama %7 getiri" planı tek başına yetmez. Esnek harcama, tahvil/nakit tamponu ve düşük çekim oranı gerekir.

---

## 3. Aktif ve pasif yatırım: kanıt ne diyor?

| Kanıt | Bulgu | Not |
|---|---|---|
| **SPIVA ABD, 2025 sonu** (S&P Dow Jones Indices) | ABD büyük şirket hisse fonlarının **%79'u** 2025'te S&P 500'ün gerisinde kaldı, 25 yıllık serinin en kötü 4. yılı ✔. **20 yılda ~%93'ü** (%92,89) geride ✔. Aynı tablo: 5 yıl ~%89, 10 yıl ~%86, 15 yıl ~%90 ◐ | Uzun vadede istikrarla endeksi geçen fonu önceden seçmek zor |
| **Barber & Odean (2000)**, *Trading Is Hazardous to Your Wealth*, 66 bin hane (1991-96) | En çok işlem yapanlar yılda **%11,4**, piyasa **%17,9** ✔ (08 §1) | Daha fazla işlem = daha fazla maliyet ve hata |
| **Morningstar "Mind the Gap" 2026** | 2025'e kadar 10 yılda ortalama yatırımcı doları yılda **%8,7**, fonların kendisi **%9,9** kazandırdı → **1,2 puan** açık ✔. En oynak fonlarda açık -2,1, en sakinlerde -0,4 puan ✔ | Açık, yanlış zamanda alıp satmaktan geliyor. Oynaklık arttıkça büyüyor |
| **DALBAR QAIB** | Yıllarca yıllık birkaç puanlık "davranış açığı" raporladı ◐ | **Eleştiri**: Pfau (2017) ve Harry Sit'e (Kitces) göre yöntem açığı abartıyor. Gerçek açık Morningstar'ın ~1 puanına daha yakın. DALBAR raporu danışmanlara sattığı için açığı büyük göstermekte çıkarı var ◐ |

**Maliyetin bileşik etkisi** (§1a tablosundan): Yıllık %2 masraf, %7 reel getiriyi kabaca %5'e indirir. 30 yılda 300$/ay: **350.836 $ yerine 244.613 $ (-%30)**. Yani masraf, düzenli yatırımcının tek başına kontrol edebileceği en büyük değişkenlerden biri.

→ ✔ Pratik sonuç: çekirdek portföy için **düşük maliyetli, geniş, pasif endeks**, seyrek işlem ve otomatik düzenli alım. "Piyasayı geçme" çabası küçük sermayede getiriyi değil riski artırıyor.

---

## 4. Kendi kendine zengin olanlar gerçekte nasıl zenginleşiyor?

### 4a. Kanıt tablosu

| Kaynak | Bulgu | Not |
|---|---|---|
| **Kaplan & Rauh (2013)**, *American Economic Review*, Forbes 400, 1982-2011 | Varlıklı ailede büyüyenlerin payı **%60'tan %32'ye** düştü. Kendi işini kuranların payı **%40'tan %69'a** çıktı. Üniversite mezunu payı %77'den %87'ye ✔ | Servet **şirket kurmaktan** (teknoloji, finans) geliyor. "Hiçbir şeyi olmayan" kökenlilerin payı ise **yaklaşık sabit** kaldı ✔ |
| **Korom, Lutter & Beckert (2017)** | Büyük aile servetinin varisleri listede, kendi servetini yapanlardan daha uzun kalıyor ✔ | Miras hâlâ önemli |
| **Forbes 400 (2025)** | Listedekilerin **%71'i** kendi servetini yapmış (2024: %67) ✔ | Forbes'un "self-made" ölçeği 1-10, 6 ve üstü "kendi yapmış" sayılıyor. "Yoksulluktan gelmiş" demek değil |
| **UBS Billionaire Ambitions 2025** | 2025'te **196** yeni kendi kendine milyarder (toplam 386,5 milyar $) ve **91** varis (297,8 milyar $) ✔ | Yeni milyarderlerin ~2/3'ü girişimci |
| **Smith, Zidar & Zwick (2019)**, *Quarterly Journal of Economics* | ABD'de en üst %0,1'in gelirinde **iş sahipliği**, maaştan da yatırım getirisinden de önemli. Bu grubun yalnızca **%13'ünden azı** ağırlıkla faiz, kira gibi sermaye gelirine dayanıyor. Ortaklık kârlarının **~%75'i sahibinin emeğine ve becerisine** atfediliyor ✔ | Tipik profil: çalışma çağında, çeşitlendirilmemiş, nitelik yoğun sektörlerde orta ölçekli şirket sahibi (avukatlık, danışmanlık, sağlık, bayilik vb.) ✔ |
| **ABD servet dağılımı** (Fed verisi üzerine analiz) | En zengin %0,1 varlıklarının ~**%71'ini** şirket hissesi ve özel işletme olarak tutuyor (2026 1. çeyrek). Alt %50'nin varlığı ağırlıkla konut ◐ | Zenginler **şirket sahibi**, orta sınıf **ev sahibi** |
| **The Millionaire Next Door** (Stanley & Danko 1996) | Milyonerlerin ~**%80'i** birinci kuşak zengin. Çalışanların %20'sinden azını oluşturan serbest meslek ve iş sahipleri milyonerlerin **2/3'ü**. Gelirinin altında yaşıyorlar, statü tüketiminden kaçınıyorlar ✔ (kitaptan) | **Eleştiri** (Taleb): **hayatta kalma yanlılığı**. Aynı tutumlu davranıp batan küçük işletme sahiplerini görmüyoruz. Veri tarihin en güçlü boğa piyasasının hemen sonrasına ait ✔. "Tutumluluk zenginleştirir" ◐: gerekli ama tek başına yeterli değil |
| **Ramsey "National Study of Millionaires"** (10.000+ kişi) | %79'u hiç miras almamış. En sık meslekler mühendis, muhasebeci, öğretmen, yönetici ve avukat. %80'i şirket emeklilik planına düzenli yatırım yapmış ◐ | Kendi beyanına dayanan anket, saha tarihleri tutarsız. Şirket kendi finans eğitimi ürünlerini satıyor → **çıkar çatışması** ◐ |
| **Fidelity 401(k) milyonerleri** | 2026 2. çeyrek sonunda rekor **769.000** kişi, Fidelity'deki hesapların ~%3'ü ✔. Tipik profil: ~59 yaş, ~25-26 yıl aynı planda, ~%17 tasarruf oranı ◐ | Bu "sıradan yol": maaş + işveren katkısı + endeks + **25-30 yıl**. Son yıllardaki güçlü boğa piyasası da sayıyı büyüttü |

### 4b. Tasarruf oranı → çalışma yılı (Mr. Money Mustache, "The Shockingly Simple Math Behind Early Retirement") ✔

**Varsayımlar** (MMM'nin kendi metninden): **sıfır net servetle** başlanıyor, biriktirme döneminde **%5 reel getiri**, emeklilikte **%4 çekim**. Tasarruf oranı **net (eline geçen) gelire** göre. Biriktirdiğin kadar az harcadığın için hedef de küçülüyor: bu yüzden oran iki yönden çalışıyor.

| Tasarruf oranı | %3 reel | **%5 reel (MMM)** | %7 reel |
|---|---|---|---|
| %5 | 92 yıl | 65 yıl | 52 yıl |
| %10 | 69 | **51** | 41 |
| %15 | 56 | 43 | 35 |
| %20 | 47 | **36** | 30 |
| %25 | 40 | 32 | 27 |
| %30 | 34 | 28 | 24 |
| %40 | 25 | 21 | 19 |
| %50 | 19 | **16** | 15 |
| %60 | 14 | 12 | 11 |
| %70 | 9 | 9 | 8 |
| %80 | 6 | 5,5 | 5 |

- MMM'nin yazısındaki değerlerle tutarlı: %10'da ~51 yıl, %50'de ~16 yıl ✔.
- **Getiri varsayımı yüksek tasarruf oranlarında çok az fark yaratıyor** (%60'ta %3 ile %7 arası yalnızca ~2,4 yıl). Düşük oranlarda ise çok büyük fark var (%10'da 28 yıl). Early Retirement Now da aynı sonuca varıyor ✔.
- **Sınırlar**: Tablo sabit getiri varsayıyor (sıra riski yok, §2e). Vergi, sağlık, çocuk ve gelir dalgalanması yok. %4 oranı 40+ yıllık emeklilik için iyimser (§2d). Basit bir ilk yaklaşım olarak oku, kesin plan olarak değil.

### 4c. Çıkarım: iki yol, iki farklı risk profili

| Yol | Nasıl | Başarı olasılığı | Süre | Kanıt |
|---|---|---|---|---|
| **Yavaş ve düşük varyanslı** | Gelir artışı (beceri, kariyer) + %20-50 tasarruf + düşük maliyetli endeks | Yüksek (disiplin varsa) | 15-35 yıl | Fidelity, MMM tablosu, §2c |
| **Hızlı ve yüksek varyanslı** | Şirket kurmak veya erken ortaklık, hisse/opsiyon sahibi olmak | Düşük (girişimlerin çoğu başarısız, hayatta kalma yanlılığı) | Değişken | Kaplan-Rauh, Smith-Zidar-Zwick, Forbes |
| **Sadece "iyi yatırım" ile küçük sermayeyi büyütmek** | Hisse seçimi, trading, zamanlama | Çok düşük | — | SPIVA, Barber-Odean, 08 §1 |

→ ✔ **Anahtar fikir**: Yatırım bir **çarpandır**. Çarpılan şey (biriktirdiğin miktar) küçükse sonuç da küçük kalır. İlk 10-15 yılda en yüksek getirili "varlık" çoğu insan için **kendi kazanma gücüdür**: beceri, sertifika, iş değiştirme, yan gelir ya da iş kurma. Getiri, sermaye büyüdükçe önem kazanır.

---

## 5. Türkiye bağlamı

### 5a. Enflasyon ve kur: TL nakit, dolar nakit, küresel hisse (✔ hesap, `verify_birikim.py` E)

Veri: USD/TRY için TCMB yıl sonu gösterge kuru, enflasyon için TÜİK Aralık ayı yıllık TÜFE.

| Yıl | USD/TRY değişimi | TÜFE | Dolar nakdin TL bazında reel getirisi | S&P 500'ün TL bazında reel getirisi | 2015'teki 100 TL'nin alım gücü |
|---|---|---|---|---|---|
| 2016 | +%20,6 | %8,5 | +%11,1 | +%24,4 | 92,1 |
| 2017 | +%7,2 | %11,9 | -%4,2 | +%16,7 | 82,3 |
| 2018 | +%40,0 | %20,3 | +%16,4 | +%11,3 | 68,4 |
| 2019 | +%12,5 | %11,8 | +%0,6 | +%32,2 | 61,2 |
| 2020 | +%24,9 | %14,6 | +%9,0 | +%29,0 | 53,4 |
| 2021 | +%79,7 | %36,1 | **+%32,0** | +%69,9 | 39,2 |
| 2022 | +%40,3 | %64,3 | **-%14,6** | **-%30,1** | 23,9 |
| 2023 | +%57,4 | %64,8 | -%4,4 | +%20,7 | 14,5 |
| 2024 | +%19,8 | %44,4 | **-%17,0** | +%3,8 | 10,0 |
| 2025 | +%21,4 | %30,9 | -%7,2 | +%9,4 | **7,7** |
| **2015 sonu → 2025 sonu** | **×14,7** | **×13,0** | **toplam +%13** | **reel ×4,5 (yılda +%16)** | **7,7 TL** |

Çıkarımlar:
- ✔ **TL nakit (faizsiz) 10 yılda alım gücünün ~%92'sini kaybetti.** Yastık altı ya da vadesiz TL, en kesin kayıp.
- ✔ **Dolar nakit bir "yatırım" değil, kaba bir sigorta.** 10 yılda TÜFE'yi yalnızca ~%13 geçti, yıllık sonucu ise -%17 ile +%32 arasında savruldu. 2022-2025 arasında reel olarak **dört yıl üst üste** kaybettirdi.
- ✔ **TL mevduatın reel sonucu reel faize bağlı ve dönemsel.** 2022'de politika faizi **%9**'a indirilmişken (TCMB, Kasım 2022) yıllık enflasyon %64'tü, yani mevduat ağır reel kayıp yaşattı. 2025'te ise net mevduat getirisi **~%38**, enflasyon ~%31, dolar **+%21,5** oldu. Dolar reel **-%7**, mevduat reel olarak artıda kaldı (Türkiye Gazetesi, 30.12.2025) ✔. Ekim 2026: yıllık TÜFE **%29,77** ✔, politika faizi **%36** ◐. Bu denge politika değişikliğiyle hızla tersine dönebilir.
- ◐ **S&P 500'ün TL bazında reel ×4,5'i istisnai.** 2016-2025, ABD hisseleri için tarihsel ortalamanın çok üstünde bir on yıldı (yılda ~%14,8 nominal USD). Üstüne TL de reel değer kaybetti. Tabloda vergi, temettü stopajı, kur çevirme ve aracı kurum maliyetleri **yok**. **Gelecek için bir tahmin değil.** Asıl ders şu: reel kazanç **üretken varlıktan** (şirket hissesi) geldi, sadece dövizden değil.
- ◐ **TÜİK verisi tartışmalı**: ENAG 2024 için %83,4, 2025 için %56,1 açıkladı (TÜİK: %44,4 ve %30,9). Gerçek enflasyon TÜİK'ten yüksekse, tablodaki tüm reel sonuçlar TL tutanlar için daha kötü.
- Kişisel not: Harcamaların TL ise hedef "dolar zenginliği" değil, **TL bazında alım gücü**. 1.000$/ay hedefi de Türkiye'deki yaşam maliyetine ve kura göre yeniden düşünülmeli.

### 5b. Türkiye'de yaşayan biri için seçenek kategorileri (ürün veya kurum önerisi değil)

| Kategori | Ne sağlar | Dikkat edilecekler |
|---|---|---|
| **Yurt dışı aracı kurum üzerinden küresel/ABD endeks ETF'leri** (ABD ya da İrlanda'da kurulu, UCITS) | En geniş çeşitlendirme, çok düşük yıllık gider (genelde ~%0,05-0,25 ◐), USD bazlı varlık | **ABD veraset vergisi**: ABD'de yerleşik olmayanların ABD'de bulunan varlıkları (ABD'de kurulu ETF ve hisseler dahil) **60.000$**'ı aşarsa ABD'de beyanname gerekir ✔ (IRS). Bu yüzden İrlanda'da kurulu UCITS fonlar sık tercih ediliyor ◐. Temettü stopajı ◐, havale ve kur maliyeti, aracı kurumun bulunduğu ülkenin yatırımcı koruma rejimi (karşı taraf riski), AB kurumlarında bireysel yatırımcıya ABD ETF'i satış kısıtları ◐ |
| **Türk aracı kurum üzerinden yurt dışı hisse/ETF** | Yerel destek, TL/USD hesap | Saklama zinciri ve ücretler. Vergi yükümlülüğü yine sende ◐ |
| **Yurt dışı menkul kıymet vergisi** (genel çerçeve) | — | ◐ Satış kazancı yıllık beyannameyle beyan edilir. Alış ve satış o günün kuruyla TL'ye çevrilir. Yİ-ÜFE artışı %10'u aşarsa maliyet endekslenebilir. Kaynaklara göre beyan sınırı ya da istisna yok (Kastamonu Defterdarlığı özelgesi). Temettü için ayrı sınır var (2026: 22.000 TL ◐). Kurallar sık değişiyor, **mali müşavire danış** |
| **TEFAS fonları** (yabancı hisse fonları, BIST endeks fonları, altın ve para piyasası fonları) | TL ile, küçük tutarla, kolay alım. Yurt içi saklama | Yıllık toplam gider genelde global ETF'lerden **çok yüksek** (yüzde 1-3 bandı yaygın ◐, fonun KAP'taki TEG bildirimine bak). Endeksi takip farkı. Fon türüne göre stopaj kuralları değişiyor ◐ |
| **BIST endeksi** (BIST 30/100 fonları veya ETF'leri) | Türkiye'deki şirketlerin hisseleri, TL enflasyonuna karşı reel varlık | Tek ülke riski yoğunlaşması (Nikkei örneği, §2b). DMS: küresel çeşitlendirme çoğu piyasada daha iyi bir risk/getiri oranı sağlıyor ✔ |
| **Altın** (fiziki, banka hesabı, fon) | Kriz ve TL değer kaybı dönemlerinde koruma, kültürel likidite | Uzun dönem reel getiri düşük (%1,3, §2a), on yıllarca düz dönemler. Fiziki altında alış-satış makası ve işçilik maliyeti. "Enflasyon kalkanı" iddiası zayıf ✘ |
| **BES** | Devlet katkısı: **1 Ocak 2026'dan itibaren %20** (önceden %30, Resmi Gazete 07.01.2026) ✔. 2026 yıllık katkı tavanı ~79.272 TL ◐ | Devlet katkısının hak edişi süreye ve yaşa bağlı (kademeli) ◐. Fon gider kesintileri. Erken çıkışta katkının bir kısmı kaybedilir. Güncel kuralları kontrol et ◐ |
| **TL mevduat / para piyasası fonu** | **Acil durum fonu** için likidite | Reel getiri döneme bağlı (§5a). Uzun vadeli servet aracı değil |

**Genel kontrol listesi**:
1. **Kur**: Gelirin ve giderin TL ise, varlıkların bir kısmı TL olabilir (acil fon), uzun vadeli kısım ise döviz bazlı küresel varlık.
2. **Maliyet**: Yıllık gider oranı ile al-sat ve kur makası toplamı.
3. **Vergi**: Beyan zorunluluğu, stopaj, veraset.
4. **Karşı taraf riski**: Kurumun lisansı, hangi ülkede düzenlendiği, müşteri varlıklarının ayrı tutulup tutulmadığı.
5. **Düzenleme riski**: Kurallar hızla değişiyor (2026'da BES katkısı %30'dan %20'ye indi).
6. **Basitlik**: Tek bir geniş küresel endeks + acil fon, karmaşık bir portföyden genellikle daha iyi uygulanır.

---

## 6. Trading ve yatırım: birlikte nasıl düşünülmeli?

**Temel oranlar** (tekrar etmemek için kısa, ayrıntılar 08 §1, 14 §3d ve 09 §4h'de):
- Day trader'ların çok büyük çoğunluğu uzun vadede kaybediyor. Brezilya'da %97'si zarar etti, Tayvan'da istikrarlı kâr edenler %1'den az ✔ (08 §1).
- Prop sektörü verisi: challenge alanların ~**%14'ü** geçiyor, ~**%7'si** ödeme alıyor, ortalama ödeme hesabın ~%4'ü (FPFX, 09 §4h) ◐.
- Brandt: 3 yıl eğitim sonrası 5 yıl boyunca yılda %30 yapabilenler "binde 2-5" (14 §3d).

**Ölçek kıyası** (basit örnek ◐): 10.000$'lık fonlu hesapta ayda **%2** net kâr (iyi bir sonuç) ve %80 kâr payı = ayda **~160$**. Bu, 10 yıl boyunca ayda 300$ biriktirip %4 ile çekilebilecek gelirle (~171$/ay, §1e) **aynı büyüklükte**, üstelik çok daha belirsiz. Küçük prop hesapları zenginlik değil, **beceri kanıtı** ve küçük ek gelir sağlar. Ölçeklenme ancak kanıtlanmış, kalıcı bir avantajla mümkün (09, 14 §3f).

**Mantıklı birleşik plan** (genel çerçeve):

| Sıra | Adım | Gerekçe |
|---|---|---|
| 1 | **Acil durum fonu**: 3-6 aylık gider, likit ve TL ağırlıklı | Kötü bir ayda yatırımı ya da hesabı bozmamak için |
| 2 | **Gelire yatırım**: beceri, kariyer, yan gelir | İlk 10 yılın en büyük kaldıracı (§1f, §4c) |
| 3 | **Otomatik tasarruf**: hedef %20 ve üstü, her zamda oranı artır | §4b tablosu. Her yıl +%5 katkı, 30 yılda geliri ~%75 artırıyor (§1c) |
| 4 | **Çekirdek portföy**: düşük maliyetli, küresel çeşitlendirilmiş endeks. İstersen küçük bir altın/TL tamponu. Yılda bir yeniden dengele | §2a, §3. Seyrek işlem, düşük gider |
| 5 | **Trading/prop bütçesi**: kaybedilmesi göze alınan küçük bir tutar. Challenge ücretleri "eğitim gideri" sayılır | Başarı oranı düşük (§6). Bütçe biterse yeni para eklenmez, önce süreç gözden geçirilir (14 §3f) |
| 6 | **Kâr akışı**: prop ödemelerinin bir kısmı çekirdek portföye aktarılır | Şanslı dönemin kazancını kalıcı servete çevirir. "Kazancı tutmak" (Brandt, 14 §3d) |
| 7 | **Ölçekleme kuralı**: aynı kurallarla **200-300 işlem** sonra beklenen değer pozitifse ve kurallara uyum yüksekse büyüt | 10 §3, 14 §3d |
| ✘ | **Asla**: geçim parası, borç ya da kredi kartıyla trading. "Kaybı hızlı kapatma" amacıyla boyut büyütme | 08 §2, 14 §3 |

> Brandt'ın gençlere tavsiyesi (14 §3d): "İyi bir işin varsa her ay biriktir ve endekse koy." Trading'i deneyeceksen **5 yıl hayatta kal, parayı bir arada tut.** Bu iki tavsiye çelişmiyor: çekirdek servet endeksle, beceri deneyi küçük ve sınırlı bütçeyle.

---

## 7. Hızlı kontrol: iddia → hüküm

| İddia | Hüküm |
|---|---|
| "10 yılda ayda 300$ ile emekli olurum" | ✘ ~171$/ay gelir. 1.000$/ay için yılda %40 reel getiri gerekir |
| "Sadece maaş + düzenli endeks yatırımıyla finansal bağımsız olunur" | ✔ Mümkün, ama tasarruf oranına göre 15-50 yıl sürer |
| "Self-made zenginlerin çoğu borsada yatırımla zengin oldu" | ✘ Çoğu şirket sahipliği ve beceri geliriyle zenginleşti. Yatırım servetlerini korudu ve büyüttü |
| "Uzun vadede hisseler hep kazandırır" | ◐ ABD'de 20 yılda neredeyse hep, ama 10 yılda %11 ihtimalle reel zarar. Tek ülkede on yıllarca düz dönem mümkün (Nikkei 34 yıl) |
| "%4 kuralı güvenli" | ◐ ABD'de 30 yıl için büyük ölçüde evet. Uluslararası veride, uzun sürelerde ve yüksek masrafta değil (%3-3,5 daha temkinli) |
| "Aktif fon ya da trading endeksi geçer" | ✘ Uzun vadede çoğunluk geçemiyor (SPIVA ~%93, 20 yıl) |
| "Altın enflasyona karşı kalkandır" | ✘ Yüksek enflasyonlu yılların ~yarısında negatif. Uzun vadede düşük reel getiri |
| "Dolar tutmak Türkiye'de servet korur" | ◐ 10 yılda TÜFE'yi ancak geçti. 2022-2025'te reel olarak kaybettirdi. Koruma oynak, büyüme yok |
| "DALBAR: yatırımcılar fonlarından yılda birkaç puan geride" | ◐ Yön doğru, büyüklük abartılı. Morningstar'a göre ~1,2 puan |
| "Millionaire Next Door: tutumlu ol, zengin olursun" | ◐ Tutumluluk gerekli ama yeterli değil. Hayatta kalma yanlılığı var |

---

## Kaynaklar

**Uzun dönem getiriler ve riskler**
- UBS Global Investment Returns Yearbook 2026, kamuya açık özet (Dimson, Marsh, Staunton): https://www.ubs.com/content/dam/assets/wm/static/cio/documents/giry2026-summary-public.pdf
- Cambridge Judge Business School, 2025 Yearbook özeti (dünya 1900-2024 %5,2 / %1,7 / %0,5; 21. yy %3,5): https://www.jbs.cam.ac.uk/2025/report-stocks-have-far-outperformed-over-the-past-125-years/
- UBS GIRY 2025 sayfası: https://www.ubs.com/global/en/investment-bank/insights-and-data/2025/global-investment-returns-yearbook-2025.html
- Shiller verisi (aylık S&P 500, temettü, CPI, faiz; DataHub kopyası): https://raw.githubusercontent.com/datasets/s-and-p-500/main/data/data.csv · Orijinal: http://www.econ.yale.edu/~shiller/data.htm
- Nikkei'nin 1989 rekorunu geçmesi: https://www.nippon.com/en/japan-data/h01927/nikkei-index-sets-first-record-high-since-1989.html · https://www.bloomberg.com/news/articles/2024-02-22/nikkei-225-heads-to-close-above-record-high-reached-in-1989

**Güvenli çekim oranı**
- Bengen 2025, 4,7%: https://www.advisorperspectives.com/articles/2025/08/29/bill-bengen-boosts-the-4-rule-to-4-7
- Trinity çalışması: https://en.wikipedia.org/wiki/Trinity_study · 2015 güncellemesi (JFP): https://financialplanningassociation.org/article/journal/AUG15-sustainable-retirement-spending-low-interest-rates-updating-trinity-study
- Pfau 2010, 17 ülke: https://www.financialplanningassociation.org/article/journal/DEC10-international-perspective-safe-withdrawal-rates-demise-4-percent-rule · https://www.thinkadvisor.com/2011/04/22/the-4-rule-has-not-worked-out-so-well-pfau-answers
- Morningstar 2026: https://www.morningstar.com/retirement/whats-safe-retirement-withdrawal-rate-2026 · 2025: https://www.morningstar.com/retirement/whats-safe-retirement-spending-rate-2025

**Aktif ve pasif, yatırımcı davranışı**
- SPIVA U.S. Year-End 2025: https://www.spglobal.com/spdji/en/spiva/article/spiva-us-year-end-2025/ · PDF: https://www.spglobal.com/spdji/en/documents/spiva/spiva-us-year-end-2025.pdf · Özet: https://www.investmentnews.com/equities/active-managers-stumble-again-in-2025-as-large-caps-dominate/265541
- Barber & Odean (2000), "Trading Is Hazardous to Your Wealth", *Journal of Finance* 55(2) (ayrıca 08 §1)
- Morningstar Mind the Gap 2026: https://www.morningstar.com/content/cs-assets/v3/assets/blt9415ea4cc4157833/blt852a4301adc2f5db/6a7373d51f7b5ae2da78e1e8/US_Mind_the_Gap_2026.pdf
- DALBAR eleştirileri: https://www.kitces.com/blog/does-the-dalbar-study-grossly-overstate-the-behavior-gap-guest-post/ · https://www.advisorperspectives.com/articles/2017/05/08/testing-dalbar-s-claims-about-mutual-fund-investors · DALBAR'ın cevabı: https://www.thinkadvisor.com/2017/04/20/lou-harvey-hits-pfau-back-over-criticism-of-dalbar/
- S&P 500 yıllık toplam getirileri (2016-2025): https://www.upmyinterest.com/sp500/ · 2025 %17,9: https://ca.rbcwealthmanagement.com/weatherill-wealth/blog/4722507-SP-500-Stats-A-Lot-of-Bull

**Servetin kaynakları**
- Kaplan & Rauh (2013), AER: https://econpapers.repec.org/RePEc:aea:aecrev:v:103:y:2013:i:3:p:158-62 · Özet: https://marginalrevolution.com/marginalrevolution/2013/08/the-origins-of-the-forbes-400.html
- Korom, Lutter, Beckert: https://pure.mpg.de/pubman/item/item_2239111_7/component/file_2239109/mpifg_dp15_8.pdf
- Forbes 400, 2025: https://www.forbes.com.au/news/billionaires/the-forbes-400-list-ranking-americas-richest-people/
- UBS Billionaire Ambitions Report 2025: https://www.ubs.com/global/en/media/display-page-ndp/en-20251204-billionaire-ambitions-report-2025.html
- Smith, Zidar, Zwick, "Capitalists in the Twenty-First Century": https://www.nber.org/papers/w25442 · NBER Digest: https://www.nber.org/digest/may19/how-top-earners-make-money-often-running-business
- En zengin %0,1'in varlık bileşimi (Center for American Progress, Fed verisi) ◐: https://www.americanprogress.org/?p=156298
- The Millionaire Next Door: https://en.wikipedia.org/wiki/The_Millionaire_Next_Door · Kitap alıntısı: https://www.bookbrowse.com/excerpts/index.cfm/book_number/242/page_number/6/The-Millionaire-Next-Door
- Ramsey National Study of Millionaires: https://www.ramseysolutions.com/retirement/the-national-study-of-millionaires-research
- Fidelity 401(k) milyonerleri: https://www.cbsnews.com/news/401k-millionaires-new-record-fidelity · https://about.fidelity.com/data-and-insights/q4-2025-retirement-analysis · https://www.moneytalksnews.com/a-record-fidelity-savers-are-now-k-millionaires-what-changes-when-the-balance-is-that-big/
- Mr. Money Mustache: https://www.mrmoneymustache.com/2012/01/13/the-shockingly-simple-math-behind-early-retirement/ · Early Retirement Now eleştirisi: https://earlyretirementnow.com/2017/11/01/shockingly-simple-complicated-random-math-behind-early-retirement/

**Türkiye**
- USD/TRY yıl sonu (TCMB gösterge kuru tablosu): https://www.simianx.ai/tr/stories/us-dollar-exchange-rate-by-year-every-year-1971-2026-table
- TÜFE: TCMB: https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Istatistikler/Enflasyon+Verileri/ · 2016 (İş Bankası): https://ekonomi.isbank.com.tr:443/ContentManagement/Documents/eg_201612.pdf · 2018: https://ekonomi.isbank.com.tr:443/contentmanagement/Documents/tr05_enflasyon/2018/EG_201812_2018_de_yillik_TUFE_artisi_20_3_oldu.pdf · 2019: https://ekonomi.isbank.com.tr:443/contentmanagement/Documents/tr05_enflasyon/2019/EG_201912_yilsonu_TUFE_enflasyonu_yuzde_11_84_oldu.pdf · 2020: https://www.hurriyet.com.tr/ekonomi/2020-enflasyonu-yuzde-14-60-41706125 · 2024: https://www.sbb.gov.tr/2024-yili-aralik-ayi-tuketici-ve-uretici-fiyat-gelismeleri/ · 2025: https://www.sbb.gov.tr/?p=62406 · Ekim 2026: https://www.sbb.gov.tr/?p=65672 · ENAG 2024 karşılaştırması: https://t24.com.tr/ekonomi/tuik-enflasyonu-acikladi,1207262
- 2025'te dolar, TÜFE ve mevduat: https://www.turkiyegazetesi.com.tr/ekonomi/2025-dolar-icin-kayip-yil-hem-tufe-hem-tlye-yenildi-1759516
- TCMB Kasım 2022 faiz kararı (%9): https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/PPK/PPK+Toplanti+Kararlari/DUY2022-47 · 2026 faiz seyri ◐: https://www.milliyet.com.tr/haber/7685697/
- BES devlet katkısı %20: https://www.bloomberght.com/bes-devlet-katkisi-yuzde-20-ye-indirildi-3765538 · PwC bülteni: https://www.pwc.com.tr/tr/hizmetlerimiz/insan-yonetimi-ve-organizasyon-danismanligi/sosyal-guvenlik-hizmetleri/bultenler/2026/bireysel-emeklilik-sistemi-devlet-katki-oraninin-dusurulmesi-hk.html
- Yurt dışı hisse vergisi (genel) ◐: https://www.yapikredi.com.tr/medium/file/yabanci-hisse-senedi-gelirlerinde-2026-yili-vergi-durumu_71999/view · https://www.ekonomigazetesi.com/kose-yazisi/abd-borsasindan-elde-edilen-kazanclar-nasil-vergilendirilir-86043 · https://www.fatiharas.com/abd-borsasi-vergi/
- ABD veraset vergisi, yerleşik olmayanlar (60.000$): https://www.irs.gov/individuals/international-taxpayers/some-nonresidents-with-u-s-assets-must-file-estate-tax-returns

**Bu bilgi tabanında ilgili dosyalar**: 08 §1 (akademik trader verileri), 09 §4h (prop sektörü oranları), 10 §3 (örneklem büyüklüğü), 14 §3d ve §3f (Brandt, Grimes: süre, sermaye, hayatta kalma).
