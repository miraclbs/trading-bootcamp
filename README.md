# Trading Bootcamp — Doğrulanmış Bilgi Tabanı

Video, kitap yazarlarının kendi siteleri ve akademik çalışmalardan toplanmış, **çapraz kontrol edilmiş ve gerektiğinde simülasyonla doğrulanmış** trading bilgisi. Yanlış/kanıtsız bilgiler ayrı bir kara listede tutulur.

Başlangıç: 2026-11-22. **Otonom öğrenme döngüsü 59. turda tamamlandı.** 73 doğrulanmış gerçek, 88 efsane, 77 doğrulama scripti var.

**Buradan başla**: [bilgi/15-prop-yol-haritasi.md](bilgi/15-prop-yol-haritasi.md), tüm bulguların FTMO odaklı karar listesi. Yan iş: son yarım saat dönüşünün önceden kayıtlı ileri testi (ara kontroller ~2027 Şubat ve Kasım, nihai karar ~2028 sonu, #32). Ana iş: kendi setup'ını replay'de ölçmek (15 §1).

## Klasör yapısı

```
bilgi/                    ← konu bazlı bilgi dosyaları (asıl içerik)
kaynaklar/                ← kanal/kaynak değerlendirmeleri, bekleyen izleme listesi
arastirma/                ← doğrulama simülasyonları + sonuçları
  araclar/                ← YouTube transkript/altyazı çekme scriptleri
```

## Bilgi dosyaları (önerilen okuma sırası)

| # | Dosya | İçerik | Güven |
|---|---|---|---|
| 01 | [Matematik: beklenen değer](bilgi/01-matematik-beklenen-deger.md) | EV, başa baş WR, örneklem, kayıp serileri, Kelly | Yüksek ✔ simüle |
| 02 | [Risk ve pozisyon boyutu](bilgi/02-risk-pozisyon-boyutu.md) | Lot hesabı, risk seviyeleri, düşüş olasılıkları, kaldıraç | Yüksek ✔ simüle |
| 03 | [İşlem planı](bilgi/03-islem-plani.md) | 4 soru, işlem yapmama koşulları, şablon | Yüksek |
| 04 | [Piyasa yapısı ve price action](bilgi/04-piyasa-yapisi-ve-price-action.md) | Brooks, Grimes şablonları, BOS/CHoCH, H2/L2, wedge | Orta-yüksek |
| 05 | [Likidite, sweep, tuzaklar](bilgi/05-likidite-sweep-ve-tuzaklar.md) | Failure test, spring/UT, SFP, stop pocket, test edilebilir sweep tanımı | Orta-yüksek |
| 06 | [Hacim: VSA / Wyckoff / profil](bilgi/06-hacim-vsa-wyckoff-profil.md) | Wyckoff yasaları ve şemaları, VSA, POC/VA, veri uyarıları | Orta |
| 07 | [Çoklu zaman dilimi](bilgi/07-coklu-zaman-dilimi.md) | Top-down, kombinasyonlar | Orta-yüksek |
| 08 | [Psikoloji ve davranışsal finans](bilgi/08-psikoloji-ve-davranissal-finans.md) | Akademik veriler, 5 fark, Mark Douglas | Yüksek |
| 09 | [Prop firm / FTMO](bilgi/09-prop-firm-ftmo.md) | Challenge geçme simülasyonu, risk kuralları | Yüksek ✔ simüle |
| 10 | [Backtest ve istatistik](bilgi/10-backtest-ve-istatistik.md) | Grimes testleri, protokol, journal alanları | Yüksek |
| 11 | [Yanlış bilgiler ve efsaneler](bilgi/11-yanlis-bilgiler-ve-efsaneler.md) | Kara liste + kırmızı bayrak kontrol listesi | — |
| 12 | [Strateji haritası](bilgi/12-strateji-haritasi.md) | 13 yaklaşım ve zayıf yanları | Yüksek |
| 13 | [Pratik rutini](bilgi/13-pratik-rutini.md) | Brooks gün sonu işaretleme, Douglas 20 işlem egzersizi, Brandt taraması, Beggs süreci, **replay uygulaması için çıkarımlar** | Yüksek |
| 14 | [Gerçekçi beklentiler](bilgi/14-gercekci-beklentiler.md) | Süre (3-6 yıl), başarı kademeleri, sermaye, sihirli para deneyi, avantajın doğası | Yüksek |
| 15 | [**Prop yol haritası (sentez)**](bilgi/15-prop-yol-haritasi.md) | 58 turun bulgularından FTMO karar listesi: avantajı kanıtlama ölçütü, hesap seçimi, challenge ve fonlu hesap ayarları, süreç, karar akışı, bilgi tabanını kullanma rehberi | Diğer dosyalara bağlı |
| 16 | [Kanıtlı trader'lar](bilgi/16-kanitli-traderlar.md) | Kaydı doğrulanmış trader'lar: başlangıç, yöntem, batışlar; perakende taban oranları (Tayvan, Brezilya, Hindistan); hayatta kalma yanlılığı | Yüksek (kaynaklı, 2026-11-25) |
| 17 | [Kanıtlı stratejiler](bilgi/17-kanitli-stratejiler.md) | Akademik literatür: yayın sonrası erime, trend takibi, faktörler, takvim ve gün içi etkiler, teknik analiz, kripto; Sharpe → FTMO geçme çevirisi, uygunluk tablosu | Yüksek (kaynaklı, 2026-11-25) |
| 18 | [Servet ve yatırım](bilgi/18-servet-ve-yatirim.md) | Bileşik getiri tabloları (ayda 300 $), tasarruf oranı ve süre, aktif ve pasif, servetin kaynakları, Türkiye koşulları, iş + yatırım + sınırlı trading planı | Yüksek (kaynaklı, 2026-11-25) |
| 19 | [Kitaplar ve hatalar](bilgi/19-kitaplar-ve-hatalar.md) | 12 kitabın pratik dersleri ve kanıt kontrolü, okuma sırası, batış vakaları (Livermore, LTCM, Niederhoffer, Amaranth, Archegos) | Orta-yüksek (kaynaklı, 2026-11-25) |
| 20 | [Yatırımcı röportajları (sentez)](bilgi/20-yatirimci-roportajlari.md) | Druckenmiller, Tudor Jones, Dalio, Munger, Marks, Lynch, Thorp, Simons, Bogle: dokuz uzun röportajın ortak dersleri, perakendeye taşınmayanlar, 6 kural. Ayrıntı `kaynaklar/roportajlar/` | Orta-yüksek (2026-11-25) |
| 21 | [Türkiye'den endeks yatırımı](bilgi/21-turkiyeden-endeks-yatirimi.md) | Acil fon, BES/OKS, İrlanda ve ABD merkezli endeks ETF'leri, TEFAS yabancı hisse fonları, altın; vergi, komisyon ve kur maliyeti; SPK, YTM; ilk 30 gün listesi | Orta (kurallar değişken, ◐ çok; 2026-11-26) |

Kaynak kararları: [kaynaklar/kanal-degerlendirmeleri.md](kaynaklar/kanal-degerlendirmeleri.md)

## En önemli doğrulanmış gerçekler

1. **Kazanma oranı da RR de tek başına bir şey söylemez**; EV = WR×kazanç − (1−WR)×kayıp. Başa baş WR = 1/(1+RR), maliyetler hariç.
2. Kârlı bir sistem (WR %40, 2R) **20 işlemde %25 ihtimalle zararda** biter, 100 işlemde %9. Sistemi 100+ işlemden önce yargılama.
3. %40 WR ile 100 işlemde **7'li kayıp serisi ihtimali ~%70**, yani normal bir durum.
4. Risk/işlem %1'de medyan maksimum düşüş ~%15. %5'te %50 düşüş ihtimali ~%85. **%0.5-1 risk** makul aralık.
5. FTMO tipi challenge'ı **avantajı sıfır olan biri bile ~%45 ihtimalle geçer**. Geçmek kanıt değildir. %3+ risk ile günde 2 işlem günlük limiti patlatır.
6. Day trader'ların **%97'si (Brezilya) / %99+'ı (Tayvan)** uzun vadede kaybediyor. En çok işlem yapanlar en az kazanıyor.
7. İnsanlar kârı erken realize edip (%14.8) zararı taşıyor (%9.8). **Stop asla zarar yönünde taşınmaz.**
8. Sweep, spring, failure test ve SFP aynı fenomen: görünür seviyelerdeki stop kümeleri. Mekanizma gerçek, ama kesin olasılıklar (Brooks'un %80'i dahil) kişisel pratik kural. **Kendi piyasanda test et.**
9. **Fibonacci oranlarının anlamlı olduğuna dair kanıt yok** (Grimes, 10 yıl, 622 enstrüman).
10. Forex/CFD'de hacim = tick volume. VSA/Wyckoff okumaları yanıltabilir. Gerçek hacim için futures verisi kullan.
11. **Gerçekçi süre 3-6 yıl** (Grimes, Beggs). İlk başarı kâr etmek değil, **işlemlerde zarar etmeyi bırakmak**. Başarısızlığın bir numaralı sebebi yanlış beklentiler.
12. **Scalp matematiği acımasız**: tipik scalp'ta risk ödülün 2 katı → %70+ WR gerekir. Yeni başlayan swing yapmalı ve stop emirle girmeli (Brooks).
13. **Replay'de bitmiş bar yanıltır**: canlıda sinyal barlarının çoğu son saniyede şekillenir. Replay bar içi oluşumu göstermeli (Brooks, 13 §5).
14. **Prop challenge iki sınırlı bir problem**: avantaj yoksa geçme ihtimali ≈ zarar sınırı / (zarar sınırı + hedef), 50k futures'ta ~%40, risk ne olursa olsun. Aynı EV'de **düşük varyanslı** strateji daha sık geçer. Trailing drawdown geçme oranını 10-20 puan düşürür (09 §1b).
15. **Fonlu aşama dahil optimal risk %1-2** (ayda ~10 işlemde). ≤%0,5 çok yavaş. %3 sadece günde ≤1 işlemde işe yarar, günde 2 işlemde %5 günlük limit yüzünden çöker (09 §1d).
16. **Düşüşte riski kurala bağlı azalt**: "≥4 ardışık kayıpta riski yarıya indir, başa başta geri yükle" gibi önceden yazılmış bir kural, avantajı olan stratejide challenge kaybetme ihtimalini yarıya indiriyor. Avantaj yoksa hiçbir boyutlandırma kuralı işe yaramaz (09 §1f).
17. **Bir strateji ne zaman bırakılır?** Durma kriteri canlıya geçmeden önce yazılır: Monte Carlo maksimum DD eşiği (işlem sayısına bağlı eğri). 30 işlemlik sapma genelde "henüz erken" (10 §6e).
18. **Günün uç noktası erken oluşur** (Brooks, gerçek veriyle test edildi): SPY, QQQ ve IWM'de ilk 18 barda (~90 dk) günün tepesi ya da dibi %85-88 oranında oluşmuş. Rastgele yürüyüşte bu oran %64. 18 barlık aralık kırılınca karşı uç %83-86 korunuyor. Örneklem 59 gün, orta güven (04 §6b-2).
19. **⚠️ Filtresiz sweep avantaj değil** (gerçek veriyle test edildi): SPY, QQQ ve IWM'de 2 yılda ~1.260 sinyal. "Önceki günün tepe/dibini süpür, içeride kapan, ters gir" sonucu rastgele yürüyüşten ayırt edilemiyor, maliyet eklenince negatif. Brooks'un ikinci giriş varyantı da ~0. Filtrelerle de pozitif avantaj çıkmadı, ama **sığ delme (<0,1 ATR) ve zayıf sinyal barı tutarlı şekilde kaybettiriyor** (-0,14R ve -0,09R, verinin iki yarısında da) → bu iki koşulda sweep alma (05 §8b).
20. **Seviye kendi başına sihirli değil** (Grimes'ın testi, gerçek veriyle tekrarlandı): PDH/PDL'ye ilk dokunuşta dönüş oranı %43,7, aynı uzaklıktaki rastgele seviyelerde %44,6. Kendi seviye tipini rastgele seviyelere karşı test etmeden ona güvenme (05 §8b).
21. **VSA tek bar okumaları ve hacim profili seviyeleri test edildi, sağlam bir avantaj bulunmadı** (1 saatlik, 2 yıl, endeks ETF'leri). "Durdurucu hacim" barı koşulsuz getiriyle aynı. "Zayıflık" barını ortalamada yükseliş izledi ama sadece bir rejimde. POC rastgele seviyelerden farksız. Hacim sinyalini önce koşulsuz getiri, verinin iki yarısı ve sembole göre ayrımla test et (06 §8b). **Arka planlı satış klimaksı** (9 ETF, günlük, 2005+): 5 günde kısa bir sıçrama var (+0,45 ATR'ye karşı koşulsuz +0,14, Wyckoff'un otomatik rallisi). Ama 10-20 günde avantaj kayboluyor (ikincil test). Klimaks hemen dönüş demek değil, teyit bekle. **Klimaks barını almak tutarlı şekilde kötü** (27 ETF: -0,09R'ye karşı rastgele düşüş günü +0,17R, t = -5). **"Düşük hacimli ikincil testte al" kuralı ise rastgele girişten farksız** (+0,16R'ye karşı +0,17R). Düşük hacim şartı katkı sağlamıyor, yüksek hacimli geri testler de aynı. İlk 9 sembolde görünen avantaj yeni 18 sembolde tekrarlanmadı (06 §8b-D2). **Ders: her bulguyu başka sembollerde tekrarla.**
22. **Piyasalar farklı, aynı araç her yerde çalışmaz** (Grimes, gerçek veriyle test edildi). 20 günlük kırılım sistemi hisselerde ~0 ve al-tut'un gerisinde. Emtiada 2005-14'te kazandırmış, 2015 sonrasında değil. Dövizde negatif. Her stratejiyi piyasa piyasa ve **al-tut temel çizgisine karşı** test et (12).
23. **Öznel formasyon becerisini replay ile doğrula** (Grimes): geçmiş grafikte, sonrasını görerek bulduğun avantaj, **farklı bir veri setinde** bar bar ilerleyip sağ kenarda yaptığın işaretlerle aynı çıkmalı. Sonra parasız ileri test, sonra çok küçük boyut. **Boyutu kâra göre değil kurala uyuma göre büyüt** (13 §5, 14 §3f).
24. **⚠️ (36. turda zayıflatıldı) Endekslerde momentum sonrası ilk pullback: 2005-14 avantajı, 2015 sonrası rastgele girişten ayırt edilemiyor (+0,06R, se 0,06; 04 §5b)** (Grimes'ın şablonu, günlük, 2005+). Güçlü itişten sonra EMA20'ye ilk geri çekilmede trend yönünde gir. Stop 1 ATR, hedef 2R. Rastgele trend girişine göre fark: endeks ETF'lerinde +0,11R, hiç görülmemiş 12 ülke ETF'inde +0,06R, iki dönemde de pozitif. ~~Neredeyse tamamı long tarafında~~: yön eşleştirilmiş temel çizgiyle bu bir ölçüm hatası çıktı. Avantaj çoğunlukla 2005-09 kaynaklı. Ülke ETF'leri korelasyonlu olduğu için gerçek örneklem dışı test sayılmaz (Grimes). Emtiada çalışmıyor, orada pullback beklemek zarar. Momentum gününde kovalamak negatif. Pullback "karakteri" filtreleri (derinlik, sessizlik, itiş gücü) sağlam bir katkı sağlamadı (04 §5b).
25. **"Bedava işlem" yoktur** (Dante + simülasyon): avantaj yoksa başa baş stopu beklentiyi değiştirmez. Avantaj varsa +0,5R'de başa baş işlem başı beklentiyi ~%40 düşürür. **Boyut değişkenliği tek başına beklentinin işaretini değiştirmez.** Pozitif sistemi zarara çeviren, büyük boyutla alınan düşük kaliteli intikam ve sezgi işlemleridir (lot başı +0,15R → +0,01R) (02 §4b-c).
26. **Prop tamponu en az 10R olmalı**: %55 isabetle 100 işlemde 5'li kayıp serisi ihtimali %65, 10'lu seri ihtimali %2. "5 işlem payı" bırakan trader büyük ihtimalle hesabı patlatır. Kopya işlem çeşitlendirme değildir, tek bahsi N ile çarpar. Önce tek hesapla bir ödeme al, sonra büyüt. Büyük kayıpların çoğu **sıcak bir seriden hemen sonra** gelir (09 §4g).
27. **Trend yapan piyasada avantaj çıkıştan gelir, girişten değil** (Brandt, gerçek veriyle test edildi). Emtiada 3 günlük trailing stop ya da 10 günlük dip stopu, sabit 2R hedefe göre sonucu 3-4 katına çıkarıyor. **Rastgele yönlü girişler** kırılım girişleri kadar iyi. Hisse endekslerinde tersi: trailing stop zarar, sabit hedef daha iyi. "Kârı koştur" piyasaya bağlı (03).
28. **Gün içinde maliyet avantajı yer**: aynı pullback kuralının maliyeti günlükte ~0,01R, 1 saatlik FX'te ~0,10R. Günlük grafikteki pullback avantajı 1 saatlikte anlamlı değil (04 §5b). Kayıplar bağımsız değil, **rejimler halinde kümelenir**. Brandt'ın 2022'deki "20 işlemde 19 kayıp" serisi, bağımsız işlem varsayımında %0,4-2 ihtimalli bir olay. Kayıp serisi tablolarını alt sınır say (14 §3d).
29. **Mum formasyonlarının "%70-84 isabeti" büyük ölçüde geometri** (gerçek veriyle test edildi). Bulkowski'nin oranı "önce hangi yöne kırıldı" sorusunun cevabı, kâr oranı değil. Kapanış formasyonun ucunda olduğu için, aynı konumdaki rastgele günler de %63-79 aynı yöne kırılıyor. Beş formasyondan sadece three black crows küçük bir fark gösterdi (+5 puan), ama 10 günlük etkisi yeni 40 sembolde tekrarlanmadı. **Her "kırılım yönü" istatistiğini kapanış konumu eşleştirilmiş temel çizgiyle kontrol et** (10 §7b). Emtiada trailing çıkışın üstünlüğü 5 tohumla tekrarlandı: ETF'lerde 12/12 sembol, futures'ta 9/12. Ama etki +0,03 ile +0,06R, ilk testteki +0,11R'den küçük (03).
30. **⚠️ İşlem başı avantaj ≠ ticari avantaj** (portföy simülasyonu, 2005-2026). Endeks pullback'i işlem başına +0,18R veriyor. Ama 20 endeks aynı günlerde sinyal verdiği için risk sınırıyla sinyallerin %46'sı atlanıyor. Sınır olmadan maksimum düşüş %57. Portföy %1 riskte yıllık **%3,3** getiriyor, **SPY al-tut ise %10,3**. FTMO tipi challenge'da geçme oranı %48, avantajı olmayan referansla (~%50) aynı. **Prop için gerekli: işlem başı R × yıllık bağımsız işlem sayısı ≥ 10-15R** (%10 hedef / %1 risk). Bir setup'ı dört şeyle birlikte değerlendir: işlem başı R, sıklık, korelasyon ve al-tut alternatifi (04 §5b, 09 §2).
31. **Brooks'un açılış istatistiklerinin bir kısmı tutuyor, bir kısmı tutmuyor** (1 saatlik ve günlük veriyle test edildi). "Günün ucu erken oluşur" doğru. Ama açılış aralığı kırılımı maliyetli olarak rastgele girişten farksız. "Atalet" (4 boğa gününden sonra yine boğa günü) yok, hafif tersi var. Gün ortası rallileri açılışa %60-70 değil, **%4-25** oranında dönüyor, rastgele yürüyüşten de az. Gün ortası hareketleri **devam etme** eğiliminde (gün içi momentum literatürü). "Gün ortası rallisini sat" fikrine güvenme (04 §6b-3).
32. **🧪 Hipotez (ileri test bekliyor): son yarım saatte dönüş.** Akademik gün içi momentum (ilk yarım saat → son yarım saat, Gao vd. 2018) son 2 yılın 1 saatlik verisinde tekrarlanmadı. Onun yerine **son yarım saatte günün yönü tersine dönüyor**. SPY'da 15:30'da günün yönüne karşı girmek net +1,8 bp/gün, Sharpe 1,3, iki yarıda da tutarlı. Bu kâğıt üzerinde ~20R/yıl eder, prop ölçütünü geçen ilk aday. **Ama** sonradan bulundu (çoklu test), sadece 2 yıl veri var, ve mekanizma (dealer gamma korunması, Baltussen vd. 2021) rejime bağlı. QQQ ve IWM'de son yıl zayıflamış. **İlk sağlamlık kontrolünde başarısız**: futures'ta son saat versiyonu Sharpe -0,05 ile -0,65 arası. Öncelik düşürüldü (04 §6b-4). **58. tur**: SPY'da VIX'in üç diliminde de pozitif, ama QQQ ve IWM'de mekanizmanın öngördüğü düşük VIX'te değil, yüksek VIX'te yoğun. **Önceden kayıtlı ileri test** 2026-11-23'te başladı (`arastirma/verify_close_reversal_forward.py`). Etki gürültüye göre çok küçük, 60 günde gerçek bir etki bile ancak %36 olasılıkla görünür. Bu yüzden 60. ve 250. günde sadece ara kontrol yapılacak (t ≤ -1 ise bırak), nihai karar 500. günde (~2028 sonu).
33. **Sektör verisi, ortalama challenge adayının rastgeleden kötü işlem yaptığını gösteriyor.** FPFX anketi (10 firma, ~300 bin hesap): %14 geçiyor, %7 ödeme alıyor, ortalama ödeme hesabın %4'ü, fonlu hesapta ortalama ömür 22 gün. Kalibrasyon: avantajı olmayan biri iki aşamayı %32 geçerdi. %12-14, işlem başına **~-0,1R** beklentiye denk geliyor, yani gün içi maliyet ve aşırı işlem seviyesi. Kalıcı ödeme alanlar: aşırı kaldıraç ve aşırı işlem yok, çoğunlukla 1-3 günlük swing, ayda %3-4. En büyük ödemeler şanslı kumarcılardan geliyor. Risk artırmak sadece negatif beklentide geçme şansını artırır (09 §4h).
34. **Yayından sonra da çalışan iki swing etkisi var, ama ikisi de prop aracı değil** (RSI-2 37. turda zaman testinden de geçti, #46) (gerçek veriyle test edildi, 2009+):
    - **Connors RSI-2** (yükselen endekste kısa vadeli aşırı satımı al): işlem başına +0,33R stopsuz, isabet %72, 8 endeksin 8'inde pozitif. Ama sinyaller kümeleniyor. Portföy %1 riskte yıllık %2,9, SPY al-tut %14,3. Challenge %11.
    - **Gece etkisi**: endeks getirisinin büyük kısmı gece oluşuyor, SPY 2018+ gece Sharpe 0,61, gün içi 0,15. Ama çoğu futures prop firması gece pozisyonu yasaklıyor, CFD'de swap avantajı yiyor.
    - **Stop**, ortalamaya dönüş beklentisini ~1/3 düşürüyor (Connors: "stoplar test sonucunu kötüleştirir").
    - **Genel ders**: Prop için ~10-15R/yıl, ya birbiriyle ilişkisiz çok sayıda piyasa ya da düşük maliyetli yüksek sıklık ister. Henüz bulunmadı (12).
35. **✔ İlk olumlu prop tablosu: çok piyasalı, düşük riskli swing portföyü, ama yavaş** (2009+, maliyetli simülasyon).
    - **Kurulum**: SPY/QQQ'da RSI-2 long ve 8 emtia ETF'inde 20 günlük kırılım + Brandt 3 günlük trailing. Kollar arası korelasyon düşük.
    - **Sonuç**: %0,5 riskte iki aşamalı challenge'ı **%93 geçiyor, %7 kalıyor**, ama medyan **~2 yıl** sürüyor. %0,75 riskte %69 / %31, ~14 ay. Fonlu aşamada beklenti yıllık %5-7.
    - **R/yıl tek başına yetmez.** Emtia kolu yılda ~14R üretiyor, ama %1 riskte %33 düşüşle %10 sınırını deliyor. Ölçü **getiri / maksimum düşüş**.
    - **Negatif beklentili kol eklemek zarar** (dört kol birlikte %1 riskte %80 kalıyor).
    - ⚠️ Kollar sonuçları gördükten sonra seçildi (seçim yanlılığı). Futures prop firmalarının çoğu gece pozisyonu yasaklıyor, CFD'de swap maliyeti testte yok. Kendi firmanın ürün listesiyle yeniden test et (09 §2 madde 7).
36. **✔ Clenow'un kıyas modeli doğrulandı: çeşitlendirilmiş 12 aylık momentum** (19 ETF ve parite, 2005+, maliyetli).
    - **Kural**: "fiyat bir yıl öncekinden yüksekse long, değilse short", volatiliteye göre boyut, taban volatilite %5.
    - **Sonuç**: Sharpe 0,55, 2015 sonrasında 0,61. Maksimum düşüş %8, SPY ile korelasyon ~0.
    - **Kısa geriye bakış artık çalışmıyor** (Parker): 1 aylık kuralın Sharpe'ı 2015 sonrasında -0,12.
    - **Prop**: yıllık %6 volatiliteyle iki aşamalı challenge %70 geçiyor, %4 kalıyor, ~2,4 yıl sürüyor.
    - **Clenow**: "Karmaşıklık ancak karşılığı çok iyi ödeniyorsa eklenir. Yıllık %10-15 çok iyidir." **Parker**: "Sistemine uy ve küçük işlem yap." (12)
37. **İlişkisiz iki avantajı birleştir: 12 ay momentumu + SPY al-tut (risk ağırlığı %50/%50).**
    - **Sonuç**: Sharpe 0,82 (2015+ 0,95), maksimum düşüş %13. Tek başlarına 0,55 ve 0,60 idi.
    - **Prop testi**: yıllık %8 volatiliteyle iki aşamalı challenge **%89 geçiyor, %11 kalıyor**, ~1,5 yıl.
    - **⚠️ CFD maliyeti**: SPY long'unda gecelik finansman ~faiz + %2-3, bacak getirisinin yarısından fazlası gider.
    - **⚠️ FTMO kuralı**: Standart fonlu hesapta hafta sonu pozisyon taşımak yasak. 2 saatten uzun kapanışlarda düz olmak gerekiyor. Haftalarca pozisyon taşıyan stratejiler **Swing hesap tipi** ister. Değerlendirmede kısıt yok (09 §4i, 12).
38. **Rob Carver'ın ilkeleri, iki tanesi veriyle doğrulandı** (10 §6j).
    - **Çeşitlendirme doğrulandı**: tek piyasanın ortalama Sharpe'ı 0,20, 19 piyasalık portföyünki 0,55, yani 2,7 kat.
    - **"Piyasa seçme" doğrulandı**: piyasalar arasındaki Sharpe farkları gürültü kadar (dağılım 0,22, standart hata ~0,21).
    - **Kurcalama**: "8 yıldır parametre değiştirmedim. Sistematik olup sistemi kurcalamak iki dünyanın en kötüsü."
    - **Düşüşte**: backtest maksimumunu aşmadıkça müdahale etme.
    - **Fikir testi**: "Karşı tarafta kim kaybediyor?" Açıklanamayan anomaliye dokunma.
    - **Yeni başlayan**: sistematik başla ("yardımcı tekerlek"). Takdirli tahmini sistematik bir risk motoruna besle.
39. **Açık pozisyonun boyutu da güncel volatiliteye göre yeniden ayarlanmalı** (Carver, 02 §6b-3, 09 §4i, 10 §6j).
    - **Test**: 12 ay momentumunda lotu girişte sabitlemek yerine ayda bir yeniden boyutlamak Sharpe'ı 0,45'ten 0,56'ya çıkarıyor. Aynı volatilitede en kötü günü −%7,1'den −%3,8'e indiriyor. Prop'ta bu, %5 günlük limitin tek günde aşılıp aşılmaması demek.
    - **Gümüş, 30 Ocak 2026 (−%31)**: sabit lotlu versiyon ayın tüm kârını tek günde verdi. Volatiliteye göre ayarlanan versiyon −27 baz puanla atlattı. Günlük ayarın aylığa ek faydası yok.
    - **Öngörülebilirlik**: volatilite öngörülebilir (R² 0,35), korelasyon daha az (0,23), getiri değil (0,008). Yani boyut volatiliteye göre belirlenir, setup'ın "güzelliğine" göre değil.
    - **FTMO günlük limiti** = gece yarısı bakiyesi − %5. Equity sayılır. Gece taşınan açık zarar o günün payını baştan yer.
40. **Firma verisindeki "geçen trader profili" büyük ölçüde şanstır** (09 §4j, 04 §6b-5, 11 #61-63).
    - **Simülasyon**: kimsenin avantajı olmayan 40.000 trader'da geçenlerin isabeti %65 ve işlem başına +0,87R, kalanlarınki %21 ve -0,51R. %20'si becerikli olsa bile geçenlerin ~%60'ı şanslı.
    - **Kontrol edebildiğin kollar**: risk boyutu (avantajın varsa düşük: %0,5 riskte %93, %4 riskte %51 geçiyor), işlem sıklığı, stop mesafesine göre lot, her işlemde stop.
    - **"Asya'nın iki ucu %80 süpürülür" yanlış**: GBPUSD'de %44, rastgele modelde %47. Süpürmeden sonra dönüş ve "ilk saat tuzağı" da rastgeleden farksız.
    - **"20-30 işlem yeter" yanlış**: +0,2R avantajla 30 işlemlik dilimlerin %28'i zararda biter.
41. **Trend kuralının türü değil hızı önemli; backtest'teki maksimum düşüş tek bir çekiliştir** (Carver, 10 §6k, 12, 11 #66).
    - **Trend kuralları**: aynı hızdaki EMA kesişimi, N günlük getiri ve Donchian kuralları neredeyse aynı (korelasyon 0,8-0,9). ~1 aylık ve daha hızlı kurallar maliyetten sonra ≤0.
    - **Maksimum düşüş**: %8 volatilitedeki trend stratejisinde 1 yıllık medyan %7, 2 yıllık 95. yüzdelik %19. %10 limiti 1 yılda %25, 2 yılda %49 olasılıkla aşılıyor. Prop'ta hesap ömrü boyunca bootstrap edilmiş dağılıma bak.
    - **Firma verileri (Phidias, PipBack, FPFX) aynı yönde**: swing işlem, statik limit, acele etmemek ve küçük zarar daha başarılı. "Yüksek isabet daha iyi" ve "günlük limit tuzaktır" çıkarımları yanlış.
42. **Prop'ta en büyük kol hesap tipi; erken ödeme beklenen değeri değil güvenceyi artırır** (09 §4l, 11 #67).
    - **Hesap tipi**: aynı büyüklükte trailing limit ve çekilemez tampon, beklenen ödemeyi yarıya indiriyor. Tipik %5'lik futures tamponu bir yarıya daha indiriyor. Firma seçerken ilk kriter statik limit ve çekilebilir kâr.
    - **Erken küçük ödeme**: en az bir ödeme alma olasılığını artırıyor (%58'den %75'e), beklenen toplamı neredeyse hiç değiştirmiyor (opsiyonel durma teoremi: avantaj yokken toplam ≈ kâr payı × tampon).
    - **"Kârlı olmasan da kazanırsın" yarı doğru**: statik limitli firmada sıfır avantajla modelde pozitif, gerçekçi -0,10R'de ~0, trailing hesapta negatif.
    - **FTMO geçme oranı yayımlamıyor**. Müşteri başına ~144 $ ödeme ediyor, 100K ücreti 540 $.
43. **Risk ayarı avantaj yaratmaz; düşük risk sadece avantajı olana yarar** (09 §4m, 10 §6l, 11 #68).
    - **Geçme oranı (RR 2)**:
      - +0,2R avantajda %2 riskle %55, %0,5'le %96.
      - Avantaj yokken her riskte ~%30.
      - -0,10R'de riski düşürmek geçme oranını %17'den %3'e indiriyor.
    - **Challenge'da %2-3 risk** zaman açısından daha iyi (günde ≤1 işlemle). **Fonlu hesapta** modelde yüksek risk daha çok kazandırıyor, çünkü getiri opsiyon gibi. Ama yasaklar, tutarlılık kuralı, ölçeklendirme ve tilt model dışında. Pratik denge: kanıtlı avantajla challenge'da %1-2, fonlu hesapta ~%1.
    - **Grimes**: rastgele veride de görülen bir istatistik geçersizdir. Rastgele piyasada stop ve hedef beklentiyi sıfırdan kurtaramaz. Replay uygulamasına "kör rastgele grafik" modu eklenebilir (13 §5 madde 12).
44. **Fonlu hesapta avantajı olan trader için en değerli şey hesabın ömrü** (09 §4n, 11 #69-70).
    - **Avantaj yokken**: tek bir fonlu hesabın değeri ≈ kâr payı × tampon (~8.000 $), risk, ödeme eşiği ve ölçeklendirme ne olursa olsun.
    - **Avantaj varsa**: tüm kârı her seferinde çekmek tamponu %10'da tutar ve hesap avantaja rağmen eninde sonunda kaybedilir. Düşük risk (%0,5) ya da %5-10'luk kâr tamponu bırakmak 3 yıllık ödemeleri ~2 katına çıkarıyor.
    - **FTMO ölçeklendirme planı** (4 ayda %10 kâr ve 2 ödeme → hesap +%25, kâr payı %90): sadece güçlü avantaj ve düşük riskle anlamlı, +0,2R'de %0,5 riskle ödemeler +%32.
    - **"Yüksek risk, hesabı yak, yenisini al" döngüsü** modelde kârlı görünse de FTMO'da "hesap döndürme" olarak yasak.
    - **Grimes**: farklı ticker örneklem dışı test sayılmaz. Bu bilgi tabanının endeks pullback avantajı bu yüzden zayıflatıldı (2015 sonrası küçülüyor).
45. **Kendi bulgularımızı zamana karşı test et: endeks pullback avantajı 2015 sonrası kayboldu** (04 §5b, 03, 11 #71).
    - **Yön ve dönem eşleştirilmiş rastgele girişe göre**: 2005-09 +0,26R, 2015+ +0,06R (se 0,06). Ülke ETF'lerinde 2015+ +0,03, hisselerde +0,02. Yani bugün için kanıtlanmış bir avantaj değil.
    - **"Avantaj long tarafında" ölçüm hatasıydı**: mutlak R'ye bakılmıştı. Long'ların temel çizgisi de yukarı eğilim yüzünden yüksek.
    - **Grimes'ın 1:1 testi**: RR ve isabet iç içe (0,5R'de %66, 1R'de %56, 2R'de %41). Hisselerde 1:1'in "boş olasılığı" ~%53. "1R en iyisi" mekanik versiyonda desteklenmedi: 2R daha iyi, 1R sadece trailing'den daha düzgün.
46. **Zaman testinden geçen işlem başı avantajlar: endekste RSI-2 ve emtiada trailing çıkış** (12, 03, 04 §6b-6, 11 #72-73).
    - **RSI-2**: aynı dönemdeki rastgele girişe göre fark 2015 sonrası +0,17R (se 0,04), 2020 sonrası +0,23R. Dört dönemin dördünde pozitif.
    - **Emtiada trailing**: 2015 sonrası da sabit hedeften ~+0,07R iyi.
    - Pullback ise geçemedi (#45). Ama iki avantaj da portföy düzeyinde prop için tek başına yetersiz (#34, #35).
    - **Brooks'un "her gün EMA'ya dokunur" iddiası doğru**, ama rastgele yürüyüşte de öyle, yani bir avantaj değil. "%80 tepe testi" %38 çıktı.
    - **Zarardaki işleme ekleme Martingale'dir**, prop'ta kullanılmaz.
47. **Ortalama prop challenge'ı maliyet ödeyen avantajsız bir strateji gibi sonuçlanıyor** (09 §4o, 11 #74).
    - **Topstep 2025 resmi verisi**: combine başına %16,8 geçme, kişilerin %51,8'i (çok denemeyle) fonlanıyor, fonlananların %33,3'ü ödeme alıyor, %0,71'i Live hesaba geçiyor.
    - **Koridor formülü**: avantaj yokken geçme olasılığı = maksimum zarar / (hedef + maksimum zarar). 50K'da 2.000 / 5.000 = %40. Gün sonu trailing bunu %29'a, maliyet %20'ye indiriyor. Topstep'in gerçeği %16,8.
    - **Dar hedefli, yüksek isabetli scalping maliyet yüzünden çöküyor**: 0,25R hedefte %5, 4R'de %27.
    - **Küçük bir gerçek avantaj** (+0,06R) geçme oranını %20'den %38'e çıkarıyor. Yapı avantajı yaratmaz, büyütür.
    - **İşlem sırasını karıştıran Monte Carlo** rejim testi yapmaz, sadece seri riskini gösterir.
48. **FTMO 1 aşamalı hesap: benzer geçme oranı, 2 kat hız, ama %3 günlük limit acımasız** (09 §4p, §4q).
    - **Geçme**: 1 aşamalı (tek hedef %10, gün sonu trailing ve hiç düşmeyen %10 limit) ile 2 aşamalı benzer. Avantaj yokken %38'e karşı %31-34, +0,1R ve %1 riskle ~%60. 1 aşamalı yarı sürede geçiliyor.
    - **Günlük limit tuzağı**: günde 2 işlem ve %1,5 riskle iki kayıp günlük limiti dolduruyor, +0,2R avantajla bile geçme %13'e düşüyor. Kural: işlem başına risk × günlük en fazla işlem sayısı < %3.
    - **Uzun fonlu kariyer için**: statik limit, iade edilen ücret ve ölçeklendirme yüzünden 2 aşamalı daha uygun.
    - **JadeCap (4,5 milyon $ ödeme)**: prop'a ~10 yıl deneyimle girmiş, firmalar arasında çeşitlendirmiş, hesap başına riski %0,25-0,5'e indirmiş, haftada 2-3 işlem yapıyor. "Prop kuralları disiplin öğretti."
49. **Haftalık inceleme ve "gün açılışı testi" geometrisi** (13 §3c, 09 §4p, 11 #75).
    - **Dante'nin icra ilkeleri**: yüksek olasılık yoksa elini otur, sırası gelince tereddütsüz gir, P&L'yi değil piyasayı işle, her hafta bir şey öğren.
    - **Haftalık rutin**: Cumartesi inceleme, Pazar plan. İncelemede "yönetmeseydim ne olurdu?" ve "kendini işe alır mıydın?" (Beggs) soruları.
    - **"Pazartesi açılışı test edilir" testi**: oran yüksek (%64-83), ama her günün açılışı için öyle (%66-80). Pazartesi'ye özgü fazlalık geleneksel piyasalarda küçük (+2 ile +5 puan), Bitcoin'de yok.
    - **FTMO 1 aşamalı**: ödemeden sonra maksimum zarar limiti sıfırlanıyor (resmi sayfa), yani ödeme tamponu yemiyor.
50. **Açık artırma ve değer alanı kuralları da rastgele kıyas testinden geçemiyor** (06 §8b-2, 11 #47, #76).
    - **Market Profile "%80 kuralı"** (VA dışında açılış, sonra 2 periyot içeride kalma → karşı kenar): gerçekte %40, rastgele modelde %49. 60 günlük 5 dakikalık veri, 148 olay.
    - **Kaynak ayıklama**: ünlü trader'ın adını kullanan ama kendisinin konuşmadığı derleme kanalları (uydurma anekdot riski) kırmızı bayrak sayılır.
51. **Süpürme ve SFP tek başına sinyal değil, filtre ve bağlam şart** (05 §8b, 13 §3c, 11 #77).
    - **Dante'nin SFP tanımı filtresiz test edildi** (9 piyasa, 1 saatlik, 3.731 işlem): -0,028R, rastgele -0,005R. Avantaj yok. Dante de "seçici ol" diyor.
    - **"Perakendenin tersini yap"** fikri, ortalama trader'ın yönü maliyet öncesi rastgeleye yakın olduğu için "rastgele + iki kat maliyet" demek.
    - **Dante'nin icra araçları**: negatif görselleştirme, iptal edilen ve kaçırılan emirleri kaydetmek, gün içinde 2R zararda durmak.
52. **Dante'nin risk hikâyelerinden kurallar** (02 §6b-4).
    - Her işlemde stop: stopsuz bakır pozisyonu 9.500 sterlinlik hesabı 50 dakikada bitirdi.
    - Emir tepki vermezse tekrar basma, gerçek pozisyonu kurumdan teyit et: bir meslektaşın kariyeri platform hatasıyla bitti.
    - Sabit kurda stopu tabanın öbür tarafına koy.
    - Kurum ya da firma hatalarını istismar etmek prop'ta yasak.
53. **Bir piyasaya özgü istatistikler başka piyasalara taşınmaz** (06 §8b-3, 13 §3c, 11 #78).
    - **Dante'nin Bund'daki "open drive %80 başarısız" istatistiği** ABD ETF'leri ve vadelilerinde %26-28 çıktı, rastgele modelle aynı ya da daha düşük. Kendi piyasanda doğrula.
    - **Dante'nin iş planı ilkeleri**: sermayenin ~%10'u kurumda, gün başına risk sınırı, strateji başına 10R düşüş sınırı (en kötüsü 12R), MAE ile stop optimizasyonu (aşırı uyum riskine dikkat), aktif ve pasif yönetimi yan yana kaydetmek.
54. **Brandt: ödemeli sim "oyun"dur, ama kuralları çözen problem çözücüdür; asıl ölçüt getiri/düşüş** (09 §4r, 03).
    - **Brandt'ın tahmini**: prop'ta yılda %1 kârlı, %0,5 gerçek hesaba. Topstep'in resmi %0,71'iyle uyumlu.
    - **İşi bırakma ölçütü**: hesabın tamamı kâr olmalı, hesaptan ayrı 2 yıllık gider birikmiş olmalı, hesap yıllık ihtiyacın 3 katı olmalı.
    - **Getiri / en kötü düşüş**: ≥3 olağanüstü, ≥4 dünya klası. Risk ≤%1 (genellikle %0,6-0,8). "Sızıntı" (kural ihlali maliyeti) hedefi yılda ≤1.000 baz puan.
    - **Erken çıkış testi**: "ilk zararlı kapanışta çık" kuralı mekanik kırılımlarda büyük kazananların %30'unu kesti. "2 gün zararda" ve "Cuma zarardaysa" kuralları nötr. Kendi kaydınla doğrula.
55. **Brandt'ın kendi kırılım kuralları test edildi: formasyonda değil piyasada ve çıkışta avantaj var** (03, 14 §3d).
    - **Kurallar**: yatay 8-14 haftalık kutu, ≤%15 genişlik, ADX<12, 0,5 ATR kırılım, 8 günlük ortalama ile trailing.
    - **Emtia vadelilerinde**: filtresiz kırılım +0,30R, rastgele +0,07R. Vade geçişi boşlukları çıkarılınca 2015 sonrası +0,16R'ye karşı +0,07R.
    - **Paritelerde ve endekslerde**: avantaj yok.
    - **Sıkışma filtreleri**: 2015 sonrası katkı vermiyor. Brandt'ın "dikdörtgende avantaj yok, avantaj risk yönetiminde" sözüyle uyumlu.
    - **Brandt'ın gerçekçi çıtası**: yılda %30-35 dünya klası. İsabeti %54, ortalama kaybı 17 baz puan, yılda 125-150 işlem.
56. **Bir trader'ın iddialarını nasıl doğrularsın?** (11 kırmızı bayraklar, 09 §4s)
    - **İmkânsız kombinasyon**: %91 isabet ve kâr faktörü 28, işlem başına ~+2,4R demek. Doğrulanmış en iyi trader'lar %50-60 isabet, 5'in altında kâr faktörü.
    - **Günlük uygulaması ekran görüntüsü** kanıt değildir. Kurum ekstresi, Kinfo ya da denetim ister.
    - **"Hiçbir şey satmıyorum" ama offshore kurum referans linki** varsa takipçi ürünün kendisidir.
    - **Prop ödeme zinciri** (avantaj yokken): ilk ödeme %22, ikinci %7, üçüncü %2. Firmayı geçme oranına göre değil, ödemeye kadar gereken hesap sayısına göre değerlendir.
57. **İşlem notlama ve boyut farkı ancak kanıtla açılır; prop kimin işine yarar?** (02 §4c, 09 §4t)
    - **Notlama (A/B/C/D)**: A'nın B'den +0,3R iyi olduğunu göstermek için ~200 A işlemi gerekir (A işlemlerin %15'iyse toplam ~1.300 işlem). Bilgisiz notlarla boyutu artırmak getiriyi değiştirmez, kuyruk riskini büyütür. Ters notlarla zarar verir. Kanıtlanana kadar sabit boyut kullan, notları sadece kaydet.
    - **Prop'tan fayda görenler** (Breitstein): yapı ve topluluk arayan, ya da kanıtlı avantajı olup sermayesi olmayan (~%1). **Zarar görenler**: avantajsız hesap yakan, sadece ES ve NQ'ya kilitlenen, simülasyonda kötü alışkanlık edinen.
58. **Risk çerçevesi = kural hiyerarşisi + "eğer-ise" eylemleri** (02 §6d).
    - **Hesap düzeyi kurallar katı** (maksimum düşüş, felaket kaybı), işlem düzeyi kurallar esnek olabilir.
    - **Günlük, haftalık ve aylık eşiklere önceden tanımlı eylem bağla**: boyutu yarıya indir, günü kapat, mola ver. Prop'ta FTMO limitlerinin ~1/4-1/5'ine ölçekle, ör. -%2,5'ta yarım boyut, -%3,5'ta günü kapat.
    - **Sabah kendine karne ver**: kötü uyku ya da stres varsa boyutu küçült.
    - **Short'larda daha küçük boyut** kullan. Kişisel hesapta kârın bir kısmını düzenli çek. Prop'ta ise tampon bırakmak hesabı uzun yaşatır.
59. **Stop gece boşluğuna karşı korumaz; boyutu "makul en kötü boşluğa" göre de sınırla** (02 §6e, 11 #80).
    - **Test** (günlük 2010+, 1 ATR stop): açılış tutuşların %1-4'ünde stopu atlıyor, ortalama kayıp 1,4-2,5R. Ortalama maliyet işlem başına ~0,01R, yani sorun ortalama değil kuyruk.
    - **En kötü tek gece**: büyük hissede -10R (bilanço), küçük hisse short'unda **-96R**, vadeli ve paritede ~-4R.
    - **Prop**: %1 riskte tek boşlukla 3R'den fazla kaybetme olasılığı büyük hissede ~700 tutuşta 1, vadelide ~3.400'de 1. FTMO 1 aşamalı hesabın %3 günlük limiti tek boşlukla dolabilir. Hafta sonu taşıyan Swing hesabı için vadeli ve parite hisseden çok daha güvenli.
60. **"Teknik analiz fraktaldır" bir hipotezdir, avantaj her zaman diliminde ayrıca test edilir** (10 §6n, 11 #79).
    - Aynı kurallar 5 dk, 1 sa ve günlükte: avantajın işareti tutarsız. Maliyet fraktal değil: EURUSD'de 5 dk'da ATR'nin %49'u, günlükte %1'i.
    - Tutarlı görünen tek şey endekslerde kapitülasyon alımının 1 saatlik ve günlükte pozitif olması (RSI-2 ile uyumlu).
61. **Yapay zekâ kısıtı çözdüğünde P&L'ye yarar; oyun kitabını önceden tanımla** (13 §3d).
    - **Breitstein**: meşgul olmak gelişmek değil. P&L'yi sınırlayan tek şeyi (avantaj, icra, fırsat, risk) bul. Yapay zekâyı işlem kaydını kategorize etmek, test kurmak ve intikam işlemini kısıtlayan araç yazmak için kullan.
    - **Test**: setup'lar arasında fark yokken bile çeyreklerin %20'si "oyun kitabı kazandı, gerisi kaybetti" görüntüsü veriyor. Tek çeyreğe bakıp kategorileri atmak kârın %39'unu yok ediyor. Çözüm: oyun kitabını önceden yaz, her işlemi girişte etiketle, plan dışı işlemleri kanıt beklemeden kes.
62. **50. tur sentezi: [Prop yol haritası](bilgi/15-prop-yol-haritasi.md)**. Avantajı kanıtlama ölçütü (maliyetten sonra ≥ +0,1R, rastgeleden ≥2 se, iki zaman yarısında pozitif, ≥200 işlem), hesap seçimi, challenge ve fonlu hesap ayarları, karar akışı.
63. **Küçük hesap challenge'ı beceri değil risk seçimidir** (09 §4u, 11 #81).
    - Bir yılda 25 kat (2.000 $ → 50.000 $), +0,2R'lik güçlü avantajla bile işlem başına ≥%5-10 risk ister. Avantajsız 31-36 kişiden biri %20-33 riskle başarır, geri kalanların %96-97'si batar.
    - Aynı risk prop hesabında +0,2R'lik avantajın geçme oranını %87'den %40'a düşürür.
64. **Breitstein'ın iki swing stratejisinin mekanik versiyonu** (12, 51. tur).
    - **Kapitülasyon "V'nin sağ tarafı"** tek hisselerde rastgele girişten kötü (-0,06 ile -0,21R). Kapitülasyon avantajı bu tabanda endekslerde görülüyor (RSI-2).
    - **Çok aylık kırılım + hacim** sadece 20 günlük ortalama çıkışıyla ve 2015 sonrasında rastgelenin üstünde (+0,46R'ye karşı +0,21R, ~1,9 se). Önceki gün dibi trailing'i avantajı siliyor. Hisse listesi hayatta kalma yanlılığı taşıyor, zayıf kanıt.
    - **Test dersi**: gün içi seviyeden giriş + "gün seviyenin üstünde kapandı" filtresi ileriye bakmadır, sahte +1,1R üretti.
65. **Kurtarma işlemi, tilt ve "hızlı bitirme" sadece avantajsız trader'a yarar** (09 §4v, 11 #82).
    - **The5ers CEO'sunun gözlemi**: kaybedenler düşüşte ya da hedefe ~%2 kala tek büyük işlem açıyor. Ödeme alanlar swing yapıyor, düşük kaldıraç kullanıyor (1:10-1:20) ve lotu tutarlı tutuyor.
    - **Simülasyon**: +0,2R'lik avantajda "2 kayıptan sonra boyutu ikiye katla" geçme oranını %89'dan %77'ye düşürüyor. -0,1R'de ise %26'dan %34'e çıkarıyor (aleyhte oyunda cesur bahis, Dubins-Savage). Hedefe yakın büyük işlem herkese zarar.
66. **SMB'nin trader geliştirme modeli: taban + A+, 4 aylık tutarlılık kapısı, ASSET protokolü** (13 §3e, 02 §4c).
    - **Sıra**: dağılım (A+/A/B/C) → stop (girişten önce) → giriş → boyut (hesaplanır) → hedef (ölçülü hareket).
    - **SMB'nin 16 katlık dağılımı** (A+ günlük stopun %80'i, C %5'i): notlar bilgi taşıyorsa getiri 2 kat, challenge geçme %57'den %88'e çıkıyor. Taşımıyorsa %10 düşüş olasılığı 4 kat artıyor. SMB'nin "4 ay tutarlı olmadan risk artışı yok" kuralı bu riski kapatıyor.
67. **"Prop oyunu" stratejilerinin kârı stratejiden değil firmanın bedava tamponundan gelir** (09 §4w, 11 #83).
    - **Model**: avantajı sıfır bir fonlu 100K hesabın değeri ≈ kâr payı × tampon ≈ 7.900 $. Maliyet sonrası tipik trader (-0,1R) ise hesap başına zararda.
    - **"Döner kapı"** (kademeli hesap, %3'te kilit, düşüşteki hesabı atma): kademelendirme ve kilit beklentiyi değiştirmez, hesabı atmak ücret dolarına düşen ödemeyi 2,5-5 kat düşürür.
    - **Değerlendirmede %4,5 tek işlem riski**: sadece negatif avantajlıya yarar, avantajlının geçme oranını %58'den %35'e indirir. FTMO'da aşırı risk ve hesap döndürme yasak.
68. **"Kendin test et" denen iddia testte ters çıkabilir: seviyeye hızlı gelen fiyat daha sık kırıyor** (05 §8c, 11 #84).
    - Dante'nin "drift of death" kuralı, 8 piyasa ve 1 saatlik ~2.400 dokunuşta: hızlı yaklaşımda tutunma %43, yavaşta %53. Rastgele seviyelerde de benzer fark var, yani genel kısa vadeli momentum.
    - %65 isabette 50 işlemde 4'lü kayıp serisi olasılığı %38,5 (Dante ">%50" diyor). Ders aynı: seriye önceden plan yap.
69. **Yön, beceri gibi görünür: kendi sonucunu yön eşleştirilmiş rastgele girişe karşı ölç** (10 §6o, 09 §4x, 11 #85-86).
    - 1,3 milyon $ prop ödemesi alan Zamco'nun yılının %60-70'i Ekim-Aralık 2025'ten geldi. O dönemde altında becerisiz rastgele long girişler RR 2 ile +0,22R ve %58 isabet verdi. Bu, zaman testinden geçen en iyi avantajlardan büyük.
    - Aynı röportaj: 6 yıl zarar, ücret/ödeme 1:4, değerlendirmede maksimum risk, hesabı bilerek patlatma, 2-4 saat uyku, kişisel hesapta 1:500 ile 100 bin $'ı 30 dakikada kaybetme. Bağımlılık işaretleri için 08 §8.
70. **Gerileyen boyut kötü günün kuyruğunu keser; dürtü sonrası tepe testi sadece 5 dakikalıkta rastgelenin üstünde** (02 §7, 06 §8b-4, 13 §3f).
    - **FT71'in kuralı** (limitin 1/3'ünde %60, 1/2'sinde %50, 3/4'ünde %20 boyut): günde 6 işlemle -%3'e hiç ulaşmıyor. Sabit boyut günlerin %13-24'ünde ulaşıyor. FTMO 1 aşamalı hesapta bu, hesabı korumak demek.
    - **"%78 tepe testi"**: 1 saatlikte rastgeleyle aynı (%56-58). 5 dakikalıkta %63-69, rastgele %54-55. Hipotez, ileri test bekliyor.
71. **Kademeli kâr alma beklentiyi yarıya indirir; zararda da kademeli çıkmak avantajı siler** (03, 11 #87).
    - RSI-2 ve emtia kırılımında 1/3'lük parçalarla 0,5R-1R-2R çıkış: +0,100R → +0,058R ve +0,071R → +0,033R. Ortalama/oynaklık oranı iyileşmiyor. Oynaklığı azaltmanın daha ucuz yolu boyutu küçültmek.
    - Bu avantajlarda kâr kuyruktan geliyor: trailing ya da "yarısı hedefte, yarısı trailing" en iyi oran.
72. **Uzun vadeli trend takibi kuyruktan yaşar; kaybettiren piyasayı bırakma** (12, 11 #88, 01 §3).
    - 30 vadeli, 2000+, 100 günlük kırılım: ortalama +0,24R, isabet %38. İşlemlerin en iyi %10'u brüt kazancın %67'si.
    - Bir piyasada 3+ ardışık kayıptan sonraki işlemler daha kötü değil (Parker: "acı arttıkça beklenti birikir"). Fark anlamlı değil, ama piyasayı bırakmayı destekleyen veri yok.
    - "İlk kârlı kapanışta çık": %96 isabet, -0,05R ortalama, en kötü %1 -11,8R.
73. **Keltner ve Bollinger bantları tek başına sinyal değil** (04 §12).
    - 24 piyasa, 2005+: bant kırılımını tersine işlemek ve "banda değ + sığ geri çekilme → devam" kuralı, rastgele kıyastan ayırt edilemiyor. İki bant türü aynı sonucu veriyor.
    - Grimes'ın kendi uyarısı da bu: "Banda değdi diye short açmam. Çoğu zaman yön yazı-tura."
74. **Rastgele girişte isabet %50 değil 1/(1+RR)'dir; trend yönü tek başına küçük bir eğim katar, maliyeti zar zor geçer** (`arastirma/verify_trend_rastgele.py`, 2026-11-26).
    - 5 piyasa, 1m veriyle, stop 1 ATR. Hücre başına ~7.500 rastgele giriş.
    - İsabet RR'yi izliyor: 1:2'de %33, 1:1'de %50, 0,5:1'de %66. Beklenti, hangi RR seçilirse seçilsin, maliyetten önce ~0.
    - Trend (EMA20/50) yönünde girmek rastgele yöne göre +0,00 ile +0,05R ekliyor. Eğim üst zaman diliminde büyüyor. En iyisi günlük trend + 4 saatlik giriş + 2R: +0,054R fark (3,9 se), net **+0,017R**. 27 hücrenin tek artısı.
    - Maliyet ölçekle büyüyor: işlem başına 15 dk'da 0,11R, 1 saatte 0,05R, 4 saatte 0,04R. 15 dk'lık bütün hücreler −0,11 ile −0,13R.
    - Sonuç: avantaj "nereden girdiğin"in rastgele hali değil; varsa trendin üstüne eklenen, önceden tanımlanmış filtrelerden ve düşük maliyetli zaman diliminden gelir. Filtreler piyasaya bağlı: CHoCH + süpürme + EMA testi paritelerde +0,25R, BTC'de −0,25R (15, #75).
75. **Filtreleri her birleşimde taramak ve "yılın en iyisi"ni seçmek avantaj bulmuyor** (`arastirma/verify_choch_kombinasyon.py`, 2026-11-26).
    - CHoCH + geri test kurulumunun 4.745 sinyali (5 piyasa, 1H ve 4H). 10 filtrenin (4H trend, süpürme, EMA testi, günlük RSI, 4H ADX, hacim, günlük EMA200, volatilite rejimi, seans, gün) 1-3'lü 3.787 birleşimi.
    - 2023 öncesinde seçim ölçütüne (n ≥ 40, t ≥ 3) ulaşan birleşim **sıfır**. Şans makinesi ortalama 0,1.
    - Her yılın en iyi birleşimi o yıl +0,3 ile +1,15R gösterdi. **Ertesi yıl ortalama −0,04R**, bütün sinyallerin ortalaması −0,07R. Örnek: 2018'in en iyisi +1,15R → 2019'da −0,54R. 2025'in en iyisi +0,77R → 2026'da −0,51R.
    - Önceki keşif hattıyla aynı sonuç (TEST_KAYDI 19-25: 1.024.833 hipotez, geçen yok). Geçmişte en iyi görünen birleşim, geleceğin en iyisi değil.
76. **Gösterge laboratuvarı: 78 göstergenin 1-4'lü 1,08 milyon birleşimi; tek ayakta kalan aile 4 saatlik trend yönlü long** (`arastirma/gosterge_lab/`, 2026-11-26).
    - 5 piyasa, 1H, 4H ve 1D. Her mumda long ve short: stop 1 ATR, hedef 2R, maliyet dahil, 10 mum seyreltme. Sıralama 2023 öncesine göre.
    - 2023 öncesinin yıldızları (işlem başı +0,4 ile +0,95R) 2023 sonrasında çoğunlukla sıfıra indi. 1H long ortalaması +0,00R, 1H short +0,01R, 4H short −0,08R, 1D short −0,15R. Günlük long birleşimleri filtresiz "her gün long"tan (+0,15R, BTC ve altın yükselişi) kötü.
    - İstisna: 4H long trend birleşimleri. Bunların %83'ü 2023 sonrasında da artı, ortalama +0,10R; filtresiz 4H long tabanı +0,01R. En basit örnek: fiyat SMA200'ün belirgin üstünde (piyasaya göre ~1,5-3,6 ATR) ve Stoch RSI > ~0,75 → long. Sonuç +0,18R (n=933), 2017-2026 her yıl artı, 5 piyasanın 5'inde artı. Ama 2023 sonrası artının çoğu altın ve GBP'den; BTC, EUR ve JPY ~0.
    - Aynası short (SMA200'ün belirgin altı + Stoch RSI düşük) −0,05R: etki simetrik değil, kısmen "yükselen varlıkta long". Trend takibi literatürüyle (17) uyumlu ama bota konmadan önce ileri test şart.
    - Şans makinesi sonuçları yıl içinde karıştırdığı için otokorelasyonu da siler. Gerçek-şans farkı bu yüzden abartılı; asıl ölçü 2023 sonrası ile taban.
77. **Gösterge laboratuvarı 2. tur: 5 zaman dilimi, ~110 gösterge, 2,94 milyon strateji, yıl × ay ve boğa/ayı rejimi. Takvim ve ay başı rejimi avantaj vermiyor; 5-15 dk'yı maliyet bitiriyor; bot kullanabileceği bir "ayı stratejisi" yok** (`arastirma/gosterge_lab/` hazirla2, tara2, rapor2, analiz2, kontrol_aday2; rapor2.html; 2026-11-26).
    - Kurulum #76 ile aynı (stop 1 ATR, hedef 2R, 1m sonuç, maliyet dahil). Yeni: 5 dk ve 15 dk, Hull/KAMA/DEMA/TEMA, Heikin-Ashi, Chaikin, Force, Elder, Coppock, KST, Fisher, Choppiness, ADX eğimi, Mass, Ulcer, sıkışma, NR4/NR7, günlük pivot, dünkü tepe/dip, Asya aralığı, VWAP, hacim z, EUR/USD ve BTC yönü, ay/ayın dönemi/saat, ay başı rejimi.
    - Yeni ölçü, **tabana göre t**: ortalamanın aynı dönemin filtresiz tabanından kaç standart hata yukarıda olduğu. Şans makinesi artık sonuçları piyasa içinde zamanda kaydırıyor; otokorelasyon korunuyor, şans daha dürüst.
    - **Rejim iki tanım.** (a) Ay sonunda bilinen: ayın getirisi ± yarım medyan. Geleceği bilir, yalnız betimleme. (b1) Ay başında bilinen: önceki ay sonu fiyat günlük SMA200'ün üstü/altı. (b2) Önceki ayın etiketi. (b1) ve (b2) bot kullanabilir.
    - **Ay başı rejimi ayın yönünü %44-57 bildi:** yazı-tura. Tek başına filtre olarak hiçbir zaman diliminde tabanı iyileştirmedi. "Ay başında SMA200 altıysa short" 2023 sonrasında tabandan kötü: 4H −0,15R, 1D −0,41R.
    - **Ayıda çalışan:**
      - (a) tanımında ayı ayında short tanım gereği kazanır; bot bunu önceden bilemez.
      - (b1) tanımında 2023 öncesi ayı aylarında güçlü görünen 3.500-4.100 short stratejiden 2023 sonrası ayı aylarında da belirgin artı kalan 4H'de 6, 1H'de 13 tane; şans makinesinde 7 ve 1. Long stratejiler ayı aylarında hiç çalışmadı.
    - **Takvim:** 12 ayın 2023 öncesi ve sonrası sıralama uyumu −0,22 ile +0,34 arası. "Şu ay iyi" bilgisi taşınmıyor.
    - **5 ve 15 dk:**
      - Filtresiz taban işlem başına −0,12 ile −0,30R. 5 dk'da önce güçlü görünüp 2023 sonrasında da sıfırdan belirgin artı kalan strateji 0. 15 dk'da 22 tane, tek aile.
      - Binlerce 5-15 dk stratejisi "tabanı geçiyor" ama bu bir tuzak: yüksek oynaklık anlarını seçip maliyetin payını küçültüyorlar, yine eksiler.
    - **Ayakta kalanlar.** Hepsi hipotez; 2,94 milyon denemenin içinden çıktılar.
      - **4H trend long (#76 kuralı):** aynen tekrarlandı: +0,18R, n=933, her yıl artı. Ayların %61'i artı, en kötü ay −9,3R.
        - Ama boğa aylarında +0,36R, ayı aylarında −0,26R. 2025-26 zayıf (+0,03 / +0,06).
        - 2023 sonrası artı çoğunlukla altın ve GBP'den.
        - Gerçek-şans farkı en net aile bu: sonra da belirgin artı 872'ye 355.
      - **1H "ölü kedi sıçraması" short'u:** sert düşüşten sonra fiyat SMA10'un belirgin üstüne çıkmış ama 20 mumluk ortalamanın altında. n=137 (yılda ~15). Önce +0,54R, sonra +0,41R. Ailede 451 strateji var, şans makinesinde 0.
        - BTC'de zayıf (+0,10R, 40 işlem); sonraki artının çoğu JPY'nin 13 işleminden.
      - **4H short:** 100 mumluk tepenin belirgin altı + SMA100 civarı + düşük ATR. n=236, sonra +0,21R. Ayı aylarına bağlı; 2024-25 zayıf.
    - **Bot için:** kurallar dondurulup ileri testte (2026-12'den itibaren) tutarsa bota konmalı.
    - Not: seyreltme kuralı koşul uzun süre doğru kaldığında yalnız ilk sinyali alır. Takvim ve rejim-filtresi sonuçları bu yüzden filtresiz tabandan hesaplandı.
78. **Stop ve hedef avantaj yaratmaz; laboratuvarın kötü sonuçları 1 ATR / 2R çıkışından gelmiyor** (`arastirma/gosterge_lab/` cikis_hazirla, cikis_analiz, cikis_yorum, cikis_brut; cikis_cikti.txt; 2026-11-26).
    - **Kurulum:**
      - Giriş laboratuvarla aynı: sinyal mumu kapanınca sonraki 1m açılışında piyasa emri.
      - Aynı 1,2 milyon girişe 113 çıkış uygulandı:
        - sabit çıkışlar: stop 0,5 / 1 / 1,5 / 2 / 3 ATR × hedef 0,5R / 1R / 1,5R / 2R / 3R / 5R / hedefsiz × 10 / 20 / 60 mum;
        - yalnız süreyle çıkış;
        - iz süren stop 1 / 2 / 3 ATR;
        - +1R'de başa baş.
      - Sonuçlar 1m verisinden, maliyet dahil.
      - Kontroller: 1 ATR / 2R / 60 mum çıkışı eski sonucu birebir verdi. Dakika dakika ilerleyen ayrı bir döngüyle 600 rastgele giriş × 113 çıkış × 2 yönde fark 0.
    - **Rastgele girişte çıkış avantaj üretmez.** Filtresiz girişte 113 çıkışın maliyetsiz ortalaması sıfır civarında: 5m −0,09 ile +0,05R, 15m −0,08 ile +0,08R. Stop/hedef yalnız dağılımın şeklini (maliyet dahil isabet %8-67) ve maliyetin R içindeki payını değiştirir (#74).
    - **5-15 dk'da sorun maliyet, çıkış değil:**
      - Stop genişleyince maliyet payı küçülüyor: 5m 1 ATR'de −0,24R, 3 ATR'de −0,09R.
      - Yine de 5m'de 2023 sonrasında artı kalan çıkış 0/113, 15m'de 3/113.
    - **1H-4H-1D'de geniş stop / hedefsiz long filtresiz de kazanıyor: bu piyasanın yükselişi.**
      - 4H'de stop ve hedef koymadan 60 mum tutmak: 2023 öncesi +0,33R, sonrası +0,79R. Short aynası eksi.
      - BTC ve altının yükselişini taşır; ayı aylarında kaybeder (#77). Gösterge avantajı değildir.
      - 1 ATR / 2R çıkışı bu yükselişi kesiyordu. Long tarafın "al ve tut"tan kötü görünmesinin nedeni bu.
    - **Adaylar:**
      - **4H trend long:** hedefsiz çıkışla ham sonuç ikiye katlanıyor: stop 1,5 ATR + hedefsiz ile önce +0,69R, sonra +0,37R (lab çıkışında +0,24 / +0,13). Ama aynı çıkışla filtresiz long da o kadar kazanıyor. Tabana göre en iyi çıkış zaten 1 ATR / 2R (fazla: önce +0,30R, sonra +0,11R). Ekstra kâr kuraldan değil, yükselen piyasadan geliyor.
      - **1H ölü kedi short:** 113 çıkışın 113'ünde 2023 sonrası artı, tabana göre 80'inde belirgin. Avantaj girişte, çıkışa duyarsız: iyi işaret, ama örnek yine küçük (n=137).
      - **4H short ve 15m NY long:** 2023 öncesine göre seçilen çıkış küçük hedefli, %80 isabetli çıkışlar oluyor. Bunlar 2023 sonrasında çöküyor: 4H short +0,20 → +0,04R. Çıkış optimizasyonu aşırı uyumdur.
    - **Bütün tekli koşullar (3.266 strateji × 113 çıkış) ve şans makinesi:**
      - Her stratejiye 2023 öncesinin en iyi çıkışı verildi; ölçü 2023 öncesi t≥3 ve 2023 sonrası t≥2.
      - Ham kârla geçen: 5m 0, 15m 0, 1H 25, 4H 37, 1D 2. Şans makinesinde 0, 0, 20, 48 ve 6,7: şanstan farksız.
      - Aynı çıkışlı tabana göre: 5m'de 107, 15m'de 86 strateji geçiyor; şans makinesinde 9,7 ve 4,3. Hepsi kısa vadeli ortalamaya dönüş: fiyat ortalamadan çok uzaklaşınca tersine.
      - Bu etki gerçek ama küçük. Maliyetsiz 2023 sonrası +0,015R (5m) ve +0,026R (15m); aynı işlemlerin maliyeti 0,34R ve 0,16R, yani etkinin 5-10 katı. Net sonuç 30 stratejinin 30'unda eksi (5m), 15m'de 29'unda eksi.
      - #77'deki "tabanı geçenler yalnız maliyet payını küçültüyor" yorumunun düzeltmesi: bir kısmı gerçek yön bilgisi taşıyor, ama bu sıradan bir maliyetle işlem yapılamayacak kadar küçük.
    - **Bot için:**
      - Çıkışı optimize etme. Stratejinin mantığına göre önceden seç: trend için koşturan çıkış, ortalamaya dönüş için kısa süre + küçük hedef.
      - Sonucu aynı çıkışla filtresiz tabana karşı ölç; ham kâr yükselen piyasada herkesi iyi gösterir.
      - Giriş tipinin etkisi (piyasa emri yerine geri çekilmede limit emir) ayrı bir soru; test edilmedi.
79. **"Her yıl kazandıran" stratejilerin yarısı şansla da çıkıyor; günlük long listesi tamamen şans düzeyinde. Girişte bilinen boğa/ayı etiketiyle "ayıda alma" kuralı işe yaramıyor** (`arastirma/bot_adaylari/` index.html, adaylar.csv; gosterge_lab/sans_tara2.py; 2026-11-26).
    - **Kriter:** n ≥ 100; en az 5 işlemli yıl sayısı ≥ 6 ve bu yılların hepsi artı; 2023 öncesi ve sonrası artı.
    - **Kademeler:** A = 2023 sonrası t ≥ 2 ve aynı dönemin tabanını da t ≥ 2 ile geçiyor; B = 2023 sonrası t ≥ 2; C = geri kalanı.
    - **Şans karşılaştırması:** aynı kriter 2. turun şans koşusuna da uygulandı (aynı tohum ve döndürmeler, bu kez stratejiler kaydedildi).
    - **Sayılar:**
      - Kriteri 7.481 strateji (1.871 aile) geçiyor; şans makinesinde 3.362. "Her yıl artı" tek başına kanıt değil.
      - 1D long: gerçek 1.388, şans 1.413. A kademesinde 84'e 235. Günlük long'un "her yıl kazanması" BTC/altın yükselişi ve az işlem sayısının ürünü.
      - Şanstan ayrışan yer A kademesi: 15m 105'e 4, 1H 157'ye 27, 4H 1.094'e 334.
      - En büyük aile yine 4H trend long (SMA100/200 belirgin üstü + Supertrend yukarı + Stoch RSI yüksek, 296 varyant): +0,41R, 10/10 yıl, 4/5 piyasa.
    - **Boğa/ayı (kullanıcının sorusu: aynı stratejide ayıda alınmaması gereken işlemler var mı?):**
      - Ay sonu etiketiyle long adaylar ayı aylarında kaybediyor: 1D long boğa ayı ~+1,0R, ayı ayı ~−0,5R; 4H long A +0,45 / −0,09R. Etiket ayın sonucunu kullanır; bot bilemez.
      - Girişte bilinen etiketle (son günlük kapanış SMA200 üstü/altı) fark yok: 4H long A boğada +0,31R, ayıda +0,34R.
      - "Ayıda alma" kuralı 2023 sonrasını iyileştirmedi: 4H long +0,19 → +0,20R, 1H long +0,23 → +0,16R, 1H short +0,18 → +0,10R.
      - Ayı işlemleri 2023 öncesi eksi olan adaylarda bile çıkarmak 2023 sonrasında 1H ve 4H'de %31-50 oranında işe yaradı: yazı-tura.
      - Kayıplar sonradan "ayı ayı" olduğu anlaşılan aylarda; girişte ayırt edilemiyor (#77 ile uyumlu).
    - **Risk:** ailelerin en büyük düşüşü medyan 6-16R. FTMO %10 sınırı için işlem başı risk %0,25-0,5.
    - **Kullanım:** listenin en üstü en çok aşırı uyumlu olandır (4 koşullu, takvimli, tek piyasalı). 15m/1H/4H A kademesinden az koşullu, çok piyasalı, büyük aileli 3-5 kural seçilip dondurulmalı ve ileri test edilmeli.
    - **Gevşek yıl kuralı (kullanıcının isteği: "6 yıl artı, 1 yıl −0,01 sorun olmaz"):** en çok 1 yıl eksi ve o yıl işlem başı ≥ −0,05R olanlar da listeye eklendi (sayfada "Yıl kuralı" süzgeci, CSV'de `yil_kurali` sütunu).
      - Toplam 14.676 aday (3.266 aile); şansta 6.725. 1 yıl hafif eksi olanlar: gerçek 7.195, şans 3.363. Şansa oranları her yıl artı olanlarla aynı.
      - A kademesi: her yıl artıda 1.440'a 600, 1 yıl hafif ekside 767'ye 312. Birleşik: 15m 128'e 9, 1H 342'ye 41, 4H 1.615'e 456, 1D long 119'a 406 (yine şans).
      - 1H short A 72'den 217'ye çıktı (şansta 16'dan 26'ya); çoğu mevcut ailelere katıldı. −0,01R'lik yıl gürültüdür; belirleyici olan şanstan ayrışma.
      - Hafif eksi yıl çoğunlukla 2023-2026'da (en sık 2025): kenar son yıllarda inceliyor olabilir.
      - "Ayıda alma" genişletilmiş listede de işe yaramıyor: A kademesi aile başlarında 1H/4H'de iyileşen pay %42-54.
80. **"2024 sonunda seçseydin 2025'te kazanır mıydın?" Gerçek ileri test: her yıl artı listesinin ortalaması 2025'te filtresiz tabandan belirgin iyi değil** (`arastirma/bot_adaylari/ileri_2025.py`, ileri_2025.csv; 2026-11-26).
    - **Yöntem:** aynı kriter yalnız 2017-2024 verisiyle uygulandı (≥6 yıl ≥5 işlemli, hepsi artı; n ≥ 80; 2017-22 ve 2023-24 artı). Seçilenlerin 2025 ve 2026 ortalaması aynı yılın filtresiz tabanıyla karşılaştırıldı. Kademe (t) uygulanmadı.
    - **2025, işlem başı ort. R, seçilen / taban:** 1D long +0,29 / +0,13 (seçilenlerin %80'i artı); 4H long +0,03 / +0,07; 1H long −0,01 / −0,03; 1H short −0,09 / −0,10; 15m long −0,05 / −0,11; 15m short −0,17 / −0,16.
    - **2026 (Kasım'a kadar):** 1D long −0,01 / +0,09 (%46 artı); 4H long +0,01 / −0,09; 1H short +0,08 / −0,04; 15m short +0,05 / −0,13.
    - **Sonuç:** "geçmişte her yıl artı" seçimi, seçilen grubun ortalamasında ertesi yıl ancak taban kadar ya da biraz üstünde. 1D long 2025'te iyi (altın +%60), 2026'da tabanın altında. Tek bir stratejinin geçmiş yılı artıysa bu seçimin sonucudur, kanıt değil.
    - **Kullanıcının sorduğu örnek** (1D long: ichimoku_tk yukarı + üst fitil düşük + boşluk düşük + nr4 yok, B kademesi): 2024 sonunda da seçilirdi (2019-2024 hepsi artı, 89 işlem). 2025: 15 işlem, +4,9R (isabet %40, en büyük düşüş 3,2R). Ama +4,27R'lik bir altın işlemi PAXG'nin hafta sonu fiyatından geliyor; hedefe indirilince +2,6R. %0,5 riskle yaklaşık +%1,3. FTMO'nun %10 hedefi için tek başına çok yavaş.
    - **Veri uyarısı: laboratuvarın altın verisi spot XAUUSD değil, Binance PAXGUSDT (2021'den), piyasa saatlerine süzülmüş.** PAXG hafta sonu da işlem görür ve spota prim/iskonto yapar. Pazartesi açılışında stop/hedefin ötesinde "boşluk" çıkışları oluşuyor: 1D altın long işlemlerinin %2,1'i 2,1R'nin üstünde kapanıyor (işlem başı +0,06R şişirme); 1H ve 4H'de ~+0,03R. Altına dayanan adaylar bot öncesi spot altın verisiyle yeniden ölçülmeli.
    - **FX 1D notu:** giriş günlük kapanıştan hemen sonra (rollover, 22:00 UTC) ve gerçek spread kullanılıyor; GBP/USD 1D işlemlerinin ~%15'i −1,15R'nin altında kapanıyor. Bot birkaç dakika bekleyerek girmeli; laboratuvar bu yüzden FX 1D'yi cezalandırıyor olabilir.
81. **"Düşüşte short, yükselişte long" kendi başına kazandırmıyor; düşüşte short her zaman diliminde eksi. Katkı, yönden bağımsız kazanan kurallarda** (`arastirma/bot_adaylari/rejim_yon.py`, rejim_yon.csv, rejim_yon_yil.csv; 2026-11-26).
    - **Test:** filtresiz taban (her sinyal satırı, G=10 seyreltme, 1 ATR / 2R / 60 mum, maliyet dahil). Rejim girişte bilinir: günlük kapanış SMA200 / SMA50 üstü-altı, 20 günlük getiri işareti, "ikisi" = SMA200 ve 20 gün aynı yönde. Şans: rejim etiketleri her piyasada zamanda kaydırıldı (300 kez).
    - **Rejime göre yön, işlem başı R (hep long → rejime göre):** 15m −0,15 → −0,12; 1H −0,06 → −0,04; 4H −0,02 → +0,01; 1D +0,13 → −0,02.
    - **Şans testi:** 15m/1H/4H'de şanstan iyi (p ≤ 0,05). Rejim gerçek bilgi taşıyor ama maliyeti karşılamaya yetmiyor. 1D'de şanstan farksız (p 0,65-0,89) ve hep long'dan kötü.
    - **Parçalar (SMA200):** düşüşte short 15m −0,13, 1H −0,08, 4H −0,02, 1D −0,31R; hiçbiri artı değil. Düşüşte short, düşüşte long'dan 15m/1H/4H'de biraz iyi. 1D'de düşüşte long (+0,07) short'tan (−0,31) çok iyi: BTC ve altın düşüşleri sert tepkilerle bitiyor.
    - **Katkı nerede:** A kademesi short aile başları iki rejimde de kazanıyor. 1H: boğada +0,37, ayıda +0,33R; 4H: +0,40 / +0,42R. Filtresiz short ise 1H'de −0,09R. Örnek 1H-short-18 (ADX yüksek + büyük mum + fiyat KAMA'nın çok üstünde + ulcer yüksek = düşüş yaşamış piyasada sert tepki yükselişini satmak): 856 işlem, 10/10 yıl, 5/5 piyasa, +0,20R; boğada +0,15, ayıda +0,22R.
    - **Sonuç:** düşüş için ayrı strateji yerine, kendi başına kazanan bir long ve bir short kuralını birlikte çalıştırmak daha mantıklı. Bunlar da tüm yıllar üzerinden seçildi; 2024 sonu ileri testi (A kademesiyle) yapılmadı.

82. **Kârlı ve mantıklı kurallar yıl yıl: grafik + ısı haritası** (`arastirma/bot_adaylari/isi_haritasi.html`; üretim isi_haritasi.py + isi_sablon.html; 2026-11-26).
    - **Seçim:** 14.676 aday → A kademesi 2.207 → 1D long hariç 2.088 → takvim koşulsuz (ay, haftanın günü, ayın günleri) 1.513 → çok piyasalı (≥ 3 piyasa, ≥ %60'ı artı, tek piyasa payı ≤ %60) 1.014 → her aileden bir kural: **256** (15m 11, 1H 24, 4H 221).
    - **Şans makinesi (A, takvimsiz):** 15m long 69 / 0, 15m short 40 / 0, 1H long 63 / 6, 1H short 189 / 3, 4H long 1.107 / 407, 4H short 45 / 19. 15m ve 1H şanstan çok net ayrışıyor; 4H'nin üçte biri kadarı şansla da çıkıyor.
    - **Yıllık medyan (işlem başı R):** 2017 +0,83 → 2018 +0,46 → 2019 +0,45 → 2020 +0,31 → 2021 +0,14 → 2022 +0,22 → 2023 +0,31 → 2024 +0,25 → 2025 +0,24 → 2026 +0,26. Yılların ~%97'si artı ama bu seçim gereği; bakılacak olan medyanın seyri: ilk yıllar şişkin, 2022'den beri ~+0,25'te sabit.
    - Sayfa: üstte her kuralın her yılı nokta (long/short), ortada kural × yıl ısı haritası (işlem başı ya da yıllık toplam R), satıra tıklayınca birikimli R eğrisi (toplam / piyasalara göre), ay × yıl tablosu, piyasa × yıl tablosu ve botun kullanacağı eşikler.

    - **Güncel (spot altınla, 2026-11-26 akşam):** sayfa yeniden tasarlandı: "Hangi kurallar kârlı?". Kurallar düz Türkçe (`bot_adaylari/okunur.py`), kazanç hesap yüzdesi olarak (işlem başı %0,25 / %0,5 / %1 risk), en kârlı kurallar listesi, "Asıl sınav" (ileri test) bölümü, kurala tıklayınca "bot ne zaman alır" + para eğrisi. Seçim 226 kural (15m 7, 1H 19, 4H 200). index.html'de de kurallar Türkçe.
83. **Altın verisi düzeltildi: PAXG yerine spot XAUUSD. Aday sayısı 14.676 → 11.006; 1H'nin "şanstan çok iyi" görüntüsü büyük ölçüde PAXG'den geliyordu** (`arastirma/gosterge_lab/altin_spot.py`, altin_kontrol.py; `bot_adaylari/altin_karsilastir.py` → altin_karsilastir.txt; eski çıktılar `arastirma/yedek_paxg_2026-11-26/`; 2026-11-26).
    - **Kaynak:** HistData.com 1m (bid, UTC−5 sabit → UTC), 2020-01 → 2026-11-13; akademinin seans süzgeci aynen. Maliyet aynı (0,35 $). FXCM'de altın yok; Dukascopy bu bağlantıdan çalışmadı. Laboratuvar spot altını `hazirla.py`'deki yama ile okur; **btc-order uygulamasının (Akademi) altını hâlâ PAXG**, senaryo bankası değişmedi.
    - **Kontrol:** bozuk OHLC 0; uzun boşluklar yalnız tatiller; PAXG ile günlük getiri korelasyonu 0,95. Hafta başı açılış boşluğu (1H ATR): medyan PAXG 0,65 / spot 0,28; 1 ATR'den büyük boşluklu hafta PAXG %37 / spot %11. Kusur: HistData 2023 şubat-temmuz arasında günlük 4-6 saatlik eksikler (≈ 40 bin dakika); laboratuvar bunları boşluk olarak işler.
    - **Filtresiz altın (2021+, işlem başı):** 4H long PAXG +0,11 → spot 0,00R; 1D long +0,60 → +0,13R (1D'de tatil boşlukları yüzünden satır az); short'lar spotta daha az eksi.
    - **Yeni sayımlar:** aday 11.006 (her yıl artı 5.495 + 1 yıl hafif eksi 5.511; 2.604 aile), şans 5.335. A kademesi gerçek / şans: 15m long 46 / 8, 15m short 42 / 14, 1H long 57 / 38, 1H short 44 / 38, 4H long 1.025 / 218, 4H short 135 / 103; 1D long hepsi 1.847 / 1.450. Takvimsiz A'da şans / gerçek: 15m long %0, 1H short %18, 4H long %23, 15m short %36, 4H short %144, 1H long %171.
    - **Eski A aile başları (511), aynı koşullar yeni veriyle doğrudan ölçülünce:** ortalama +0,341 → +0,299R; hâlâ aday %45, hâlâ A %27. İşlemlerinin %30'undan fazlası altın olanların yalnız %9'u hâlâ aday. 1D-long-108 +0,61 → +0,50R, 2025 artık −0,11R (aday değil). 1H-short-18 +0,20 → +0,18R, yine 10/10 yıl artı (t 2,0, kademe C).
    - #79-#82'deki sayılar PAXG dönemine aittir. rejim_yon (#81), cikis_* (#78), rapor2.html (#77) spotla yeniden koşulmadı.
84. **Asıl sınav: A kademesi yöntemi 2024 sonunda uygulansaydı, seçilen kurallar 2025-2026'da kazandırmazdı** (`arastirma/bot_adaylari/ileri_A.py` → ileri_A.csv, ileri_A_kurallar.csv/.parquet; spot altınla; 2026-11-26).
    - **Seçim yalnız 2017-2024:** ≥ 6 yıl (≥ 5 işlem), hepsi artı ya da en çok 1'i ≥ −0,05R; 2017-24 n ≥ 80; 2023 öncesi ve 2023-24 ortalaması > 0; takvimsiz. Kurallar işlemlerinden yeniden ölçüldü: A_ileri = t(2023-24) ≥ 2 ve tabana göre t(2023-24) ≥ 2; ≥ 3 piyasa, ≥ %60 artı, tek piyasa ≤ %60; aileler 2017-24 örtüşmesiyle. Tarama eşikleri ve ışın araması zaten 2023 öncesinden.
    - **2025-26 işlem başı, aile başları (filtresiz taban):** 15m long −0,11 (−0,14), 15m short −0,12 (−0,13), 1H long −0,04 (−0,06), 1H short −0,04 (−0,06), 4H long −0,04 (−0,05; 203 kural), 4H short −0,02 (−0,03). Hepsi 265 kural: **−0,04R** (taban −0,05R), kârlı biten %37. 1D long başları −0,03 (taban +0,01).
    - **Yorum:** seçim tabanı ~+0,01-0,03R geçiyor (biraz bilgi var) ama maliyeti karşılamıyor. Tam veriyle seçilen listedeki "her yıl kârlı" görüntüsü büyük ölçüde seçimden geliyor. Bu tarama yöntemiyle bota konacak kâr eden kural bulunamadı; bot için kural ancak dondurulup ileri testte (demo) kanıtlanırsa kullanılmalı.

85. **"Her yıl benzer büyüme" seçimi: kayan ileri testte 4H long'da hafif artı, diğer gruplarda maliyet sonrası eksi** (`arastirma/bot_adaylari/istikrar_ileri.py` → istikrar_ileri.csv; spot altın; 2026-11-26).
    - **Soru (kullanıcı):** 2026'yı yok sayınca her yıl artı kurallar yine çıkıyor mu; yıllık kazancı birbirine yakın (istikrarlı) kuralları seçmek işe yarar mı?
    - **Yöntem:** 2020'den itibaren yıllık toplam R (5 piyasanın hepsi 2020'den). Kesim 2023/2024/2025: yalnız 2020..kesim yılları; her yıl ≥ 5 işlem ve artı, ≥ 60 işlem, takvimsiz. İstikrar = yıllık toplam R'nin std/ortalaması; üçe bölündü. "Yakın" = her yıl ortalamanın ≥ yarısı ve CV ≤ 0,35. Test = sonraki yıl. Aileler ayrılmadı (varyantlar örtüşür).
    - **4H long, 2024 / 2025 / 2026 (işlem başı; rastgele = filtresiz):** her yıl artı +0,09 / −0,06 / +0,04R; yakın +0,07 / −0,03 / +0,10R; rastgele +0,04 / +0,01 / −0,12R. Yakın: 3 yıl ortalaması +0,05R (rastgele −0,03R), kârlı biten kural %70 / %39 / %71. Kural başına yıllık medyan +5,3 / −3,5 / +4,7R; %0,5 riskle yaklaşık +%2,7 / −%1,8 / +%2,3.
    - **3 yıl ortalaması, diğer gruplar (yakın / rastgele):** 4H short −0,01 / −0,05R; 1H short −0,02 / −0,09R; 1H long −0,04 / −0,03R; 15m long −0,04 / −0,14R; 15m short −0,02 / −0,15R. Seçim rastgeleyi geçiyor ama 4H long dışında maliyeti karşılamıyor.
    - **İstikrarlı ve dalgalı üçte birlikler** arasında tutarlı fark yok (4H long +0,034 / +0,007R; diğerlerinde karışık). Katı "yakın" süzgeci 4H long'da en iyi sonuç. Ama 2025 her yöntemde eksi; bu da büyük ölçüde tek fikir (4H trend long, fiyat SMA200'ün belirgin üstünde) ve BTC/altın yükselişine bağlı.

86. **4 × 100.000 $ FTMO, her hesapta bir 4H trend long kuralı: gerçekçi avantajla (+0,05R) yılda 4 hesap toplamı ortalama ~1.200 $ (%0,5 risk) ile ~9.700 $ (%1 risk)** (`arastirma/bot_adaylari/donuk_aday.py` → donuk_aday.json; ftmo_4hesap.py → ftmo_4hesap.csv; 2026-11-26).
    - **Kurallar:** "yakın büyüme" süzgecinden (2020-2025 her yıl artı ve birbirine yakın, 2026 artı) 179 kural, 62 aile; en güçlü ve birbirine benzemeyen 4 aile başı. Yılda 64 / 125 / 72 / 89 işlem (birlikte ~290, %15 çakışma). Geçmişte işlem başı +0,21 ile +0,33R (seçim yanlılığı).
    - **Simülasyon:** iki aşama +%10 / +%5, %10 toplam, %5 günlük; ücret 600 $ (ilk ödemede iade); fonlu hesapta ayda %80 ödeme; 3 yıl, 2.000 yol. Gelecek yıllar geçmişten rastgele aylarla kuruldu; dört hesap aynı ayları yaşar.
    - **+0,05R (ileri test düzeyi):**
      - %0,25 risk: neredeyse hiç fonlanmıyor (3 yılda %3); yalnız ücretler gider.
      - %0,5 risk: 4 hesap toplamı yılda ortalama +1.196 $ (medyan +360 $). 3 yılda zararda bitme olasılığı %45. Fonlanma 3 yılda %37, medyan 23 ay.
      - %1 risk: ortalama +9.684 $ (medyan +8.173 $, P10 −39 $, P90 +21.330 $), zarar olasılığı %10. Fonlanma 1 yılda %36, medyan 14 ay; hesap başına 3 yılda ~3 challenge.
    - **Karşılaştırma:**
      - Avantaj 0R iken bile %1 riskte yılda +3.922 $. Bu kazanç kuraldan değil, challenge yapısından geliyor: kayıp ücretle sınırlı, kârın %80'i trader'a.
      - −0,03R iken %1 riskte +1.383 $, ama zarar olasılığı %47.
      - "Geçmişteki gibi" (iyimser): %0,5 riskte +19.205 $, %1 riskte +51.707 $. Bu rakamla plan yapılmamalı.
    - **İyimser varsayımlar:**
      - Swap yok (4H işlemler günlerce açık kalır; FTMO'da kripto swap'ı büyük).
      - Günlük limit açık pozisyon dalgasını görmüyor. En kötü gün −3,1 ile −4,9R; %1 riskte %5 sınırına yakın.
      - FTMO kuralları ve kişi başı sermaye sınırı güncel siteden teyit edilmeli.

87. **Kural + parite ileri testi: 30 gruptan yalnız altın 4H long (güçlü), EUR/USD 1H short ve altın 1H long (zayıf) test yıllarında artı** (`arastirma/bot_adaylari/parite_hazirla.py` → gosterge_lab/parite/<TF>.npz; parite_ileri.py → parite_ileri.csv, parite_ileri_ozet.csv; parite_aday.py → parite_aday.json; spot altın; 2026-11-26).
    - **Neden:** tarama bir kombinasyonu 5 piyasanın toplamında ölçüyordu; piyasa başına yalnız adaylar için bakılmıştı. Burada 15m, 1H, 4H'deki takvimsiz bütün kombinasyonlar her piyasada yıl yıl yeniden ölçüldü (180-310 bin kombinasyon; havuzlanmış sonuçla birebir aynı, doğrulandı).
    - **Kayan ileri test:** seçim 2020..C (C = 2021…2025; FX ve altın 2020'den), test C+1..2026. "Yakın" = her yıl ≥ 5 işlem ve artı, her yıl ortalamanın ≥ yarısı, CV ≤ 0,35.
    - **Testte artı çıkan gruplar (yakın; 5 kesimin ortalaması; test yılında kural başına R; işlem başı; rastgele işlem):**
      - altın 4H long: +3,4R/yıl, +0,19R (rastgele 0,00), %79 kârlı, 5/5 kesim;
      - altın 1H long: +1,6R/yıl, +0,04R (+0,02), 4/5;
      - EUR/USD 1H short: +1,5R/yıl, +0,06R (−0,05), 5/5;
      - USD/JPY 4H long: +1,1R/yıl, 4/5.
      - Kalan 26 grup eksi: BTC'nin tümü, EUR ve GBP long, 15m'nin tümü, satışların çoğu.
    - **Seçimde yılda ≥ 10R olanlar, testte:** altın 4H long +6,0R/yıl (%86 kârlı, 5/5), EUR/USD 1H short +3,3R (%73, 5/5), altın 1H long +2,9R (4/5), USD/JPY 4H long +0,2R (2/4). Seçimdeki R/yıl testte kabaca yarıya ya da dörtte bire iniyor.
    - **Yıl yıl:**
      - Altın long kazancı büyük ölçüde altının yükseliş yıllarından geliyor: 4H 2024 +0,21…0,27R, 2025 +0,30…0,33R. 2022 ve 2026'da başabaş civarı, ama rastgele altın alışını her yıl ~0,1R geçiyor.
      - EUR/USD 1H short 2024'ten beri neredeyse her yıl rastgele satıştan +0,04…0,17R iyi.
    - **Bugünkü adaylar (parite_aday.json, örnekler):**
      - altın 4H long "Stokastik yüksek · son mum yükselişle kapandı" (yılda 34 işlem);
      - altın 1H long "EMA20 > EMA50 · MACD histogramı yüksek · fiyat dünkü pivotun belirgin üstünde" (yılda 89);
      - EUR/USD 1H short "Fiyat DEMA20'nin belirgin üstünde · Elder boğa gücü yüksek" (yılda 164).
      - Geçmişte yılda 10-21R gösteriyorlar; gerçekçi beklenti test sonuçlarındaki kadar (yılda 3-6R).
    - **Dikkat:** 30 grup denendi, 3-4'ü artı. Altın 4H long farkı büyük ve tutarlı; diğerleri küçük. Altın kuralları altın trendine bağlı; ayı piyasasında kaybettirir.

88. **Uzun veri (altın 2010+, dövizler 2012+): altın 4H long'un gücü 2020-2026 altın boğasına aitmiş; en tutarlı küçük avantaj EUR/USD 1H short** (`arastirma/gosterge_lab/uzun_veri.py` → arastirma/veri_uzun/; LAB_UZUN=1 ile hazirla2 → veri2_uzun, parite_hazirla → parite_uzun/; `bot_adaylari/parite_uzun.py` → parite_uzun_A.csv, parite_uzun_B.csv, parite_uzun_B_ozet.csv; 2026-11-26).
    - **Veri:** HistData altın 2010-01 → 2026-11-13 (yılda ~342 bin dakika, eksiksiz). FXCM EUR/USD, GBP/USD, USD/JPY 2012 → 2019 indirildi (her yıl 52-53 hafta), 2020+ akademinin deposundan kopyalandı. FXCM 2012'den eskiyi vermiyor. BTC aynı (2017+). Akademi uygulamasına dokunulmadı.
    - **A. Geriye dönük sınav** (kısa testte 2020-2026 ile seçilen kurallar; 2010-2019 seçimde hiç görülmedi):
      - Altın 4H long (73 kural): 10 yılın 6'sında eksi. 2012-2015 altın ayı piyasasında işlem başı −0,11…−0,30R. 2010-19 ortalaması −0,03R/işlem, kural başına −0,4R/yıl. Rastgele altın alışından ortalama ~+0,05R iyi. "Günlük EMA200 üstü" filtresi kurtarmadı (−0,03R).
      - Altın 1H long karışık.
      - EUR/USD 1H short (81 kural): 8 yılın 6'sında artı, ortalama +0,02R/işlem, rastgele satıştan ortalama +0,08R iyi.
      - USD/JPY 4H long karışık.
    - **B. Uzun kayan test, yalnız 1-2 koşullu kurallar** (her test yılı için seçim önceki bütün yıllardan; 3-4 koşullular 2017-2022'ye göre seçildiği için alınmadı):
      - "Her yıl artı" kurallar bir sonraki yılda: USD/JPY 4H long +1,2R/yıl (11 yılın 6'sı artı), EUR/USD 1H short +1,1R/yıl (10 yılın 6'sı), diğerleri ≤ 0. Altın 4H long −0,5R/yıl.
      - "Yakın" süzgeci uzun pencerede çok az kural bırakıyor; sonuçlar gürültülü.
    - **Örnek, 2018 sonu seçimi** (kullanıcının sorusu; 1-2 koşullu, 15m/1H/4H, altın 2011-2018, dövizler 2012-2018 her yıl ≥ 5 işlem ve artı):
      - 2.255 kural-parite seçildi; seçimde yılda 4-19R yapıyorlardı. Evren ~1,15 milyon ikili; her yıl artı olma olasılığı ~%30-50 olan avantajsız bir kural 7-8 yıl üst üste şansla da artı olabilir, beklenen şans sayısı yüzlerle binler arası.
      - 2019-2026, kural başına medyan yıllık R: 2019 −4,3, 2020 −4,6, 2021 +2,6, 2022 +3,0, 2023 −0,7, 2024 −3,1, 2025 −3,0, 2026 −1,3. İşlem başı −0,06…+0,05R; kârlı kural payı %33-60.
      - Tutan tek büyük grup USD/JPY 4H long: 317 kural, 2019-26 toplamı medyan +11,7R, %73'ü kârlı.
    - **Sonuç:** uzun geçmiş şansı büyük ölçüde temizledi. Kalan avantajlar küçük: kural başına yılda ~1-3R, işlem başı +0,02…0,06R. Altın long kuralları rejime (altın boğası) bağlı. Bot için en makul aday EUR/USD 1H short; o da maliyete yakın.

89. **RSI-2 endeks dışında ve satış yönünde: alış yalnız hisse endekslerinde (ve zayıf olarak büyük ABD hisseleri ve sağlıkta) çalışıyor; emtia, kripto, Türk hisseleri ve paritelerde yok; satış yönü hiçbir yerde kâr etmiyor** (`arastirma/verify_rsi2_genis.py` → verify_rsi2_genis_sonuc.txt; Yahoo günlük, 2003+; 2026-11-27).
    - **Kural:** alış = kapanış > SMA200 ve RSI(2) < 10, ilk kapanış > SMA5'te çık (en çok 10 gün); satış aynası = kapanış < SMA200 ve RSI(2) > 90. Her işlem aynı sembol, 5 yıllık dönem, rejim ve yönde 5 rastgele girişle kıyaslandı (R = ATR, maliyetsiz).
    - **Alış, 2015+, rastgeleye göre fark (se):**
      - endeks +0,28 (0,06), 2015 öncesi +0,20;
      - büyük ABD hisseleri +0,10 (0,05); GOOGL, AMZN, META, MSFT iyi, NVDA ~0, TSLA −0,16;
      - sağlık +0,11 (0,08);
      - emtia −0,02 (0,13): altın +0,05, gümüş −0,24, petrol +0,11, hepsi gürültü;
      - kripto −0,19 (0,13);
      - Türkiye −0,12 (0,08): BIST 100 −0,38;
      - parite +0,01 (2015 öncesi +0,18).
    - **Satış:** RSI-2 satışının kendi sonucu endekste ~0R, büyük hisselerde −0,08R, sağlıkta −0,19R, emtiada −0,36R, kriptoda −0,63R. Rastgele satıştan iyi görünmesi rastgele satışın yükselen piyasada kaybetmesinden. Maliyet sonrası hiçbir grupta kâr yok.
    - **Kümelenme:** alış sinyallerinin SPY sinyaliyle aynı günlere (±1 gün) düşme payı endekste %56, büyük ABD hisselerinde %32, sağlıkta %22, emtia, kripto, parite ve Türkiye'de %13-15. SPY ile günlük korelasyon (2015+): pariteler ~0, altın +0,09, Türk hisseleri +0,11…0,23, petrol, gümüş ve BTC +0,24, büyük ABD hisseleri +0,5…0,75.
    - **Ders:** ilişkisiz piyasalar çeşitlendirir, ama yalnız orada da avantaj varsa. RSI-2'nin avantajı olan yerler (endeks, büyük ABD hisseleri) birbiriyle ilişkili. İlişkisiz piyasalar (emtia, kripto, döviz) kısa vadede dönmüyor, trend yapıyor; onlar için doğru araç trend takibi (17 §2, §7). Kriptoda ve Türk hisselerinde düşüşü almak rastgeleden kötü.

90. **10 prop hesabı almak avantaj yaratmaz: beklenen geçen hesap = 10 × tek hesap olasılığı. Bağımsız denemelerde "en az biri geçer" %72 (-0,10R) ile %98 (0R) arası; aynı işlemi 10 hesapta açınca tek hesapla aynı (%12 / %33)** (`arastirma/verify_10_hesap.py` → verify_10_hesap_sonuc.txt; 09 §4y; 2026-11-27).
    - FTMO 2-Step 100K 540 €, 200K 1.080 €; 10 hesap 5.400 € / 10.800 €. Büyüklük geçme olasılığını değiştirmez.
    - FTMO'da trader başına toplam 400.000 $ sınırı var, aynı anda en fazla 4 × 100K.
    - Art arda alıp geçince durmak, aynı olasılığa ortalama ~6 ücretle ulaşır (-0,10R).
    - **Geç + %10 büyüt + çek** (`verify_10_hesap_cekim.py`): %1 riskle tek hesapta -0,10R %3, 0R %17, +0,10R %46. %90 için 75 / 13 / 4 hesap. Sektör ortalamasında çekim başına net -11.000 $, başa baş ~-0,05R.

91. **Initial balance (IB) setup'ları NQ'da avantajsız, altında maliyet sonrası ~0; "%70 kazanma" ve "2 ayda 100.000 $" desteklenmedi** (`arastirma/verify_ib_fitmom.py` → verify_ib_fitmom_sonuc.txt; 04 §6b-7; 11 #93; 2026-11-27).
    - Veri: HistData 1m, NAS100 ve spot altın, 2020-2026, ~1.600 seans. Kıyas: aynı gün rastgele dakikada aynı yön, stop ve hedef.
    - IB ortasına geri çekilme (TC) ve failed auction (FA): NQ'da net -0,02…-0,06R, şansa göre fark t < 1,5. FA ve Asya süpürmesi altında net -0,16…-0,26R.
    - Kazanma oranı en fazla %53 ve her setup'ta hedef/stop geometrisinin başa baş oranına eşit.
    - Tek ipucu altında TC: brütte şanstan +0,10…0,16R iyi (t 2,3-3,6). Ama net ~0, artı yıllar yalnız 2024-2026 altın rallisi ve NQ'da tekrar yok → izleme listesi.
    - 200 $ riskle 2 ayda 104.000 $ tek hesapta günde ~12R demek; ancak çok sayıda kopya hesapla mümkün, bu da beceri değil bahis büyüklüğü.

## Çalışma prensipleri

- Her yeni bilgi **en az iki bağımsız kaynakla** veya simülasyon/test ile doğrulanır. Doğrulanamayan bilgi "pratik kural" ya da "iddia" olarak etiketlenir.
- Kanal değerlendirmesi: içerik doğruluğu, kanıt kullanımı, şeffaflık (satış baskısı, doğrulanmış kayıt) ve yorumlar.
- Yanlış bilgi silinmez, [11](bilgi/11-yanlis-bilgiler-ve-efsaneler.md)'e gerekçesiyle eklenir.

## Araçlar

```bash
# Kurulum (bir kez): python -m venv venv && venv/Scripts/pip install youtube-transcript-api yt-dlp
python arastirma/araclar/fetch.py   <cikti_dizini> <video_id> ...   # metadata + transkript
python arastirma/araclar/subs.py    <cikti_dizini> <video_id> ...   # yedek: yt-dlp altyazı
python arastirma/araclar/channel.py list   <kanal_url>/videos 60    # kanal video listesi
python arastirma/araclar/channel.py search "<sorgu>" 10             # YouTube arama
python arastirma/araclar/channel.py comments <video_id> 20          # en iyi yorumlar
python arastirma/verify_math.py ; python arastirma/verify_ftmo.py   # doğrulama simülasyonları
```
⚠️ YouTube kısa sürede çok istekte 429 (hız sınırı) veriyor. Videoları 8-10 sn arayla, 10-15'lik partiler halinde çek.
