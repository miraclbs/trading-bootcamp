# 16 — Kanıtlı Trader'lar: "Sıfırdan Zengin" Gerçekte Nasıl Oluyor?

> Güven seviyesi: **ORTA-YÜKSEK**. Taban oranlar (§2) akademik makale ve düzenleyici verisi. Trader kayıtlarının doğrulama düzeyi kişiden kişiye çok değişiyor, her biri ayrı derecelendirildi.
> Derecelendirme: ✔ birincil kaynak, düzenleyici, denetimli fon ya da birden çok güvenilir kaynakla belgeli · ◐ kendi beyanı, tek kaynak ya da doğrulanamadı · ✘ kanıtla çelişiyor.
> Tarih: 2026-11-25. Simülasyon (§3) bu dosya için yapıldı, parametreleri metinde.
> Zaten kapsananlar, burada tekrarlanmadı: Peter Brandt (14 §3d, 03, 09 §4r), Al Brooks (04), Adam Grimes (14, 10), Lance Breitstein (14 §3g, 12), Trader Dante (08 §5b, 13), Mark Douglas (08 §5), Jerry Parker ve Turtle kuralları (12).

## Özet

1. **Taban oran acımasız** ✔: Tayvan'da day trader'ların yılda ~%13'ü kâr ediyor, ama ertesi yıl da öngörülebilir şekilde kâr edenler **%1'in altında** (~1.000 / 360.000). Brezilya'da işe başlayan 19.646 kişiden 300 günden uzun dayanan 1.551 kişinin **%97'si zararda**, asgari ücretten fazla kazanan **17 kişi**. Yani başlayanların **~1.150'de 1'i**. Hindistan'da F&O yapan 11,3 milyon bireyin **%93'ü** 3 yılda zarar etti.
2. **"Sıfırdan zengin" listesindeki isimlerin çoğu sıfırdan başlamadı** ✔. Tudor Jones, Druckenmiller, Soros, Simons ve Thorp kurum içinde yetişti ya da kurum parası yönetti. Servetlerinin büyük kısmı **başkasının parası üzerinden alınan ücretlerden** geldi, küçük bir hesabı bileşiklemekten değil.
3. **Gerçekten küçük hesapla başlayanlar** (Dennis 400 $, Kullamägi 5.000 $, Livermore 5 $, Minervini, BNF) ya **defalarca battı** ya da **olağanüstü bir piyasa rejimine** denk geldi. Çoğunda ikisi birden var. Kullamägi ilk 2 yılda 3-4 hesap patlattı. Minervini ~6 yıl para kazanamadı. Livermore 3 kez iflas etti.
4. **Ortak olan bir formasyon ya da gösterge değil** ✔. Yöntemler birbirine zıt: makro, trend takibi, momentum hisseleri, istatistiksel arbitraj, ortalamaya dönüş. Ortak olanlar şunlar: **kaybı küçük kesmek, kazananı büyütmek** (isabet çoğu zaman <%50), hayatta kalmayı önce koymak, tek bir tarzda uzmanlaşmak ve yıllarca piyasanın içinde çıraklık.
5. **Yarışma birinciliği beceri kanıtı değil** ✔ (simülasyon). Avantajı sıfır, işlem başına %10 risk alan rastgele hesapların **~%10'u** tek yılda Minervini'nin 1997 getirisini (%155) yakalıyor, %15'i ise %90 eriyor. Yarışma sonuçları gerçek, ama tek yıllık ve yüksek varyansı ödüllendiriyor.
6. **Dünya klası getiri bile küçük hesabı zengin etmez** ✔ (aritmetik). 10.000 $ yılda %30 ile 10 yılda 138.000 $ olur. "Zengin" olmak için ya yıllarca %100+ getiri gerekir (yüksek risk, çoğunlukla batış), ya da başkasının sermayesi (fon ücreti, prop).
7. **Dürüst cevap**: kendi küçük hesabından trading ile zengin olmak **mümkün ama piyango düzeyinde nadir** (binde 1 ve altı). Gerçekçi yol yavaş: küçük riskle ölçülebilir avantaj kurmak (15), sermayeyi kaldıraçla değil prop ya da ücretle büyütmek, geliri trading'e bağlamamak.

---

## 0. Kayıtlar nasıl doğrulanır? (Güven merdiveni)

