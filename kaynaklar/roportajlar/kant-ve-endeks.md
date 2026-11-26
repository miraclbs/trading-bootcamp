# Thorp, Simons, Bogle: Avantaj, Boyut ve Endeks (röportaj analizi)

> Tarih: 2026-11-25. Üç röportajın transkripti (otomatik altyazı) baştan sona okundu. Kelly hesabı ve FTMO simülasyonu bu dosya için yapıldı (20.000 deneme/satır, §1c).
> Derecelendirme: ✔ bağımsız kanıtla uyumlu · ◐ kısmen doğru ya da kendi beyanı · ✘ kanıtla çelişiyor. Alıntılar otomatik altyazıdan.
> Bilgi tabanında zaten olanlar tekrarlanmadı: Simons ve Thorp profilleri (16 §1.6-1.7), Kelly formülü (01 §7), aktif-pasif kanıtı (18 §3), yayın sonrası erime (17 §1).

## Özet

1. **Üçü de sıradan yatırımcıya aynı şeyi söylüyor: düşük maliyetli endeksi al ve tut** ✔. Thorp'a göre cevap "neredeyse herkes için çok basit". Bogle'a göre yatırımcılar toplamda piyasa getirisi eksi maliyeti alır. Simons dolaylı olarak aynı yerde: Renaissance dışarıya kapalı, giriş bariyeri çok yüksek.
2. **Avantaj var, ama küçük, gizli ve geçici** ✔. Simons'a göre avantaj, tek başına hiçbiri büyük olmayan "ince anomaliler"in toplamı. Thorp'unki rekabet gelene kadar sürdü. Maliyet sonrası 100-200+ işlemle ölçülmüş bir avantajın yoksa avantajın yok.
3. **Senin sayılarınla (%40 isabet, 2R) Kelly işlem başına %10 risk diyor, yarım Kelly %5. FTMO'da ikisi de challenge'ı tek işlemlik yazı-turaya çeviriyor**: geçme olasılığı ≈ %40, yani isabet oranın kadar. %1 riskte geçme %87. İsabeti 5 puan fazla tahmin etmek (100 işlemde ~1 standart hata) yarım Kelly'nin büyümesini sıfıra indiriyor.
4. **Şansın payı büyük** ✔. Simons modelsiz ilk iki yılındaki başarıya "düpedüz şans" diyor. Thorp'a göre endeksi geçen azınlığın "kimi şansla, kimi beceriyle" geçiyor. Tek dönemin sonucu kanıt değil (16 §3).
5. **Maliyet ve işlem sıklığı sessiz düşman** ✔. Bogle'ın "aracının payı", Simons'un "çıkarma" ve Thorp'un "kumarhane payı" aynı ders: gün içinde maliyet avantajı yer (README #28).

---

## 1. Ed Thorp: The Tim Ferriss Show

**Künye**: `CNvz91Jyzbg`, "Legendary Trader Edward O. Thorp on Beating the Stock Market and Blackjack", Tim Ferriss, 2022-05-25, 1:33:33, ~283 bin izlenme. Thorp kayıt sırasında 89 yaşında. Resmi yazılı transkript tim.blog'da var.
**Not**: Bu bölümde de, ikinci bölümün yazılı transkriptinde de Kelly geçmiyor. Thorp'un Kelly görüşü ortak yazarı olduğu makaleden alındı (§1c).

### 1a. Ana iddialar

