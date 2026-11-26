# 02 — Risk Yönetimi ve Pozisyon Boyutu

> Güven seviyesi: **YÜKSEK** (matematik doğrulandı: `arastirma/verify_math.py`, `arastirma/verify_ftmo.py`)
> Kaynaklar: AlgoCoinism (matematik + işlem planı videoları), DD Finance "Kazananlar vs Kaybedenler", Tradeciety position sizing makalesi.

## 1. Altın kural: risk sabit, lot değişken

```
Pozisyon büyüklüğü = (Hesap × risk%) / stop mesafesi
```

- Stop geniş → lot küçük. Stop dar → lot büyük. **Riske edilen para her işlemde aynı.**
- Örnek: 1000$ hesap, %0.5 risk = 5$. Stop %1 uzakta → pozisyon 500$. Stop %2 → 250$.
- Forex/CFD: `lot = risk$ / (stop_pip × pip_değeri)`. Futures: `kontrat = risk$ / (stop_tick × tick_değeri)`.
- **Önce stop yeri belirlenir (fikrin geçersiz olduğu yer), sonra lot hesaplanır.** Asla tersi değil ("şu kadar lot açayım, stopu da sığacak yere koyarım" = hata).

## 2. Risk/işlem seviyesine göre ne olur? (WR %40, 2R, 500 işlem — kârlı sistem!)

| Risk/işlem | Tepeden dibe %50 düşüş ihtimali | Medyan maks. düşüş | %95'lik kötü senaryo düşüş |
|---|---|---|---|
| %0.5 | ~0 | %8 | %13 |
| %1 | ~0 | **%15** | **%25** |
| %2 | %2.2 | %29 | %45 |
| %5 | **%85** | — | — |
| %10 | **~%100** | — | — |

**Kritik çıkarım:** Kârlı bir sistemle bile %1 riskte medyan maksimum düşüş ~%15. FTMO gibi **%10 maks. zarar** limitli hesaplarda %1 risk bile sınırda → prop hesaplarda %0.5–1 makul üst sınır. (Detay: [09-prop-firm-ftmo.md](09-prop-firm-ftmo.md))

## 3. Kayıp-toparlanma asimetrisi

| Kayıp | Başa dönmek için gereken kazanç |
|---|---|
| %10 | %11.1 |
| %20 | %25 |
| %30 | %42.9 |
| %50 | **%100** |
| %65 | %186 |
| %80 | %400 |

10 ardışık stop: %1 riskte −%9.6 (toparlanır), %2'de −%18.3, %5'te −%40, **%10'da −%65** (toparlanması için hesabı ~3 katına çıkarmak gerekir).

## 4. Stop kuralları

- Stop = **fikrin geçersiz olduğu yer** (yapı noktasının ötesi), rastgele pip sayısı değil.
- Seviyenin **tam altına değil, biraz ötesine** koy — herkesin stopunun olduğu yer avlanır (bkz. [05-likidite-sweep-ve-tuzaklar.md](05-likidite-sweep-ve-tuzaklar.md)).
- Stop **asla zarar yönünde uzatılmaz**. Kâr yönünde taşıma (breakeven/trailing) olacaksa önceden plana yazılır.
- Veri (Odean 1998): yatırımcılar kârların %14.8'ini, zararların sadece %9.8'ini realize ediyor → kârı erken kesip zararı taşıyoruz (disposition effect). Stop çekmek bu önyargının ta kendisi.

## 4b. ✔ Başa baş stopu ve "bedava işlem" efsanesi (Dante CWT 39 + simülasyon, `arastirma/verify_dante_sizing_be.py`)

Dante'nin prop'ta öğrendiği ders: "**Desteği aldın, 20 tick yükseldi, desteğe geri geldi. Başa başta çıkarsan pozisyonu tam desteğin içine kusmuş olursun.** Piyasayı işle, P&L'ini değil." Risk/ödül statik değildir, işlem boyunca değişir.

Simülasyon: Gauss rastgele yürüyüş, stop 1R, hedef 2R, 20.000 işlem. Çıkış, ulaşılan gerçek fiyattan (stop kayması dahil).
| Trend (avantaj) | Başa baş yok | +0,5R'de başa baş | +1R'de | +1,5R'de |
|---|---|---|---|---|
| 0 (avantaj yok) | ≈0 | ≈0 (%46 başa baş çıkış) | ≈0 | ≈0 |
| Küçük (+0,01/adım) | **+0,21R** | +0,13R (**-%39**) | +0,14R | +0,20R |
| Orta (+0,03/adım) | **+0,67R** | +0,39R (**-%41**) | +0,54R | +0,61R |

- **Avantaj yoksa hiçbir stop kuralı işe yaramaz** (optional stopping teoremi). Başa baş sadece dağılımı değiştirir: daha az tam kazanç, daha çok "sıfır" işlem. Dikkat: ilk denemede çıkışı tam stop fiyatından kaydettiğimde sahte bir +0,04R çıktı. Başa baş stoplarının sık tetiklenmesi, kaymayı yok sayan bir backtest'i iyimser yapar.
- **Avantaj varsa erken başa baş işlem başı beklentiyi ciddi düşürür.** +1,5R gibi geç taşıma neredeyse maliyetsiz. Zaman başına beklenti kabaca aynı kalıyor, çünkü işlemler daha erken bitiyor. Ama bu, serbest kalan zamanı dolduracak başka bir setup varsa işe yarar. Çoğu takdirli trader için önemli olan işlem başı beklentidir.
- **Kural**: Başa başa taşıma **yapıya bağlı** olmalı. Fiyat yeni bir yüksek dip yaptıysa stopu onun altına taşı. "Kendimi rahat hissetmek için" sabit bir pip ya da R'de taşıma. Taşıma kuralı varsa önceden yaz ve backtest'te kaymayla test et.

