# 15 — Prop Yol Haritası: 58 turun doğrulanmış bulgularından karar listesi

> Bu dosyada yeni bilgi yok. Diğer dosyalardaki doğrulanmış bulguları FTMO odaklı bir sıraya ve kontrol listesine çevirir. Her madde kaynağına bağlı, ayrıntı ve sınırlar orada. 50. turda yazıldı, 59. turda (2026-11-22, döngünün son turu) son haline getirildi. Yeni bulgu geldikçe ilgili maddeyi güncelle.

## 0. Önce gerçek tablo

- **Geçmek kanıt değildir.** Avantajı olmayan biri iki aşamalı bir challenge'ı modele göre ~%30-45 olasılıkla geçer (09 §1, §4m).
- **Koridor formülü**: avantaj yokken geçme olasılığı ≈ maksimum zarar / (hedef + maksimum zarar). Trailing limit ve maliyet bunu düşürür (09 §1b, §4o).
- **Sektörün gerçeği**: FPFX verisinde hesapların %14'ü geçiyor, %7'si ödeme alıyor. Topstep 2025'te combine başına %16,8 geçme, fonlananların %0,71'i Live hesaba geçiyor. Bu, işlem başına ~-0,1R'ye denk: **ortalama aday maliyet ödeyen avantajsız bir strateji gibi sonuçlanıyor** (09 §4h, §4o).
- **"Geçenlerin profili" çoğunlukla şanstır**: avantajı olmayan geçenlerin isabeti bile %65 görünür (09 §4j).
- **Brandt'ın tahmini**: prop'ta yılda %1 kârlı (09 §4r).
- **Risk ayarı avantaj yaratmaz**: avantaj yoksa hiçbir boyut ya da risk kuralı işe yaramaz. Düşük risk sadece avantajı olana yarar (09 §1f, §4m).

## 1. Aşama 0 — Para ödemeden önce avantajı kanıtla

1. **Setup'ı yazılı tanımla**: giriş, stop, çıkış ve işlem yapmama koşulları (03).
2. **Rastgele kıyasa karşı test et**: aynı dönem, aynı yön, gün içinde aynı saat profili (10 §6l, 04 §6b-5). Bu kıyastan **geçemeyenler**: filtresiz sweep ve SFP, PDH/PDL dönüşü, Asya iki uç süpürmesi, Market Profile %80 kuralı, open drive başarısızlığı, mum formasyonu isabetleri, Fibonacci, "iki mum" stratejisi, Brooks'un "%80 tepe testi", Keltner ve Bollinger bant kuralları, tek hissede mekanik "kapitülasyon" alımı (11 #61-88, 04 §12, 12). Dante'nin "seviyeye sert gelen tutunur" kuralı testte **tersine** çıktı (05 §8c).
   - **Yönü de eşleştir**: yükselen bir piyasada becerisiz rastgele long girişler bile işlem başına +0,15 ile +0,22R görebilir (2025 4. çeyrekte altın). Birkaç aylık başarıyı o dönemin yönüne karşı ölç (10 §6o).
   - **Zaman dilimini ayrı test et**: aynı kural farklı zaman diliminde farklı çalışır, maliyet ölçekle büyür (10 §6n).
3. **Zamana karşı test et** (2015 öncesi ve sonrası): endeks pullback'i düştü, RSI-2 kaldı (04 §5b, 12).
4. **Maliyetten sonra R cinsinden ölç**: 1 saatlik FX'te maliyet ~0,10R, günlükte ~0,01R. 5 dakikalık EURUSD'de ATR'nin yarısı (04 §5b, 10 §6n).
5. **Örneklem büyüklüğü**: +0,2R'lik avantajda 30 işlemlik dilimlerin %28'i zararda biter. +0,3R'lik farkı göstermek ~200 işlem ister (README #40, 02 §4c).
6. **Sağ kenar doğrulaması**: geçmiş grafikte bulduğun avantaj, farklı bir veri setinde kör replay ile de çıkmalı (13 §5 madde 7, 12).
7. **Parasız ileri test, sonra çok küçük boyut.** Boyutu kâra göre değil kural uyumuna göre büyüt (14 §3f).

**Geçme ölçütü (öneri)**: maliyetten sonra ≥ +0,1R, rastgele kıyastan ≥2 standart hata fark, verinin iki zaman yarısında da pozitif, ve en az 200 işlem.

**Bu bilgi tabanında şu an testten geçenler** (hiçbiri tek başına hızlı bir prop aracı değil):