1. **Teoriyi parayla test et.** Blackjack sistemini kitabı yazmadan önce kendisi oynadı: 10.000 $ kasa, ~20 saat, +11.000 $. Sonuç tahmin ettiği gibi çıktı, ama teoride çalışan şeylerin denenince beklenmedik sorunlar çıkardığını vurguluyor.
2. **Avantaj, matematiğe dökülebilen bir fiyatlama hatasından geldi.** Ucuz varantı alıp hisseyi açığa sattı (ya da tersini yaptı). İlk hesaplarda "neredeyse risksiz yıllık %25" kazandı. Fonu ~20 yıl boyunca yıllık "%20'nin biraz altında" getiri yaptı, sadece 3 zararlı ayı oldu ve her biri %1'in altındaydı.
3. **Avantaj yayıldıkça biter.** Opsiyon modelini 1967'de bulup sakladı, sonra Black ve Scholes yayımladı. 1973'te opsiyon borsası açıldığında trader'ları yine "ok ve yaya karşı makineli tüfek" gibiydi. ~1988'e kadar "doktoralı lejyonların" önünde kaldı.
4. **Neredeyse herkes için cevap: hisse endeksini al ve tut.** Aktif yatırımcılar toplamda yine endeksin kendisidir, ama üstüne işlem maliyeti, vergi ve danışman ücreti öderler. Thorp'un rakamları: aracılara para ödemezsen %10,5, ödersen %8, 7 ya da 6. Kendisi de vergi yüzünden Citadel'den çıkıp endekse geçti.
5. **Piyasa tam etkin değil, ama endeksi geçmek ciddi emek ister.** Geçen küçük grubun "kimi şansla, kimi beceriyle" geçiyor.
6. **Önce batmaktan kaçın.** %90 kaybı telafi etmek için %900 kazanman gerekir. Kripto gibi çok oynak varlıklarda büyük kaybı, oyundan atılma riski olarak gör.
7. **"Korkmuş tavşan" (scared rabbit) olma.** Yükselişte alıp dipte satan en kötü sonucu alır. Anlamadığın plana krizde sadık kalamazsın.
8. **Doğrulanamayan bir kayda güvenme (Madoff, 1991).** Her ay kazanan stratejinin opsiyon işlemlerinin yarısı hiçbir borsada gerçekleşmemişti. Kalabalığın ne düşündüğüne değil kanıta bak.

### 1b. Kanıt kontrolü

| İddia | Durum | Dayanak |
|---|---|---|
| Endeksi tutan, aktif grubun ortalamasını yener | ✔ | Sharpe (1991) aritmetiği. SPIVA: 20 yılda fonların ~%93'ü geride (18 §3) |
| ABD hisseleri 200 yıldır ~%10-10,5 kazandırdı | ◐ | 1926 sonrası nominal ~%10 doğru, 200 yıllık reel ~%6,5-7 (Siegel). ABD hayatta kalan piyasa, Nikkei 34 yıl bekledi (18 §2b) |
| Fon "%20'nin biraz altında", 3 zararlı ay, varantta "risksiz %25" | ✔-◐ | Princeton Newport ücret öncesi ~%19,1, ücret sonrası %15,1 (16 §1.7). Zararlı ay sayısı ve %25 kendi beyanı |
| Yayımlanan avantaj erir | ✔ | McLean ve Pontiff: getiri yayından sonra %58 düşüyor (17 §1) |
| -%90 kayıp → +%900 gerekir | ✔ | Aritmetik |
| Korkmuş tavşanın maliyeti | ✔ | Morningstar: yatırımcı kendi fonunun yılda ~1,2 puan gerisinde (18 §3) |
| Madoff'u 1991'de fark etti | ✔-◐ | Dolandırıcılık 2008'de ortaya çıktı ✔. 1991'e ait ayrıntılar kendi anlatımı |

### 1c. Kelly: Thorp'un yazılı görüşü ve senin sayıların

MacLean, Thorp ve Ziemba (2010, *Quantitative Finance*) Kelly'nin iyi ve kötü yanlarını sıralıyor ✔:
- Yarım Kelly, tam Kelly büyümesinin ~%75'ini veriyor. "Yarıya düşmeden önce ikiye katlama" olasılığı %67'den %89'a çıkıyor (blackjack tablosu).
- **2 kat Kelly'de büyüme sıfır.** Kelly'den fazla risk almak hem riski artırır hem büyümeyi azaltır.
- Ortalamayı yanlış tahmin etmek, varyansı yanlış tahmin etmekten çok daha pahalı, bu yüzden bahsi küçült. Sermayeyi korumak isteyenler düşüş büyüdükçe riski sert biçimde azaltır.

**Hesap.** Formül `f* = p − (1−p)/b` (p = isabet, b = kazanç/kayıp oranı). İşlem başına log büyüme `g(f) = p·ln(1+b·f) + (1−p)·ln(1−f)`.
p = 0,40, b = 2 → f* = 0,40 − 0,60/2 = **0,10 (%10)**. EV = +0,20R.