## 4c. ✔ Değişken boyut pozitif bir sistemi öldürebilir mi? (Dante'nin öğrencisi + simülasyon)

Dante'nin vakası: Öğrencinin günlüğünde boyut tutarsızdı. Sezgiyle beğendiği setup'ta 4-5 lot, bir kayıptan sonra intikam için 2 katı, iki kayıptan sonra korkuyla 1 lot, sonra da tabii ki kazanç geliyordu. Uzun örneklemde **beklentisi pozitif ama hesabı zararda**. "Hep 1 lot ya da hep 5 lot girseydi çok para kazanırdı."

Simülasyon: WR %50, kazanç 1,3R, lot başına +0,15R, 200 işlem, 20.000 tekrar.
| Boyut kuralı | Ortalama P&L | Lot başına | 200 işlem sonunda zararda olma ihtimali |
|---|---|---|---|
| Sabit 2 lot | +60R | +0,150 | %3 |
| Dante deseni, işlem kalitesi aynı | +67R | +0,149 | %5 |
| + sezgiyle 5 lot, kalite aynı | +89R | +0,151 | %5 |
| **İntikam işlemleri (4 lot) WR %40** | +22R | **+0,050** | **%30** |
| **İntikam WR %40 + sezgi 5 lotları WR %42** | +7R | **+0,012** | **%45** |

- **Matematik**: İşlemler bağımsızsa geçmiş sonuçlara göre seçilen boyut beklentinin işaretini **değiştiremez**. Beklenen kâr = ortalama boyut × EV. Sadece varyansı büyütür, zararda bitme ihtimalini %3'ten %5'e çıkarır.
- **Asıl zarar**, büyük boyutun **kötü işlemlerle** birleşmesinden gelir. İntikam işlemleri ve "sezgi" işlemleri, duygusal durumda alındıkları için daha düşük kaliteli. Lot başına beklenti +0,15'ten +0,01'e düşüyor, zararda bitme ihtimali %45. Dante'nin öğrencisinde olan muhtemelen buydu.
- **Kural**: Boyut sabit, istatistikle değişir, sezgiyle değil (§6c, 10 §6h madde 4). Bir kayıptan sonraki işlemi günlükte ayrıca etiketle ve kalitesini ölç. Bu sütun "intikam" etkisini doğrudan gösterir.


**Breitstein'ın A/B/C/D notlama sistemi** (ubofAZwgd4w):
- **Notlar**:
  - **D**: işlem yok. "Grafiklerin %99,9'u D ya da daha kötü."
  - **C**: küçük "yoklama" boyutu.
  - **B**: standart boyut, işlemlerin çoğu.
  - **A**: her şey aynı yönü gösteriyor. Boyut artırılır.
- Her setup'ın **ayrı bir puan tablosu** var. Ör. panik dibi yakalamada hızlı düşüş, "sıkıcı" hisse, günlük destek, gün içi tablo ve haber olmaması. Kırılımda uzun ve sıkı konsolidasyon, hacim, haber, piyasa koşulları ve günlük grafik.
- **Kural**: notu **girmeden önce** günlüğe yaz. Birkaç ay sonra "A'lar B'lerden gerçekten iyi mi?" diye kontrol et. Değilse puan tablon yanlış.
- Grimes ve Brandt farklı düşünüyor: "Boyut takdire bırakılmaz" (§6c), "Beklentisi en yüksek işlemlerim çoğu zaman en kötüleri" (09 §4r).

**✔ Test** (`arastirma/verify_trade_grading.py`, RR 2, B işlemleri +0,10R):

1. **A'nın B'den gerçekten iyi olduğunu göstermek için gereken A işlemi sayısı.** Tek yönlü test, %5 anlamlılık; hücreler testin farkı yakalama olasılığı.

| A işlemi sayısı | Fark +0,15R | Fark +0,30R | Fark +0,50R |
|---|---|---|---|
| 20 | %10 | %19 | %38 |
| 50 | %16 | %34 | %67 |
| 100 | %22 | %57 | %90 |
| **200** | %36 | **%82** | %100 |

   - +0,3R'lik gerçek bir farkı güvenle görmek için **~200 A işlemi** gerekiyor. A'lar işlemlerin %15'iyse bu **~1.300 işlem** eder.
   - "Birkaç ay" ancak çok sık işlem yapan biri için yeterli.

2. **Notlamanın bir yıla etkisi** (200 işlem; A 2 kat, C 0,5 kat boyut ile sabit %1 risk karşılaştırması). Hücreler: ortalama getiri / en kötü %5'lik dilim / medyan maksimum düşüş.