| Aday | Bulgu | Kaynak |
|---|---|---|
| Endekste RSI-2 | 2015+ rastgeleden +0,17R (se 0,04) | 12, README #46 |
| Emtiada kırılım + trailing çıkış | 2015+ +0,16R, rastgele +0,07R | 03, README #55 |
| 12 ay momentumu + SPY (çok piyasalı) | Sharpe 0,82, challenge %89 geçiyor ama ~1,5 yıl | 12, README #37 |
| Uzun vadeli çok piyasalı trend (100 günlük kırılım, 30 vadeli) | +0,24R, kâr en iyi %10'luk işlemlerden. Çok yavaş, CFD'de swap maliyeti test edilmedi | 12, README #72 |
| Çok aylık kırılım + hacim (hisse) | Sadece 20 günlük ortalama çıkışıyla, 2015+ rastgeleden +0,25R. Hayatta kalma yanlılığı var, zayıf | 12, README #64 |
| **CHoCH + geri test, üç filtreyle** (üst zaman dilimi uyumlu, CHoCH öncesi fitille süpürme, EMA20 geri testi; 1H ve 4H) | **Düzeltildi (2026-11-26, tam veri)**: bütün piyasalarda +0,00R (n=586). İlk testteki +0,175R bankanın örneklem şansıydı. **BTC −0,25R** (üç dönemde de eksi), altın 0. **Pariteler +0,25R** (n=265), 2023 öncesi, 2023 ve 2024-26'da artı. Sonradan seçilmiş alt grup: **hipotez**, ileri test. Aynı turda 10 filtrenin 3.787 birleşimi tarandı: hiçbiri seçim ölçütüne bile ulaşmadı, yılın en iyisi ertesi yıl tutmadı | `arastirma/verify_choch_filtreleri.py`, `verify_choch_kombinasyon.py`, `FTMO-PLANIM.md` |
| 5 dakikalıkta dürtü sonrası tepe testi | %63-69 (rastgele %54-55), 60 günlük örneklem, hipotez | 06 §8b-4 |
| Son yarım saatte dönüş | 🧪 Zayıf hipotez. Önceden kayıtlı ileri test 2026-11-23'te başladı. Ara kontroller 60. ve 250. günde, nihai karar 500. günde (~2028 sonu), çünkü etki gürültüye göre çok küçük | README #32, 04 §6b-4 |

## 2. Aşama 1 — Hesap ve firma seçimi

- **En büyük kol hesap tipi**: aynı büyüklükte trailing limit ve çekilemez tampon, beklenen ödemeyi yarıya indiriyor. İlk kriter statik limit ve çekilebilir kâr (09 §4l).
- **FTMO 1 aşamalı mı, 2 aşamalı mı?**
  - 1 aşamalı: benzer geçme oranı, 2 kat hız, ama %3 günlük limit acımasız (09 §4p).
  - Uzun fonlu kariyer için 2 aşamalı daha uygun: statik limit, iade edilen ücret, ölçeklendirme.
- **Strateji hesap tipine uymalı**: FTMO Standart fonlu hesapta 2 saatten uzun kapanışlarda (hafta sonu) pozisyon taşımak yasak. Haftalarca tutan stratejiler Swing hesap ister. Değerlendirmede kısıt yok (09 §4i).
- **Hafta sonu taşıyacaksan enstrüman seç**: vadeli, parite ve endekste en kötü açılış boşluğu ~-4R, tek hissede -10R (bilanço), küçük hissede -96R (02 §6e).
- **Firmayı geçme oranına göre değil, ilk ödemeye kadar gereken hesap sayısına göre** değerlendir. Avantaj yokken ödeme zinciri: ilk ödeme %22, ikinci %7, üçüncü %2 (09 §4s).
- **Kuralları yazılı oku**: haber, tutarlılık, yasaklı uygulamalar, ödeme süreci. Çoğu hesap strateji yüzünden değil kural ihlali yüzünden kaybedilir (09 §4d, §4e, §4i).

## 3. Aşama 2 — Challenge ayarları