| Risk/işlem | g/işlem | Kelly büyümesinin | 100 işlem sonra medyan | Bir noktada −%20 görme* |
|---|---|---|---|---|
| %10 (tam Kelly) | 0,0097 | %100 | ×2,64 | %80 |
| %5 (yarım) | 0,0073 | %76 | ×2,09 | %51 |
| %2,5 (çeyrek) | 0,0043 | %45 | ×1,54 | %21 |
| %1 (1/10) | 0,0019 | %19 | ×1,21 | ~%1 |

\*Yaklaşık değer, sürekli zaman formülüyle: Kelly'nin c katında P(servetin x'e düşmesi) = x^(2/c−1).

**Tahmin hatası.** 100 işlemde %40 isabetin standart hatası ~4,9 puan. Gerçek isabet %35 ise (EV +0,05R) gerçek Kelly %2,5'tir: "yarım Kelly" sandığın %5 aslında 2 kat Kelly olur, büyüme ~0. "Tam Kelly" %10'da büyüme negatif (−0,0047/işlem): **avantajın pozitifken hesabın küçülür**.

**FTMO'da.** Bu dosya için yapılan simülasyon: +%10 hedef, −%10 statik maksimum zarar, −%5 günlük limit, günde 2 işlem, en fazla 300 işlem.

| Risk | Geçme | Maks. zarardan düşme | Günlük limitten düşme |
|---|---|---|---|
| %10 | %40 | %60 | — |
| %5 | %40 | — | %60 |
| %2,5 | %36 | — | %64 |
| %1 | **%87** | %13 | — |
| %0,5 | %96 | %2 | — (%2 süre doldu) |

Gerçek isabet %35 ise geçme oranı %5 riskte %35'e, %1 riskte %61'e iniyor.