| Notların bilgi değeri | Notlu boyut | Sabit boyut |
|---|---|---|
| Bilgili (A +0,40R, C 0) | **+%45** / -%3,9 / %14,5 | +%28 / -%9,5 / %14,1 |
| Bilgisiz (hepsi +0,10R) | +%23 / **-%17,5** / %17,1 | +%22 / -%14,7 / %15,0 |
| Ters (A -0,10R, C +0,30R) | **+%14** / -%24 / %18,8 | +%24 / -%12 / %14,9 |

   - **Notlar gerçekten bilgi taşıyorsa** boyutlandırma büyük kazandırıyor.
   - **Bilgi taşımıyorsa** getiri aynı kalıyor, kuyruk riski artıyor.
   - **Ters yöndeyse** (Brandt'ın uyarısı) zarar veriyor. Dante'nin öğrencisi örneğiyle (yukarıda) aynı sonuç.

**Sonuç**:
- **Kanıtlanana kadar sabit boyut kullan, notları sadece kaydet.**
- Yeterli A örneklemi birikip A'ların üstünlüğü istatistiksel olarak görüldüğünde boyut farkını aç. Önce küçük farkla başla, ör. A için 1,5 kat.
- Prop hesabında A'da 2 kat boyutun günlük limite etkisini de hesaba kat (09 §4p).

**SMB Capital'in daha uç dağılımı** (Jeff Holden, Chat With Traders UWDFkMaJXNw; `arastirma/verify_smb_allocation.py`):
- SMB'de risk **günlük stopun yüzdesi** olarak dağıtılıyor: A+ %80, A %30, B %15, C %5. Yani A+ ile C arasında 16 kat fark var.
- **Prop çevirisi**: kişisel günlük stop hesabın %2'si (FTMO'nun %5'inin içinde) → A+ %1,6, A %0,6, B %0,3, C %0,1. Karışım A+ %5, A %15, B %40, C %40, yılda 250 işlem. Kıyas: aynı ortalama riskle (%0,33) sabit boyut.

| Notlar | SMB dağılımı: yıllık ort. / 5. yüzdelik / P(düşüş > %10) / P(+%10, -%10'dan önce) | Sabit boyut |
|---|---|---|
| Bilgi taşıyor (A+ +0,5R ... C 0) | **+%19,7** / +%1,4 / %13 / **%88** | +%9,1 / -%3,3 / %6,5 / %57 |
| Bilgi taşımıyor (hepsi +0,1R) | +%8,3 / -%9,2 / **%34** / %58 | +%8,3 / -%4,3 / %7,6 / %53 |
| "Kaygan A+" (A+ -0,1R) | +%7,6 / -%9,4 / **%35** / %56 | +%6,6 / -%5,3 / %10 / %45 |

- Notlar gerçekten bilgi taşıyorsa getiri 2 katına çıkıyor, challenge geçme %57'den %88'e çıkıyor.
- Taşımıyorsa getiri aynı, ama %10'luk düşüş (FTMO toplam limiti) olasılığı **4 katına** çıkıyor.
- Holden'ın kendi uyarısı: "A+'yı tanımlamada çoğu zaman kaygan davranıyoruz." Ve: "İlk 3 ay risk artışını düşünme bile. Başarılı trader'larda dönüm noktası 4 aylık tutarlılıktı." Bu kapı, notların bilgi taşıdığı kanıtlanmadan büyük boyut farkını açmamak demek. Buradaki sonuçla aynı.
## 5. Kaldıraç ve marj (kripto/vadeli)

- Kaldıraç riski **artırmaz**, risk stop mesafesi × pozisyonla belirlenir. Kaldıraç sadece teminatı küçültür. Ama yüksek kaldıraç = likidasyon fiyatı stopa yakın.
- **İzole marj**: kayıp o pozisyonun teminatıyla sınırlı; likidasyon stoptan **önce** gelmemeli → teminatı ona göre ayarla.
- **Çapraz marj**: tüm bakiye teminat; likidasyon uzak ama kötü günde tüm hesap gider.
- ⚠️ "Likidasyonu stop gibi kullan" (DD Finance eski risk videosu) **kötü uygulama**: likidasyonda ek ücret/kayma olur, kontrol borsada kalır. Her zaman gerçek stop emri kullan.

## 6. Pratik risk seviyeleri (konsensüs, kanıtla tutarlı)

- Öğrenme/kanıtlama aşaması: **%0.25–0.5**
- Kanıtlanmış sistem, kişisel hesap: **%0.5–1**
- Prop challenge (%10 max DD / %5 günlük): **%0.5–1** (detay 09)
- %2 üstü: profesyonellerin neredeyse hiçbiri tek işlemde kullanmaz.
- Kendine sor: *"Arka arkaya 7 kayıp gelirse hâlâ planıma uyabilir miyim?"* Cevap hayırsa risk çok büyük.

## 6b. Doğrulanmış kaydı olan bir ustanın gerçek risk rakamları (Peter Brandt, TraderLion 2025, _G8QyHkvQ2Q)

> Brandt'ın kaydı Jack Schwager tarafından Market Wizards için aylık ekstreler ve vergi beyannamesi-banka mutabakatıyla incelendi: ortalama yıllık ~%51 getiri. Son zararlı yılı 2013. O tarihten beri ~%45 ±10-15.

| Kalem | Brandt'ın rakamı |
|---|---|
| Kariyerinin başında işlem başına risk | **%10**, "Delilik. Kesinlikle delilik." Yeni başlayanların metrikleriyle nasıl sıfırlanacaklarını gösterebileceğini söylüyor |
| Bugün işlem başına risk | **~70 baz puan (%0,7)**, "100 baz puanın (%1) altında tut" |
| Başlangıç riski | 35-40 baz puan |
| Ortalama kayıp | **15-17 baz puan**. Stopu sürekli sıkılaştırarak, tercihen 1 hafta içinde başa başa çekerek |
| Yanılma oranı | **~%45** |
| Yıllık hedef maksimum düşüş | **%3-4** (eskiden %35-40 aylık, %50-60 gün içi düşüşler yaşamış: "Gençken yapabiliyordum, şimdi yapamam") |
| Pozisyon sayısı | Aynı anda 6-10 |
| Örnek boyut | Her 1 milyon $ için 3 micro Nasdaq kontratı |

- **Bileşik (korele) risk**: Hisselerde pozisyonlar birbirine çok bağlıdır. "Polis depoyu bastığında piyanistle birlikte herkesi tutuklar." Üç yarı iletken hissesinde %0,7'şer risk = tek bir **%2+** bahis. Futures'ta farklı sektörlerle (yumuşak emtia, endeks, metal, tahıl) çeşitlendirme daha kolay. → **Toplam açık risk** de bir limit olmalı, sadece işlem başına risk değil.
- **Aracı kurum riski**: Brandt'ın çalıştığı **4 aracı kurum battı**, para kaybettirdi. Kurumlarda sadece gereken marjı tutuyor, fazlasını her hafta çekiyor, mümkünse kendi adına hazine bonosu (T-bill) tutuyor. → Prop firm/broker seçiminde karşı taraf riskini düşün (09 §4).
- Twitter'da sorduğunda gelen cevaplar: "İşlem başına %5, %10, %15 risk." → "**Patlamaya mahkumlar.**"

## 6b-2. Volatiliteye göre boyutlandırmada taban volatilite (Clenow ve Parker, Top Traders Unplugged #91)

Volatiliteye göre boyut ("pozisyon = risk / volatilite") düşük volatilitede çok büyük pozisyon üretir. Volatilite yapay olarak bastırılmışsa (sabit kur, para politikası tabanı) bu ölümcül olur. Örnek: 15 Ocak 2015'te SNB EUR/CHF tabanını kaldırınca CHF dakikalar içinde %20-30 hareket etti, ve düşük volatilite yüzünden büyük pozisyon taşıyan fonlar o ay %25-30 kaybetti. → **Formüle taban volatilite koy**: örneğin yıllık %5 ya da ATR için son 1-2 yılın alt yüzdelik dilimi. **Aynı riski taşıyan araçları ayrı pozisyon sayma**: CHF futures ve EUR/CHF, ya da ham petrol, benzin ve ısınma yakıtı. Kısa vadeli faiz kontratlarının 100 üstü gibi **asimetrik risk** durumlarında trend modeli riski göremez, kontrol et.

## 6b-3. ✔ Piyasa kırılınca pozisyon boyutu: sürekli volatilite ayarı (Rob Carver, Top Traders Unplugged #386, OVh3f8hmchA)

> **Olay**: 30 Ocak 2026'da gümüş ~46 yılın en büyük günlük düşüşünü yaşadı. Veriyle kontrol ettim: gümüş vadelisi (SI=F) **−%31**, SLV **−%28,5**. Doğalgaz 9-30 Ocak arasında ~+%60 yükseldi, 2 Şubat'ta **−%25** düştü (UNG, Carver'ın −%26 rakamıyla uyumlu).

**Carver'ın anlattıkları:**
- **Sonuç**: Carver'ın sistemi o gün hesabın sadece **~%3**'ünü kaybetti.
  - Birinci sebep **sürekli volatilite ayarı**: fiyat yükseldikçe volatilite de arttığı için sistem 31 Aralık'ta ve ertesi pazartesi kontrat sattı. Pozisyon fiyatla birlikte büyümedi, volatilite arttıkça küçüldü.
  - İkinci sebep **çeşitlendirme**.
  - Volatilite ayarı yapmayan bir CTA ise o ay perşembe günü **+%72**'deydi, ayı **+%27** ile kapattı.
- **Stop ile volatilite birlikte düşünülür.** Volatilite artarken stopu genişletiyorsan lotu küçültmen gerekir, yoksa işlem başına risk büyür. Stopu dar tutarsan bu kez gürültüyle erken silkelenirsin. → §1'deki "stop mesafesi × lot = sabit risk" kuralını **açık pozisyonlar için de her gün** yeniden uygula.
- **Likidite sabit değildir.** Carver'ın benzetmesi: "Tek yangın kapısı olan sinema." Fiyat yükselirken piyasaya giren "gümüş turistleri" aynı anda çıkmak isteyince kapı daralır. Bir enstrümanın likiditesine son birkaç aya değil, son **1-2 yılın** geçmişine bakarak karar ver.
- **Kalabalık (crowding)**: CTA'lar, risk paritesi fonları ve kantitatif fonlar volatilite sıçradığında **hep birlikte** risk azaltır, bu da hareketi büyütür. (Ocak 2026'da CTA'lar zaten satıcı tarafındaydı ve tampon oldular.)
- **Nelson Bunker Hunt (1979-80)**: kaldıraçlı dev gümüş pozisyonu, borsanın marj artışlarıyla çöktü. Ders: **piramitleme yaparak pozisyonun kontrolden çıkmasına izin verme.**
- **Gümüş altın değildir.** Gümüşün sadece ~%30'u kendi madeninden çıkıyor, geri kalanı altın ve bakır madenciliğinin yan ürünü. Arz fiyata yavaş tepki veriyor, bu yüzden gümüş daha oynak.
- **"Sistematik Rob ile takdirli Rob"**: Nisan 2025 tarife çalkantısında Carver takdirli hesabındaki tüm hisseleri sattı ve bu ona performans kaybettirdi. Sistematik sistemi o tarihten beri +%20-25 kazandı (08 ve 10 §6j'deki "kurcalama" dersinin canlı örneği).
- **Toplam riski hedefe ölçeklemek** (dinleyici sorusu):
  - Her enstrüman aynı volatiliteye ayarlanmışsa, portföy riskini belirleyen tek şey korelasyondur. Korelasyon 1'in altındaysa portföy hedef riskin altında kalır.
  - Carver'ın **çeşitlendirme çarpanı 4-5**. Bu çarpanla ölçeklemezse yıllık %15'lik risk hedefi fiilen ~%3 olurdu.
  - Korelasyonu enstrümanların **P&L akışlarından ~6 aylık pencereyle** tahmin etmek makul, çünkü bu hem varlık hem sinyal korelasyonunu birlikte yakalar.
  - Kitaplarındaki "0,7" sabit bir korelasyon değil. Trend P&L korelasyonunun ham varlık korelasyonuna oranı.
- **Volatiliteyi ve korelasyonu ayrı tahmin et.** Volatilite için ~1 aylık, korelasyon için ~6 aylık pencere kullan; volatilite daha öngörülebilir. Aşağıda test edildi.

**✔ Test** (`arastirma/verify_vol_adjust.py`, 12 ay momentumu, 19 ETF ve parite, 2005+). Sinyal aynı, varyantlar sadece **pozisyon büyüklüğünün sinyalden sonra nasıl yönetildiğinde** farklı:

| Varyant | Sharpe | Maks. düşüş | En kötü gün (kendi günlük std'si cinsinden) | Basıklık | %10 vol'e ölçekli en kötü gün |
|---|---|---|---|---|---|
| A: aylık volatiliteye göre yeniden boyutlama | **0,56** | %8 | **−6,1σ** | 3,5 | **−%3,8** |
| B: günlük volatiliteye göre yeniden boyutlama (%10 tampon) | 0,49 | %8 | −5,8σ | 2,2 | −%3,7 |
| C: girişte volatiliteye göre boyut, sonra **sabit lot** | 0,45 | %11 | **−11,3σ** | 6,8 | **−%7,1** |
| D: sabit lot, eşit nominal (volatilite hiç yok) | 0,39 | %23 | −16,5σ | 18,0 | −%10,4 |

- **Gümüş olayında** (SLV pozisyonunun sermayeye katkısı):
  - **A**: Ocak'ta +28 baz puan, en kötü günde −27 baz puan.
  - **C**: Ocak'ta +118 baz puan, en kötü günde **−211** baz puan. Lot sabit kaldığı için pozisyon %5'ten %8'e büyümüştü.
  - **D**: Ocak'ta +323 baz puan, en kötü günde **−578** baz puan, yani ayın tüm kârı ve fazlası tek günde gitti. Carver'ın anlattığı "+%72'den +%27'ye" düşüşün küçük ölçekli kopyası.
- **Sonuç**:
  - **Pozisyonu güncel volatiliteye göre yeniden boyutlamak** Sharpe'ı artırıyor (0,56'ya karşı 0,45/0,39) ve **kuyruk günlerini yarıya indiriyor**. ✔ Carver'ın ana iddiası doğrulandı.
  - Aynı toplam volatilitede sabit lotlu versiyonun en kötü günü ikiye katlanıyor (−%7,1'e karşı −%3,8). Prop hesabında bu, **%5 günlük limiti tek günde aşmak** demek.
- **Günlük ile aylık ayar arasında fark yok.** Bu kaba uygulamada B, A'dan biraz kötü (0,49'a karşı 0,56). Asıl kazanç ayarın **sıklığından** değil, **hiç yapılıp yapılmamasından** geliyor. Ayda bir yeniden boyutlamak yetiyor.
- **Challenge sonuçları gürültülü.** %8 volatilitede A %73 geçiyor, %23 kalıyor. C %66 geçiyor, %15 kalıyor. Ama aylık başlangıçlar üst üste bindiği için bu ~10 puanlık farklar güvenilir değil. Kuyruk günü bulgusu ise sağlam.

**Takdirli ve prop trader için uygulama:**
1. **Açık bir kazanan pozisyonun bugünkü riskini her gün hesapla**: lot × güncel ATR (ya da stop mesafesi). Başlangıç riskinin belirgin üstüne çıktıysa (ör. 2 kat), pozisyonu kısmen kapatıp riski başlangıç seviyesine indir. Parabolik harekette lot sabit kalırsa, hem fiyat hem volatilite büyüdüğü için risk **çarpımsal** artar (C ve D varyantları).
2. **Piramitleme yapıyorsan toplam açık riski sınırla** (Hunt dersi, §6c).
3. **FTMO'nun günlük limiti nasıl hesaplanıyor?** Resmi sayfadan okundu (2026-11-22), ayrıntı 09 §4i'de.
   - Limit = **gece yarısındaki (CE(S)T) bakiye** − başlangıç sermayesinin %5'i (tek aşamalıda %3).
   - Açık pozisyonlar **varlık değeri (equity)** üzerinden sayılır.
   - Bu yüzden **gece taşınan bir değişken zarar, o günün tamponunu baştan yer.** −%3 açık zararla güne başlarsan, o gün kaybedebileceğin sadece %2 kalır.
   - Gece taşınan değişken kâr ise sayfadan çıkan yoruma göre (açıkça yazmıyor) tampon gibi çalışır.
   - Kâr geri verilince limit ihlali olmasa bile hedefe ulaşma gecikir.

## 6b-4. Gerçek hayattan risk dersleri (Trader Dante, "Stories From 15 Years As A Trader - Part 1", HdqVExefJP0)

1. **Stopsuz işlem hesabı bir saatte bitirir.**
   - 2005'te Dante, bakır boğa piyasasında her sabah alıp gün sonu kapatarak birkaç yüz sterlini ~9.500 sterline çıkarmıştı. Stopu yoktu.
   - Bakırın (kendi ifadesiyle) en büyük düşüş gününde hesap **~50 dakikada 160 sterline** indi ve zorla kapatıldı. Kendi zararını önce "trend benim yanımda, dönecek" diye geçiştirmişti.
   - O günden beri her işlemde stop kullanıyor.
2. **Zarardaki pozisyona eklemek ve plansızlık.** Bir fonun bankadan gelen "yıldız" ham petrol trader'ı, 10 $ zarara kadar ekleme yaptı, sonra Dante'ye "Sen olsan nereden eklerdin?" diye sordu. Ertesi gün işe gelmedi, pozisyonu Dante kapattı. "Başkasına ne yapacağını soruyorsan planın yoktur" (11 #72).
3. **Platform ve aracı kurum riski gerçek.**
   - Bir prop meslektaşının platformu pozisyonu yanlış gösterdi. Kapatmak için tekrar tekrar "sat"a bastı ve farkında olmadan dev bir short açtı. Sürpriz bir BoE faiz indiriminde **kariyeri dakikalar içinde bitti**.
   - **Kural**: emir tepki vermiyorsa tekrar tekrar basma. **Gerçek pozisyonu aracı kurumdan ya da firmadan teyit et.**
   - Dante'nin bir limit emri CFD kurumunca dolmadı ve stopsuz 30 puan zarara düştü.
4. **Sabit kur ya da taban ile işlem yaparken stopu tabanın öbür tarafına koy.** Ocak 2015'te EUR/CHF long'unda Dante stopu tabanın üstüne (1,2002) koymuştu. SNB tabanı kaldırınca **kayma olmadan** çıktı. Bunu "kör şans" olarak niteliyor; çoğu kişi yüzlerce pip kaydı (§6b-2).
5. **Kurum hatalarından kazanmak**:
   - Gecikmeli fiyat akışı arbitrajı: haber anında bir kurumun fiyatı 6-8 saniye geride kalıyordu.
   - Fiyat akışındaki veri hatası sıçramaları.
   - Garantili stop ile seans arası boşluk (gap) istismarı: bir meslektaş 200 sterlini 50 bin sterline çıkarmış.
   - Hepsi birkaç ayda kapatıldı. Bu tür "bedava para", prop firmalarında **yasaklı uygulamalardır**: gecikme arbitrajı, haber ve gap istismarı, sim fiyat hatası kullanma. Ödeme reddi ve hesap iptali getirir (09 §4i, §4d).
6. **Duygu ve aşırı risk**: Dante prop masasında ekran kıranlar, banyoda ağlayanlar ve kaybettikten sonra arkadaşına tekme atanlar görmüş. "Normal boyutla 3-4 kayıp yüzünden kimse ağlamaz. Bu ancak aşırı riskle olur."
7. **Kararsızlık**: Dante bir T-note işlemi için patrondan limit istedi, sonra tetiği çekmedi ve işlem dev bir harekete dönüştü. Patron sandalyeye çıkıp bağırdı. "O günden sonra hiç tereddüt etmedim."
8. **"5-10 yıl sonra kazanmaya devam edeceğini nereden biliyorsun?" "Bilmiyorum."** Şans payı her zaman var. Riski elinden geldiğince yönet, gerisini kabul et.
9. **İşlemlerini herkese açık paylaşırken dikkatli ol.** Twitter'daki işlem çağrılarını tarayıp kaybedenleri fade eden, kazananları takip eden yazılımlar ve kişiler var (13 §3c).
## 6c. Pozisyon boyutu takdire bırakılmaz, korelasyonlu pozisyonlar tek bahistir (Grimes, CWT 115)

- **Boyut takdire bırakılmaz.** "Grafik çok güzel diye 4 kat boyutla giremem. En iyi ihtimalle çok küçük bir olasılık eğimim var, 'kesin haklıyım' diyebileceğim bir nokta yok." Takdir, önceden belirlenmiş sınırlar içinde kullanılır: stop'u şu ya da bu seviyeye koymak, işlemi alıp almamak. Takdirli trading "canın ne isterse yap" demek değil. **Takdirin nerede kullanılacağı önceden net tanımlanır.**
- **Korelasyon**: "En iyi 6 hisseyi long tutsan bile piyasa çökerse 4-6'sında kaybedersin." Ham petrol, benzin ve ısınma yakıtında long olmak 3 pozisyon değil, **1 pozisyondur**. Toplam riski hesaplarken ilişkili pozisyonları tek bahis say (Brandt'ın bileşik risk fikriyle aynı, §6b). Prop hesabında birden fazla korelasyonlu pariteyle (ör. EURUSD + GBPUSD long) aynı anda işlem açmak, günlük limiti tek bir haberle tüketebilir.

## 6d. Kural hiyerarşisiyle risk çerçevesi (Lance Breitstein, "52 Minute Risk Management Masterclass", hC4g7qY6UcQ)

**Tanım**: Risk yönetimi, hedeflerine ulaşma olasılığını en üste çıkarırken **senin için kabul edilemez sonuçların** olasılığını en aza indiren kurallar bütünüdür. Kişiseldir: aynı 50 bin $ kayıp birine rahatsızlık, diğerine yıkım. İnsanlar kaldırabileceği riski hep olduğundan yüksek tahmin eder ("Herkesin bir planı vardır, ağzına yumruğu yiyene kadar"). Bu yüzden ilk tahmininden daha temkinli başla.

**Savunma araçları:**
1. **"Eğer X ise Y yap" türü kayıp kuralları** (gün, hafta, ay). Örnek bir gün içi trader:
   - Günde 1.500 $ zararda boyutu yarıya indir, 2.500 $'da günü kapat.
   - Haftalık 7.500 $ zararda bir hafta yarım boyutla işlem yap ve incele.
   - Aylık 15.000 $ zararda birkaç gün tamamen dur, sonra en küçük boyutla dön.
   - Örnek bir swing trader: zirveden %5 düşüşte tüm pozisyonları yarıya indir, %10'da çekirdek dışındaki her şeyi kapat.
2. **Kural hiyerarşisi.** İşlem düzeyindeki kurallar esnek olabilir: stop yeri, o güne özel risk. Ama **hesabı ayakta tutan kurallar katıdır**: maksimum düşüş, felaket kaybı. "Hatanın telafi edilebileceği yerde esneğim, varoluşsal olduğu yerde değil."
3. **Zihinsel ve fiziksel durum kuralları.** Kötü uyku, hastalık ya da stres varsa boyutu küçült. Breitstein her sabah kendine bir "karne" veriyor: C ise -%50 risk, D ise -%80, F ise hiç işlem yok.
4. **Stop türleri.**
   - Sabit (emirle girilmiş) stop yeni başlayan ve duygusal trader için şart.
   - Zihinsel stop sadece çok deneyimli biri içindir: "Zihinsel stop kullandığını söyleyenlerin çoğunun aslında stopu yoktur."
   - **Zaman stopu**: "En iyi işlemler hemen çalışır." Ama 03'teki test, mekanik kırılımlarda "ilk zararlı kapanışta çık" kuralının büyük kazananları kestiğini gösterdi. Kendi verinle doğrula.
5. **Fiyat stopu sıçrayıp geçerse** (boşluk, durdurma): Breitstein "şu an düz olsaydım bu pozisyonu alır mıydım?" diye bakıp tutabildiğini söylüyor. Bunu sadece **hesap düzeyi kurallar ihlal edilmiyorsa** ve yeni sabit stopla yapıyor. ⚠️ Yeni başlayan için tehlikeli bir esneklik: "zarardakini tutma" bahanesine dönüşür (11 #72).
6. **Pozisyon boyutu stoptan daha güçlü bir araç.** Boşluk, işlem durdurma ve haber riski stopun ötesindedir. Doğru boyut bunları hayatta kalınabilir kılar. **Short pozisyonlar long'lardan çok daha küçük olmalı**: kayıp teorik olarak sınırsız, ani sıçramalar küçük şirketlerde ve satın alma haberlerinde sık görülür.
7. **Kârı hesaptan çekmek** en az konuşulan savunma aracıdır. Hesaptaki para hâlâ risk altındadır, tek bir kötü gün yılları silebilir. Kurallar: ayda bir kârın %25'ini çek, ya da yeni zirvenin üstündeki kârın %50'sini çek.
   - **Prop'ta ayrım**: kişisel hesapta kâr çekmek felakete karşı korur. Fonlu prop hesabında ise kârın bir kısmını **tampon olarak bırakmak** hesabın ömrünü uzatır (09 §4n). Ödemeler zaten "çekilmiş kâr" sayılır.

**Saldırı araçları:**
- "Ortalama setup'a da istisnai setup'a da aynı riski vermek, beklenen değerle sermaye dağılımını eşleştirmemektir." Breitstein fırsatlı günlerde yavaş günlere göre 10 kat, nadiren 100 kat risk aldığını söylüyor. Kelly formülü kullanmıyor: girdiler hiçbir zaman kesin bilinemez ve formül kişiye uyarlanamaz.
- ⚠️ Bu ancak notların bilgi taşıdığı **kanıtlandıktan sonra** geçerli. Kanıtlanmamış notlarla boyut farkı kuyruk riskini büyütür (§4c'deki test).
- **Ortam okuması**: kendi avantajının olmadığı dönemde savunmaya geç: küçük boyut, sadece A+ setup ya da araştırma modu. Kötü dönemde işlem sayısını artırıp kaybı hemen telafi etmeye çalışmak en yıkıcı hatalardan biri.

**Psikolojik tuzaklar:**
- **Tilt.**
- **FOMO.**
- **Aşırı güven**: patlamalar en çok büyük kazanç serilerinden sonra gelir.
- **Çapalanma**: hesabın eski zirvesine ya da hissenin eski fiyatına.
- **Sosyal medya kıyası.**
- **Hareket eden hedef çizgisi**: "100 bin $'a ulaşınca riski azaltırım" deyip hedefi hep ileri atmak.

**Örnek çerçeve** (agresif bir "home run" trader'ı için):
- Hesabın en fazla %50'sini kaybetmek.
- Aylık -%20'de 3 gün mola ve yarım boyut.
- Günlük -%10.
- Tek işlemde ya da tek temada en fazla hesabın %50'si, short'ta %25.
- Gece taşınan küçük şirket hissesi en fazla %2.
- Her sabah karne.
- Ay sonu yeni zirvenin üstündeki kârın %50'sini çek.
- **Prop'a uyarlama**: FTMO'da günlük limit %5, toplam limit %10 olduğu için bu oranları ~1/4-1/5 ölçeğe indir. Ör. günde -%2,5'ta boyutu yarıya indir, -%3,5'ta günü kapat, -%6 toplam düşüşte bir hafta yarım boyut. "Eğer-ise" yapısı aynı kalır.

## 6e. ✔ Gece ve hafta sonu boşluğu (gap): stop seni her zaman korumaz (Breitstein, "16 Years of Swing Trading Lessons", bZ7-iBaI_Xw + simülasyon)

**Breitstein'ın iddiası**:
- Gün içinden swing'e geçerken boyutu stop mesafesi oranından **daha fazla** küçültmek gerekir, çünkü fiyat stopuna "kibarca" gelmez. "50'de yatarsın, gece haber çıkar, 42'de uyanırsın."
- En tehlikelisi küçük şirket hissesinde gece taşınan short'tur: satın alma haberiyle hisse bir gecede yüzde yüzlerce açılabilir.
- Kendi hatası da buydu: gün içi boyutuna demir atmış, ve swing işlemlerinden sistemi ihlal etmeyen hareketlerle sürekli silkelenmiş. "Daha küçük boyut daha küçük fırsat demek değil. Hedef 5-10 kat büyükse boyut da o kadar küçük olabilir."

**Test** (`arastirma/verify_gap_risk.py`, günlük 2010+): Kapanışta açılan bir pozisyonun stopu kapanıştan k×ATR14 uzakta. Ertesi açılış stopun **ötesinde** açılırsa ne olur?

| Grup (1 ATR stop) | Stopu atlayan açılış: hafta içi gece / hafta sonu | Atlarsa ortalama kayıp | En kötü tek gece |
|---|---|---|---|
| Büyük hisseler (12) | Long %1,3 / %1,9, short %1,3 / %1,2 | -1,4 ile -1,9R | Long -9,3R, short -10,3R (bilanço) |
| Oynak küçük/orta hisseler (11) | Long %1,2 / %1,4, short **%1,8 / %2,5** | -1,8 ile -2,5R | Long -49R (hafta sonu), **short -96R** |
| Vadeli, parite, endeks (8) | Long %2,0 / **%3,7**, short %2,0 / %2,8 | -1,4R | ~-4R |

- 2 ATR stopta atlama olasılığı %0,1-0,45'e iniyor, ama en kötü değerler küçük hissede yine -25 ile -48R.
- **Ortalama maliyet küçük**: olasılık × ortalama fazla kayıp ≈ işlem başına ~0,01R. **Sorun ortalama değil kuyruk.**
- **Breitstein'ın short uyarısı doğrulandı**: küçük hissede short tarafı hem daha sık atlıyor hem de tek gecede -96R gördü. %1 riskle bu, hesabın tamamı demek.
- **Prop açısı** (%1 risk, 1 ATR stop): tek bir pozisyonun açılış boşluğuyla 3R'den fazla kaybetme olasılığı büyük hissede tutuş başına %0,14 (~700'de 1), küçük hissede %0,18 (~570'te 1), vadeli ve paritede %0,03 (~3.400'de 1). FTMO 1 aşamalı hesabın %3 günlük limiti tek boşlukla dolabilir. Günlük limit equity'den hesaplandığı için **boşluk, tepki veremeden limiti aşabilir** (09 §4i).

**Kurallar**:
1. Gece ya da hafta sonu taşınan pozisyonda boyutu stopa göre değil **"makul en kötü boşluğa"** göre de sınırla. Ör. pozisyon değeri × makul boşluk ≤ hesabın %X'i. Breitstein'ın kendi sınırı: gece taşınan küçük şirket hissesi en fazla hesabın %2'si (§6d).
2. Bilanço ve önemli haber öncesinde ya pozisyonu kapat ya da değerini küçült. Büyük hisselerdeki -9 ile -10R'lik geceler bilanço geceleriydi.
3. Hafta sonu taşınan, aynı faktöre bağlı pozisyonlar (ör. 5 USD paritesi) birlikte açılır, **tek bahis** gibi say (§6c).
4. FTMO Swing hesabında (hafta sonu serbest) vadeli, parite ve endeks enstrümanlarının boşluk kuyruğu hisselerden çok daha ince (~-4R). Yine de "3R'den fazla tek boşluk" senaryosunu günlük limit planına dahil et.

⚠️ Sınırlar: yfinance düzeltilmiş verisi, küçük hisse listesi hâlâ işlem gören hisselerden oluşuyor (hayatta kalma yanlılığı) ve gerçek mikro şirket değil. Bilanço tarihleri ayrıca işaretlenmedi.

## 7. Günlük/haftalık devre kesiciler

- Günlük maks. kayıp (örn. 2 kayıp veya −%2) → ekranı kapat.
- Haftalık maks. kayıp → hafta biter, sadece günlük incelemesi yapılır.
- Bu kurallar istatistiksel avantajı değil, **duygusal bozulmayı (tilt / intikam işlemi)** sınırlar.

**Futures Trader 71'in "gerileyen risk" kuralı** (Chat With Traders 82, woT6d7xUtOs; `arastirma/verify_ft71.py` B bölümü):
- Günlük zarar limitinin 1/3'ünde boyutu %60'a, 1/2'sinde %50'ye, 3/4'ünde %20'ye indir, limite kadar o boyutla devam et. "Günlük limite mümkün olan en küçük boyutla ulaşmak istiyorum. Amacım kaybı geri kazanmak değil, piyasayla yeniden uyum yakalamak."
- Ayrıca **üst üste 4 zararlı günden sonra bir gün izin**. Gerekçesi: zararlı gün olasılığı %50 ise 4'lü seri %6,25. ⚠️ Bu hesap zararlı gün olasılığının gerçekten %50 olduğunu varsayıyor. Kendi kaydından ölç.
- **Simülasyon** (100K, günde en fazla 6 işlem, işlem başı %0,75, RR 2, kişisel günlük stop -%3):

| İşlem başı beklenti | Sabit: ortalama gün / P(gün -%3'e değer) / 5. yüzdelik | Gerileyen: aynı ölçüler | Challenge geçme (sabit / gerileyen) |
|---|---|---|---|
| -0,10R | -%0,40 / %24 / -%3,00 | -%0,37 / **%0** / -%2,55 | %17 / %15 |
| 0 | %0,00 / %20 / -%3,00 | +%0,02 / %0 / -%2,55 | %51 / %50 |
| +0,10R | +%0,42 / %16 / -%3,00 | +%0,40 / %0 / -%2,55 | %81 / %82 |
| +0,20R | +%0,85 / %13 / -%3,00 | +%0,82 / %0 / -%2,33 | %95 / %96 |

- Gerileyen boyut ortalama günü sadece %4-7 azaltıyor, ama günde 6 işlemle -%3'e **hiç ulaşmıyor**. Sabit boyut günlerin %13-24'ünde -%3'e değiyor.
- **FTMO 1 aşamalı hesabın %3 günlük limiti** hesabı kaybettirir. Orada bu fark hayati: sabit %0,75 × 6 işlem = %4,5 > %3 (09 §4p kuralını ihlal eder). Gerileyen boyut aynı işlem sayısında bile limiti korur.
- Avantajın varsa challenge geçme oranı biraz artıyor, negatif avantajda biraz düşüyor. Avantaj yaratmaz, kötü günün kuyruğunu keser.

## 8. İhtiyacın olmayan parayla işlem

Kira/borç parasıyla açılan işlemde grafiğe değil paranın gideceği yere bakarsın (DD Finance). "Sonraki işlem TP olmalı ki fatura ödensin" ruh hali = başarısızlık reçetesi (Yusuf Trades röportajındaki tek doğru tespitlerden biri).