| Düzey | Örnek | Ne kanıtlar |
|---|---|---|
| Denetimli fon kaydı, düzenleyici dosyası | Medallion (yatırımcı mektupları, Zuckerman'ın verisi), Princeton Newport, CTA kayıtları | Getiri büyük ölçüde gerçek. Yine de hayatta kalan fonlar görünür. |
| Bağımsız denetim isteyen röportaj | Schwager ve Coyle, *Market Wizards: The Next Generation* (2026): %800-1.000 getiri için "ekstre yetmez, denetim şart" | Güçlü. Ama her trader için hangi belgenin istendiği yayımlanmıyor. |
| Gerçek paralı yarışma | US Investing Championship, Robbins World Cup | Sonuç gerçek hesaptan. **Tek yıl**, katılımcılar kendini seçiyor, yüksek varyans ödülleniyor, denetim yok. |
| Basın ve fonun kendi beyanı | Duquesne "%30, zararlı yıl yok", Quantum "%30+" | Büyük ihtimalle doğru, ama bağımsız denetimli yıllık seri kamuya açık değil. |
| Kitap, kendi anlatımı | Darvas, Livermore (*Reminiscences* kurgusal anlatı), Seykota'nın müşteri hesabı | Anekdot düzeyi. |
| Ekran görüntüsü, canlı yayın P&L | Sosyal medya | Kanıt değil (11, README #56). |

- Schwager'ın ölçütü ◐: en az **10, tercihen 20 yıllık** kayıt. "Herkes 2-3 yılda servet yapıp sonra genelde batırabilir" (Excess Returns özeti).

---

## 1. Trader profilleri

### Özet tablo

| Trader | Doğrulama | Başlangıç | Piyasa / vade | En büyük hata |
|---|---|---|---|---|
| Paul Tudor Jones | ◐-✔ fon getirileri basında | Kurum içi: pamuk salonunda çırak | Makro, vadeli; gün-hafta-ay | Müşteri hesaplarında pamuk kaybı ◐ |
| Stanley Druckenmiller | ◐-✔ fon beyanı, çok kaynak | Banka stajyeri, ~1 M$ ile fon | Makro; aylar | 2000 tepesinde 6 milyar $ teknoloji alımı ✔ |
| George Soros | ◐-✔ fonun kendi mektubu | Arbitraj trader'ı (Londra, NY) | Makro; aylar | 1987 çöküşü, 1998 Rusya ✔ |
| Ed Seykota | ◐ Market Wizards, denetim yok | MIT mühendisi, aracı kurum | Sistematik trend, vadeli | Belgelenmiş hata bulamadım |
| Richard Dennis | ✔ başlangıç, ◐ zirve | **400 $** (borçla) | Vadeli, trend; salon | 1987-88 ~50 M$ kayıp, kurallarına uymama uzlaşması ✔ |
| Jim Simons | ✔ (aritmetik ortalama) | Matematik profesörü | İstatistiksel arbitraj, çok kısa vade | 1989 zararı, model yeniden kuruldu ◐ |
| Ed Thorp | ✔-◐ fon kaydı | Matematik profesörü | Konvertibl/varant arbitrajı | — |
| Linda Raschke | ◐ NFA kayıtlı CTA, kendi sıralaması | Opsiyon piyasa yapıcısı | Vadeli, kısa swing | Belgelenmiş kayıt yok |
| Mark Minervini | ✔ 2 yarışma, ◐ çok yıllık iddia | Küçük hesap, ~6 yıl zarar ✔ (kendi sözü) | ABD hisse momentumu, swing | İlk 6 yılda sermayeyi bitirdi |
| David Ryan | ✔ 3 yarışma | O'Neil'in yanında çalıştı | ABD hisse, CAN SLIM | — |
| Larry Williams | ✔ 1987 yarışması | — | Vadeli, kısa vade | Yarışma yılında ~%60 düşüş ◐ |
| Jesse Livermore | ✔ iflaslar (basın, mahkeme) | **5 $**, bucket shop | Hisse, emtia; spekülasyon | 3 iflas, intihar ✔ |
| Nicolas Darvas | ◐ tartışmalı | Dansçı, birkaç bin $ | ABD hisse, kırılım | Kayıt tartışmalı (savcılık: sadece 216 bin $) |
| Kristjan Kullamägi | ◐ kendi beyanı + Schwager'ın kitabı | **5.000 $**, güvenlik görevlisi | ABD hisse momentumu, swing | 3-4 patlama, 2022'de zirvenin yarısını geri verdi ◐ |
| Takashi Kotegawa (BNF) | ✔ tek olay, ◐ toplam | ~1,6 milyon ¥ ◐ | Japon hisse, kısa vade | — |

### 1.1 Paul Tudor Jones

- **Doğrulama**: 1987'de ana fon ücret sonrası **+%125,9** ✔ (birden çok kaynak). Uzun vade ortalaması ~%19-20 ◐ (fon kamuya açık değil, ikincil kaynaklar). 2010'lardan sonra getiriler belirgin düştü ◐.
- **Başlangıç**: Virginia Üniversitesi ekonomi (1976). Pamuk trader'ı Eli Tullis'in yanında New York pamuk borsasında işe başladı. Masada uyuyakaldığı için kovuldu, Tullis sonradan ilk müşterilerinden oldu ✔ (Wikipedia). Tudor Investment 1980'de kuruldu. Sıfırdan değil: **mentor + kurum** yolu.
- **Yöntem**:
  - Savunma önce: "Kaybedenlerle ortalama düşürme" yasağı ("Losers average losers") ✔ (Market Wizards).
  - **200 günlük ortalama** ana filtre: "Baktığım her şeyin ölçüsü 200 günlük kapanış ortalaması. Altına inince çıkarım, savunma oynarım" ✔ (Tony Robbins, *Money: Master the Game*, 2014; ikincil alıntılar).
  - **5'e 1 risk/ödül**: "5'e 1 ile isabet %20 olsa da kazanırsın" ◐ (aynı kaynak, ifade farklı aktarılıyor).
  - Tarihsel benzetme: 1987 çöküşünü 1929 grafiğiyle karşılaştırarak öngördü ✔ (PBS belgeseli *Trader*, 1987).
- **Hata**: E.F. Hutton'da aracıyken tek bir aşırı kaldıraçlı pamuk işleminde müşterilerinin özsermayesinin **%60-70'ini** kaybettiği, bırakmanın eşiğine geldiği anlatılıyor ◐ (Market Wizards'a atfediliyor, birincil metni doğrulayamadım).
- **Ders**: En büyük işlemi (1987) bir savunma kuralı (200 günlük) ve risk tanımı üzerine kurulu. Kaynak tahmin değil, **çıkış disiplini**.

### 1.2 Stanley Druckenmiller

- **Doğrulama**: Duquesne Capital'de ortalama **~%30/yıl, zararlı yıl yok** (1986-2010; bazı kaynaklar 1981'den) ◐. Basında yaygın (Bloomberg kaynaklı), ama denetimli yıllık seri kamuya açık değil. 2010'da fonu kapattı. Zirvede ~12 milyar $ ◐.
- **Başlangıç**: Michigan'da ekonomi doktorasını bıraktı. 1977'de Pittsburgh National Bank'ta yönetici adayı, ~1 yıl sonra hisse araştırma bölümünün başı ◐. 1981'de Duquesne'i ~1 M$ ile kurdu ✔. 1988-2000 Soros'un Quantum fonunun baş yöneticisi ✔.
- **Yöntem**:
  - Yukarıdan aşağı makro: merkez bankası likiditesi, 12-18 ay sonrası.
  - **Sermaye koruma + büyük vuruş**: "Uzun vadeli üstün getiri sermayeyi korumak ve home run'larla yapılır" ✔ (Soros'tan aldığını söylüyor, *New Market Wizards*).
  - "Önemli olan haklı ya da haksız olmak değil, **haklıyken ne kadar kazandığın, haksızken ne kadar kaybettiğin**" ✔ (aynı kaynak, Soros'un dersi).
  - Yüksek inançta yoğunlaşma (1992 sterlin short'u, Soros ile).
- **Hata** ✔ (kendi anlatımı): 1999'da internet hisselerini erken açığa sattı ve kaybetti. Sonra yön değiştirdi, Mart 2000 tepesinde **6 milyar $** teknoloji hissesi aldı ve 6 haftada **3 milyar $** kaybetti. Dersi: "Hiçbir şey öğrenmedim. Bunu yapmamam gerektiğini zaten biliyordum, duygusal bir enkazdım."
- **Ders**: 30 yıl zararsız bir kayıt bile tek bir duygusal kararla dev bir kayıp içerebilir. Kural bilmek uygulamak demek değil.

### 1.3 George Soros

- **Doğrulama**: 2000 tarihli kendi hissedar mektubu: Quantum 31 yılda yıllık **%30'un üzerinde** ✔ (fonun beyanı). 1992 sterlin short'u ~1 milyar $ ✔.
- **Başlangıç**: 1930 Budapeşte doğumlu, savaştan sonra Londra'ya göçtü, LSE. Londra'da ve 1956'dan sonra New York'ta **arbitraj trader'ı**. 1969'da kendi fonu (Double Eagle, sonra Quantum) ✔. Kurum içinden.
- **Yöntem**:
  - "Refleksivite": algı fiyatı, fiyat temelleri etkiler, yükseliş-çöküş döngüleri.
  - Tezini küçük pozisyonla test eder, piyasa doğrularsa büyütür, yanılınca hızla çıkar ◐ (yaygın aktarım).
  - Druckenmiller'a göre "gördüğüm **en iyi zarar kesen**" ✔ (*New Market Wizards*).
- **Hatalar** ✔: 1987 çöküşünde fon büyük kayıp verdi (tahminler 300-800 milyon $, NAV'de ~%26 düşüş ◐). 1998 Rusya krizinde ~2 milyar $ ✔. 2000 teknoloji çöküşü (Druckenmiller ile).
- **Ders**: Büyük getiriler büyük, kaldıraçlı bahislerden geliyor. Bunun bedeli de büyük kayıplar. Ayakta kalmanın sırrı yanılınca hızlı çıkmak.

### 1.4 Ed Seykota

- **Doğrulama** ◐: Schwager'ın *Market Wizards* (1989) kitabında, 1972'de 5.000 $ ile açılan bir **müşteri hesabı** 1988 ortasına kadar ~15 milyon $ (nakit bazında %250.000+). Hesap ekstresi ya da denetim kamuya açık değil. Hesap müşterinin, kendi parası değil.
- **Başlangıç**: MIT elektrik mühendisliği (1969). Bir aracı kurumda ilk ticari bilgisayarlı trend takip sistemlerinden birini kurdu ◐. Michael Marcus'un hocası.
- **Yöntem**:
  - Uzun vadeli, sistematik trend takibi, vadeli işlemler.
  - "İyi işlemin unsurları: zararı kes, zararı kes, zararı kes" ✔ (Market Wizards).
  - Kurallar: zararı kes, kazananı taşı, bahsi küçük tut, kurala sorgusuz uy.
  - "Kazansa da kaybetse de herkes piyasadan istediğini alır" (psikoloji vurgusu).
- **Hata**: Belgelenmiş erken patlama bulamadım. Uydurmamak için boş bırakıldı.
- **Ders**: Trend takibinin kârı kuyruktaki birkaç büyük işlemden gelir (bu bilgi tabanında test edildi: README #27, #72). Seykota'nın getirisi 1970-80'lerin emtia ve faiz trendlerinde oluştu. Clenow'a göre "o dönem bitti" (12).

### 1.5 Richard Dennis ve Turtle'lar

- **Başlangıç** ✔: 1970'te ailesinden **1.600 $** borç aldı, 1.200 $'ı MidAmerica borsasında koltuğa verdi, **400 $** ile işlem yaptı (Wikipedia, FIA). 1974 sonunda, 26 yaşına girmeden milyoner ✔. Zirve servet "200-350 milyon $" ◐ (kaynaklar çelişiyor).
- **Yöntem**: Vadeli işlemlerde kırılım ve trend takibi. Salon trader'ı olarak başladı.
- **Turtle deneyi** ✔: 1.000'den fazla başvurudan 23 kişi (21 erkek, 2 kadın), iki grup (Aralık 1983 ve 1984), **2 haftalık eğitim**. Başarılı olanlara Dennis'in parasından 250 bin - 2 milyon $'lık hesaplar verildi. ~5 yılda toplam "175 milyon $ kâr" ◐ (Russell Sands'in iddiası, doğrulanmadı). Curtis Faith "4 yılda 30 milyon $" ◐ (kendi kitabı). Jerry Parker Chesapeake Capital'i kurdu ✔ (12).
- **Hatalar** ✔: 1987 çöküşünde ~10 milyon $, 1987-88'de toplam ~50 milyon $ kayıp (bildirilen). Bahar 1988'de müşteri fonlarını bıraktı. 1990'da firması, **Dennis'in kendi kurallarına uymadığı** iddiasıyla açılan şikâyetleri 2,5 milyon $'ın üzerinde bir tutarla uzlaştırdı (kabul ya da ret yok). 1990'larda geri döndü, 2000 yazında zararla yine kapattı.
- **Kurallar bugün** ✔: Yayımlanan Turtle kurallarının geriye dönük testinde 1986'dan sonra performans düşüyor, 1996-2009 arası düz (Wikipedia'da aktarılan testler). Bu bilgi tabanının testi de aynı: 20 günlük kırılım hisselerde ~0, dövizde negatif, emtiada 2015 sonrası çalışmıyor (README #22).
- **Ders**: Kurallar 2 haftada öğretilebiliyor. Zor olan uymak: **kuralları yazan hocanın kendisi bile uymadı**. Yayımlanan bir "sır" kalabalıklaştıkça zayıflıyor.

### 1.6 Jim Simons / Renaissance Medallion (neden perakende kopyalayamaz)

- **Doğrulama** ✔: Zuckerman'ın verisine göre 1988-2018 ortalama **%66,1 ücret öncesi, %39,1 ücret sonrası**. Bunlar **aritmetik** ortalama. Bileşik getiri tartışmalı: Cornell (2020) ~%63, bir arXiv çalışması fon büyüklüğü ve kâr verisinden ücret öncesi **<%35** hesaplıyor ◐.
- **Başlangıç**: Matematik profesörü, Soğuk Savaş'ta şifre çözücü. 1978'de takdirli işlemle başladı, sonra tamamen modellere geçti ◐ (Zuckerman).
- **Yöntem**: Binlerce enstrümanda aynı anda, çok kısa vadeli, küçük istatistiksel avantajlar. Robert Mercer: "**Zamanın %50,75'inde haklıyız**, ama o %50,75'te yüzde yüz haklıyız. Böyle milyarlar kazanılır" ✔ (Zuckerman, *The Man Who Solved the Market*).
- **Kopyalanamaz, çünkü**:
  1. İşlem başı avantaj yazı-turadan ancak biraz iyi. **Milyonlarca işlem** ve neredeyse sıfır maliyet ister. Perakende spread ve komisyon bunu silip atar (README #28: gün içinde maliyet avantajı yer).
  2. Yüzlerce bilim insanı, onlarca yıllık temizlenmiş veri ve icra altyapısı.
  3. **Kapasite sınırlı**: Simons fonun ~10 milyar $'dan fazlasını yönetemeyeceğini düşündü, dış yatırımcıları çıkardı. Ücretler %5 yönetim + %44 performans ✔.
  4. **Aynı firmanın dışarıya açık fonları bile tutturamıyor** ✔: 2020'de Medallion +%76, dışarıya açık RIEF -%19, RIDA ~-%33.
- **Ders**: Kopyalanacak şey avantajın kendisi değil, süreç: veri, test, maliyet kontrolü, işlem başına küçük ama sayısız bağımsız avantaj.

### 1.7 Edward Thorp (denetimli kayda ek örnek)

- **Doğrulama** ✔-◐: Princeton Newport Partners, Kasım 1969 - 1988: ücret sonrası **%15,1/yıl** (S&P %10,2). 1.000 $ → 13.920 $, endekste 6.450 $ (MoneyWeek). Ücret öncesi ~%19,1. Kaynaklar %15-20 arasında değişiyor. "227 kârlı ay, 3 zararlı ay" ◐.
- **Başlangıç**: Matematik profesörü. Blackjack kart sayma (*Beat the Dealer*, 1962), varant fiyatlaması (*Beat the Market*, 1967).
- **Yöntem**: Yanlış fiyatlanmış konvertibl tahvil ve varantları al, dayanak hisseyle hedge et. Pozisyon boyutu **Kelly** ile (01).
- **Ders**: Kalıcı kayıt, **açıklanabilir bir fiyatlama hatası** ve matematiksel boyutlandırmadan geldi. Grafik deseninden değil. Carver'ın "karşı tarafta kim kaybediyor?" sorusu (README #38).

### 1.8 Linda Bradford Raschke

- **Doğrulama** ◐: 1992-2015 arası NFA kayıtlı CTA ✔. Fonunun BarclayHedge'de "5 yıllık performansta ~4.500 fon içinde 17." olduğunu kendi sitesi söylüyor. Tarih, fon adı ve getiri verisi verilmiyor. *New Market Wizards* (1992) ✔.
- **Başlangıç** ✔: 1981'de Pacific Coast ve Philadelphia borsalarında opsiyon piyasa yapıcısı. CTA olmadan önce ~11 yıl salonda.
- **Yöntem** (*Street Smarts*, Connors ile, 1995):
  - Kısa vadeli swing, vadeli işlemler.
  - "Holy Grail": güçlü trendde (ADX) 20 EMA'ya ilk geri çekilme.
  - "**Turtle Soup**": 20 günlük tepe/dip kırılımının başarısız olması, yani **sweep / failure test** (05).
  - "Anti" (04), 3/10 osilatörü.
- **Bu bilgi tabanıyla bağ**: Turtle Soup bu kullanıcının sweep ilgisinin en yakın kanıtlı atası. Ama filtresiz sweep testte rastgeleden ayırt edilemedi (README #19, #51). Raschke de bağlam ve seçicilik şart diyor.
- **Hata**: Kitabında (*Trading Sardines*, 2019) zor dönemlerini anlatıyor, ama ayrıntısını doğrulayamadım ◐.
- **Ders**: Uzun bir kariyer, tek bir sihirli setup'tan değil, **salonda yıllarca öğrenilmiş icra ve risk becerisinden** geliyor.

### 1.9 Mark Minervini ve David Ryan (US Investing Championship ne demek?)

**US Investing Championship (USIC) doğrulaması**:
- 1983'ten beri düzenleniyor. "Gerçek paralı, doğrulanmış yarışma" ✔. Katılımcı bir aracı kurum hesabı gösterir, ekstrelerini gönderir (aylık ya da çeyreklik, kaynaklar farklı söylüyor).
- **Denetim yok**. Küçük hesapla manşet yüzde üretilmesin diye minimum var: 1 M$+ bölümünde 1 milyonun altındaki hesabın kârı 1 milyona bölünüyor, diğer bölümde eşik ~20.000 $.
- ⚠️ **Sınırları**: tek yıl, katılımcılar kendini seçiyor, tüm katılımcıların dağılımı yayımlanmıyor, sadece kazananlar duyuruluyor. Yarışma yapısı varyansı ödüllendiriyor (§3). **Sonuç gerçek ✔, beceri çıkarımı ◐.**

**Mark Minervini**:
- **Doğrulama**: USIC 1997 **%155** ✔. 2021, 1 M$+ hisse bölümü **%334,8** ✔ (önceki rekor %119,1). "1994-1999 yıllık ortalama %220, toplam %33.500" ◐ (kendi tanıtım metni, denetim bulunamadı).
- **Başlangıç** ✔ (kendi sözü): 1983'te başladı. "**İlk ~6 yıl hiç para kazanamadım**." 1980'lerin sonunda sermayesi bitmişti. Sonra kazanan hisselerin ortak profilini çıkardı ("liderlik profili").
- **Yöntem**: SEPA / VCP (volatilite daralması), trend şablonu (fiyat yükselen 150/200 günlük ortalamanın üstünde), güçlü kazanç büyümesi, sıkı stop ◐ (kendi kitapları).
- **Ders**: Kendi anlatımında bile **~6 yıllık başarısızlık** var. Rekor yılları 1990'ların sonu ve 2021, ikisi de güçlü momentum rejimleri.

**David Ryan** ✔: William O'Neil'in yanında çalıştı, CAN SLIM. USIC 1985 **%161**, 1986 **%160**, 1987 **%118** (3 yılda bileşik ~%1.379; kontrol: 2,61 × 2,60 × 2,18 ≈ 14,8). *Market Wizards*'ta ("Treasure Hunt"). Ders: **bir ustanın yanında çıraklık** ve tek bir yönteme odaklanma.

### 1.10 Larry Williams

- **Doğrulama** ✔: 1987 Robbins World Cup Championship of Futures Trading, 12 ayda **10.000 $ → ~1,1 milyon $ (%11.376)**. Hâlâ rekor olarak aktarılıyor. Kızı Michelle Williams aynı yarışmayı 1997'de kazandı ✔.
- ⚠️ **Yarışma yılının içi** ◐: Hesap ~2 milyon $'a çıkıp Ekim 1987 çöküşü civarında ~750 bin $'a düştü, ~1,1 milyonla bitti. Yani kazanan yıl içinde **~%60'lık düşüş**. Aynı yıl yönettiği müşteri hesaplarının toplamda zarar ettiği iddiası var. Kaynak bir forum alıntısı, doğrulanamadı.
- **Yöntem**: Vadeli işlemlerde kısa vadeli formasyonlar, mevsimsellik, COT verisi, Williams %R ✔.
- **Ders**: "Bir yılda 100 kat" yüksek kaldıraçla oynanmış bir yarışma sonucu. Aynı yıl içinde %60 düşüş olan bir eğri, prop limitlerinde (09) günler içinde biterdi.

### 1.11 Jesse Livermore (iflaslarıyla birlikte)

- **Başlangıç** ✔: 14 yaşında PaineWebber'de kotasyon yazan çocuk (haftalık 5 $). 15 yaşında bucket shop'ta 5 $'lık ilk bahis. Bucket shop'lardan men edilene kadar ~10.000 $ biriktirdi.
- **Büyük kazançlar** ✔ (bildirilen): 1907 paniğinde açığa satışla bir günde ~1 milyon $. 1929 short'ları ~100 milyon $ (o baharda kâğıt üstünde 6 milyon $ zarardaydı).
- **Batışlar** ✔:
  - 1901: %400 marjla short, tüm sermaye gitti.
  - 1908: pamukta başkasının tavsiyesine uydu, önceki yılın kârının çoğunu kaybetti.
  - 1915: ilk resmi iflas.
  - 1934: üçüncü iflas, 84.000 $ varlığa karşı 2,5 milyon $ borç.
  - 1940: intihar. Notunda "Savaşmaktan yoruldum."
- **Yöntem**: Bant ve fiyat okuma, kritik seviye ("pivotal point") kırılımı, kazanana ekleme ◐ (*Reminiscences* kurgusal bir anlatı, kendi 1940 kitabı).
- **Ders**: Kurallarını yazan biri, **kaldıraç ve kurala uymama** yüzünden üç kez battı. Bir servetin büyüklüğü onu tutmayı garanti etmez (Brandt: "Para kazanmak kolay, tutmak zor", 14 §3d).

### 1.12 Nicolas Darvas

- **Kayıt** ◐ (tartışmalı): Dansçı, Macar göçmen. *How I Made $2,000,000 in the Stock Market* (1960) 1957-58 boğa piyasasında ~2 milyon $ iddia ediyor. **New York Başsavcılığı** (1960) iddiayı "tamamen yanlış" dedi, tespit edebildiği kârı **216.000 $** olarak açıkladı. Ocak 1961'de mahkeme soruşturmayı basın özgürlüğü gerekçesiyle durdurdu. Müfettişler tüm aracı kurum hesaplarını bulamadıklarını kabul etti ✔ (Time 1960-61).
- **Yöntem**: "Kutu teorisi". Fiyat kutudan yukarı kırılınca alış stop emri, stop kutunun hemen altında. Hacim ve kazanç artışıyla seçim. Turnedeyken haberi gecikmeli okuyup emirleri telgrafla verdi, yani **ekrandan uzaktı** (Brandt'ın gece emir girme yöntemine benzer, 14 §3d).
- **Ders**: Yöntem mantıklı (kırılım + stop), ama kazancın büyük kısmı tek bir boğa piyasasında. Rakam ise doğrulanamadı.

### 1.13 Kristjan Kullamägi (Qullamaggie)

- **Kendi anlatımı** (Chat With Traders #212, K0F73Sq90j0) ✔ beyan:
  - 2011'de **5.000 $** ile tam zamanlı başladı. Biyomedikal laboratuvar derecesini bitirmeden bıraktı. Yarı zamanlı **güvenlik görevlisi**ydi.
  - İki haftalık kâğıt işlemde hesabı ikiye katladı, "sonbahara zengin olurum" dedi, gerçek parayı **ilk iki ayda** kaybetti.
  - **İlk ~2 yılda 3-4 kez battı.** Her seferinde güvenlik işine dönüp ~6 ay biriktirdi, 3-4 bin $ ile yeniden başladı. "Her patlama daha uzun sürdü, demek ki gelişiyordum." "Hayatımın birikimiydi, sürekli depresyondaydım."
  - Başta stop, pozisyon boyutu ya da çıkış kavramı yoktu, "her işleme tüm parayla" giriyordu.
  - 2013 civarı kârlı oldu. **İlk milyonunu çoğunlukla day trading ile** yaptı, sonra swing'e geçti (daha ölçeklenebilir, daha az efor).
  - Bir yıl için isabeti ~%34. "İşlemlerimin belki %20'si tüm paramı getiriyor, ben home run trader'ıyım."
- **Doğrulama** ◐: 100 milyon $ üstü zirve, Schwager ve Coyle'un *Market Wizards: The Next Generation* (2026) kitabında yer alıyor. Kitabın onun için hangi belgeyi denetlediğini bulamadım. Zirveden sonra kaldıraçlı long'dayken **yarısından fazlasını geri verdi** ◐.
- **Yöntem**:
  - Merdiven gibi yükselen güçlü hisselerde volatilite daralmasından günlük kırılım.
  - Tarama: 1-18 ayda en güçlü %2, likidite filtresi.
  - İlk itişte bir kısmı sat, kalanı 10/20 günlük ortalamayla taşı.
  - Diğer iki setup: episodic pivot, parabolik short.
  - Bu bilgi tabanındaki mekanik versiyon testi zayıf ama pozitif (+0,46R'ye karşı rastgele +0,21R, ~1,9 se, sadece 20 günlük ortalama çıkışıyla, README #64) ◐.
- **Ders**: Patlamalar **çok küçük hesapla ve bir maaş güvencesiyle** yaşandı, yani öğrenme bedeli hayatı bitirmedi. Servetin büyük kısmı 2020-21 momentum rejiminden geldi, 2022'de rejim dönünce büyük kısmı geri verildi (14 §3g: "rejimi bil").
- **Benzer örnek** ◐: Aynı kitapta Simon Rousseau ~40.000 $'dan 9 yılda ~yarım milyar $. O da defalarca para kaybetmiş, babasından borç almış, bırakmanın eşiğine gelmiş (Excess Returns özeti).

### 1.14 Takashi Kotegawa (BNF)

- **Doğrulama**: Aralık 2005'teki J-Com olayında (Mizuho'nun "1 hisseyi 610.000 ¥'den sat" yerine "610.000 hisseyi 1 ¥'den sat" hatası) ~2 milyar ¥ kâr. Maliye Bakanlığı'na verilen belgeye dayanıyor ✔ (Globe and Mail). 2000/2001'de ~1,6 milyon ¥ ile başlayıp ~18-20 milyar ¥'e ulaştığı ◐ (birbirini kopyalayan bloglar).
- **Yöntem** ◐: 25 günlük ortalamadan aşırı uzaklaşmış büyük hisselerde kısa vadeli dönüş (ortalamaya dönüş).
- **Ders**: Efsanenin bir kısmı **tek seferlik bir piyasa anomalisinden** geliyor. Hayatta kalma yanlılığının tipik örneği.

---

## 2. Taban oranlar: perakende trader'ların ne kadarı kazanıyor?

| Çalışma | Örneklem | Bulgu |
|---|---|---|
| **Barber, Lee, Liu, Odean** — *The Cross-Section of Speculator Skill* (2011 taslağı; J. Financial Markets 2014) ✔ | Tayvan, 1992-2006, **tüm** day trader'lar (yılda ortalama 360.000 kişi) | Tipik bir yılda **~%13** ücret sonrası kârda. Ama ertesi yıl da güvenilir kâr edenler **%1'den az** (~1.000 / 360.000 = %0,28). En iyi 500 kişi ertesi yıl günde net +28,1 bp, en kötüler -34,2 bp. |
| **Barber, Lee, Liu, Odean, Zhang** — *Do Day Traders Rationally Learn…?* (2017; RAPS 2020, "Learning, Fast or Slow") ✔ | Aynı veri | Toplam day trader performansı **15 yılın her birinde** ücret sonrası negatif. **%75'ten fazlası 2 yıl içinde bırakıyor.** 10+ gün işlem yapanların hayatta kalma oranı 1. yılda %44, 2. yılda %24, 3. yılda %15. Ömür boyu kârda olanlar deneyimlilerin ~%5'i. Zarar geçmişi olanlar hacmin **%72'si** (son yıllarda ~%80, yayımlanan özette %74). 50+ gün deneyimli **zarardaki** trader'ların **%95,3'ü** ertesi 12 ayda yine işlem yapıyor. |
| **Chague, De-Losso, Giovannetti** — *Day Trading for a Living?* (2019, rev. 2020) ✔ | Brezilya, 2013-2015'te mini Ibovespa vadelisinde ilk kez day trade yapan **19.646** kişi | 300 günden fazla devam eden **1.551** kişinin **%97'si zararda**. Asgari ücretten (günde 16 $) fazla kazanan **17 kişi (%1,1)**. Banka gişe memurundan (günde 54 $) fazla kazanan %0,4-0,5. En iyi kişi günde 310 $, standart sapması 2.560 $. **Öğrenme kanıtı yok.** |
| **SEBI** (Hindistan düzenleyicisi), Eylül 2024 ✔ | Hisse vadeli ve opsiyon, FY22-FY24, **1,13 crore (~11,3 milyon)** birey | **%93'ü zararda.** Kişi başı ortalama ~2 lakh ₹ zarar (maliyet dahil), toplam 1,81 lakh crore ₹. Zarar edenlerin **%75'ten fazlası** art arda zarar yıllarına rağmen devam etti. FY22 tek yılda %89. |
| **SEBI**, Temmuz 2024 ✔ | Nakit hisse piyasasında gün içi, FY23, ~7 milyon birey | **%71'i zararda.** Yılda 500'den fazla işlem yapanlarda %80. Zarar edenler zararlarının üstüne **%57** daha işlem maliyeti ödedi. |
| **ESMA** ürün müdahalesi, 27 Mart 2018 ✔ | AB'deki ulusal düzenleyicilerin CFD analizleri | Perakende hesapların **%74-89'u** zarar ediyor. Müşteri başı ortalama kayıp **1.600-29.000 €**. Bu yüzden her CFD aracısı kendi zarar oranını yayımlamak zorunda. |
| **AMF** (Fransa), 2014 ✔ | 14.799 aktif perakende FX/CFD müşterisi, 2009-2012 | **%89'u zararda**, ortalama kayıp ~10.900 €. |
| **IG UK** risk uyarısı (Kasım 2026'da sitede) ✔ | Aracının perakende hesapları, son 12 ay | "**%70**'i CFD ve spread bet'te para kaybediyor." Diğer büyük aracılar yaklaşık %50-80 aralığında ◐ (karşılaştırma siteleri). |
| **Topstep 2025** (09 §4o) ✔ | Prop combine'ları | Fonlananların %0,71'i Live hesaba geçiyor. |

**Okuma notları**:
- **Tek yılın kârı beceri değildir** ✔. Tayvan'da her yıl ~%13 kârda, ama sadece ~%0,3'ü bunu öngörülebilir şekilde tekrarlıyor. Bu, Grimes'ın sihirli para deneyinin (14 §5) gerçek veri karşılığı.
- **Yıllık oran, çok yıllık oranı olduğundan iyi gösterir**: aracının 12 aylık "%70 kaybediyor" rakamı, 4 yıllık bakışta %89'a (AMF), kalıcı kârlılıkta %99+'ya (Tayvan) dönüşüyor.
- **Kaybedenler bırakmıyor** ✔: Tayvan'da hacmin ~3/4'ü, Hindistan'da zarar edenlerin 3/4'ü. Piyasayı besleyen, zarar geçmişi olan ve devam eden trader.
- **Çok işlem daha kötü** ✔: SEBI'de yılda 500+ işlemde zarar oranı %80. Barber ve Odean (2000) ile aynı yön (08 §1).
- "%95 kaybeder" sloganının doğrudan kaynağı yok, ama gerçek rakamlar sloganla aynı ya da daha kötü (11 #11).

---

## 3. Hayatta kalma yanlılığı: şans kaç "sıfırdan zengin" hikâyesi üretir?

> Model (bu dosya için): her biri bağımsız işlemler, RR 2 (kazanınca +2R, kaybedince -1R). Avantaj sıfırsa isabet 1/3. Sabit yüzde risk (her işlemde güncel bakiyenin f'i). 1 milyon simüle trader. Gerçek kayıplar kümelendiği için (README #28) gerçek dünya bundan daha kötü.

**A) 5 yıl, 500 işlem, avantaj yok**

| İşlem başı risk | ≥100 kat (milyonda) | ≥10 kat | %90+ eriyen | Medyan sonuç |
|---|---|---|---|---|
| %1 | 0 | %0 | %0 | 0,96 |
| %5 | 96 | %1,25 | %25 | 0,31 |
| %10 | **989** | %0,96 | **%80** | 0,01 |
| %20 | 50 | %0,03 | %99,7 | 0 |
| %10, maliyetle (-0,05R) | 49 | %0,09 | %95 | 0,001 |

→ Avantajı olmayan **bir milyon** kişi %10 riskle işlem yaparsa, ~**1.000 kişi** 5.000 $'ı 500.000 $'a çıkarır ve hikâyesini anlatır. ~800.000 kişi hesabını kaybeder ve sessiz kalır. Dışarıdan bakan sadece 1.000 kişiyi görür.

**B) Yarışma benzeri tek yıl, 100 işlem**

| Avantaj | Risk | ≥2,5 kat (Minervini 1997 = %155) | ≥10 kat | %90+ eriyen |
|---|---|---|---|---|
| 0 | %10 | **%9,7** | %1,0 | %15 |
| 0 | %20 | %4,4 | %1,7 | %68 |
| +0,10R | %10 | %27,6 | %5,3 | %4 |

→ Basit modelde rastgele, yüksek riskli hesapların **~10'da biri** bir yarışma yılında %155 yapıyor. Bu Minervini ya da Ryan'ın şanslı olduğu anlamına **gelmez** (Ryan 3 yıl üst üste kazandı, ikisinin de çok yıllık kariyeri var). Anlamı şu: **tek bir yılın getirisi beceriyi tek başına kanıtlamaz** ✘ ("yarışma birinciliği beceri kanıtıdır" iddiası).

**C) Gerçek ve güçlü avantaj (+0,20R), 5 yıl, 500 işlem**

| Risk | Medyan sonuç | ≥10 kat | %90+ eriyen |
|---|---|---|---|
| %1 | **2,6 kat** | %0 | %0 |
| %2 | 6,0 kat | %22 | %0 |
| %5 | 39 kat | %81 | ~%0 |
| %10 (bu RR ve isabette tam Kelly) | 129 kat | %78 | %1,2 |

→ +0,20R, 500 bağımsız işlem boyunca, bu bilgi tabanının zaman testinden geçirebildiği her avantajdan büyük (README #46: RSI-2 ~+0,17R, ama seyrek ve kümelenmiş). Ders iki yönlü:
1. **Makul riskle** (%1) gerçek bir avantaj bile küçük hesabı 5 yılda ancak 2-3 katına çıkarır. "Sıfırdan zengin" için ya çok güçlü avantaj ya da çok yüksek risk gerekir.
2. Yüksek risk + gerçek avantaj çok güçlü. Ama avantajın gerçek olup olmadığını **önceden** bilmiyorsun (14 §6, README #62: ≥200 işlem ölçütü). Avantaj sanılan şey sıfırsa aynı risk %80 batış demek (tablo A).

---

## 4. Kanıtlı kazananların ortak noktaları

1. **Asimetri: küçük kayıp, büyük kazanç; isabet çoğu zaman %50'nin altında** ✔.
   - Kanıt: Tudor Jones 5:1 ve %20 isabet, Kullamägi ~%34, Parker ~%40 (12), Medallion %50,75, Brandt %54 ama kazanç/kayıp 4:1 (14 §3d).
   - Schwager'ın yeni kitaptaki sentezi: "**Büyük çoğunluğu zamanın yarısından fazlasında kaybediyordu**", ama kazandıklarında çok daha büyük kazanıyorlardı ◐ (Excess Returns özeti).
   - Bu bilgi tabanının testleri de aynı yerde: trend takibinde kârın %67'si işlemlerin en iyi %10'undan geliyor (README #72).
2. **Hayatta kalma önce gelir** ✔. Druckenmiller "sermaye koruma + home run", Tudor Jones "savunma", Seykota "zararı kes ×3", Soros "en iyi zarar kesen". Ters örnekler de aynı dersi veriyor: Livermore, Dennis ve Williams'ın kazandığı yıl içindeki %60 düşüş, kuralı bırakınca ya da kaldıraç artınca geldi.
3. **Uzun çıraklık ve piyasaya fiziksel yakınlık** ✔.
   - Tudor Jones: Tullis'in yanında pamuk salonu. Dennis: salon. Raschke: ~11 yıl opsiyon salonu. Druckenmiller: banka, sonra Soros. Soros: arbitraj masası. Ryan: O'Neil. Livermore: kotasyon tahtası.
   - Kârlılığa kadar geçen süre: Brandt 3-4 yıl ve ~3 patlama, Minervini ~6 yıl, Kullamägi ~2 yıl ve 3-4 patlama. Schwager'a göre ~90 Market Wizard'dan sadece **3-5'i** baştan kârlıydı (14 §3d).
4. **Tek bir tarzda ve piyasada uzmanlaşma** ✔. Brandt "berbat bir hisse trader'ıyım" diyor. Kullamägi ve Minervini sadece ABD momentum hisseleri, Raschke kısa vadeli vadeli işlemler, Seykota ve Turtle'lar trend.
5. **Erken patlamalar küçük hesapla yaşandı** ✔ (Brandt, Kullamägi, Minervini). Hayatta kalanların ortak yanı, öğrenme bedelini **hayatlarını bitirmeyecek boyutta** ödemiş olmaları. Kullamägi her seferinde maaşlı işe döndü. Brandt'ın tavsiyesi: "Çok küçük bahisler yap, yeterince küçük değil diyorsan yarıya indir" (14 §3d).
6. **Kurallarını yazdılar. Büyük felaketler kurala uyulmayan anlarda geldi** ✔. Dennis'in 1990 uzlaşması, Livermore'un pamuk tavsiyesi, Druckenmiller'ın 2000'deki "duygusal enkaz" anı. Parker: "Disiplin eksikliğinden kaçırdığım para, yöntemden kaçırdığımdan çok daha fazla" (12).
7. **Büyük servetler olağanüstü rejimlerde yoğunlaştı** ✔ (tarihler). Livermore 1907 ve 1929, Dennis ve Seykota 1970'lerin emtia enflasyonu, Tudor Jones 1987, Soros ve Druckenmiller 1992, Minervini 1990'ların sonu ve 2021, Darvas 1957-58, Kullamägi 2020-21, BNF 2005. Hazır oldular, ama büyüklüğü rejim verdi. Rejim dönünce geri verdiler: Kullamägi 2022, Druckenmiller 2000, Livermore 1930'lar.
8. **Sermaye büyük ölçüde başkasının parasıydı** ✔. Turtle'lar Dennis'in, Tudor Jones ve Marcus Commodities Corporation'ın, Druckenmiller Soros'un parasıyla işlem yaptı. Soros, Druckenmiller, Tudor Jones ve Simons'ın servetinin çoğu fon ücretlerinden. Perakende karşılığı prop sermayesi (09, 15), ama oradaki taban oranlar da düşük (README #47).

## 5. Ortak OLMAYAN şeyler (sır sanılanlar)

- **Ortak bir gösterge, formasyon ya da "gizli setup" yok** ✔. Yöntemler zıt: makro tez (Soros), trend sistemi (Seykota), momentum kırılımı (Kullamägi), başarısız kırılımı ters işlemek (Raschke'nin Turtle Soup'u, Kullamägi'nin kırılımının tam tersi), istatistiksel arbitraj (Simons), ortalamaya dönüş (BNF).
- **Yüksek isabet ortak değil** ✔. Neredeyse hepsi %35-55 isabette (Brandt: "%80 isabet kovalayanlar rüya dünyasında").
- **Yayımlanan "sır" yayımlandıktan sonra zayıflıyor** ✔: Turtle kuralları 1986 sonrası, 20 günlük kırılım bugün (README #22), sweep ve SFP filtresiz (README #19, #51). Fibonacci hiçbir kanıtlı trader'ın ana aracı değil (README #9).
- **Hız ve gün içi scalping ortak değil**. Kanıtlı servetlerin çoğu günler ile aylar arası vadede. Kullamägi bile ilk milyondan sonra day trading'i bıraktı. Medallion'un kısa vadesi ise perakende maliyetiyle imkânsız (§1.6).

## 6. Dürüst sonuç: trading ile "sıfırdan zengin" gerçekçi mi?

1. **Olasılık** ✔: Kalıcı kârlı day trader oranı %0,3-1 (Tayvan). Brezilya'da başlayan her ~1.150 kişiden 1'i asgari ücretin üstünde kazanıyor, zengin olan değil. Brandt'ın tahmini: 3 yıl eğitim sonrası 5 yıl %30 ortalama **binde 2-5** (14 §3d). "Zengin" eşiği bundan da nadir.
2. **Bileşik getiri aritmetiği** ✔:
   - 10.000 $ yılda %30 (dünya klası) ile 10 yılda **~138.000 $**, 20 yılda ~1,9 milyon $.
   - Yılda %50 ile 10 yılda ~577.000 $.
   - "Sıfırdan zengin" için ya yıllarca %100+ getiri gerekiyor. Bu yüksek risk demek ve avantaj yoksa %80+ batış (§3A). Ya da **başkasının sermayesi**: fon ücreti ya da prop kâr payı.
3. **Görünen hikâyeler** ✔: Avantajı olmayan milyon kişiden ~1.000'i yüksek riskle 100 kat yapar (§3A). Hikâyeyi bu bin kişi anlatır, ~800 bin batan anlatmaz. Kanıtlı listedekilerin bile çoğu batmış, başarısız olmuş ya da olağanüstü bir rejime denk gelmiş.
4. **Ne zaman sürer?** Hayatta kalanlarda bile **2-6 yıl** ve birkaç patlama (Brandt, Minervini, Kullamägi). 6 yılda olmayanlar görünmüyor. Tayvan'da 3 yıl sonra başlayanların %15'i hâlâ işlem yapıyor, onların da çoğu zararda.
5. **Kanıtla tutarlı tek yol** (15'teki prop yol haritasıyla aynı):
   - Geliri trading'e bağlama. Kullamägi'nin güvenlik işi, Brandt'ın "işin varsa SPY biriktir" tavsiyesi (14 §3d).
   - Küçük riskle (%0,5-1) **ölçülebilir** bir avantaj kur ve rastgeleye karşı test et (README #62).
   - Avantaj kanıtlanınca sermayeyi kaldıraçla değil **prop ya da yönetilen para** ile büyüt (09, 15).
   - Başarıyı Grimes'ın kademeleriyle ölç (14 §2): önce zarar etmeyi bırak, sonra masrafları karşıla, sonra büyü.
   - Ve kabul et: bu yol "zengin" değil, büyük ihtimalle **ek gelir ya da yan meslek** üretir. Dev servet kanıtlı örneklerde bile çoğunlukla fon yönetiminden geldi.

## 7. Bu bilgi tabanı için çıkarımlar

- **İddia değerlendirme**: Bir trader'ın kaydını §0 merdiveniyle derecelendir. Tek yıl, yarışma ya da ekran görüntüsü = beceri için zayıf kanıt (§3B). En az 10 yıl, mümkünse denetim (Schwager).
- **Replay uygulaması**: Hedefi "bir yılda 10 kat" değil, Grimes kademeleri ve kendi setup'ının rastgeleye karşı farkı olarak koy. "Kaç kişiden biri bunu şansla yapardı?" sorusunu §3 tablosuyla cevapla.
- **Sweep ilgisi**: Kanıtlı ataları var (Raschke'nin Turtle Soup'u, Wyckoff spring'i). Ama bu ataların hiçbiri filtresiz kullanmadı. Bu bilgi tabanının testi de filtresiz versiyonu destekleklemiyor (README #19, #51, #68).
- **Psikoloji**: Kanıtlı trader'ların büyük hatalarının ortak noktası kural bilgisizliği değil, **bildiği kurala uymamak** (Dennis, Livermore, Druckenmiller). 08 ve 02 §6d'deki önceden yazılmış eğer-ise kuralları bu yüzden önemli.

---

## Kaynaklar

**Akademik ve düzenleyici**
- Barber, Lee, Liu, Odean (2011), *The Cross-Section of Speculator Skill: Evidence from Day Trading*: https://faculty.haas.berkeley.edu/odean/papers/day%20traders/Day%20Trading%20Skill%20110523.pdf
- Barber, Lee, Liu, Odean, Zhang (2017), *Do Day Traders Rationally Learn About Their Ability?* (RAPS 2020'de "Learning, Fast or Slow"): https://faculty.haas.berkeley.edu/odean/papers/day%20traders/day%20trading%20and%20learning%20110217.pdf · https://ideas.repec.org/a/oup/rasset/v10y2020i1p61-93..html
- Chague, De-Losso, Giovannetti (2019/2020), *Day Trading for a Living?*: https://ideas.repec.org/p/fgv/eesptd/525.html · özet ve sayılar: https://quantpedia.com/retail-day-trading-is-an-uphill-battle/
- SEBI, F&O çalışması (Eylül 2024): https://www.sebi.gov.in/media-and-notifications/press-releases/sep-2024/updated-sebi-study-reveals-93-of-individual-traders-incurred-losses-in-equity-fando-between-fy22-and-fy24-aggregate-losses-exceed-1-8-lakh-crores-over-three-years_86906.html · https://www.outlookbusiness.com/markets/fo-frenzy-over-93-retail-investors-lost-average-rs-2-lakh-in-three-years-says-sebi
- SEBI, gün içi nakit piyasa çalışması (Temmuz 2024): https://www.business-standard.com/markets/news/7-in-10-intraday-traders-in-equity-cash-suffered-losses-in-fy23-sebi-study-124072400975_1.html
- ESMA basın açıklaması (27.03.2018): https://www.esma.europa.eu/node/84933
- AMF (Fransa) FX/CFD çalışması 2014: https://www.financemagnates.com/forex/analysis/amf-publishes-four-year-fx-study-89-of-investors-experiencing-losses/
- IG UK risk uyarısı: https://www.ig.com/uk/trading

**Trader'lar**
- Tudor Jones: https://en.wikipedia.org/wiki/Paul_Tudor_Jones · 1987 getirisi: https://insidermonkey.com/blog/paul-tudor-jones-tudor-investment-corps-return-aum-and-holdings-728583 · erken kariyer: https://seanperry.substack.com/p/eagle · 200 günlük ortalama alıntısı: https://www.kagels-trading.de/paul-tudor-jones/
- Druckenmiller: https://www.wikipedia.org/wiki/Stanley_Druckenmiller · 2000 hatası: https://novelinvestor.com/stan-druckenmillers-worst-mistake-ever/ · Soros dersleri: https://acquirersmultiple.com/2017/11/stanley-druckenmiller-the-greatest-lesson-i-ever-learned-from-george-soros/
- Soros / Quantum: https://www.wikipedia.org/wiki/Quantum_Fund · 2000 mektubu: https://money.cnn.com/2000/04/28/mutualfunds/soros/letter.htm
- Seykota: https://www.wikipedia.org/wiki/Ed_Seykota
- Dennis ve Turtle'lar: https://en.wikipedia.org/wiki/Richard_Dennis · https://en.wikipedia.org/wiki/Turtle_Traders · https://www.fia.org/hall-fame/articles/richard-j-dennis
- Medallion: https://www.institutionalinvestor.com/article/2bswymr8cih3jeaslxc00/portfolio/famed-medallion-fund-stretches-explanation-to-the-limit-professor-claims · bileşik getiri eleştirisi: https://arxiv.org/pdf/2405.10917v2 · 2020 farkı: https://www.institutionalinvestor.com/article/2bswms7wco7as686o8ikg/portfolio/renaissances-medallion-fund-surged-76-in-2020-but-funds-open-to-outsiders-tanked · %50,75 alıntısı: https://physicsworld.com/a/money-from-maths/
- Thorp: https://en.wikipedia.org/wiki/Princeton_Newport_Partners · https://moneyweek.com/461698/edward-thorp-the-worlds-greatest-investors
- Raschke: https://en.wikipedia.org/wiki/Linda_Bradford_Raschke · https://lindaraschke.net/bio-linda/
- USIC ve Minervini: https://www.prnewswire.com/news-releases/stock-trader-wins-us-investing-championship-a-second-time--breaks-record-301466652.html · kurallar: https://parakeet-oboe-9cy6.squarespace.com/faq · Minervini'nin ilk yılları: https://michaelsincere.com/articles/my-marketwatch-interview-with-stock-market-wizard-mark-minervini
- David Ryan: https://www.turtletrader.com/trader-ryan/
- Larry Williams: https://en.wikipedia.org/wiki/Larry_R._Williams · yarışma içi düşüş (◐): https://www.elitetrader.com/et/threads/larry-williams.379087/post-5953152
- Livermore: https://en.wikipedia.org/wiki/Jesse_Lauriston_Livermore
- Darvas: https://en.wikipedia.org/wiki/Nicolas_Darvas · Time 1960: https://time.com/archive/6811019/wall-street-216000-or-2000000/
- Kullamägi: Chat With Traders #212 (YouTube K0F73Sq90j0) · Schwager ve Coyle, *Market Wizards: The Next Generation* (2026), özet: https://excessreturnspod.substack.com/p/walk-on-water-five-lessons-from-jack
- BNF / J-Com: https://www.theglobeandmail.com/report-on-business/two-investors-reap-millions-from-bungled-j-com-trade-on-tokyo-exchange/article18255536/

**Bu bilgi tabanındaki bağlantılı dosyalar**: 08 §1 (akademik veriler), 09 (prop), 11 (efsaneler), 12 (Parker, Turtle, Clenow), 14 (Brandt, Grimes, Breitstein), 15 (yol haritası).