**Yarım Kelly bile neden fazla:**
1. Kelly sınırsız bir kasa varsayar. Prop'ta oyunu bitiren sınırlar var (%10 toplam, %5 günlük). Tam ve yarım Kelly'de ilk kayıp challenge'ı bitiriyor, geçme olasılığı isabet oranına eşitleniyor, avantajın işe yaramıyor.
2. Gerçek kasan hesabın nominal büyüklüğü değil, kaybedebileceğin para (09 §1b). 10.000 $'lık challenge'da bu 1.000 $. Kelly'yi bu 1.000 $'a uygularsan tam Kelly 100 $ (nominalin %1'i), yarım Kelly %0,5 çıkıyor ◐. Kaba bir yaklaşım, ama 01 §7 ve 09 ile uyumlu.
3. Günlük limit kuralı: risk × günlük maksimum işlem sayısı < %5 − tampon (09 §1d). %2,5 riskte iki kayıp limiti doldurmaya yetiyor.
4. Kelly bağımsız işlem varsayar, oysa kayıplar rejimler halinde kümelenir (README #28). Bu da gerçek Kelly'yi düşürür.

### 1d. Perakende trader'a aktarılamayanlar
- 1960-80'lerin varant ve konvertibl piyasası: modeli başka kimse bilmiyordu. Bugün bu hatalar saniyeler içinde kapanıyor.
- Blackjack'te olasılıklar desteden hesaplanabilir. Piyasada isabet ve RR yalnızca tahmindir. Kelly'nin "p'yi biliyorum" varsayımı Thorp için geçerliydi, senin için değil.
- Kurumsal erişim: açığa satış, ucuz finansman, düşük maliyetli icra ve başkasının parası (16 özet 2).

### 1e. Senin için 3 kural
1. **Risk = en küçüğü (%1; alt sınır isabetle hesaplanan Kelly'nin yarısı; (günlük limit − %2) / günlük maksimum işlem).** Örnek: 100 işlemde %40 ölçtün. Alt sınır %35 → Kelly %2,5, yarısı %1,25. Günlük sınır (5−2)/2 = %1,5. Sonuç: risk %1.
2. **Önce küçük parayla gerçek test.** Thorp kitaptan önce sistemi kendi parasıyla denedi. Sıra: replay → demo → en küçük boyut. 100-200 işlem olmadan boyut büyütme (15 §1, README #23).
3. **Düşüşte riski kurala bağlı azalt.** Örneğin hesap −%4'teyken riski yarıya indir, yeni zirvede eski seviyeye dön (09 §1f, README #16).

---

## 2. Jim Simons: Numberphile

**Künye**: `QNznD9hMEh0`, "Jim Simons (full length interview) - Numberphile", Numberphile2, 2015-05-13, 1:00:43, ~1,37 milyon izlenme. Piyasa kısmı ~20 dakika, gerisi matematik ve vakıf.

### 2a. Ana iddialar
1. **İlk iki yıl modelsiz, "normal insanlar gibi" işlem yaptı** (döviz, emtia, finansal vadeli). "Son derece başarılı" oldular, ama ona göre bu "düpedüz şanstı". İş "mide bulandırıcıydı": bir sabah dahi, ertesi sabah aptal gibi hissediyorsun.
2. **Etkin piyasa teorisi "doğru değil".** Fiyat verisinde anomaliler var, örneğin emtialar eskiden trend yapardı. Ama tek bir anomali çok büyük olamaz, olsaydı başkaları da görürdü. Avantaj, **birçok ince anomalinin toplamından** çıkıyor.
3. **Yöntem basit bir döngü**: Öngörücü olabilecek bir fikir bul, uzun geçmiş veride test et. Çalışıyorsa sisteme ekle, çalışmıyorsa at. Tahmin kısmında karmaşık denklemler yok.
4. **Tahmin işin sadece bir parçası.** "Maliyetlerini bilmek zorundasın": büyük emir fiyatı iter. Ayrıca pozisyonların toplam oynaklığını en aza indirmen gerekir. Ona göre işte en önemli matematik becerisi çıkarma: gelirin giderden büyük mü?
5. **Kapasite sınırlı.** Model ancak belirli bir miktarı yönetebiliyor, fazlası piyasayı itiyor.
6. **İşlemlerin %100'ü modelden geliyor.** Kimse "IBM'i alalım" diye işlem açamaz, çünkü modeli geçmiş veride simüle edebilirsin, sezgisel müdahaleyi edemezsin. Modele "dini bağlılık" tek yol.
7. **Giriş bariyeri yüksek.** Yıllardır toplanan dev veri setleri, test yazılımları, ~100 doktoralı, ömür boyu gizlilik sözleşmesi. Finansçı değil bilim insanı alıyorlar, herkes kârdan pay alıyor.
8. **Şansın rolünü küçümsüyoruz.** Başarısız olunca kötü şans deriz, başarılı olunca zekâ. Kendisi "doğru zamanda doğru yerdeydim" diyor.

### 2b. Kanıt kontrolü

| İddia | Durum | Dayanak |
|---|---|---|
| Avantaj ince anomalilerin toplamı | ✔ | Mercer: "Zamanın %50,75'inde haklıyız" (16 §1.6). Grinold'un temel yasası: bilgi oranı ≈ tahmin becerisi × √(bağımsız bahis sayısı) |
| Etkin piyasa teorisi yanlış | ◐ | Anomaliler gerçek (Jensen, Kelly, Pedersen; 17 §1), ama yayından sonra ~%58 eriyor. "Yanlış" olması perakendenin kullanabileceği anlamına gelmez |
| Emtia eskiden trend yapardı | ✔-◐ | Trend takibinin 137 yıllık kanıtı (17 §2). Bilgi tabanında 20 günlük kırılım emtiada 2015 sonrası çalışmıyor (README #22) |
| Maliyet belirleyici | ✔ | Gün içinde maliyet avantajı yer (README #28). İşlem başı avantaj portföy düzeyinde eriyor (README #30) |
| Kapasite sınırlı | ✔ | Medallion dış yatırımcıları çıkardı, ~10 milyar $ sınırı (16 §1.6) |
| Modele sadakat | ✔ | 02 §4b-c: sezgi ve intikam işlemleri lot başı +0,15R'yi +0,01R'ye indiriyor |
| İlk başarı şanstı | ◐ | Kendi beyanı. Zuckerman'a göre erken yıllar oynaktı ve 1989 zararından sonra model yeniden kuruldu (16 §1.6) |

### 2c. Perakende trader'a aktarılamayanlar
- **Genişlik**: Onlarda binlerce enstrüman ve milyonlarca işlem, sende ayda 10-40 işlem var. %50,75 isabetli bir avantajın istatistiksel olarak görünmesi bile yıllar alır.
- **Maliyet**: Kurumsal komisyon ve kendi icra modelleri var. Spread ödeyen perakendede aynı ince avantaj negatife döner.
- **Veri, yazılım, insan ve gizlilik**: Aynı firmanın dışarıya açık fonları bile 2020'de Medallion'un ~95 puan gerisinde kaldı (16 §1.6).

### 2d. Senin için 3 kural
1. **Simons döngüsünü uygula.** Her setup bir hipotezdir: geçmiş veride rastgele girişe karşı test et, verinin iki yarısında tekrarla, tutmuyorsa at (README #19-21).
2. **Kuralı ezme, ezersen etiketle.** Kural dışı her işlemi journal'da "sezgi" diye işaretle, 30 işlem sonra iki grubu R olarak karşılaştır. Sezgi daha iyi değilse bırak.
3. **Önce çıkar.** Her işlemin maliyetini R cinsinden kaydet (spread + komisyon + kayma). Ortalama maliyet beklenen avantajın üçte birini aşıyorsa daha yüksek bir zaman dilimine geç (README #28).

---

## 3. Jack Bogle: The Motley Fool

**Künye**: `MLgn_kVKjCE`, "Jack Bogle on Index Funds, Vanguard, and Investing Advice", The Motley Fool (Tom Gardner ile), yayın 2019-01-17 (Bogle'ın ölümünden bir gün sonra), kayıt ~2016 (Bogle 87 yaşında, ilk endeks fonunun 40. yılı), 51:13, ~2,2 milyon izlenme.

### 3a. Ana iddialar
1. **Yatırımcılar toplamda şirketlerin kazandığını alır, aracının payı düşülerek.** Wall Street ile yatırımcı arasındaki paylaşım sıfır toplamlı. Bogle buna "alçakgönüllü aritmetiğin acımasız kuralları" diyor.
2. **Maliyetin bileşik etkisi.** 50 yılda 1 $ %7 getiriyle ~30 $, yıllık %2 maliyet düşülünce (%5) ~10 $ olur. "Sermayenin %100'ünü koydun, riskin %100'ünü aldın, getirinin %33'ünü aldın." Vanguard'ın gideri ~%0,12, ortalama fonun ~%1,12.
3. **Fon seçerken maliyete bak.** Morningstar bile kendi derecelendirmesinin, fonları maliyete göre sıralamaktan pek iyi olmadığını kabul ediyor.
4. **Satma.** 1976'da ilk endeks fonuna 15.000 $ koyan avukatın payı 40 yılda ~903.000 $ oldu.
5. **Basit kural: tahvil payı = yaş** (ilk yıllarda %100 hisse olabilir). Dengeli fon (60/40) duygulara karşı korur: hisseler %50 düşerken ~%32-33 düşer. Uzun vadede %100 hisse daha çok kazandırır.
6. **Risk oynaklık değil, kalıcı kayıptır.** 1929'dan önce tamamen hisseye giren %90 kaybetti, başa başa dönmesi ~15 yıl sürdü. Ama hiç yatırım yapmazsan sıfır garantidir.
7. **Kısa vadede piyasa bir kumarhane, uzun vadede bileşik getiri makinesi.** "Faaliyet Wall Street'in lanetidir": her işlemde krupiye payını alır.
8. **Bakma.** Emekli olana kadar ekstreni açma. Kadınlar daha az işlem yaptıkları için daha iyi getiri alıyor.

### 3b. Kanıt kontrolü

| İddia | Durum | Dayanak |
|---|---|---|
| Toplam getiri = piyasa getirisi − maliyet | ✔ | Sharpe (1991), SPIVA (18 §3). Pedersen (2018): pasif de işlem yapmak zorunda (yeni ihraç, endeks değişimi), eşitlik tam değil. Veri yine aynı yönde |
| 30 $ - 10 $, "getirinin %33'ü" | ◐ | 1,07^50 = 29,5, 1,05^50 = 11,5 → oran **%39**. Yön doğru, sayı abartılı yuvarlanmış. Sadece gider oranı farkıyla (%1,12'ye karşı %0,12): 27,8 $'a karşı 17,4 $ |
| Maliyet en iyi öngörücü | ✔ | Kinnel (Morningstar, 2010, 2016): her varlık sınıfında en ucuz beşte bir en pahalıdan iyi. Gider oranı yıldızları 40 gözlemin 23'ünde geçti |
| 15.000 $ → 903.000 $ | ✔ | Yılda ~%10,8, S&P 500'ün 1976-2016 toplam getirisiyle uyumlu. Ama bu ABD'nin çok iyi geçen 40 yılı (18 §2b) |
| 1929: %90 kayıp, ~15 yıl | ✔ | 1929-32'de düşüş ~%85-89. Temettü dahil nominal toparlanma ~1944-45 ◐ |
| Faaliyet getiriyi düşürür | ✔ | Barber ve Odean (2000): en çok işlem yapanlar %11,4, piyasa %17,9 (08 §1) |
| Kadınlar daha az işlem yapıp daha iyi getiri alıyor | ✔ | Barber ve Odean (2001): erkekler %45 daha çok işlem yapıyor. İşlem, net getiriyi erkeklerde yılda 2,65, kadınlarda 1,72 puan düşürüyor |
| Bakmamak iyidir | ✔ | Benartzi ve Thaler (1995): miyopik kayıptan kaçınma. Morningstar'ın davranış açığı (18 §3) |

### 3c. Türkiye'deki birine aktarılamayanlar
- **ABD'ye özgü yapılar** (Social Security, 401(k), Vanguard). Türkiye'de TL enflasyonu ve TEFAS'ın yüksek giderleri var. ABD'de kurulu ETF'lerde 60.000 $ üstü ABD veraset vergisi → İrlanda'da kurulu UCITS (18 §5).
- **"Tahvil = yaş"** düşük enflasyonlu ABD tahvili için yazıldı, TL tahvili ya da mevduat aynı rolü oynamayabilir. 1976-2016 dönemi de ABD'nin en iyilerinden biri (tek ülke riski: Nikkei).

### 3d. Senin için 3 kural
1. **İki ayrı kova.** Birikimin çekirdeği otomatik aylık alımla düşük maliyetli küresel endekse. FTMO ve trading önceden belirlenmiş sınırlı bir bütçeyle ayrı dursun, kaybı endeks kovasına dokunmasın (18 §6).
2. **Gider oranı filtresi.** Çekirdek fonun yıllık toplam gideri %0,25'i geçmesin. TEFAS'ta fonun KAP'taki TEG bildirimine bak. %1-3'lük gider 30 yılda servetin ~%30'unu yer (18 §3).
3. **Bakma ve satma.** Endeks kovasını yılda bir dengele, düşüşte satma. Trading'de de kararı tek işleme değil, 20 işlemlik bloklara bakarak ver.

---

## Kaynaklar
- Thorp, Tim Ferriss Show: https://www.youtube.com/watch?v=CNvz91Jyzbg · yazılı transkript: https://tim.blog/2022/05/28/ed-thorp-transcript/ · 2. bölüm: https://tim.blog/2022/06/30/edward-o-thorp-2-transcript/
- Simons, Numberphile: https://www.youtube.com/watch?v=QNznD9hMEh0
- Bogle, The Motley Fool: https://www.youtube.com/watch?v=MLgn_kVKjCE
- MacLean, Thorp, Ziemba (2010), *Good and bad properties of the Kelly criterion*: https://www.stat.berkeley.edu/~aldous/157/Papers/Good_Bad_Kelly.pdf
- Sharpe (1991), *The Arithmetic of Active Management*: https://web.stanford.edu/~wfsharpe/art/active/active.htm · Pedersen (2018), *Sharpening the Arithmetic of Active Management*: https://research-api.cbs.dk/ws/files/60084093/lasse_heje_pedersen_sharpening_the_arithmetic_of_active_management_publishersversion.pdf
- Kinnel (Morningstar, 2016), *Fund Fees Predict Future Success or Failure*: https://www.morningstar.com/funds/fund-fees-predict-future-success-or-failure
- McLean ve Pontiff (2016): 17 §1'deki bağlantı · Barber ve Odean (2001), *Boys Will Be Boys*, QJE 116(1) · Benartzi ve Thaler (1995), *Myopic Loss Aversion*, QJE 110(1) · Siegel, *Stocks for the Long Run*
