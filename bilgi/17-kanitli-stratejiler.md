# 17 — Kanıtlı Stratejiler: Akademik Kanıt, Yayın Sonrası Erime ve FTMO'ya Uygunluk

> **Amaç**: Bu bilgi tabanının kendi testlerini (12, 15, README #30-48) **dış kanıtla** genişletmek. Hangi stratejinin maliyetten sonra kalıcı bir avantajı olduğuna dair en güçlü kanıt var, hangisi küçük bir perakende/prop hesabında (FTMO 10K: günlük %5, toplam %10 zarar, +%10 hedef) kullanılabilir?
> **Derece**: ✔ güçlü kanıt, örneklem dışında tekrarlandı · ◐ kısmi/karışık kanıt ya da sayı doğrulanamadı · ✘ kanıt yok ya da çürütüldü.
> **Tarih**: 2026-11-25. Sayıların hepsi kaynaklardan. İkincil özetten gelen ya da tam doğrulanamayanlar ◐ ile işaretli. "Bkz. 12" gibi göndermeler bu bilgi tabanındaki dosyalardır.

## Özet

- **Literatürün çoğu yayından sonra eriyor.** 97 anomalide getiri örneklem dışında %26, yayından sonra %58 düşüyor (McLean ve Pontiff 2016). 452 anomalinin %65'i t > 1,96 eşiğini bile geçemiyor (Hou, Xue, Zhang 2020). Sonradan bulunan bir etki için çıta **t ≥ 3** (Harvey, Liu, Zhu 2016).
- **En güçlü kanıt: çok piyasalı, volatiliteye göre boyutlanmış trend takibi (3-12 ay)** ✔. 58 vadelinin 58'inde pozitif (1985-2009). 1880-2016 arasında her on yılda pozitif. Ama 2010'larda zayıfladı, 2022'de rekor yaptı. Tek piyasada kanıt zayıf (Huang vd. 2020). Bu, bilgi tabanının bulgusuyla aynı: tek piyasa Sharpe 0,20, 19 piyasa 0,55 (README #38).
- **Hızlı teknik kurallar öldü.** BLL'nin (1992) kuralları 1987-96 örneklem dışında çalışmadı. Dövizde filtre ve hareketli ortalama kârları 1990'ların başında kayboldu. Düşük maliyet bile 1897-2011 kâr tablosunu siliyor. Formasyonlar "bilgi taşıyor" ama kâr kanıtı yok.
- **Takvim etkilerinin çoğu ya öldü ya zayıf.** FOMC öncesi drift (+49 bp) 2015 sonrası kayboldu. PEAD büyük hisselerde 2006'dan beri yok. Ay dönümü uzun dönemde güçlü, 1990 sonrası tartışmalı ◐.
- **Gün içi piyasa momentumu** akademik olarak güçlü (60+ vadeli, 1974-2020) ve FTMO'nun "gün sonunda düz" yapısına en uygun aday. Ama bu bilgi tabanının son 2 yıllık verisinde tekrarlanmadı, yerine son yarım saatte dönüş çıktı (README #32). Durum ◐.
- **FX carry** akademik olarak gerçek (Sharpe ~0,7), ama çarpıklığı negatif, 2008 sonrası zayıf ve CFD'de getirinin kendisi olan swap'tan broker payı kesiliyor. Prop için ✘.
- **Kripto trend** güçlü ama kısa geçmişli ◐. Yüksek oynaklık, 10K hesapta lot granülerliği ve bilinmeyen swap maliyeti sorun.
- **Sharpe → FTMO çevirisi** (yeni simülasyon, §9): avantaj yokken iki aşamayı geçme ~%30. Maliyet sonrası Sharpe 0,5 ve %8-10 volatiliteyle ~%57 geçer, ~%35 kalır, medyan 14-19 ay. Sharpe 1,0 ile ~%80. **Literatürdeki Sharpe'lar brüt ve futures içindir.** CFD'de finansman payı × brüt nominal (1-3 kat) düşülür.
- **Sıralama** (§11): (1) çok piyasalı trend, (2) trend + endeks long karışımı, (3) endekste kısa vadeli dönüş, (4) gün içi endeks momentumu, ileri testle, (5) kripto trend, küçük pay. Kanıtı olmayanlar: formasyonlar, Fibonacci, tek enstrümanda kısa vadeli MA ve kırılım, maliyet sonrası ORB, perakende scalping ve order flow, FOMC drift.

---

## 1. Önce filtre: yayın sonrası erime ve çoklu test

| Çalışma | Bulgu | Senin için anlamı |
|---|---|---|
| **McLean ve Pontiff (2016, JF)**, 97 hisse getirisi öngörücüsü | Getiri örneklem dışında **%26**, yayından sonra **%58** düşük. Aylık ortalama: örneklem içi %0,582 → yayın öncesi örneklem dışı %0,402 → yayın sonrası %0,264. Örneklem içi getirisi yüksek olanlar daha çok eriyor, arbitrajı pahalı olanlar daha az. | Yayımlanmış bir etkinin bugünkü değeri ≈ makaledekinin **yarısı**. |
| **Harvey, Liu, Zhu (2016, RFS)** | 316 "faktör" önerilmiş. Yeni bir faktör için gereken çıta **t > 3,0**. "Finansal ekonomideki iddiaların çoğu muhtemelen yanlış." | Sonradan, veriye bakarak bulduğun bir etki (ör. README #32 son yarım saat dönüşü) için **2 se yetmez, ~3 se iste.** 15 §1'deki "≥2 se" ölçütü önceden tanımlı hipotezler içindir. |
| **Hou, Xue, Zhang (2020, RFS)**, "Replicating Anomalies" | Mikro hisseler kontrol edilince 452 anomalinin **%65'i** \|t\| > 1,96'yı, **%82'si** t > 2,78'i geçemiyor. İşlem sürtünmesi kategorisinin %96'sı başarısız. Tekrarlananların büyüklüğü de raporlanandan çok küçük. | Küçük, likit olmayan hisselerden gelen "avantaj" senin piyasalarına taşınmaz. |
| **Jensen, Kelly, Pedersen (2023, JF)**, karşı görüş | Bayesçi yaklaşımla ABD'de temel tekrarlanma oranı ~%56, CAPM alfasıyla **%83**, 93 ülkede de benzer. Faktörlerin çoğu 13 temaya toplanıyor. | Kesitsel faktörlerin bir çekirdeği gerçek. Ama hepsi **çok hisseli long/short portföy** ister. FTMO CFD evreninde uygulanabilir değil (§3). |

**Ders (15 §1'e ek)**: (a) Etkinin yayım tarihini bil ve sadece yayından sonraki veriye güven. (b) Önceden kayıtlı test → ≥2 se, sonradan bulunan → ≥3 se. (c) Akademik bir sonuç "çoklu piyasa + 100 yıl + örneklem dışı" değilse ◐ say.

---

## 2. Zaman serisi momentumu / trend takibi ✔ (çok piyasalı) · ◐ (tek piyasa)

**Ana kanıt**
- **Moskowitz, Ooi, Pedersen (2012, JFE)**: 58 likit vadeli ve forward (endeks, döviz, emtia, tahvil), 1985-2009.
  - 12 aylık TSMOM **58 enstrümanın 58'inde** pozitif, 52'si %5 düzeyinde anlamlı.
  - Getiriler 1-12 ay sürüyor, daha uzun vadede kısmen tersine dönüyor (önce eksik tepki, sonra aşırı tepki).
  - Çeşitlendirilmiş portföyün brüt Sharpe'ı **> 1**, hisse piyasasının ~2,5 katı. Standart faktörlere maruziyeti az. **En iyi performans uç piyasalarda.**
  - 1966-1985 (örneklem dışı) Sharpe **1,1**.
- **Hurst, Ooi, Pedersen (2017, JPM)**, "A Century of Evidence": 67 piyasa (29 emtia, 11 endeks, 15 tahvil, 12 döviz), **1880-2016**. 1, 3 ve 12 aylık sinyaller eşit ağırlıklı, %10 volatilite hedefi, maliyet ve 2/20 ücret düşülmüş.
  - **Her on yılda pozitif.** Üç sinyal hızı da her on yılda pozitif. Sinyal 1 ay gecikmeyle uygulanınca kısa sinyaller belirgin zayıflıyor.
  - Piyasa başına ortalama Sharpe ~**0,4** (brüt). 1985 öncesi her piyasada da tutarlı, yani MOP'a göre örneklem dışı.
  - 60/40 portföyünün en büyük 10 düşüşünün **8'inde pozitif**. En kötü dönemleri: çok piyasada aynı anda sert dönüşler ve uzun trendsiz dönemler. En büyük düşüş **%25'e kadar** (%10 volatilitede).
  - ◐ İkincil özetlere göre (2014 sürümü) yıllık brüt %14,9, ücret sonrası %11,2, volatilite ~%9,7, Sharpe ~0,77. Tablolar görüntü olduğu için doğrudan okunamadı.

**Erime ve eleştiri**
- **2010'lar zayıf**: AQR, "You Can't Always Trend When You Want" (2019/2020). Sebep stratejinin bozulması değil, **piyasa hareketlerinin küçük olması**. Trend yakalama verimliliğinde ve çeşitlendirmede yapısal bir değişim bulunmadı.
- **2022**: SG Trend Endeksi **+%27,3**, 2000'den beri en iyi yıl (basın, ◐ kesin sayı için SG verisi).
- **Huang, Li, Wang, Zhou (2020, JFE)**: Varlık bazında zaman serisi regresyonlarında TSMOM'un kanıtı az. Havuzlu t istatistiği bootstrap kritik değerlerinin altında. TSMOM stratejisinin kârı, öngörü gerektirmeyen "geçmiş ortalama" stratejisinin kârıyla **neredeyse aynı**. → **Tek piyasada "trend var mı" sorusu ◐. Kâr, çeşitlendirme ve volatilite ölçeklemesinden geliyor.**

**Bu bilgi tabanıyla uyum**
- ✔ Hız: Hurst'te gecikmeli kısa sinyaller zayıflıyor. Carver testinde ≤1 aylık kurallar maliyetten sonra ≤0 (12, README #41). Uyumlu.
- ✔ Çeşitlendirme: Tek piyasa Sharpe 0,20, 19 piyasa 0,55 (README #38). Huang vd. ile aynı mesaj.
- ✔ 12 ay kuralı 2015 sonrası Sharpe 0,61 (12). AQR'nin "2010'lar zayıf" bulgusundan iyi, çünkü bu bilgi tabanının testi 2022'yi içeriyor ve küçük bir evren kullanıyor. Büyük ihtimalle tek bir çekiliş.
- Döviz: bilgi tabanının testinde ~0 (12). Literatürde dövizler portföy içinde pozitif, ama tek başına bir avantaj kaynağı sayma.

**Pratik profil**: Tutma süresi haftalar-aylar (Parker: ~1 yıl). Piyasa başına yılda birkaç sinyal dönüşü, artı aylık yeniden boyutlama (README #39). %10 volatilitede maksimum düşüş tarihsel olarak ~%25. %10'luk FTMO limiti için hedef volatilite **%6-8** (README #36: %6'da %70 geçer, %4 kalır, ~2,4 yıl).

---

## 3. Diğer akademik faktörler: çoğu gerçek ama FTMO'da uygulanamaz

| Faktör | Kanıt | Erime / risk | FTMO |
|---|---|---|---|
| **Kesitsel momentum** (hisse) | Jegadeesh ve Titman (1993): 3-12 ay kazananı al, kaybedeni sat. 6/6 stratejisi ~%1/ay (1965-89). ✔ | **Çöküş riski** (Daniel ve Moskowitz 2016): Mart-Mayıs 2009'da kaybeden desil +%163, Temmuz-Ağustos 1932'de +%232 (short bacak patlıyor). Lou, Polk, Skouras (2019): momentum getirisi neredeyse tamamen **gece** oluşuyor (gece 3F alfa %0,95/ay, gün içi %0,11, ◐ çalışma kâğıdı). | ✘. Onlarca hisse CFD'si long/short, swap ve spread gerekir. Gün içi kapanan hesap getirinin oluştuğu geceyi kaçırır. |
| **Döviz momentumu** | Menkhoff, Sarno, Schmeling, Schrimpf (2012): yıllık %10'a kadar. ◐ | Yazarlar: "çok etkili **arbitraj sınırları**" var, getiri likit olmayan kurlarda ve maliyetli. | ✘. Majörlerle sınırlı evrende zayıf. |
| **Kısa vadeli dönüş** | Jegadeesh (1990), Lehmann (1990). De Groot, Huij, Zhou (2012): büyük hisselerle sınırlanınca, kurumsal gerçek maliyetle **haftada 30-50 bp net** (1998-2011, 19 piyasa). ◐ | Novy-Marx ve Velikov (2016): aylık devri **%50'yi aşan** anomalilerin azı maliyet sonrası anlamlı kalıyor. | Endeks düzeyindeki karşılığı **RSI-2** (12, README #46): 2015 sonrası rastgeleden +0,17R. İşlem başı ✔, portföy düzeyinde zayıf. |
| **Carry** (FX) | Koijen, Moskowitz, Pedersen, Vrugt (2018, JFE): döviz carry Sharpe **0,68**, çarpıklık **-0,68**. Tüm sınıflarda global carry Sharpe 1,2. ✔ (akademik) | Brunnermeier, Nagel, Pedersen (2008): **çöküş riski**, faiz farkı büyüdükçe çarpıklık daha negatif. Global carry'nin en büyük düşüşleri 1972-75, 1980-82 ve 2008-09. G10 carry ETF'i (DBV, 2006) **Mart 2023'te tasfiye edildi**. | ✘. CFD'de carry getirisinin kendisi swap'tır, broker iki yönde de pay keser. FTMO swap tablosu yayımlanmıyor (09 §4i). Negatif çarpıklık ile %5 günlük limit kötü bir kombinasyon. |
| **Değer** (HML) | Fama-French. Uzun dönemde ✔. | 2007-2020 düşüşü ~%55, başlangıç tarihine göre tarihin en uzun ve derin düşüşü (◐ ikincil). | ✘ (hisse L/S). |
| **Düşük volatilite / BAB** | Frazzini ve Pedersen (2014). | Novy-Marx ve Velikov (2022): sonuçların bir kısmı standart dışı beta tahmininden ve fiilen eşit ağırlık / küçük hisse ağırlığından geliyor. Maliyet kârlılığı belirgin düşürüyor. ◐ | ✘. |
| **PEAD** (bilanço sonrası drift) | Bernard ve Thomas (1989). | Martineau (2022): **büyük hisselerde 2006'dan beri yok**, mikro hisselerde de yakın zamanda kayboldu. 2025'te iki makale itiraz ediyor. ✘/◐ | ✘. Bilanço boşluğu da -10R'ye ulaşabilir (02 §6e). |

**Volatilite yönetimi notu** (README #39 ile bağlantılı): Moreira ve Muir'in (2017) "volatiliteye göre ölçekle, Sharpe artar" bulgusu gerçek zamanlı testte çoğu faktörde tutmadı (Cederburg vd. 2020). İstisnalar momentum, ROE ve BAB. Yani volatilite ölçeklemesini **Sharpe artırıcı olarak değil, kuyruk ve günlük limit kontrolü olarak** kullan. Bilgi tabanının testi de bunu gösterdi: en kötü gün -%7,1'den -%3,8'e indi.

---

## 4. Gün içi ve takvim etkileri

### 4a. Gün içi piyasa momentumu ◐ (akademik ✔, güncel veride çelişkili)
- **Gao, Han, Li, Zhou (2018, JFE)**: SPY 1993-2013. Önceki kapanıştan itibaren ilk yarım saatin getirisi son yarım saati öngörüyor. R² örneklem içi **%1,6**, örneklem dışı **%1,2**. Volatilite ve hacimle güçleniyor.
- **Baltussen, Da, Lammers, Martens (2021, JFE)**: 60+ vadeli (hisse, tahvil, emtia, döviz), **1974-2020**. "Günün geri kalanı → son 30 dakika" momentumu **her piyasada** var ve sonraki günlerde tersine dönüyor. Mekanizma: opsiyon kurucularının ve kaldıraçlı ETF'lerin **gamma koruması**. Net pozitif gamma günlerinde etki yok.
- 16 gelişmiş hisse piyasasının 12'sinde (Li, Sakkas, Urquhart 2022, ◐ künye). Bitcoin'de de var (Shen, Urquhart, Wang 2022).
- **Uygulama makalesi** (Zarattini, Aziz, Barbon 2024, ◐ yazarların da satıcı olduğu pratisyen çalışma): SPY'da 14 günlük "gürültü bandı" dışına çıkınca yarım saatlik kontrolle trend yönünde gir, gün sonunda kapat. **2007-2024 net yıllık %19,6, Sharpe 1,33, maksimum düşüş %25.** Ama günlük %2 volatilite hedefi ve 4 kata kadar kaldıraç var, sonuçlar örneklem içi.
- **⚠️ Bu bilgi tabanıyla çelişki**: Gao tipi ilk yarım saat → son yarım saat, son 2 yılın 1 saatlik verisinde tekrarlanmadı. Onun yerine **son yarım saatte dönüş** çıktı (README #32, 04 §6b-4). Baltussen'in mekanizması bunu açıklayabilir: piyasa yapıcıların net gamma'sı pozitifken momentum kaybolur, hatta dönüş görülebilir. Gamma rejimi değiştiyse işaret değişir. **Rejime bağlı bir etki için 2 yıl kısa.**
- **FTMO uygunluğu yüksek**: gün sonunda düz (Standart hesap), endeks CFD'lerinde komisyon yok, günde ≤1 işlem. Ama ölçek: günlük %2 volatilite hedefinde %5'lik günlük limit 2,5σ uzakta. Kalın kuyrukla bu birkaç ayda bir demek. Volatiliteyi günlük %0,5-0,7'ye indir: aynı Sharpe ile beklenen getiri orantılı olarak yıllık ~%5-7 (◐ kaba ölçekleme).

### 4b. Açılış aralığı kırılımı (ORB) ✘ (maliyetten sonra)
- Zarattini ve Aziz (2023): QQQ'da 5 dakikalık ORB, 2016-2023: yıllık %33,2'ye karşı al-tut %14,9 (CXO özeti). **Kayma sıfır varsayılmış**, 4 kat kaldıraç var.
- Bağımsız tekrar (MQL5 blogu, ◐ zayıf kaynak, yazar ürün satıyor): 5 endeks CFD'si, 2015-2026, kural değiştirilmeden. Brüt **+0,05 ile +0,13R**, makaledeki NQ sonucu tutuyor. Spread ve kayma eklenince **-0,08 ile +0,00R**, beşte dördü negatif. İlk 5 dakikalık mumun küçük bir yön bilgisi var, ama maliyet kadar.
- **Bu bilgi tabanının bulgusuyla aynı**: ORB maliyetli olarak rastgele girişten farksız (README #31).

### 4c. Gece etkisi ◐ (gerçek ama CFD'de swap yiyor)
- Hisse endekslerinde getirinin büyük kısmı gece oluşuyor (Cliff, Cooper, Gulen 2008; Kelly ve Clark 2011). Bilgi tabanında SPY 2018+ gece Sharpe 0,61, gün içi 0,15 (12).
- **Altın**: COMEX altın vadelisinde, Londra fixinde, altın madencilerinde ve fonlarında gece getirisi pozitif, gündüz getirisi negatif (Blose vd., 1985-2012). Asimetri "önemli ölçüde zayıfladı ama hâlâ var". ◐
- **FTMO**: Standart hesapta 2 saatten kısa günlük aralar sorun değil, yani gece taşımak serbest, hafta sonu yasak (09 §4i). Ama swap gece başına ~2 bp, gece getirisi ~3 bp (12). Tek başına işlem olarak ✘. **İcra eğilimi olarak** kullan: zaten long alacaksan kapanışa yakın al, açılışa yakın sat (Carver, 12).

### 4d. Takvim etkileri
| Etki | Kanıt | Bugünkü durum | Not |
|---|---|---|---|
| **Ay dönümü** (ayın son günü + ilk 3 gün) | McConnell ve Xu (2008): 1926-2005. TOM günlerinde günlük ortalama %0,15 (değer ağırlıklı), ayın diğer 16 gününde **-%0,001**. Yani ortalamada piyasa riskinin karşılığı yalnızca ay dönümünde alındı. 35 ülkenin 31'inde var. | ◐. Maberly ve Waggoner (2000): S&P'de 1990 sonrası kayboldu. Carchano ve Pardo (2011): S&P vadelilerinde net kârlı kalan tek takvim etkisi (ikincil). 2025'te "kaybolan TOM" başlıklı bir makale var (okunamadı). | Yılda 12 işlem, 4 gün tutma. Pencere çoğunlukla hafta sonu içerir → değerlendirmede ya da **Swing** hesapta. Tek başına prop aracı değil (README #30 formülü), ama long endeks pozisyonları için **zamanlama filtresi** olabilir. Kendi verinde test et. |
| **FOMC öncesi drift** | Lucca ve Moench (2015): 1994-2011, planlı FOMC kararından önceki 24 saatte S&P **+49 bp** (t > 4,5). Yıllık hisse prim getirisinin ~%80'i. | ✘. Kurov, Wolfe, Gilbert (2021): **2015 sonrası esasen kayboldu.** | Yayın sonrası erimenin ders kitabı örneği. |
| **Halloween** ("Mayısta sat") | Jacobsen ve Zhang: 108 piyasa. Son 50 yılda Kasım-Nisan ile Mayıs-Ekim farkı %6,25 (2012 sürümü). Yazarlara göre son yıllarda güçlenmiş. ◐ | 6 aylık bir rejim, ayrıca tek bir gözlem/yıl. İstatistiksel güç düşük. | Prop aracı değil. |
| **FX seans deseni** | Breedon ve Ranaldo (2013): kurlar **kendi yerel seans saatlerinde değer kaybetme** eğiliminde (yerel katılımcılar kendi saatlerinde net döviz alıcısı). 2011 sürümüne göre EUR/USD'de basit strateji kârlı. ◐ | Yayın sonrası ve maliyetli test görmedim. | Bilgi tabanının "seans" testleri (Asya uçları, README #40) farklı bir iddia. Bu desen test edilmeye değer bir aday. |

---

## 5. Teknik analiz: klasik kurallar ve formasyonlar ✘

- **Brock, Lakonishok, LeBaron (1992)**: 26 MA ve kanal kuralı, DJIA 1897-1986. Hepsi nakitten iyi.
- **Sullivan, Timmermann, White (1999, JF)**: 7.846 kurallık evren, Reality Check bootstrap.
  - 1897-1986'da bazı kurallar data snooping düzeltmesinden sonra bile üstün.
  - **1987-1996 örneklem dışında** en iyi kuralın üstün olmama olasılığı ~%12, yani "ekonomik değerin kanıtı çok az".
  - **S&P 500 vadelisinde (1984-96) üstünlük yok.**
  - En iyi kural yılda 63 işlem yapıyor, başa baş maliyeti işlem başına %0,27.
- **Bajgrowicz ve Scaillet (2012, JFE)**: DJIA 1897-2011, aynı kural evreni, yanlış keşif oranı (FDR) kontrolü. **Düşük işlem maliyetleri bile örneklem içi performansı tamamen siliyor.** En iyi kuralları önceden seçmek mümkün değil.
- **Park ve Irwin (2007)**: 95 modern çalışmanın 56'sı pozitif, 20'si negatif, 19'u karışık. Kârlar "en azından 1990'ların başına kadar". Pozitif sonuçlar data snooping, sonradan kural seçimi ve maliyet tahmini sorunlarıyla zayıflıyor.
- **Döviz**: Neely, Weller, Ulrich (2009): 1970-80'lerdeki TA kârları gerçek, ama **filtre ve MA kurallarının kârları 1990'ların başında kayboldu.** Uyarlanabilir piyasa hipotezi: bilinen kural zamanla erir.
- **Formasyonlar**: Lo, Mamaysky, Wang (2000): çekirdek regresyonla otomatik formasyon tanıma, ABD hisseleri 1962-1996. Bazı formasyonlar getiri dağılımına **"artımsal bilgi"** katıyor, ama **kârlı işlem kuralı gösterilmedi.** Bilgi tabanının mum formasyonu testiyle uyumlu: "isabet" büyük ölçüde geometri (README #29).
- **Perakende döviz trader verisi** ◐: Abbey ve Doukas (2015): 428 hesap, 2004-09. Çalışma kâğıdına göre ~%25'i maliyetten sonra anormal getiri sağlıyor. Aynı veriyle yapılan tezde **teknik analiz kullanımı performansla negatif ilişkili.** ESMA (2018): ulusal düzenleyicilerin verisinde perakende CFD hesaplarının **%74-89'u** para kaybediyor.
- **Bu bilgi tabanının ✘ listesiyle uyum**: Fibonacci (README #9), mum formasyonları (#29), Keltner ve Bollinger (#73), filtresiz sweep ve SFP (#19, #51), PDH/PDL seviyeleri (#20), Market Profile %80 (#50). Literatürle **çelişen tek bulgu yok.**

**Ayrım**: "Teknik analiz çalışmaz" ile "trend takibi çalışır" çelişmez. Fark: (1) çok piyasa, (2) yavaş hız (haftalar-aylar), (3) volatiliteye göre boyut, (4) tek kural. Parker'ın ayrımıyla aynı (12).

---

## 6. Gün içi işlem, scalping ve emir akışı ✘ (perakende için)

- **Day trader sonuçları**: bkz. 08 (Barber vd. Tayvan: <%1 kalıcı kâr; Chague vd. Brezilya: %97 zarar). Burada tekrarlanmıyor.
- **Yüksek frekans rakip**: Baron, Brogaard, Hagströmer, Kirilenko (2019, JFQA): HFT geliri az sayıda firmada yoğun. **Göreli gecikmedeki küçük farklar gelirde büyük farklar yaratıyor.** Kolokasyon yükseltmesi performansı artırıyor. Saniye ölçeğindeki avantaj gecikme yarışıdır, perakende CFD platformu bu yarışta değil.
- **Emir akışı eş zamanlıdır, öngörü değil**:
  - Cont, Kukanov, Stoikov (2014): emir defteri dengesizliği (OFI) ile kısa ölçekli fiyat değişimi arasında doğrusal ilişki var, ortalama R² ~%65 (◐ tek alıntı). Ama aynı zaman aralığında.
  - Evans ve Lyons (2002): bankalar arası emir akışı DM/$ günlük değişiminin ~%60'ını açıklıyor. Bu da eş zamanlı, ve veri perakendede yok.
  - CFD'de hacim tick hacmidir (06). Footprint ve delta okumasının **öngörü** gücüne dair hakemli bir kanıt bulunamadı. Ancak icra (giriş zamanlaması) aracı olabilir.
- **FTMO maliyetleri** (resmi güncellemeler):
  - FX: **2,5 $/lot/taraf** (29 Eylül 2025'ten beri, öncesi 1,5 $). Yani 5 $ gidiş-dönüş + spread.
  - Endeks: komisyon yok.
  - Metal ve enerji: %0,0007/taraf.
  - Kripto: **%0,0325/taraf** (Temmuz 2025).
  - Swap: sembol bazında, platformdan kontrol et.
  - Scalp matematiği için bkz. README #12, #47 (0,25R hedefte geçme %5).

---

## 7. Kripto ◐

- **Liu ve Tsyvinski (2021, RFS)**: Kripto getirileri hisse, döviz ve makro faktörlere maruz değil. Onları kriptoya özgü iki şey öngörüyor: **zaman serisi momentumu** ve **yatırımcı ilgisi** (Google aramaları).
  - Bitcoin'de bu haftanın getirisinde 1 standart sapma artış, sonraki 1, 2, 3 ve 4. haftaların getirisini sırasıyla **+%3,16, +%3,66, +%3,49 ve +%1,50** artırıyor. Günlükte de var.
  - 2013 sonrası alt örneklemde ve önden bakmasız kesimde de tutuyor. Ethereum'da daha zayıf.
  - ⚠️ Haftalık 1 standart sapma = **%16,6**, yani erken dönemin aşırı oynaklığı. Bugünkü büyüklük daha küçük olmalı.
- **Liu, Tsyvinski, Wu (2022, JF)**: Kesitsel kripto momentumu (2014-2018) büyük coinlerde haftalık %4,2 ve anlamlı, küçük coinlerde anlamsız.
- **Zarattini, Pagani, Barbon (2025)** ◐: En likit 20 coinlik dönen portföy, farklı geriye bakışlı Donchian kanallarının topluluğu, volatiliteye göre boyut. Hayatta kalma yanlılığı olmayan veri, 2015+. **Net Sharpe > 1,5, Bitcoin'e karşı yıllık alfa %10,8.** Tek ekip, örneklem içi, ayrı bir örneklem dışı test yok.
- Grobys, Ahmed, Sapkota (2020): 20 günlük değişken MA kuralı Bitcoin **hariç** coinlerde yıllık %8,76 fazla getiri. ◐
- Bitcoin'de gün içi momentum (ilk yarım saat → son yarım saat, hacimle tanımlanan işlem zamanı): Shen, Urquhart, Wang (2022). ◐
- **FTMO'da pratik sorunlar**:
  - Komisyon %0,0325/taraf. Swap bilinmiyor, platformdan kontrol et.
  - Sembol başına hacim tavanı var (BTCUSD 5 lot).
  - **10K hesapta lot granülerliği**: %10 volatiliteli çok piyasalı bir portföyde piyasa başına risk bütçesi yıllık ~%1-2 volatilite. BTC'nin ~%60 volatilitesiyle bu ~200-300 $ nominal eder. Asgari lot (0,01 lot ≈ 0,01 BTC ◐) çok daha büyük olabilir. **Kontrat büyüklüğünü kontrol et**, gerekirse kripto payını düşür ya da 10K'da dışarıda bırak.
  - Kripto hafta sonu da işlem görür. FTMO bakım saatleri nedeniyle hafta sonu saatlerinin değişebileceğini söylüyor. Standart hesapta "2 saatten uzun ara" kuralının kriptoya nasıl uygulandığı **belirsiz**, FTMO'ya sor.
- Clenow: "Temel değeri sıfır, ama psikolojiyle hareket ettiği için trendleri var" (12). Literatür trend tarafını destekliyor.

---

## 8. Altın, petrol ve döviz özelinde

- **Altın**: TSMOM evreninde 1880'den beri var (Hurst vd.). Gece/gündüz asimetrisi zayıflayarak sürüyor (Blose vd.). ⚠️ Kısa dönem başarısını yönle karıştırma: 2025'in son çeyreğinde rastgele long girişler +0,22R verdi (README #69).
- **Petrol ve doğalgaz**: Trend portföyünün en oynak kolları. Hacmi küçük tut. Bilgi tabanında emtiada trailing çıkış zaman testinden geçti (README #46, 03). Brandt'ın kırılım avantajı emtiada var, paritede ve endekste yok (README #55).
- **Döviz**: (1) TA kuralları 1990'larda öldü (Neely vd.). (2) Basit trend bilgi tabanında ~0 (12). (3) Carry 2008 sonrası zayıf ve CFD'de swap payı var. (4) Seans deseni (Breedon ve Ranaldo) test edilmemiş bir aday. → FX, FTMO'da **en ucuz çeşitlendirici kol**, ama tek başına avantaj kaynağı değil.
- **Tarım CFD'leri**: FTMO Eylül 2023'ten beri kakao, kahve, mısır, soya ve buğday sunuyor. Bunlar trend portföyüne gerçek çeşitlendirme katar (Parker'ın kakao örneği, 12). Ama **Eylül 2024'ten beri asgari pozisyon 1,00 lot**, yani 10K hesapta risk boyutu kaba olabilir. Kontrat değerini kontrol et.

---

## 9. Sharpe'tan FTMO sonucuna: genel çeviri tablosu (yeni simülasyon)

**Model**: Günlük getiriler bağımsız, kalın kuyruklu (Student-t, df = 4). Sabit %10 toplam limit ve başlangıç bakiyesinin %5'i günlük limit (gün sonu kapanışla yaklaşık). Aşama 1 +%10, aşama 2 +%5, aşama başına en fazla 3 yıl. Her hücre için 20.000 yol. Sharpe **maliyet sonrası** değerdir. Script: `arastirma/verify_sharpe_ftmo.py`.

| Sharpe (net) | Yıllık vol | İki aşamayı geçer | Kalır | 3 yılda bitmez | Medyan süre (ay) |
|---|---|---|---|---|---|
| 0 | %8 / %10 / %15 | %27 / %31 / %30 | %57 / %65 / %70 | %15 / %5 / 0 | 21 / 15 / 7 |
| 0,3 | %8 / %10 / %15 | %45 / %47 / %41 | %41 / %49 / %59 | %14 / %4 / 0 | 21 / 15 / 7 |
| **0,5** | %5 / **%8** / %10 / %15 | %43 / **%58** / %56 / %48 | %10 / **%31** / %40 / %52 | %46 / %11 / %3 / 0 | 31 / **19** / 14 / 7 |
| 0,8 | %5 / %8 / %10 / %15 | %65 / %75 / %70 / %58 | %5 / %19 / %28 / %42 | %30 / %6 / %2 / 0 | 29 / 18 / 13 / 7 |
| **1,0** | %5 / **%8** / %10 / %15 | %77 / **%82** / %78 / %64 | %3 / **%14** / %21 / %36 | %20 / %4 / %1 / 0 | 27 / **16** / 12 / 6 |
| 1,5 | %5 / %8 / %10 / %15 | %94 / %94 / %89 / %77 | %1 / %5 / %10 / %23 | %4 / %1 / 0 / 0 | 21 / 13 / 10 / 6 |

- **Avantajsız referans** ~%30, bilgi tabanının koridor formülüyle uyumlu (README #47). Sharpe 0,3 bunu sadece ~15 puan artırıyor.
- **Optimum volatilite ~%8.** Daha yüksek volatilite süreyi kısaltıyor ama kalma oranını hızla artırıyor. Bu, README #43 ile aynı: yüksek risk sadece avantajı olmayana "yardım eder".
- Bu genel model bilgi tabanının trend testinden (README #36: Sharpe 0,55, %6 volatilite → %70 geçer, %4 kalır) biraz kötümser. Gerçek trend getirilerinin **pozitif çarpıklığı** ve bilgi tabanının testindeki farklı yapı bunu açıklayabilir. Kendi stratejin için kendi getiri serinle bootstrap yap.

**Literatürdeki Sharpe'ı CFD'ye çevir**
1. Makaledeki Sharpe çoğunlukla **brüt**, kurumsal maliyetli ve futures üzerinedir. Önce yayın sonrası erimeyi düş (~yarısı, §1).
2. **CFD finansmanı**: CFD long'u faiz + markup öder, short'u faiz − markup alır. Faiz kısmı futures fiyatında zaten var. Futures'a göre **ek maliyet ≈ markup × brüt nominal**.
3. FTMO benzeri 21 piyasalık bir evrende (6 parite, 4 endeks, 4 metal/enerji, 5 tarım, 2 kripto; tipik volatiliteler varsayıldı) eşit risk dağıtılırsa: %6-10 portföy volatilitesi için brüt nominal **~1-3 kat özsermaye** (piyasalar arası korelasyon 0-0,2 varsayımıyla). Nominalin ~%57'si dövizde.
4. Yani her **%1 markup yılda %1-3 getiri yer**. Sharpe 0,5 ve %8 volatilitede beklenen getiri yıllık ~%4. Markup %1,5-2'yi geçerse avantajın çoğu gider. **FTMO swap tablosunu sembol sembol çıkarmadan trend portföyüne başlama** (15 §7 açık soru).

---

## 10. FTMO için uygunluk tablosu

Kısaltmalar: **Std** = FTMO Standart hesap (fonlu aşamada hafta sonu yasak). **Swing** = hafta sonu serbest. Değerlendirme aşamasında ikisinde de kısıt yok (09 §4i).

| Strateji | Kanıt | Tutma süresi | İşlem/yıl | Beklenen Sharpe (gerçekçi) | Maks. düşüş | FTMO kuralları | CFD maliyeti | Karar |
|---|---|---|---|---|---|---|---|---|
| **Çok piyasalı trend** (3-12 ay, volatiliteye göre boyut, 15-20 piyasa) | ✔ (1880-2016, 58/58 piyasa). 2010'lar zayıf. | Haftalar-aylar | ~50-150 (dönüş + aylık boyutlama) | Lit. brüt 0,7-1+. Bilgi tabanında 0,55. CFD sonrası ~0,3-0,5 ◐ | %10 volatilitede ~%25 (Hurst) → %6-8 volatilite | Günlük limit sorun değil (düşük volatilite). Hafta sonu → **Swing**. +%10 ~1,5-2,5 yıl. | Finansman markup'ı × 1-3 kat nominal. En büyük risk bu. | **Evet, ana omurga.** Ama yavaş. |
| **Trend + endeks long karışımı** (%50/%50 risk) | ✔ bilgi tabanı (Sharpe 0,82, 2015+ 0,95). Faber/Parker "Trinity" ile uyumlu. | Aylar | ~50-150 | 0,5-0,7 (endeks long'unun finansmanı düşülünce) ◐ | %13 (bilgi tabanı) | **Swing.** Bilgi tabanında %89 geçti, ~1,5 yıl (README #37). | Endeks long'u: faiz + %2-3 → bacak getirisinin yarısı gider (12). | **Evet**, swap kontrolüyle. |
| **Endekste kısa vadeli dönüş** (RSI-2 tipi) | ✔ işlem başı (2015+ +0,17R, se 0,04). Lit.: kısa vadeli dönüş. | 2-5 gün | Endeks başına ~10-20, kümelenir | Portföy düzeyinde düşük: %1 riskte yıllık %2,9 (12) | %14 (12) | Std'de hafta sonu kesintisi gerekebilir. Tek başına challenge %11. | Gecelik swap birkaç gün, küçük. | **Kol olarak evet**, tek başına hayır. |
| **Gün içi endeks momentumu** (gün sonu kapanış) | Akademik ✔ (Gao, Baltussen). Bilgi tabanında son 2 yıl çelişkili → ◐ | Dakikalar-saatler | ~150-250 | Lit. 1,33 (örneklem içi, pratisyen). Gerçekçi: bilinmiyor | %25 (Zarattini, yüksek kaldıraçla) | **Std'ye en uygun yapı.** Günlük volatiliteyi ≤%0,7'ye indir. | Endekste komisyon yok, spread önemli. Swap yok. | **İleri test et**, sonra küçük pay. |
| **Kripto trend** | ◐ (güçlü ama kısa geçmiş, tek ekip) | Günler-haftalar | ~20-60 | Lit. > 1,5 (spot, örneklem içi). CFD sonrası bilinmiyor | Yüksek. Volatilite BTC ~%60. | Hafta sonu kuralı belirsiz (bakım araları). Lot granülerliği 10K'da sorun. | %0,0325/taraf + swap (bilinmiyor) | **Küçük pay**, maliyet netleşince. |
| **Ay dönümü** (endeks long, 4 gün) | ◐ (1926-2005 güçlü, 1990 sonrası karışık) | 4 gün | 12 | Bilinmiyor. Tek başına düşük R/yıl. | — | Hafta sonu içerir → Swing ya da değerlendirme. | 4 gece swap | **Filtre olarak**, kendi testinden sonra. |
| **Gece etkisi** (endeks, altın) | ✔ var / ◐ altın | 1 gece | ~250 | Swap sonrası ~0 | — | Std'de gece serbest | Swap getirinin çoğunu yer | ✘ işlem olarak. İcra eğilimi olarak evet. |
| **FX carry** | ✔ akademik (Sharpe 0,68), ◐ 2008 sonrası | Aylar | Az | CFD'de ≤0 olabilir | Ani çöküş, negatif çarpıklık | Günlük %5 limitine çöküş riski. Swing. | Getiri = swap. Broker payı iki yönde. | ✘ |
| **Kesitsel momentum, değer, düşük volatilite, PEAD** | ✔/◐ akademik (hisse L/S) | Aylar | Yüksek devir | — | Momentum çöküşü (2009) | Onlarca hisse CFD'si L/S | Swap + spread | ✘ (uygulanamaz) |
| **ORB (5 dk)** | ✘ maliyetten sonra (lit. tekrarı + README #31) | Gün içi | ~250 | ~0 | — | Std'ye uygun ama avantaj yok | Spread R'nin %6-12'si | ✘ |
| **Klasik TA**: formasyon, mum, Fibonacci, tek enstrümanda kısa MA ve kırılım | ✘ (STW 1999, Bajgrowicz ve Scaillet 2012, Neely vd. 2009, README ✘ listesi) | — | — | ≤0 | — | — | — | ✘ |
| **Scalping / order flow** (perakende) | ✘ (HFT gecikme yarışı, eş zamanlı OFI, %74-89 CFD kaybı) | Saniyeler-dakikalar | Binlerce | Maliyet sonrası negatif | — | Günlük limit tuzağı (README #48) | 5 $/lot + spread, her işlemde | ✘ |
| **FOMC öncesi drift** | ✘ (2015 sonrası kayboldu) | 1 gün | 8 | ~0 | — | — | — | ✘ |

---

## 11. Sıralama: kanıt × küçük hesap uyumu

1. **Çok piyasalı, yavaş, volatiliteye göre boyutlanmış trend takibi** (FTMO'nun FX, metal, enerji, tarım ve endeks CFD'leri; 3-12 ay; %6-8 volatilite; **Swing hesap**). En güçlü ve en uzun kanıt (137 yıl, örneklem dışı tekrar), kriz dönemlerinde pozitif. **Zayıf yanları**: yavaş (+%10 ~1,5-2,5 yıl), 2010'lar gibi uzun durgun dönemler, CFD finansman payı. Sharpe beklentisini 0,3-0,5'te tut.
2. **Trend + endeks long karışımı (%50/%50 risk)**: iki ilişkisiz getiri kaynağı, bilgi tabanında Sharpe 0,82, düşüş %13. Endeks long'unun CFD finansmanı en büyük çekince.
3. **Endekste kısa vadeli dönüş (RSI-2 tipi)**: yayından sonra da işlem başına çalışan nadir kısa vadeli etki (✔ bilgi tabanı, lit. "kısa vadeli dönüş"). **Kol olarak** ekle, tek başına prop aracı değil.
4. **Gün içi endeks momentumu / gün sonu deseni**: FTMO Standart hesabın yapısına en uygun akademik aday (gece riski ve swap yok, endekste komisyon yok). Ama güncel veride işaret çelişkili → **önce ileri test** (04 §6b-4'teki kayıtlı test ile birlikte yürüt) ve volatiliteyi düşür.
5. **Kripto trend (küçük pay)**: literatürde güçlü ve diğer kollarla ilişkisi düşük. Maliyet, lot granülerliği ve hafta sonu kuralı netleşmeden 10K hesapta büyük pay verme.

**Popüler ama kanıtı olmayanlar** (literatür + bilgi tabanı): mum formasyonları, Fibonacci, grafik formasyonları ve SMC'nin öznel bölgeleri (test edilemeyen kısım), tek enstrümanda kısa vadeli MA kesişimi ve 20 günlük kırılım, maliyet sonrası ORB, filtresiz sweep ve SFP, Market Profile %80, perakende scalping ve footprint/delta ile öngörü, FOMC öncesi drift, "haber spike'ı scalping". Kanıtı akademik olarak var ama **senin hesabında uygulanamayanlar**: kesitsel hisse momentumu, değer, BAB, PEAD, FX carry.

**Genel ders**: Kalıcı avantajlar **yavaş** (haftalar-aylar), **çeşitlendirilmiş** ve **sıkıcı**. FTMO'nun "+%10, günlük %5" yapısı ise hızlı ve yoğun işlemi ödüllendiriyor gibi görünüyor. Kanıtla uyumlu yol, yavaş bir avantajı **Swing hesapta, düşük volatiliteyle, sabırla** taşımak (README #41, #44 firma verileri de aynı yönde).

---

## 12. Bilgi tabanı için çıkarımlar ve açık sorular

1. **Ölçüt güncellemesi önerisi (15 §1)**: Sonradan bulunan etkiler için rastgele kıyastan **≥3 se** iste (Harvey, Liu, Zhu). Önceden kayıtlı hipotezlerde ≥2 se yeterli.
2. **FTMO swap tablosu**: Platformdan her sembolün long ve short swap'ını çıkar, markup'ı hesapla. Trend portföyünü markup %0, %1 ve %2 ile yeniden test et (§9 madde 2-4).
3. **Trend evrenini genişlet**: FTMO tarım CFD'leri ve kriptoyla 12 ay ve 3-12 ay karışım kuralını test et. Lot granülerliğini 10K ve 100K için ayrı kontrol et.
4. **Gün içi momentum ile son yarım saat dönüşü**: Baltussen'in gamma mekanizması işaretin rejime göre değişebileceğini söylüyor. Kayıtlı ileri teste dokunmadan, ayrı bir hipotez olarak "ilk yarım saat → son yarım saat" kuralını US500 ve GER40 CFD'lerinde yayın sonrası dönemle (2014+) test et.
5. **Ay dönümü**: US500 ve GER40'ta 2000+ ve 2015+ dönemlerinde, rastgele 4 günlük pencerelere karşı test et.
6. **FX seans deseni** (Breedon ve Ranaldo): EURUSD, GBPUSD ve USDJPY'de yerel seans getirisi, maliyetle.

---

## Kaynaklar

**Erime ve çoklu test**
- McLean, Pontiff (2016), *Does Academic Research Destroy Stock Return Predictability?* JF 71(1): https://Www.Gwern.net/doc/economics/2016-mclean.pdf · özet: https://rpc.cfainstitute.org/research/cfa-digest/2016/06/does-academic-research-destroy-stock-return-predictability-digest-summary
- Harvey, Liu, Zhu (2016), *…and the Cross-Section of Expected Returns*, RFS 29(1): https://www.nber.org/papers/w20592
- Hou, Xue, Zhang (2020), *Replicating Anomalies*, RFS 33(5): https://econpapers.repec.org/RePEc:oup:rfinst:v:33:y:2020:i:5:p:2019-2133.
- Jensen, Kelly, Pedersen (2023), *Is There a Replication Crisis in Finance?* JF 78(5): https://www.nber.org/papers/w28432
- Novy-Marx, Velikov (2016), *A Taxonomy of Anomalies and Their Trading Costs*, RFS 29(1): https://www.nber.org/papers/w20721

**Trend ve momentum**
- Moskowitz, Ooi, Pedersen (2012), *Time Series Momentum*, JFE 104(2): https://fairmodel.econ.yale.edu/ec439/jpde.pdf
- Hurst, Ooi, Pedersen (2017), *A Century of Evidence on Trend-Following Investing*, JPM 44(1): https://fairmodel.econ.yale.edu/ec439/hurst.pdf · ikincil sayılar: https://alphaarchitect.com/time-series-momentum-aka-trend-following-the-historical-evidence/
- AQR (2019/2020), *You Can't Always Trend When You Want*: https://www.aqr.com/Insights/Research/Journal-Article/You-Cant-Always-Trend-When-You-Want
- SG Trend 2022: https://www.hedgeweek.com/flat-december-sees-ctas-complete-record-year-2022/
- Huang, Li, Wang, Zhou (2020), *Time Series Momentum: Is It There?* JFE 135(3): https://econpapers.repec.org/RePEc:eee:jfinec:v:135:y:2020:i:3:p:774-794
- Jegadeesh, Titman (1993), JF 48(1): https://econpapers.repec.org/RePEc:bla:jfinan:v:48:y:1993:i:1:p:65-91
- Daniel, Moskowitz (2016), *Momentum Crashes*, JFE: https://www.nber.org/system/files/working_papers/w20439/w20439.pdf
- Lou, Polk, Skouras (2019), *A Tug of War*, JFE 134(1): https://personal.lse.ac.uk/polk/research/TugOfWar.pdf
- Menkhoff, Sarno, Schmeling, Schrimpf (2012), *Currency Momentum Strategies*, JFE 106(3): https://www.bis.org/publ/work366.pdf
- Cederburg, O'Doherty, Wang, Yan (2020), *On the Performance of Volatility-Managed Portfolios*, JFE 138(1): https://www.lehigh.edu/~xuy219/research/COWY.pdf

**Carry, değer, düşük volatilite, PEAD, kısa vadeli dönüş**
- Koijen, Moskowitz, Pedersen, Vrugt (2018), *Carry*, JFE 127(2): https://research-api.cbs.dk/ws/files/57294842/lasse_heje_pedersen_et_al_carry_acceptedmanuscript.pdf
- Brunnermeier, Nagel, Pedersen (2008), *Carry Trades and Currency Crashes*: https://www.nber.org/papers/w14473
- DBV tasfiyesi (SEC 424B3, 2023): https://sec.gov/Archives/edgar/data/1354730/000119312523013247/d407214d424b3.htm
- Novy-Marx, Velikov (2022), *Betting Against Betting Against Beta*, JFE 143(1): https://mysimon.rochester.edu/novy-marx/research/BABAB.pdf
- Değer düşüşü (Arnott vd. 2021 özeti): https://www.advisorperspectives.com/commentaries/2021/02/12/reports-of-values-death-may-be-greatly-exaggerated
- Martineau (2022), *Rest in Peace Post-Earnings Announcement Drift*, CFR: https://cfr.ivo-welch.info/published/papers/martineau2021rest.pdf
- de Groot, Huij, Zhou (2012), *Another Look at Trading Costs and Short-Term Reversal Profits*, JBF 36(2): https://repub.eur.nl/pub/25718

**Gün içi ve takvim**
- Gao, Han, Li, Zhou (2018), *Market Intraday Momentum*, JFE 129(2): https://econpapers.repec.org/RePEc:eee:jfinec:v:129:y:2018:i:2:p:394-414
- Baltussen, Da, Lammers, Martens (2021), *Hedging Demand and Market Intraday Momentum*, JFE 142: https://www3.nd.edu/~zda/intramom.pdf
- Zarattini, Aziz, Barbon (2024), *Beat the Market* (SFI 24-97): https://ideas.repec.org/p/chf/rpseri/rp2497.html · CXO özeti: https://www.cxoadvisory.com/momentum-investing/complex-intraday-time-series-momentum-strategy-applied-to-spy/
- Zarattini, Aziz (2023), *Can Day Trading Really Be Profitable?*: https://papers.ssrn.com/abstract=4416622 · bağımsız CFD tekrarı (blog, ◐): https://www.mql5.com/en/blogs/post/776235
- Cliff, Cooper, Gulen (2008), *Return Differences between Trading and Non-trading Hours*: https://www.cxoadvisory.com/calendar-effects/buy-at-the-close-and-sell-at-the-open
- Blose vd. (2018), *Overnight versus day returns in gold*, J. Econ. Finance: https://ideas.repec.org/a/spr/jecfin/v42y2018i3d10.1007_s12197-017-9403-0.html
- McConnell, Xu (2008), *Equity Returns at the Turn of the Month*, FAJ 64(2): https://rpc.cfainstitute.org/research/financial-analysts-journal/2008/equity-returns-at-the-turn-of-the-month
- Lucca, Moench (2015), *The Pre-FOMC Announcement Drift*, JF 70(1): https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf
- Kurov, Wolfe, Gilbert (2021), *The Disappearing Pre-FOMC Announcement Drift*, FRL: https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html
- Jacobsen, Zhang, *The Halloween Indicator: Everywhere and All the Time*: https://ideas.repec.org/a/eee/jimfin/v110y2021ics0261560620302242.html
- Breedon, Ranaldo (2013), *Intraday Patterns in FX Returns and Order Flow*, JMCB 45(5): https://www.snb.ch/en/mmr/papers/id/working_paper_2011_04

**Teknik analiz, perakende ve mikro yapı**
- Sullivan, Timmermann, White (1999), *Data-Snooping, Technical Trading Rule Performance, and the Bootstrap*, JF 54(5): https://bashtage.github.io/kevinsheppard.com/files/teaching/mfe/advanced-econometrics/Sullivan_Timmermann_White.pdf
- Bajgrowicz, Scaillet (2012), *Technical Trading Revisited*, JFE 106(3): https://econpapers.repec.org/RePEc:eee:jfinec:v:106:y:2012:i:3:p:473-491
- Park, Irwin (2007), *What Do We Know About the Profitability of Technical Analysis?* JES 21(4): https://ideas.repec.org/a/bla/jecsur/v21y2007i4p786-826.html
- Neely, Weller, Ulrich (2009), *The Adaptive Markets Hypothesis: Evidence from the FX Market*, JFQA 44(2): https://files.stlouisfed.org/files/htdocs/wp/2006/2006-046.pdf
- Lo, Mamaysky, Wang (2000), *Foundations of Technical Analysis*, JF 55(4): https://www.nber.org/papers/w7613
- Abbey, Doukas (2015), *Do Individual Currency Traders Make Money?* JIMF 56: https://ideas.repec.org/a/eee/jimfin/v56y2015icp158-177.html
- ESMA (2018), CFD ürün müdahalesi (%74-89): https://www.esma.europa.eu/node/84933
- Baron, Brogaard, Hagströmer, Kirilenko (2019), *Risk and Return in High-Frequency Trading*, JFQA 54(3): https://ideas.repec.org/a/cup/jfinqa/v54y2019i03p993-1024_00.html
- Cont, Kukanov, Stoikov (2014), *The Price Impact of Order Book Events*: https://arxiv.org/abs/1011.6402
- Evans, Lyons (2002), *Order Flow and Exchange Rate Dynamics*, JPE 110(1): https://www.nber.org/papers/w7317

**Kripto**
- Liu, Tsyvinski (2021), *Risks and Returns of Cryptocurrency*, RFS 34(6): https://www.nber.org/papers/w24877
- Liu, Tsyvinski, Wu (2022), *Common Risk Factors in Cryptocurrency*, JF 77(2): https://www.nber.org/papers/w25882
- Zarattini, Pagani, Barbon (2025), *Catching Crypto Trends* (SFI 25-80): https://ideas.repec.org/p/chf/rpseri/rp2580.html
- Grobys, Ahmed, Sapkota (2020), *Technical Trading Rules in the Cryptocurrency Market*, FRL 32: https://ideas.repec.org/a/eee/finlet/v32y2020ics1544612319308852.html
- Shen, Urquhart, Wang (2022), *Bitcoin Intraday Time-Series Momentum*, Financial Review 57(2): https://centaur.reading.ac.uk/100181

**FTMO resmi**
- Gece ve hafta sonu SSS: https://ftmo.com/en/faq/can-i-hold-positions-overnight/
- FX komisyonu 2,5 $/lot/taraf (25 Eylül 2025): https://ftmo.com/en/blog/trading-updates/trading-update-25-sep-2025/
- Kripto %0,0325/taraf (24 Temmuz 2025): https://ftmo.com/en/blog/trading-updates/trading-update-24-jul-2025/
- Endekste komisyon yok: https://ftmo.com/en/blog/zero-commissions-on-indices/
- Tarım CFD'leri (2023) ve asgari 1,00 lot (2024): https://ftmo.com/en/blog/trading-updates/trading-update-14-sep-2023/ · https://ftmo.com/en/blog/trading-updates/trading-update-19-sep-2024-2-2/
- Semboller (swap ve spesifikasyon): https://ftmo.com/en/symbols/
