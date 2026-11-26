# 10 — Backtest, Replay ve İstatistik (Kanıta Dayalı Yaklaşım)

> Güven seviyesi: **YÜKSEK** (yöntemsel ilkeler + Grimes'ın yayımlanmış testleri + kendi simülasyonlarım).
> Kaynaklar: Adam Grimes blog (Fibonacci testleri 2013, breadth testi 2026, "Surviving isn't thriving" 2025), Tradeciety backtest rehberi, AlgoCoinism, Bulkowski (erişilemedi — bkz. §7).

## 1. Kanıta dayalı zihniyet (Grimes)

- "**Bulduğun her avantaj sadece küçük bir eğim** olacak."
- "Çoğu trading fikri anlamlılık testlerinden geçemez."
- "Herhangi bir grafiğe çizilen herhangi bir çizgi muhtemelen 'anlamlı' görünür" → göz yanılgısı.
- Rastgele yürüyüş (random walk), GARCH ve **karıştırılmış barlar** ile karşılaştır: setup'ın rastgele veride de "çalışıyorsa" avantaj yoktur.
- Kıyas noktası: sistemin yıllık %6 ama al-tut %7-8 ise → "Yaklaşımının avantajı var mı? (Muhtemelen yok.)"

## 2. Grimes'ın yayımlanmış test sonuçları

| Konu | Veri | Sonuç |
|---|---|---|
| **Fibonacci geri çekilmeleri** (2013) | 600 hisse + 16 futures + 6 döviz, 10 yıl günlük, 2-ATR swing filtresi; rastgele yürüyüş/GARCH/karıştırılmış barlarla kıyas | **"Fibonacci oranlarının piyasada anlamlı olduğuna dair kanıt yok."** Ortalama geri çekilme trend filtresiyle ~%65 (çok yüksek standart sapma); 2016 notu: düzeltmeler "~%50 civarında, çok büyük hata payıyla" biter |
| **Market breadth** (2026) | 35 yıl, 9 breadth ölçüsü, S&P 500 52-hafta zirvesinde ~1 çeyrek sonraki getiri | "Güçlü/zayıf breadth sonrası getirilerde **anlamlı fark yok**"; en iyi ölçünün %95 güven aralığı sıfırı içeriyor |
| **Mum formasyonları** | Test detayı yayında gösterilmemiş | "Mum formasyonlarını test edersen istatistiksel avantaj olmadığını görürsün" (iddia; test koşulu belirtilmemiş → orta güven) |
| Ölçekleme | "yüzlerce veri noktası" | Haftalık range ≠ 5 × günlük; ≈ **√5 ≈ 2.24×** (volatilite karekökle ölçeklenir) |

→ Pratik sonuç: Fibonacci seviyelerini **tek başına** giriş/stop sebebi yapma (AlgoCoinism de aynı uyarıyı yapıyor: "çok oran var, her dönüşün yakınında bir seviye bulunur").

## 3. Örneklem ve istatistik gücü

- WR40/2R kârlı sistem: 20 işlemde %25, 100'de %9, 300'de %0.7 ihtimalle zararda (01 §4).
- Tradeciety "30-50 işlem yeterli" → kaba ilk eleme için evet, kanıt için **hayır**.
- Grimes: işlem sıklığını yarıya indirmek standart hatayı **√2** kat artırır → az işlemle avantajı ölçmek daha uzun sürer. "Kaybettiğini geri almak için **boyutu artırma**." "P&L'i dolar değil **R** cinsinden grafikle."
- Bir sonucun anlamlılığı için kaba kural: `t ≈ ortalama_R / (std_R / √n)`; t > 2 → şans eseri olma ihtimali düşük (~%5). Örn. ortalama +0.2R, std 1.4R → n ≈ (2×1.4/0.2)² ≈ **196 işlem** gerekir.
- **Bir değişikliğin işe yaradığını anlamak ne kadar sürer?** Brandt: "Nasıl işlem yaptığımda bir değişiklik yaparsam, işe yarayıp yaramadığını anlamak muhtemelen **2 yıl** sürer" (AlphaMind #145, mXmDCIju98U). Hesap: önceki ve sonraki dönemi karşılaştırmak, her dönemde n ≈ 2×(2σ/Δ)² işlem gerektirir. σ ≈ 1,5R kabul edildi.
  | İyileşme (Δ, işlem başı) | Dönem başına gereken işlem | Ayda 8-10 işlemle (Brandt) | Günde 2 işlemle |
  |---|---|---|---|
  | +0,1R | ~1.800 | ~16 yıl | ~3,5 yıl |
  | +0,2R | ~450 | ~4 yıl | ~11 ay |
  | +0,3R | ~200 | ~2 yıl | ~5 ay |
  | +0,5R | ~70 | ~8 ay | ~2 ay |
  → Brandt'ın "2 yılı" ancak **büyük** bir iyileşme (~+0,3R) için yeterli. Küçük iyileştirmeleri canlı sonuçlarla kanıtlamak pratikte imkânsız. Bu yüzden değişiklikler önce backtest ve replay'de, büyük örneklemle değerlendirilir. Canlıda ise sadece "bozulma var mı" diye izlenir (§6e). **Kuralı sık değiştirmek**, hiçbir değişikliğin değerlendirilemeyeceği anlamına gelir.

## 4. İyi backtest protokolü

1. **Kuralları önceden yaz** (03'teki şablon). Belirsiz kural = test edilemez.
2. Veri: intraday için en az 2-3 ay değil, **farklı rejimleri** kapsayacak kadar (trend, range, yüksek/düşük volatilite). Tercihen 1+ yıl.
3. **Replay'de grafiğin sağını görme**; daha önce baktığın grafiği test etme (look-ahead / hindsight).
4. Her işlem: tarih, setup, giriş/stop/hedef, **R sonucu**, MFE/MAE, ekran görüntüsü (giriş + çıkış), kurallara uyum.
5. **Maliyetleri ekle**: spread + komisyon + kayma (özellikle scalp).
6. Aynı girişlerle farklı çıkışları test et (2R / 3R / trailing / kısmi) — Tradeciety'nin iyi önerisi.
7. Kontroller:
   - Kârın %90'ı 2 işlemden mi geliyor? (aykırı değer bağımlılığı)
   - En uzun kayıp serisi ve maks. düşüş (R cinsinden) kaldırılabilir mi?
   - Sonuçlar günün saatine/seansa göre ayrıştırınca tutarlı mı?
8. **Overfitting'e karşı**: kuralları veri üzerinde ayarladıysan, ayarlamadığın ayrı bir veri diliminde (out-of-sample) tekrar test et. Parametre sayısı az olsun.
9. Sonra **forward test** (demo/küçük hesap, canlı hız): kuralları gerçek zamanda uygulayabiliyor musun? Replay'de 5 saniyede geçen 6 saatlik drawdown canlıda başka hissettirir (Yusuf röportajındaki doğru gözlem).

## 5. Replay/backtest'in iki farklı amacı

| Amaç | Örneklem | Ölçüt |
|---|---|---|
| **Görsel tanıma** (setup'ı görmeyi öğrenmek) | 50-100 örnek | "Bunu gerçek zamanda fark edebiliyor muyum?" |
| **Avantaj kanıtı** | 100-300+ işlem | EV (R), güven aralığı, maks. DD |

## 6. Günlük (journal) — minimum alanlar

`tarih | piyasa | seans | setup | HTF bağlam | giriş | stop | hedef | R sonucu | MFE | MAE | kurala uyum (E/H) | hata etiketi | duygu (1-5) | ekran görüntüsü`

Haftalık soru: "En pahalı hatam neydi ve hangi kural bunu önlerdi?"
(Tradeciety Edgewonk'u öneriyor ama **Edgewonk'un sahibi Tradeciety** — çıkar çatışması. Bir tablo dosyası da yeterli.)

## 6b. Hangi metrikler önemli? (Brandt, TraderLion 2025)

- Brandt 2013'teki zararlı yılından (17 aylık tepeden yeni tepeye düşüş süresi, en kötü yılı ~-%3) sonra "istatistiğin tünellerine" girmiş. Büyük bir sistematik fonla 1 milyondan fazla formüllü hücresi olan bir what-if tablosu kurmuş: "Stopu 2 gün sonra başa başa çekseydim? Kazananlardan çıkışı değiştirseydim?"
- **Hedef olarak** getiri oranı ve kazanma oranı **kullanılmaz**, bunlar sonuçtur. Takip edilenler: **profit factor, beklenen değer, basıklık (kurtosis), Calmar, Sortino**. Brandt'ın iddiası: "Sharpe ve kazanma oranı işe yaramaz." Bu abartılı, ama WR'ın tek başına anlamsız olduğu doğru (01).
- **Aynı şekilde en az 1, tercihen 2 yıl işlem yap** → 100-300 veri noktası → **Monte Carlo**'ya koy → olası özsermaye eğrilerinin aralığını gör. "Güveni işlem yapış şekline değil, **işlem yapış şeklinin ürettiği metriklere** duyarsın."
- **Kurala yeni değişken ekleme**: "Neden %70'te kâr alıyorsun?" "Çünkü almasaydım metriklerim ne olurdu bilmiyorum." Kuralları sürekli optimize etmeye çalışma: "Bu yıl optimize edersin, gelecek yıl farklı olur."
- **Kayıp serisi örneği**: "Birkaç yıl önce 21 işlemin 19'unda yanıldım. Sonraki 10 işlem beni yeni tüm zamanların zirvesine taşıdı." (01 §5'teki seri hesabının gerçek hayattaki karşılığı)
- **NAV eğrisi**: Dolarla değil standartlaştırılmış NAV ile takip (1981'den beri). Hedef: yeni tüm zamanlar zirvesinden en fazla **1-2 işlem / 200-300 baz puan** uzakta olmak.
- **Pareto 80/20**: Tanıdığı her başarılı profesyonelde, kariyer boyunca net kârın en az %80'i işlemlerin **%20 veya daha azından** geliyor. → Kendi günlüğünde de "en iyi %20 işlemi çıkar, kârın ne kadarını yapıyor, ortak özellikleri ne?" analizi yap (Brandt'ın yaptığı gibi, bkz. 04 §11 "Tip 1 kırılım").
- **Performans raporlama**: Sonuçları **toplam nominal sermayeye** göre ifade et. Opsiyon priminin, marjın ya da hisse maliyetinin yüzdesi olarak değil. "İki haftada %1.174 kazandım" diyen opsiyon ekran görüntüleri: "Sonucu nasıl ifade edeceğini bile bilmiyor → kimi takip etmeyeceğini bilirsin."

## 6c. Çoklu test / veri madenciliği tuzağı (Kevin Davey örneği, 5Bnjq9vNzCg)

- Video: "High/low" kırılım sistemi (günün/haftanın/ayın/yılın en yüksek tepesinin üstünde al, en düşük dibinin altında sat). **54 piyasa × 6 bar boyutu × 3 parametrenin 90 kombinasyonu** test ediliyor (~29.000 test). Sonuç: "91 kombinasyon son birkaç yılda sağlam görünüyor."
- **Sorun**: ~29.000 testin ~%0,3'ü. **Rastgele bir sistemle bile** bu kadar test yapılırsa bir kısmı sadece şansla "sağlam" görünür (çoklu karşılaştırma problemi). Davey de "sonuçlar tam test edilmedi, kendin test et" diyor, walk-forward ve çoklu piyasa testi kullanıyor. Bunlar doğru adımlar. Ama video bu yanlılığı açıklamıyor.
- **Kurallar**: (1) Kaç varyant denediğini kaydet. Ne kadar çok denersen, kazanan için o kadar yüksek kanıt eşiği gerekir (kaba kural: 100 varyant denediysen tek bir "%5 anlamlı" sonuç beklenen şans sonucudur). (2) Seçtiğin varyantı **hiç görmediği veride** (out-of-sample / walk-forward) doğrula. (3) Parametre komşuluğuna bak: iyi sonuç tek bir parametre değerinde mi, yoksa geniş bir plato boyunca mı? Plato yoksa muhtemelen gürültüdür. (4) Mümkünse **farklı piyasalarda** benzer sonuç ara (Grimes ve Davey'nin ortak önerisi).
- Video, Davey'nin sadece kendi ücretli kursunun (Strategy Factory) öğrencilerine açık test yazılımını (MultiOp) tanıtıyor. Bilgi içeriği zayıf.

## 6d. Backtest motoru nasıl yazılır? (SharpeEdge, "How to Properly Backtest Algorithmic Trading Strategies", KWIT8YOQ4Do)

**Vektörel backtestin 2 kör noktası:**
1. **Bar içi stop ve hedefi göremez.** Fiyat bar içinde TP'ye değip kapanışta geri dönebilir, ama vektörel hesap sadece kapanışı görür.
2. **Sermayeye bağlı komisyonları** doğru hesaplayamaz (sermaye her barda değişir).

**Doğru yaklaşım: her mumu döngüyle, iki anda işle (açılış ve kapanış):**
1. Açık pozisyon varsa → **gap getirisi** (bu açılış − önceki kapanış) uygula.
2. Kapanış sinyali varsa kapat. Açılış sinyali varsa ve pozisyon yoksa **bu mumun açılışında** gir. **Sinyal t mumunun kapanışında hesaplanır, giriş t+1 açılışında yapılır** (look-ahead önlemi).
3. Mum içinde SL/TP seviyesi geçildiyse → o seviyeden çık. Geçilmediyse gövde getirisini uygula.
- ⚠️ Kendi ekim: Aynı mumda **hem SL hem TP** geçildiyse hangisi önce geldi bilinemez → **muhafazakâr varsayım: önce SL**. Ya da alt zaman dilimi verisine in. (Brooks'un "bar içi oluşum" uyarısıyla aynı konu, 13 §5.)
- Pozisyon boyutu vektörü: SL mesafesine göre "sermayenin %X'ini riske et" (02).

**4 maliyet türü (hepsini ekle):** (1) işlem ücretleri/komisyon (sabit ya da hacme bağlı); (2) **swap** (gece taşıma, hafta sonu genelde 3×); (3) **spread**; (4) **kayma** (slippage, pozitif ya da negatif). "Çok kârlı bir strateji bile biraz ücret ve swap eklenince tüm performansını kaybedebilir."

**Backtestten önce sinyal doğrulaması**: Grafikte birkaç girişi elle kontrol et (sinyal doğru barda mı, SL seviyesi doğru mu?).

**Dürüstlük örneği**: Gösterdiği MA kesişim stratejisi Apple'da 2020-2026 arası 30 işlem ve Sharpe 0,2 verdi. SharpeEdge "beklediğim gibi değersiz" diyor. 30 işlem zaten anlamlılık için yetersiz (01 §4).

## 6e. Bir strateji (ya da setup) ne zaman bırakılır? Alpha decay çerçevesi (SharpeEdge, CWOhChDdnn4)

"Otomatik sistemde psikoloji yok" doğru değil. Ya 5 kayıptan sonra çok erken bırakırsın, ya da toparlanmasını umarak çok geç bırakır ve tüm kârı geri verirsin. Bu çerçeve elle işlem yapan biri için de geçerli: "setup'ım bozuldu mu, yoksa normal bir kayıp serisi mi?"

**Düşük performansın 3 nedeni:**
1. **Hata / uygulama farkı**: test edilen mantık uygulanan mantık değil.
2. **Yanlış pozitif**: avantaj hiç gerçek değildi, testleri şansla geçti.
3. **Gerçek alpha decay**: avantaj vardı ama zamanla aşındı (kalabalıklaşma, rejim değişimi, maliyet artışı). Tanımı gereği **yavaş**, ani değil.

**Durma kriterleri (canlıya geçmeden ÖNCE belirlenir):**
1. **Monte Carlo maksimum DD eşiği**: walk-forward ve örneklem dışı getirilerden blok bootstrap ile, **işlem sayısının fonksiyonu olarak** maksimum DD dağılımı çıkar. %95 eşiğini aşarsan **dur**. Eşik sabit bir sayı değil bir eğridir: ne kadar çok işlem yaparsan o kadar derin bir DD olası.
2. **Özsermaye vs Monte Carlo %5-%95 bantları** → bandın dışına çıkış = **alarm** (durmak değil).
3. **Aylık getiri yüzdelik sıralaması** → tarihsel dağılımla karşılaştır.
4. **CUSUM testi**: standartlaştırılmış getirilerde ortalama kaymasını biriktirir. `C_t = max(0, C_{t−1} + z_t − K)`. Eşik H, bootstrap ile hedef yanlış alarm oranına (%5) göre kalibre edilir.
5. **Hareketli alfa regresyonu**: güven aralığının **üst sınırı sıfırın altına** düşerse aşınma istatistiksel olarak anlamlıdır.

**Piyasa dışı kontroller:** (a) **işlem sayısı** tarihsel orandan farklı mı? (filtreler, lot yuvarlama, indikatör formülü farkları; örn. Python'daki ATR ile MT5'in yerleşik ATR'si farklı hesaplıyor); (b) işlem başına **gerçek maliyet** (komisyon, swap, spread) backtest varsayımından yüksek mi?; (c) kod taşıma hataları.

**Karar çerçevesi:** DD eşiği aşıldı → **dur**. İşlem sayısı farklı → **duraklat ve incele**. MC bantlarının dışı → **alarm, izle**. Aşınma teyit edildi → **dur**. Bu sırada veri toplamaya devam et.

**Gerçek örnek (SharpeEdge'in kendi sistemi):** 30 canlı işlemden sonra Sharpe -5, ödeme oranı (payoff) 1,5'tan 0,5'e düştü, özellikle short tarafında. WR aynı kaldı. Yine de "**30 işlem ve 1 ay çok az, henüz erken**" dedi ve izlemeye aldı: "DD eşiği tekrar aşılırsa kesin dururum." → Sonuçları ayrıca **R çoklusu** cinsinden de analiz et. Dolar bazında bozulma var ama R bazında yoksa sorun boyutlandırma, uygulama ya da ücretlerde, avantajda değil.

**Elle işlem yapanlar için uyarlama:** Setup bazında R kaydı tut. Önceden "bu setup için maksimum kabul edilebilir DD (R) ve minimum değerlendirme örneklemi (örn. 100 işlem)" yaz. Beggs'in 20'lik grupları (13 §3b) bu çerçevenin basit bir versiyonu.

## 6f. Optimizasyon ve doğrulama hattı (SharpeEdge, qcUCBLRcGLA)

1. Veriyi **örneklem içi (IS)** ve **örneklem dışı (OOS)** olarak böl (örn. OOS %30). Optimizasyon sadece IS'te yapılır.
2. **Kaba ve gerçekçi** bir parametre ızgarası kullan (çok ince adım = overfit).
3. Metrik seç: Sharpe (yüksek ve istikrarlı getiri), Sortino (negatif getiriyi daha çok cezalandırır), profit factor, Calmar (yıllık getiri / maksimum DD), **Ulcer Index** (DD'nin derinliği ve süresi).
4. Sadece en iyi kombinasyona değil, **tüm kombinasyonların dağılımına** bak. Çoğu kârlı mı?
5. En iyi ~100 kombinasyonu **kümele** (k-means) ve küme merkezine en yakın gerçek parametre setlerini seç.
6. **Duyarlılık analizi**: Her parametreyi tek tek komşu değerlere kaydır. Sağlam sistem **düz bir plato** gösterir, overfit sistem bir adımda çöker. Örnek: 22 değeri daha iyi ama bir adım solda performans yarıya iniyor. 18 biraz daha düşük ama düz bir bölgede → **18'i seç**.
7. OOS testi: tek bölme (hızlı eleme, az veri, basit stratejiler) ya da **walk-forward** (örn. 3 yıl eğit, 1 yıl test, her yıl yeniden eğit). Walk-forward daha gerçekçidir: farklı rejimleri test eder ve parametre kararlılığını gösterir. OOS getirileri gerçek performansın **tek yansız tahminidir**.
8. OOS getirileri üzerinde **bootstrap** (Sharpe ve maksimum DD için güven aralıkları) ve **permütasyon** (aynı getirilerin farklı sırayla gelmesi → DD dağılımı).
- **Dürüst örnek**: Üçlü MA kesişimi, NASDAQ 1 saatlik. IS'te ve iç OOS'ta sağlam görünüyordu. Gerçek OOS'ta (2024+) bir küme **çöktü**, diğeri vasat kaldı. Bootstrap'te Sharpe güven aralığı **-0,4 ile 2**, maksimum DD -%30 ile -%8 arası. Gerçekleşen -%17'lik DD dağılımın en kötü kısmındaydı. Walk-forward'da Sharpe ~1. Hepsi **komisyonsuz**. → Güzel bir IS sonucu hiçbir şey kanıtlamaz.

## 6g. Rastgele yürüyüş temel çizgisiyle test: Brooks'un açılış kuralı örneği

Grimes'ın yöntemi (14 §7): Bir "kalıbın" gerçek piyasada oluşma sıklığını, **aynı kalıbın rastgele veride oluşma sıklığıyla** karşılaştır. Örnek (04 §6b-2): "Günün tepesi veya dibi ilk 90 dakikada oluşur" iddiası gerçek veride %85-88 çıktı. Rastgele yürüyüşte de %64. Yani bunun bir kısmı rastgeleliğin doğal sonucu (uç noktalar zaten başta ve sonda yoğunlaşır, arcsine yasası), ama **fazlası** (+21-24 puan) gerçek bir piyasa yapısı. Temel çizgi olmadan "%90" rakamı yanıltıcı olurdu. Her yeni "istatistiğe" bu soruyu sor: **"Rastgele veride bu oran ne olurdu?"**

## 6h. Günlüğü analiz etmek: Trader Dante'nin yöntemi ("Stop Moaning Part 2", azDga9p6QhU)

> "Kayıt tutmak ile analiz etmek arasında **çok büyük** fark var. Kaydına sık bakmıyorsan hiç tutmasan da olur."

Her gün sorulacak soru: "**Bugün trader olarak gelişmek için ne yaptım?**" Üç inceleme sorusu: (1) Kazananlardan nasıl daha çok kazanırım? (2) Kaybedenlerden nasıl daha az kaybederim? (3) Nasıl daha çok kazanan fikir üretirim?

**Kazananlar için:**
1. **Aktif yönetim ve "hiç dokunmasaydım" karşılaştırması**: Tabloya bir sütun ekle. İşleme hiç dokunmasaydın ve stop ya da hedefe kadar bıraksaydın sonuç ne olurdu? Yönetimin uzun vadede değer kaybettiriyorsa "**kişisel kutsal kâsene**" ulaştın: daha az emekle daha çok para.
2. **Fırsatın ne kadarını yakalıyorsun?** Örnek: Öğrenci 187 tick'lik hedefle girdi, 21 tick aldı = hareketin **%11'i**. Dante'nin prop firmasına göre "yakalanan fırsat" bir trader'ı değerlendirmenin en önemli metriklerinden biri. Geçmiş işlemlerde alternatif çıkışları dene (son derin swing'in arkasından trailing, sabit X pip trailing). "Bu sayılarla uğraşırken para kazanmıyorum" itirazına cevap: "Grafiğe bakarken de kazanmıyorsun, kaybediyorsun."
3. **MAE (maximum adverse excursion)**: Kazanan işlemlerin kazanmadan önce ne kadar ters gittiğine bak. Kazananlar asla 25 pip'ten fazla ters gitmiyorsa ama stopun 100-150 pip ise → stopu küçült, payoff'u iyileştir. Tersi: 50 tick stopla girdiğin her işlem 42 tick ters gidip sonra kazanıyorsa **girişin kötü**. Dante kendi girişini böyle geliştirmiş: kırılım sonrası fiyat genelde son tepeye geri dönüyordu → daha iyi giriş yeri orası oldu.
4. **Risk dağılımı**: Başlangıçta her işlem aynı riskle. "Bu setup'ı sevdim, 6 kat boyut" gibi istatistiksiz, sezgiye dayalı boyut değiştirme yok. Test: tüm işlemler sabit %1 olsaydı sonuç ne olurdu? İstatistik bir setup'ın EV'sinin açıkça daha iyi olduğunu gösteriyorsa o setup'a daha fazla risk ayır.
   - Dante'nin vakası ve simülasyonu (02 §4c): Boyut tek başına beklentinin işaretini değiştirmez, ama **büyük boyutla alınan intikam ve sezgi işlemleri daha kötü kalitedeyse** pozitif bir sistem zarara döner. Günlüğe "önceki işlem kayıp mıydı?" ve "boyut normalin üstünde miydi?" sütunlarını ekle, bu grupların EV'sini ayrı hesapla.
   - Dante günlüğünü **her çeyrekte** bu üç soruyla gözden geçiriyor. Prop'ta en çok kazanan trader'ı büyük bir günün akşamı saat 21:00'de ofiste işlemlerini kaydederken görmüş: "**Sen avantajın üzerinde çalışmıyorsan başkası çalışıyor**, ve senin paranı o alıyor."

**Kaybedenler için:** Kayıpları birbirine bağlayan bir fiyat davranışı var mı (örn. seviyenin 60 dakikalık kapanışla kırılması)? **Günün saati** (ABD seansında kaybedip sabah kazanıyorsan ABD seansında işlem yapma), **haftanın günü** (Dante için Salı ve Cuma en iyi, Çarşamba en kötü; bu kişisel, kendi verine bak), **mevsimsellik** (Dante ve birçok profesyonel için Temmuz kötü, o yüzden Temmuz'da işlem yapmıyor), **piyasa** (DAX'ta sürekli kaybeden, Bund'da kazanan ama "Bund sıkıcı" diye DAX'a dönen trader). "Demon finder" denen bir hata çetele listesi: hangi hata en sık tekrarlanıyor?

**Yeni fikirler için:**
- "**Parlak fikirler defteri**": Aklına takılan her soruyu yaz, sonra test et. Dante her gün **en az 1 saat** elle istatistik topluyor.
- Örnek (Dante'nin kendi verisi, doğrulanmadı, tek broker verisi): EUR/USD Pazar açılış gap'i (FXPro, tam 22:00'de gap'e karşı giriş, hedef gap'in kapanması). Stop gap'in yarısı → **%55** WR. Stop gap kadar → **%67**. Stop gap'in 2 katı → **%75,5**. (RR'a göre EV: +0,65R / +0,34R / +0,13R, komisyon ve kayma hariç.) "Tüm gap'ler kapanır" efsanesini de test etmiş: kapanmayan gap'ler var.
- Bund'da ay sonu: son işlem günü 16:00'da al, stop 15-16 saatlik barın altında → %51 WR, 10 yılda +30,75R. 3 kayıp üst üste gelince insanlar paniğe kapıldı. "%51 WR'da 3'lü kayıp serisi neredeyse kesin. 7'li seri görsem şaşırmam" (01 §5'teki matematik).
- **Başkasının işlemlerinden desen bulmak**: Dante SFP setup'ını, bir öğrencinin kayıplarını inceleyerek bulmuş. Swing tepesinin üstünde **kapanış** varsa işlem genelde kazanmış, kapanış yoksa genelde stop olmuş (05).
- **İptal edilen emirleri de kaydet**: Bir arkadaşı, Dante'nin fiyat seviyeye dikey gelirken iptal ettiği 37 emirden 32'sinin kazanacağını tespit etmiş → "**Sürünmeyi fade etme, keskin hareketi fade et.**"
- **Kaçırdığın işlemleri** say: hem kazanacak hem kaybedecek olanları, dürüstçe.
- Problem çözmenin 3 adımı: problem ne → **neden** var (en çok atlanan adım) → çözüm.
- Anekdot (doğrulanmadı): Bir poker oyuncusu, işlem paylaşan ve sürekli kaybeden trader'ların (örn. 116 işlemde %60 WR ama -0,15R EV) istatistiklerini tutup onlara ters işlem açarak yüz binlerce kazanmış. Ders yöntemde değil düşüncede: "Herkes kazanan birini arıyor. Kaybedenler etrafımızda."

## 6i. Grimes'ın araştırma çerçevesi: "Veriye soralım" (Chat With Traders 115, dfRPZfkrDKk)

- **Avantajın tanımı**: Çok işlemde kazandığın para yığını kaybettiğinden büyüktür. Matematiksel olarak, **belirli bir zaman ufkunda** olasılıkların 50/50'den kaymasıdır. Aynı sinyalin 3 günlük, 1 aylık ve 6 aylık ufukta avantajı farklı olabilir. Avantaj yönsüz de olabilir, örneğin volatilitenin artacağını önceden bilmek.
- **Uzun süre piyasada kalan her takdirli trader, istatistik çalışmasını kendi P&L'iyle yapar.** Araştırma bu süreci kısaltır: "Her gün %5 yükselen hisseyi ertesi gün alıyorum ve kaybediyorum" sonucunu para kaybetmeden de bulabilirsin.
- **Başlamak için kod gerekmez**: ücretsiz grafik ve kağıt kalem, sonra Excel. Elle çalışmanın da değeri var, verinin "dokusunu" öğretir. Basit sorularla başla, örneğin "kapanış dünkü tepenin üstündeyse almak avantajlı mı?". İndikatörlerden önce saf fiyatla çalış.
- **Temel çizgi (drift)**: "Sistemim yılda %5 kazandırıyor" → "Al-tut ne kazandırırdı?" Al-tut %7 ise sistem değersiz. Aktif işlem çaba, risk ve maliyet ister, karşılığını al-tut'un **üstünde** ödemeli.
- **İstatistiksel ve ekonomik anlamlılık ayrıdır.** Yükselen bir piyasada, temel çizgiden anlamlı derecede kötü giden hisseleri gösteren bir "short sinyali" istatistiksel olarak anlamlı olabilir, ama short açan yine para kaybeder. Gün içi sistemlerde avantaj sık sık maliyeti karşılamaz.
- **Alış-satış farkı (bid-ask bounce) tuzağı**: gün içi backtest'te avantaj gibi görünen birçok şey, alış ve satış fiyatı arasındaki sekmeden ibarettir ve gerçekte uygulanamaz.
- **"Zaman makinesi" işlemi (geleceğe bakma)**: Örneğin "hareketli ortalamaya değince al" backtest'i. Ortalama bar oluşurken kayar. Bar açılışta ortalamanın üstündeyken fiyat hiç geri çekilmeden yükselir, kapanışta ortalama barın aralığına girmiş olur. Backtest dokunuş görür, canlıda dokunuş hiç olmamıştır. Çözüm: **parasız ileri test**.
- **"Backtest'in iyi görünmüyorsa canlıda daha iyi görünmeyecek."** İyi görünse bile canlı sonuç backtest'ten kötü olur. Her aşamada (backtest → ileri test → küçük canlı) avantajın biraz aşınmasını bekle.
- **Ek ders (bu bilgi tabanının testlerinden)**: Bir sembol setinde bulunan avantaj, **başka sembollerde tekrarlanmadan** kabul edilmez. Wyckoff ST testinde 9 ETF'te +0,23R görünen sonuç, 18 yeni ETF'te rastgele girişten farksız çıktı (06 §8b-D2).

## 6j. Rob Carver'ın sistematik işlem ilkeleri (Desire To TRADE, lMY9n1c3tFU)

> Carver, AHL'de sabit getirili portföyü yönetmiş (2006-2013). Şimdi kendi parasını tamamen otomatik bir futures sistemiyle işliyor, Londra Üniversitesi'nde sistematik trading dersi veriyor. Kitapları: *Systematic Trading*, *Smart Portfolios*, *Leveraged Trading*, *Advanced Futures Trading Strategies*.

- **"Kurcalama, kurcalama, kurcalama."** "8 yıldır sistemin temel parametrelerini değiştirmedim. 50 yıllık backtest'im var, son bir ayın ya da yılın bana yeni ne bilgisi var? Neredeyse hiç." Örnek: Mart 2020 COVID çöküşünde hızlı trend sistemleri yavaşlardan çok iyi yaptı. Ama buna göre ağırlıkları değiştirmek, 50 yılın 1-2 ayına göre karar vermek demek. Sık yeniden kalibrasyon ancak yüksek frekans işlem için mantıklı, çünkü veri çok ve piyasa birkaç ayda bir değişiyor.
- **"Sistematik olup sistemi kurcalamak iki dünyanın en kötüsü."** Ne sistematik işlemin avantajını alırsın, ne de takdirin. İşler kötü gidince hatanın kimde olduğunu bilemezsin.
- **Düşüşte ne zaman endişelenmeli?** Backtest'teki maksimum düşüşle karşılaştır. Backtest maksimumu %40 ve şimdiki düşüş %10 ise endişelenme, müdahale etme. Şimdiki düşüş backtest maksimumunu aşıyorsa olası sebepleri incele: aşırı uyum, piyasa değişimi, maliyet artışı ya da koddaki bir hata. (§6e'deki durma kriteriyle aynı mantık.) Carver'ın 8 yıllık canlı kaydı: 2-3 zararlı yıl (%5-10), en kötü canlı düşüş ~%15.
- **Riski, en kötü düşüşü kaldırabileceğin seviyeye ayarla.** "Riski 2-3 katına çıkarsam en kötü düşüşüm %30-45 olurdu, ve o zaman ben de sistemi değiştirmek isterdim."
- **Piyasa seçme** (✔ test edildi, aşağıda). "Piyasaları performansa göre seçmek aşırı uyumdur. Grafiğe hata çubuklarını ekleyince tüm farkın gürültü olduğunu görüyorsun." Çıkarma ölçütleri sadece likidite, maliyet ve **çok düşük volatilite** (aşırı kaldıraç yaratır, 02 §6b-2).
- **Maliyet hızı belirler.** Ucuz piyasada daha hızlı kurallar işlenebilir, pahalıda daha yavaş, sonunda hiç işlenmez. Enstrümanlar arasındaki tek gerçek fark maliyet.
- **Çeşitlendirici ama marjinal stratejiyi ekle, yüksek getirili ama korelasyonlu olanı ekleme.** Gerekçe teknik: korelasyon tahmininin örnekleme hatası, ortalama ve Sharpe tahmininkinden küçük. Düşük korelasyonlu bir kural backtest'te getiri katmamış olabilir, ama bu şanssızlık da olabilir. Örnek dışı dönemde çeşitlendirme faydası sağlaması daha olası. Clenow'un "zarar eden piyasa da portföyü iyileştirebilir" görüşüyle aynı (12). Ama kuralın **negatif beklentili** olmaması ve korelasyonun gerçekten düşük olması gerekir. 25. turdaki tahvil ve döviz kollarında ikisi de yoktu.
- **Bir fikri test etmeden önce sor: "Karşı tarafta kim kaybediyor, ve kaybetmeye devam etmeye razı mı?"** Davranışsal risk primleri, yani karşı tarafın rahatsız olduğu riskler kalıcıdır, çünkü insan davranışı değişmiyor. "Neden çalıştığını açıklayamadığın garip bir anomaliye asla dokunmam, neredeyse kesin aşırı uyumdur." Bu, 22. turdaki gün sonu dönüş hipotezinin akıbetiyle uyumlu (04 §6b-4).
- **"Gizli sos" efsanesi.** "Başarılı hedge fonlarında bile getirinin %90'ı herkesin bildiği şeylerden gelir. Kalan %10'un çoğu aptalca bir şey yapmamaktan." "Momentum neden çalışır? Çünkü sistem olmadan momentumu işlemek bir insan için çok rahatsız edici." Fikirlerinin çoğu AQR gibi yerlerin yayımladığı araştırmalardan.
- **Hibrit yaklaşım**: Takdirli tahmini 1-5 arası puanla ver, sonra **sistematik bir pozisyon ve risk motoruna** besle. "Pozisyon boyutu, risk yönetimi ve maliyet yönetimi kesinlikle bilime bırakılmalı." Takdirli tahminlerin gerçekten kârlı olup olmadığını istatistikle test et: "4 işlem kazandırdı diye Buffett olduğunu sanma."
- **Yeni başlayan için**: "Herkes sistematik başlamalı. Bisikletteki **yardımcı tekerlek** gibi, aşırı işlemi ve aşırı kaldıracı engeller." Başlangıç sistemi (*Leveraged Trading*): tek bir kırılım kuralı + ATR + 10 satırlık bir tablo. Kod bile gerekmiyor.

**✔ Test** (`arastirma/verify_carver_claims.py`, 19 ETF ve parite, 12 ay momentumu, 2005+):
- **Çeşitlendirme**: tek piyasanın ortalama Sharpe'ı **0,20**, 19 piyasalık eşit riskli portföyünki **0,55**, yani **2,7 kat**. Rastgele alt kümelerde 1 piyasa 0,30, 3 piyasa 0,30, 5 piyasa 0,40, 10 piyasa 0,46. Carver'ın "100 piyasayla ~5 kat" iddiasıyla aynı yönde. ✔
- **Piyasa seçmenin anlamsızlığı**: tek piyasa Sharpe'larının dağılımı (standart sapma **0,22**), 22 yıllık bir Sharpe'ın standart hatasıyla (**~0,21**) aynı. "SPY 0,55, USDCHF -0,18" farkı **istatistiksel olarak gürültüden ayırt edilemiyor**. ✔
- **Sürekli sinyal** (fiyatın N günlük aralıktaki konumuna orantılı pozisyon, haftalık yeniden dengeleme) bu kaba uygulamada ikili 12 ay sinyalinden **kötü** çıktı. Uzun geriye bakışlarla Sharpe 0,26-0,32, ikili sinyalde 0,55. Kısa geriye bakışlar (20-80 gün) eklenince ~0, bu da Parker'ın gözlemiyle tutarlı. Carver'ın asıl iddiası daha az maliyet ve daha az uç sonuç, Sharpe değil. Gerçek sisteminde sinyal yumuşatılıyor ve ölçekleniyor. → **Bu uygulamada doğrulanmadı**, ama Carver'ın tam yöntemi test edilmiş sayılmaz.

**Neyin öngörülebilir olduğu** (Carver, Top Traders Unplugged #386, OVh3f8hmchA). Carver'ın iddiası: "Gelecek ayın volatilitesini bu ayınkiyle regresyona sokunca R² ~0,35 çıkar, korelasyonda 0,2-0,25. Ortalama getiride hiçbir şey çıkmaz, sadece gürültü." ✔ Test (`arastirma/verify_vol_adjust.py`, 19 piyasa, aylık, piyasa başına R² ortalaması):

| Ne tahmin ediliyor | R² |
|---|---|
| Aylık volatilite | **0,35** (logaritmik volatilite 0,41; piyasaya göre 0,04-0,54) |
| Korelasyon, 6 aylık pencere | **0,23** |
| Korelasyon, aylık pencere | 0,12 |
| Aylık getiri | **0,008** |

Rakamlar Carver'ınkilerle neredeyse birebir aynı.

**Pratik anlamı**:
- **Risk tahmin edilebilir, yön tahmin edilemez.** Bu yüzden boyut, volatiliteye göre sistematik ayarlanır.
- Getiri "tahmini" (setup'ın ne kadar güzel göründüğü) boyutu belirlemez (02 §6b-3, §6c).
- Korelasyon daha yavaş değişir, daha uzun pencereyle tahmin edilir.

**AI ve LLM'ler üzerine** (aynı bölüm):
- Carver kendini şüpheci olarak tanımlıyor.
- Ona göre sistematik finans zaten bir tür makine öğrenmesi: regresyon ve optimizasyon da bu sınıfa girer.
- Yapay zekânın en anlamlı olduğu alan **dar tanımlı ve verisi bol** problemler, örneğin tick verisiyle emir icrası araştırması.
- 50 yıllık günlük veri, doğrusal olmayan büyük modeller için az.
- "Bizim yapay zekâ botumuz" pazarlamasına karşı bu bir kırmızı bayrak hatırlatması (11).

## 6k. Carver ikinci bölüm: maksimum düşüş, değerlendirme süresi, risk yönetimi ile optimizasyon farkı (Zerodha "In The Money" #04, p0znNV4oWe8)

- **"Maksimum düşüş berbat bir performans ölçütü."** Üç sebebi var:
  1. **Uç olaylara bağlı.** Backtest kısaysa kötü olayları kaçırır ve maksimum düşüş olduğundan iyi görünür.
  2. **Örnekleme hatası büyük.** Tek bir sayı, geniş bir dağılımdan tek bir çekiliş.
  3. **Zamanla büyür.** 2 yıllık backtest'te %20 olan maksimum düşüş, 5 yılda daha büyük beklenir.
  - Çözüm: backtest'i **bootstrap** et ve **ilgilendiğin süre için** maksimum düşüş dağılımına bak. "%10 ihtimalle %50 düşüş var" çıkarsa riski düşür.
- **Bir stratejiyi ne zaman kapatmalı?** Maksimum düşüşe değil, **kayan dönem ortalama getirisine** bak. Bunu backtest'ten bootstrap edilmiş beklenen dağılımla karşılaştır. **Alt %5'e** düşerse ("20'de 1") kapat ya da incele. Olası sebepler: maliyet artışı, kod hatası, rejim değişikliği.
  - Gereken kanıt "insanların sandığından çok çok fazla". Yavaş bir sistem için en az 10 yıllık pencere gerekir. Yüksek frekanslı bir sistem için bir hafta yeterli olabilir.
  - "Birkaç ay çalışmadı diye bir şey yapmak gerekmez." 14 §3d'deki Brandt'ın seri analizi ve §3'teki tabloyla aynı mantık.
- **"2008'den sonra piyasa değişti, sadece son 17 yılı kullanayım"**: 17 yıl, yavaş bir sistemde istatistiksel olarak anlamlı bir fark göstermeye yetmez. Uzun veri, farklı rejimleri (resesyon, enflasyon, kriz) kapsamak içindir.
- **Risk yönetimi ≠ optimizasyon.**
  - Son dönemde iyi giden stratejiye ağırlık vermek ya da kötü gideni kısmak **optimizasyondur** ve yavaş sistemlerde gürültüye göre karar vermek demektir. Carver "**asla**" yapmıyor.
  - Risk yönetimi şudur: **şu anki pozisyonlarla** beni korkutan belirli bir riske aşırı maruz kalmış mıyım? Öyleyse toplam risk küçültülür.
- **Canlı sonuç ile backtest'i karşılaştır.**
  - Pozisyon pozisyon karşılaştır. Fark varsa sebebi ya üretim kodu ile araştırma kodunun farklı olması ya da gerçekçi olmayan dolum varsayımlarıdır.
  - Yeni başlayana öneri: canlıya geçmeden önce backtest'in bootstrap'ından **günlük ve haftalık getiri dağılımı ile düşüş profili** beklentisi çıkar. Canlı sonuçlar bu aralığın dışına çıkarsa fark edersin.
- **Yeni enstrüman**:
  - Her enstrümanı aynı kuralla işle.
  - Volatilite ve hareketli ortalama için kısa bir ısınma süresi yeter.
  - Korelasyon tahmini yoksa **diğer her şeyle korelasyonu 1 varsay** (temkinli). Gerekirse vekil seriyi ekle: E-mini'den önce büyük S&P kontratı, vadeliden önce spot Bitcoin.
- **Yapay zekâ ve LLM'ler**:
  - Carver üretim kodunda **asla** kullanmıyor. Sadece hatası kolay görülen küçük işlerde kullanıyor; bir eğri uydurma kodu "10 denemede" doğru çıkmış.
  - "Hazır bir LLM'le piyasada gizli bir para kazanma yolu bulmak absürt. Büyük ihtimalle yeni bir dolandırıcı ve fırsatçı sektörü olacak: 'AI trading bot' etiketiyle aynı çöp."
  - "Kendi yazmadığın ve tam anlamadığın kodla otomatik işlem yapmak çok tehlikeli."
- **Kriz anında korelasyon artar.** Herkes nakit için her şeyi sattığından, normalde ilişkisiz pozisyonlar birlikte hareket eder (Nisan 2025).
  - Büyük fon dezavantajı: Carver AHL'de 8 milyar $ yönetirken riskin ~%15'ini ABD tahvil piyasasına koymak zorundaydı. Mayıs 2013 tahvil şokunda çok hızlı kaybettiler.
  - Küçük trader daha iyi çeşitlendirebilir.

**✔ Test: maksimum düşüşün örnekleme dağılımı** (`arastirma/verify_carver_zerodha.py`)
- **Kurgu**: 12 ay momentumu, yıllık %8 volatiliteye ölçeklendi, 23 yıl, Sharpe 0,47. 20 günlük bloklarla bootstrap.
- **Tarihsel tek maksimum düşüş: %18,5.**

| Süre | 5. yüzdelik | Medyan | 95. yüzdelik | P(maks. düşüş > %10) |
|---|---|---|---|---|
| 1 yıl | %3,8 | %7,4 | %14,6 | %25 |
| 2 yıl | %5,4 | %9,9 | %19,2 | %49 |
| 5 yıl | %8,3 | %14,2 | %25,6 | %85 |
| 20 yıl | %14,4 | %21,9 | %35,7 | %100 |

- ✔ **Zamanla büyüyor**: medyan 1 yılda %7, 20 yılda %22.
- ✔ **Dağılım geniş**: 20 yıllık pencerede %14 ile %36 arası. Tarihsel %18,5 bu dağılımdan sadece bir çekiliş.
- **Prop için anlamı**:
  - "Backtest'imde maksimum düşüş %6'ydı, %10 limitli hesapta güvendeyim" demek yanlış.
  - Sorulacak soru şu: **challenge ve fonlu hesap süresi boyunca** maksimum düşüşün %10'u aşma olasılığı ne?
  - Bu stratejide %8 volatiliteyle 1 yıl içinde **%25**, 2 yılda **%49**. Fonlu hesapta uzun kalmak istiyorsan volatiliteyi daha da düşük tutmak gerekir. Bu, 09'daki "fonlu hesabın ortalama ömrü kısa" verisiyle tutarlı.

## 6l. Rastgelelik düşmandır: rastgele grafik atölyesi (Grimes, MarketLife "Traders Workshop" Ep. 16, N11WdgrQDA4)

- **Bir istatistik ancak rastgele veride görülmüyorsa geçerlidir.** Bir dinleyicinin fizikçi arkadaşı haklı: gerçek ve rastgele veri aynı eğilimi gösteriyorsa ortada bir eğilim yoktur. Bu bilgi tabanının test yöntemi de bu: rastgele yürüyüş, bootstrap ve konumu eşleştirilmiş rastgele giriş (§6g, 04 §6b-5, §7b).
- **Rastgele piyasada hiçbir stop, hedef ya da para yönetimi avantaj yaratmaz.**
  - Dar stop ve büyük hedef koyarsan isabet oranı kendiliğinden düşer. Beklenti = isabet × ortalama kazanç − kayıp oranı × ortalama kayıp = 0 kalır. Bu bilgi tabanındaki simülasyonların p = (1+e)/(1+k) varsayımı tam da budur.
  - Kısa vadede şans her iki yönde de büyük sonuç verir. Yazı-tura oynayan biri neredeyse hiçbir anda sıfırda değildir.
- **"Mükemmel görünen setup da rastgele oluşmuş olabilir."** Grimes bu yüzden hiçbir işlemde "her şeyi ortaya koymuyor" ve risk kuralını çiğnemiyor (02 §6c ile aynı).
- **Akademik görüş**: piyasalar büyük ölçüde rastgeleye yakın hareket ediyor. Grimes'a göre gün içi veride rastgele yürüyüşten sapmalar daha belirgin, ama maliyet de daha yüksek.
  - ⚠️ Bu bilgi tabanının testleri bunu kısmen destekliyor. Gün içinde ortalamaya dönüş ve mikro yapı etkileri olabilir, ama maliyetten sonra test ettiğimiz gün içi setup'ların (açılış kırılımı, süpürme, gün içi momentum) hiçbiri rastgeleden ayrılmadı.
  - Carver'a göre trend haftalar ile aylar arasında çalışır (12).
- **Yükselme eğilimli rastgele yürüyüş bile uzun ayı piyasaları üretir.** Ör. %55 yukarı olasılıklı yazı-tura. Bu yüzden al ve tut, her aktif strateji için geçilmesi gereken çıtadır.
- **"Açılış fiyatı çoğunlukla günün tepesine ya da dibine yakın olur, demek ki piyasa rastgele değil"** yanlış. Bu durum rastgele yürüyüşte de görülür. Brooks testimizle aynı sonuç (§6g).
- **Örneklem**: günlük veride birkaç bin veri noktası var. Hisseler birbiriyle çok korelasyonlu olduğu için 50 hisse eklemek örneklemi 50 kat büyütmez.

**Grimes'ın 4 adımlı rastgele grafik atölyesi** (Excel ya da Python):
1. **Yazı-tura yürüyüşü** (+1/-1), sonra eğilimli versiyonu (%52-55 yukarı).
2. **Normal dağılımdan günlük getiri.**
3. **Normal dağılımların karışımı**: %95 sakin gün (±%1), %5 çılgın gün (±%5). Gerçek piyasaya çok daha yakın kalın kuyruklar üretir.
4. **En iyisi, gerçek getirileri karıştırmak (bootstrap).** Kapanıştan kapanışa getiri, ayrıca yüksek, düşük ve açılış değerleri önceki kapanışa göre. Gün içi veride gece boşluklarına ve saat profiline dikkat et.

Kendi formasyonunu (kırılım, Fibonacci, osilatör) bu grafiklerde ara. Gerçek veride gördüğün ama rastgelede görmediğin şey sinyaldir. Bu, replay uygulaması için bir mod olabilir (13 §5 madde 12).

## 6m. Grimes: trading neden bu kadar zor, avantaj nasıl kanıtlanır, örneklem dışı test tuzakları (Better System Trader, -RzXLy2SPC4)

- **Tek kelimelik cevap: rastgelelik.**
  - Piyasa psikoloji literatüründeki anlamıyla bir **"kötü öğrenme ortamı" (wicked learning environment)**. Avantaj küçük ve sonuçlar yaptığın şeye çok gevşek bağlı.
  - Doğru işlemi yapıp haftalarca ceza yiyebilirsin, ya da tersine yanlış işlemden kazanabilirsin.
  - Bu yüzden piyanoda ya da tenis sporunda işleyen **"bilinçli pratik" (deliberate practice) modeli trading'de büyük ölçüde başarısız oldu.** Geri bildirim tutarlı değil.
  - Mühendisler, beklenenin aksine, en çok zorlanan gruplardan biri.
- **Acemi şansı en kötü öğretmendir.**
  - Örnekler: anaokulu öğretmeni 2.000 $'ı birkaç haftada 300.000 $ yapmış (2000), değersiz bir kripto paradan yarım milyon dolar kazanan biri.
  - "Çok para kazanmak için beceri gerekmez, şans yeter. Ama tutarlı kazanmak ve kazandığını tutmak için beceri ve disiplin gerekir." Bu kişiler normal piyasaya uyum sağlayamaz.
- **Gerçek avantajlar küçüktür**: %52-55 yazı-tura. %90'lık bir avantaj olsaydı piyasa var olamazdı.
  - İş, piyasanın **daha az rastgele olduğu anları** bulmak: lastik bant gerilmişken (aşırı hareket) ya da volatilite çok sıkışmışken.
  - Rastgele bölgede işlem yapmak "en iyi ihtimalle işlem maliyeti ödemek".
- **Zaman dilimleri**:
  - Akademik bulgu: yüksek zaman dilimleri istatistiksel olarak daha rastgele görünür. Düşük zaman diliminde rastgele yürüyüşten sapmalar daha sık, örneğin büyük bir haberden sonraki salınımlar.
  - Ama 1 dakikalık grafikte "çöp" çok. Yer seçmek şart.
  - (Bu bilgi tabanının maliyetli gün içi testlerinde bu sapmalar işlenebilir bir avantaja dönüşmedi, §6l.)
- **Takdirli trader avantajını nasıl kanıtlar?** Geçmiş test + **ona uyan ileri test ya da gerçek para sonuçları.**
  - "Backtest'e güvenim sıfıra yakın. Başkası yaptıysa sıfırın altında."
  - Takdirli yöntem zamanla kendiliğinden evrilir (stop ve çıkış ayarları). Düşüşlerin bir kısmı bu yeniden uyum dönemleri.
  - Performansı **kontrol grafikleriyle** (üretimden ödünç; normal bandın dışına çıkış) izle (Carver'ın önerisiyle aynı, §6k).
  - Sonuçlar iyiyse: "Neyi bekliyorsun? İşle, boyutu artır, izle."
- **Hayat olayları** (hastalık, boşanma, dava, yeni doğan bebek, yani iyi olaylar da dahil): **işlem boyutunu küçült.** "Milyonlar kazanan trader'lar 'bana olmaz' der, olur."
- **Psikoloji mi, avantaj eksikliği mi?**
  - "Avantajı olmayan ve kaybeden bir trader'ın psikolojik sorunu **olmalı**, işe yaramayan bir şey yapıyorsun."
  - "Trading tamamen psikolojidir" ve "piyasayı değil, piyasa hakkındaki inançlarını işlersin" görüşleri, avantajın gerekliliğini küçümsüyor. Önce avantaj, sonra psikoloji.
  - Çoğu zaman **davranışı değiştirmek psikolojiyi düzeltir.** Örnek: işlem başına %20 riskle hiçbir inanç sistemi kurtarmaz.
  - Grimes'ın deneysel protokolü (yayımlanmadı): yazı-tura ve kart serileri, sonra çok küçük **rastgele** gerçek işlemler (farklı stop ve hedef oranlarıyla), en son karar hakkı.
    - Eğitimsiz kararlar **rastgeleden kötü** çıkıyor.
    - Rastgeleliği içselleştirdikten sonra kararlar rastgeleden iyi.
    - Replay uygulamasında uygulanabilir (13 §5 madde 12).
- **✘ "Örneklem dışı test için başka bir ticker kullanayım"**: Hayır, tickerlar korelasyonlu, gerçek bir örneklem dışı test değil.
  - Örneklem dışı veriye bir kez dokununca "yanar". Pratikte **walk-forward ya da ileri test** (simülatörde ya da küçük gerçek parayla) daha iyi.
  - Örneklem dışı dönemin rejimi de önemli: örneklem dışını Mart-Aralık 2020 seçmek garip bir test olur.
  - Bu bilgi tabanı için ders: sembol dışı tekrarlar (14. ve 15. turlar) korelasyonlu semboller içeriyordu. Endeks pullback avantajı zaman bölmesinde zayıflıyor (04 §5b madde 4).
- **Ne kadar geriye test?**
  - Günlük sistem için ~10 yıl, artı özel dönemler: 2000'lerin ayı piyasası, 1980'ler. "Nasıl başarısız olduğunu merak ediyorum."
  - 700 hisseyle test etmek korelasyon yüzünden sanıldığı kadar güçlü değil.
  - Gün içi sistemlerde birkaç yıl yeter, ama istikrar beklentisi daha düşük.
  - (Grimes kendi pullback tezini ABD hisselerinin tüm tarihinde, Orta Çağ arpa fiyatlarında ve Mezopotamya kil tabletlerindeki fiyat kayıtlarında da benzer bulduğunu söylüyor. İlginç ama doğrulanamaz.)
- **Forex neden zor?** Daha rastgele ve gürültülü.
  - "Bankaların hareketli ortalamayla işlem yaptığını anlatan Forex YouTube kanalları... para piyasaları öyle işlemez."
  - Hisselerde 20 pozisyon ≈ 1 risk. Hisse ve kur programlarının düşüşleri birbirini dengeleme eğiliminde.
- **Haber**: "Haber olduğunda iş bitmiştir. Algoritmalar savaşı bitirmiş, ben sopamla geliyorum." Haberle hareket eden fiyatı işler (kazanç sonrası drift gibi), haberin kendisini değil.
- **Hibrit ("gri kutu")**: algoritmik giriş + takdirli çıkış. İyi olabilir ama serbestlik derecesi patlar, backtest güvenilmez olur.
- **Takdirli pullback, sistematik ortalamaya dönüş**:
  - Pullback'in nicel versiyonu daha küçük bir avantaj gösteriyor, takdirli uygulaması daha iyi.
  - Ortalamaya dönüş takdirli trader için sezgiye ters, sistematik yapılmalı.
  - Basit pullback taraması: "son N günün en yüksek değerinin X ATR altında" + momentum filtresi.

## 6n. ✔ "Teknik analiz fraktaldır" iddiası: aynı kural farklı zaman dilimlerinde (Breitstein, bZ7-iBaI_Xw + test)

**İddia**: "5 dakikalık grafikteki kavramlar günlük, haftalık ve aylık grafikte neredeyse aynen görülür. İyi bir gün içi setup neredeyse her zaman iyi bir günlük setup'tır. Swing'e geçmek için yeni bir oyun kitabı gerekmez."

**Test** (`arastirma/verify_gap_risk.py` B bölümü): Aynı iki kural 5 dakikalık (60 gün), 1 saatlik (730 gün) ve günlük (2005+) barlarda. Ölçü: ATR cinsinden ileri getiri eksi aynı yönün koşulsuz getirisi.
- (i) 20 bar tepesini kapanışla kır, 10 bar tut.
- (ii) "Kapitülasyon": toplam düşüşü 2 ATR'yi geçen 3 ardışık düşüş kapanışı, al ve 5 bar tut.

| Sembol | Zaman dilimi | Gidiş-dönüş maliyet (ATR) | Kırılım | Kapitülasyon alımı |
|---|---|---|---|---|
| SPY | 5 dk / 1 sa / günlük | 0,031 / 0,009 / 0,011 | -0,27 / -0,03 / -0,05 | +0,07 / +0,23 / +0,28 (se ~0,15) |
| QQQ | 5 dk / 1 sa / günlük | 0,022 / 0,007 / 0,016 | +0,01 / +0,14 / +0,03 | +0,13 / +0,03 / +0,19 |
| GLD | 5 dk / 1 sa / günlük | 0,048 / 0,017 / 0,013 | **-1,27 (se 0,64)** / -0,08 / +0,13 | -0,04 / -0,22 / -0,05 |
| EURUSD | 5 dk / 1 sa / günlük | **0,489** / 0,095 / 0,011 | -0,09 / -0,03 / -0,18 | +0,06 / +0,02 / +0,19 |

**Sonuç**:
- **Şekiller her ölçekte görülür, ama bu bir avantaj kanıtı değil.** Rastgele yürüyüş de ölçekten bağımsızdır, yani her zaman diliminde aynı "formasyonları" üretir (10 §6l).
- **Avantajın işareti zaman dilimleri arasında tutarlı değil.** Altında kırılım 5 dakikada -1,27 ATR (2 se), günlükte +0,13. SPY'da kırılım her ölçekte ≤0.
- **Tutarlı görünen tek şey**: endekslerde kapitülasyon alımı 1 saatlik ve günlükte pozitif (+0,19 ile +0,28 ATR, ~1,5-1,8 se). RSI-2 bulgusuyla uyumlu (12), ama 5 dakikada gürültü.
- **Maliyet fraktal değil**: EURUSD'de gidiş-dönüş maliyeti 5 dakikada ATR'nin %49'u, günlükte %1'i (45 kat). Aynı şekil, küçük zaman diliminde çok daha büyük bir maliyet engelini aşmak zorunda.
- **Hüküm**: "Kavram taşınabilir" makul bir **hipotez**, "iyi gün içi setup neredeyse her zaman iyi günlük setup'tır" desteklenmedi. Her zaman dilimini ayrı ve maliyetten sonra test et. Breitstein'ın kendisi de geçişin "birkaç yıl" sürdüğünü, boyut, sabır ve portföy yönetimini yeniden öğrendiğini söylüyor (14 §3g).
- ⚠️ 5 dakikalık örneklem 60 gün, zayıf. Kurallar basit tutuldu, Breitstein'ın takdirli setup'larını temsil etmez.

## 6o. ✔ Yön ve rejim: rastgele long girişler boğa yılında "avantajlı" görünür (54. tur, `arastirma/verify_regime_beta.py`)

**Bağlam**: 1,3 milyon $ prop ödemesi alan Zamco'nun (09 §4x) kârının %60-70'i altının tarihi yükselişindeki 3 aydan geliyor. Kendisi "piyasa koşulları stratejime çok uygundu" diyor. Sunucunun tespiti: "Altın ve endeksler doğası gereği yükselen varlıklar, alışlar bu yüzden çalışıyor."

**Test**: Hiçbir beceri olmadan her gün açılışta rastgele giriş. Stop 0,5 ATR, hedef 1 ATR (RR 2, başa baş isabet %33,3), ikisi de olmazsa kapanışta çıkış ("günlük mumu yakala").

| Piyasa | Dönem | Rastgele long: ort. R / isabet | Rastgele short | Al-tut |
|---|---|---|---|---|
| Altın | 2015+ tümü | +0,05R | +0,01R | |
| Altın | 2024 | +0,15R / %54 | -0,08R / %40 | +%27 |
| Altın | 2025 | +0,17R / %52 | -0,18R / %37 | +%64 |
| Altın | **2025 4. çeyrek** | **+0,22R / %58** | **-0,31R / %31** | +%12 |
| Altın | 2015 | -0,06R / %41 | +0,14R / %52 | -%10 |
| Nasdaq 100 | 2015+ tümü | +0,06R | -0,03R | |
| Nasdaq 100 | 2017 | +0,19R / %57 | -0,17R / %34 | +%32 |
| Nasdaq 100 | 2022 | -0,10R / %39 | +0,14R / %51 | -%32 |
| DAX | 2015+ tümü | +0,03R | 0,00R | |

(EURUSD'nin yfinance günlük verisi 2022 sonrasında bozuk göründüğü için tablodan çıkarıldı.)

**Ders**:
- Becerisi olmayan bir trader bile, yükselen bir piyasada **sadece long** işlem yaparak işlem başına +0,15 ile +0,22R görebilir. Bu, bu bilgi tabanında zaman testinden geçen en iyi avantajlardan (RSI-2 +0,17R, 12) daha büyük. Ve tamamen piyasanın yönünden geliyor.
- Yön değişince (altın 2015, Nasdaq 2022) aynı "strateji" negatife döner.
- **Kendi sonucunu her zaman yön ve dönem eşleştirilmiş rastgele girişe karşı ölç.** Birkaç aylık büyük kâr, o dönemin yönünü ölçmeden beceri kanıtı sayılmaz (11 #85). Bu tabanın pullback düzeltmesi de aynı nedenle yapılmıştı (04 §5b).
- Prop'ta pratik anlamı: bir trend döneminde art arda challenge geçip ödeme almak, piyasa yatay ya da ters döndüğünde sürmeyebilir. Ödeme aldığın ayları piyasanın o aylardaki yönüyle birlikte kaydet.

## 7. Bulkowski (Encyclopedia of Chart Patterns / Candlestick Charts) — site hâlâ erişilemiyor, mum istatistikleri test edildi

thepatternsite.com DNS hatası nedeniyle okunamadı. Arama özetinden **doğrulanmamış** tek veri: OBO tepe (boğa piyasası) — başa baş başarısızlık oranı ~%19, pullback ~%68, fiyat hedefine ulaşma ~%51. Bulkowski verisinin önemli özellikleri (genel bilgi): çoğunlukla **ABD hisseleri, günlük grafik**; "başa baş başarısızlık" = kırılım yönünde en az %5 hareket edememe.

### 7b. ✔ "%84 isabetli mum formasyonu" ve geometri (`arastirma/verify_candles_bulkowski.py`)

Financial Wisdom (4Lx-NnMOpWs), Bulkowski'nin "en güvenilir 5 mum formasyonunu" isabet oranlarıyla aktarıyor: three-line strike %84, three black crows %78, evening star %72, abandoned baby %70, two black gapping %68. **Önemli tanım**: Bulkowski'nin oranı **kâr oranı değil**, fiyatın formasyonun tepesinin üstünde mi yoksa dibinin altında mı **önce kapandığını** ölçüyor. Video bu oranları kâr gibi sunuyor ve 10 günlük getiriyi "yıllık %274" diye yıllıklandırıyor. Nadir bir formasyon sürekli tekrarlanamaz, bu yanıltıcı.

**Hipotez**: Formasyonun son mumu aralığın ucunda kapanıyor. Fiyat zaten o kırılım seviyesine yakın olduğu için önce onu geçmesi muhtemel. Yani oranın büyük kısmı **geometri** olabilir.

**Test** (günlük, 2005+, 30 büyük ABD hissesi + 10 ETF). Her formasyon, kapanışı aralık içinde **aynı konumda** olan rastgele günlerle karşılaştırıldı.
| Formasyon (n) | Beklenen yönde kırılma | Tüm günler | **Konumu eşleştirilmiş rastgele günler** | Fark | 10 günlük getiri (eğilim çıkarılmış) |
|---|---|---|---|---|---|
| Three-line strike, boğa (22) | %68 | %57 | %79 | **-11 puan** (se 10) | -0,39 ATR (se 0,55) |
| Three black crows (853) | %73 | %43 | %67 | **+5 puan** (se 2) | **+0,21 ATR** (se 0,09) |
| Evening star (141) | %65 | %43 | %63 | +1 puan (se 4) | -0,01 ATR |
| Two black gapping (666) | %64 | %43 | %67 | -3 puan (se 2) | -0,11 ATR |
| Abandoned baby, boğa (41) | %73 | %57 | %72 | +2 puan (se 7) | -0,37 ATR |

**Sonuç:**
1. **"%70-80 isabet" oranlarının neredeyse tamamı geometri.** Kapanış aralığın dibindeyse, rastgele günlerin de ~%65'i önce aşağı kırılıyor. Formasyonların bunun üstüne kattığı -11 ile +5 puan arası.
2. **Tek küçük istisna three black crows**: +5 puan (t≈2,5) ve 10 günde eğilim çıkarılınca +0,21 ATR'lik devam etkisi. 5 formasyon test edildiği için bu tek bulgu çoklu test şüphesi taşıyor.
   - **Sembol dışı tekrar** (19. tur, 40 yeni hisse ve ETF, `verify_candles_bulkowski.py new`): **10 günlük etki tekrarlanmadı** (+0,04 ATR, se 0,08). Kırılma yönündeki fazla +3 puan, ekonomik olarak önemsiz. Diğer formasyonlarda da geometri açıklaması aynen tekrarlandı: formasyonun katkısı -4 ile +6 puan arası, getiriler ~0. → **Three black crows dahil hiçbir formasyonun tek başına avantajı yok.**
3. Kendi mekanik tanımlarımız Bulkowski'ninkilerle birebir aynı değil. Örneklem farklı (onun verisi 1990'lar ve 2000'ler, binlerce hisse). Ama mesaj genel: **Bir "kırılım yönü" istatistiğini, aynı kapanış konumundaki rastgele günlerle karşılaştırmadan avantaj sanma.**
4. 12'deki mum formasyonu satırındaki "bağlamsız anlamsız" notu destekleniyor. Mum, bir **giriş tetiği** olarak bağlamla (seviye, trend, failure test) birlikte kullanılabilir. Tek başına tahmin aracı değil.

## 8. Kendi simülasyonlarım

`arastirma/verify_math.py` ve `arastirma/verify_ftmo.py` — sonuçlar `arastirma/*_sonuc.txt`. Yeni bir iddia gördüğünde aynı şekilde simüle et.