- **Risk**: kanıtlı avantajla %1-2, günde ≤1 işlem (09 §1d, §4m).
- **Kurtarma ve bitirme işlemi yok**: avantajın varsa düşüşte büyük işlem, 2 kayıptan sonra boyutu ikiye katlama ya da hedefe yakın büyük işlem geçme oranını düşürür. Tilt, +0,2R'de geçmeyi %89'dan %77'ye indiriyor (09 §4v).
- **Notlara göre büyük boyut farkı ancak kanıtla**: SMB tipi 16 kat fark, notlar bilgi taşımıyorsa %10 düşüş olasılığını 4 katına çıkarıyor. Önce ~4 ay tutarlılık (02 §4c, 13 §3e).
- **Küçük hesap challenge'ı alışkanlığı taşıma**: işlem başına %5 ve üstü risk, +0,2R'lik avantajın geçme oranını %87'den %40'a düşürüyor (09 §4u).
- **Günlük limit formülü**: işlem başına risk × günlük en fazla işlem sayısı < günlük limit (1 aşamalıda %3, 2 aşamalıda %5). Günde 2 işlem ve %1,5 riskle 1 aşamalı geçme %13'e düşüyor (09 §4p).
- **Önceden yazılmış düşüş kuralı**: ≥4 ardışık kayıpta riski yarıya indir, başa başta geri yükle. Avantajı olan stratejide kaybetme olasılığını yarıya indiriyor (09 §1f).
- **Gün içi gerileyen boyut** (FT71): günlük limitin 1/3'ünde boyut %60, yarısında %50, 3/4'ünde %20. Günde 6 işlemle bile -%3'e hiç ulaşmıyor, sabit boyut günlerin %13-24'ünde ulaşıyor. **FTMO 1 aşamalı hesapta en önemli tek kural olabilir** (02 §7).
- **"Tek işlemde geç" yalnız avantajı olmayanın en iyi kumarı** (`arastirma/verify_tek_islem_ftmo.py`, 2026-11-25). İki aşamayı geçme: avantaj yokken tek atış %34, %0,5 risk %33. −0,05R'de tek atış %32, %0,5 risk %12. +0,1R'de tek atış %40, %0,5 risk **%80**. +0,2R'de %45'e karşı **%97**. Avantajın varsa küçük risk geçme olasılığını ikiye katlar; videolardaki tek işlem geçişleri (kanal değerlendirmeleri) bu yüzden beceri kanıtı değil.
- **Kademeli kâr alma yok**: test edilen iki avantajda beklentiyi yarıya indiriyor. Oynaklığı azaltmak istiyorsan boyutu küçült (03).
- **"Eğer-ise" çerçevesi** (FTMO'ya ölçeklenmiş): günde -%2,5'ta yarım boyut, -%3,5'ta günü kapat, toplam -%6'da bir hafta yarım boyut (02 §6d).
- **Volatiliteye göre boyut**, açık pozisyonları da ayda bir yeniden boyutla. En kötü günü yarıya indiriyor (02 §6b-3).
- **İlişkili pozisyonlar tek bahistir** (02 §6c).
- **Gece**: günlük limit gece yarısı bakiyesinden hesaplanır, equity sayılır. Gece taşınan açık zarar o günün payını baştan yer (09 §4i).
- **Açılış boşluğu**: gece taşınan pozisyonu "makul en kötü boşluğa" göre de sınırla. 1 ATR stop, tutuşların %1-4'ünde açılışta atlanıyor (02 §6e).
- **Yasaklar**: zarardaki işleme ekleme (Martingale), stopsuz işlem, firma hatası istismarı (11 #72, 09 §4b, 02 §6b-4).
- **Tampon**: en az 10R. "5 işlem payı" bırakan trader büyük ihtimalle hesabı patlatır (09 §4g).
- **Acele etme**: firma verilerinde swing işlem, statik limit ve sabır daha başarılı (09 §4k, README #41).

## 4. Aşama 3 — Fonlu hesap

- **Avantajın varsa en değerli şey hesabın ömrü**: düşük risk (%0,5) ya da %5-10'luk kâr tamponu 3 yıllık ödemeleri ~2 katına çıkarıyor (09 §4n).
- **Erken küçük ödeme** en az bir ödeme alma olasılığını artırır, beklenen toplamı değiştirmez (09 §4l).
- **Pratik risk ~%1**. Model yüksek riskte daha fazla kazanç gösterse de tutarlılık kuralı, ölçeklendirme ve tilt model dışında (09 §4m).
- **Ölçeklendirme planı** ancak güçlü avantaj ve düşük riskle anlamlı (09 §4n).
- **"Hesabı yak, yenisini al" döngüsü** FTMO'da "hesap döndürme" olarak yasak (09 §4n).
- **"Döner kapı" gibi prop oyunu stratejileri** avantaj yaratmaz. Düşüşteki fonlu hesabı atmak, firmanın verdiği bedava tamponu çöpe atmaktır. Değerlendirmede tek işlemde %4,5 risk avantajlının geçme oranını %58'den %35'e düşürür (09 §4w).
- **Önce tek hesapla bir ödeme al, sonra büyüt.** Kopya işlem çeşitlendirme değildir (09 §4g).
- **JadeCap modeli**: firmalar arasında çeşitlendirme, hesap başına %0,25-0,5 risk, haftada 2-3 işlem (09 §4q).
- **Ödeme alan trader profili** (The5ers CEO'su): swing işlem, az işlem, düşük efektif kaldıraç (1:10-1:20), tutarlı lot (09 §4v).
- **Ödeme aldığın ayları piyasanın o aylardaki yönüyle birlikte kaydet.** Bir trend döneminde art arda gelen ödemeler, piyasa yatay ya da ters döndüğünde sürmeyebilir (10 §6o, 09 §4x).

## 5. Süreç: her aşamada

- **Oyun kitabını işlemden önce tanımla, her işlemi girişte etiketle.** "Plan dışı" işlemleri kesmek için kanıt gerekmez. Tanımlı bir setup'ı tek çeyreğin sonucuyla bırakma (13 §3d).
- **İşlemleri notla ama boyutu nota göre ancak kanıtla değiştir** (~200 A işlemi) (02 §4c).
- **Kısıt analizi**: P&L'yi en çok sınırlayan tek şeyi bul. Yapay zekâyı bunu analiz etmek ve kısıtlayıcı araç yazmak için kullan, düşünmeyi devretmek için değil (13 §3d).
- **Haftalık inceleme** (Cumartesi inceleme, Pazar plan) ve **Douglas'ın 20 işlemlik disiplin egzersizi** (13 §2, §3c).
- **Stop asla zarar yönünde taşınmaz** (08).
- **Büyük kayıplar çoğunlukla sıcak bir seriden hemen sonra gelir.** Pozitif sistemi zarara çeviren, büyük boyutla alınan intikam ve sezgi işlemleridir (09 §4g, 02 §4c).
- **ASSET sırası** (SMB): dağılım (A+/A/B/C) → stop (girişten önce) → giriş → boyut (hesaplanır) → hedef. 4 ay tutarlılık olmadan risk artışı yok (13 §3e).
- **İlerlemeyi P&L ile değil hata kaydıyla ölç**: hata çetelesi (Dante), hata işlemleri (FT71), beklenti tick/R cinsinden. Ekranda P&L'yi gizle (13 §3c, §3f).
- **Aylık bağımlılık kontrolü**: kaybı geri almak için boyut büyütme, bozulan uyku, plansız gece işlemi, tatmin vermeyen kazanç. İkiden fazla "evet" bir davranış sorunudur (08 §8).

## 6. Bir bakışta karar akışı

```
Aşama 0 ölçütünü geçen yazılı bir avantajın var mı?
├─ Hayır → challenge satın alma. Replay, kör mod ve ileri testle devam et.
│          Yine de alacaksan ücreti eğitim gideri say: beklenen sonuç negatif.
└─ Evet → Strateji hafta sonu pozisyon taşıyor mu?
          ├─ Evet → FTMO Swing hesap. Hafta sonu boşluk senaryosunu günlük limit planına ekle.
          └─ Hayır → Standart hesap.
          → Risk × günlük en fazla işlem < günlük limit mi? Değilse riski düşür
            ya da gün içi gerileyen boyut kullan (1 aşamalıda zorunlu say).
          → Challenge: %1-2 risk + düşüş kuralı + eğer-ise çerçevesi.
            Kurtarma, bitirme ya da tilt işlemi yok. Kademeli kâr alma yok.
          → Fonlu: ~%1 risk + %5-10 kâr tamponu, önce tek ödeme, sonra büyüt.
```

## 7. Açık sorular

- Son yarım saat dönüşünün ileri testi: `arastirma/verify_close_reversal_forward.py` dosyasını ~2027 Şubat ortasında (60. gün) ve ~2027 Kasım'da (250. gün) ara kontrol için, ~2028 sonunda (500. gün) nihai karar için çalıştır. Kurallar dosyada sabit (README #32). Ana planı engellemez, yan iştir.
- Brooks'un EMA dokunuşu testinin yeni veriyle tekrarı.
- CFD swap maliyetinin swing portföyüne etkisi: FTMO ücret tablosunu yayımlamıyor (09 §4i).
- Senin kendi replay ve sim verinle Aşama 0 ölçütü: uygulamadaki setup ayrıştırma raporu, kör mod, hata çetelesi ve yaklaşma hızı etiketi (13 §5 madde 12-15).
- 5 dakikalıkta dürtü sonrası tepe testi (06 §8b-4): daha uzun 5 dakikalık veriyle ve maliyetle yeniden test.

## 8. Bu bilgi tabanını nasıl kullanmalı?

1. Önce bu dosyayı oku, sonra README'deki "En önemli doğrulanmış gerçekler" listesini.
2. Bir video ya da tweet yeni bir iddia getirdiğinde önce 11'deki efsaneler listesine ve kırmızı bayrak kontrol listesine bak. Çoğu iddianın bir benzeri zaten test edildi.
3. Yeni bir iddiayı kendin test edeceksen `arastirma/` altındaki benzer bir scripti kopyala. Kalıp hep aynı: kural → aynı dönem ve yönde rastgele kıyas → zaman bölmesi → maliyet. Test hatalarına karşı hafıza notlarındaki uyarıları uygula: gün içi giriş + kapanış filtresi = ileriye bakma, giriş günü stopu = gün dibi tuzağı.
4. Replay uygulamanı 13 §5'teki 15 madde üzerine kur: avantajı ilk orada, para riske etmeden ölçeceksin.
