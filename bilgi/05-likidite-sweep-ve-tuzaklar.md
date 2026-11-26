# 05 — Likidite, Sweep, Failure Test, Spring (Sahte Kırılımın Anatomisi)

> Güven seviyesi: **ORTA-YÜKSEK** — fenomen (stop kümeleri, sahte kırılım) birçok bağımsız ekolde aynı şekilde tarif ediliyor. Kesin olasılıklar ise **çoğunlukla kanıtsız pratik kurallar**.
> Kaynaklar: Adam Grimes "Trading Patterns 101: The Failure Test" (mVCH9ceqkss) + blog; Al Brooks (brookstradingcourse.com glossary/manual); Wyckoff Analytics; Rubén Villahermosa (tradingwyckoff.com); Tradeciety "stop pocket" videosu (AdA-9SpJWeo); DD Finance likidite/SFP videoları.

## 1. Aynı fikir, beş isim

| Ekol | İsim | Tarif |
|---|---|---|
| Wyckoff (1900'ler) | **Spring** / Shakeout / **Upthrust (UT, UTAD)** | Range dibinin altına iniş → hızla range içine dönüş; "büyük oyuncuların halkı yanıltıp ucuza mal toplaması" |
| Klasik PA (Grimes) | **Failure test** | Seviyenin ötesine "test" → hızla geri dönüş; "bir tür başarısız kırılım" |
| Brooks | **Failed breakout** / trap | Range'de kırılımların çoğu başarısız olur |
| Swing failure | **SFP** | Son swing tepesinin üstüne fitil, üstünde kapanış yok |
| SMC / ICT | **Liquidity sweep / grab / stop hunt** | Eşit tepe/dip üstündeki stopların alınıp dönülmesi |

Villahermosa bunu açıkça yazıyor: Spring = liquidity grab; SOS (Sign of Strength) = CHoCH/MSS. **SMC'nin sweep kavramı Wyckoff'un spring'inin yeniden paketlenmesi.**

## 2. Neden çalışır? (mekanizma)

- Herkesin gördüğü seviyelerin (range uçları, belirgin swing tepe/dipleri, eşit tepeler) ötesinde **stop emirleri kümelenir** (hem zarar-durdur hem kırılım-giriş stopları).
- Fiyat oraya gidince bu stoplar **piyasa emrine dönüşür** → büyük katılımcı için karşı taraf likiditesi oluşur.
- Kırılımın arkasından yeni alıcı/satıcı gelmezse ("kimse takip etmez") fiyat geri döner → kırılımcılar tuzağa düşer → onların stopları ters yönde yakıt olur.
- ⚠️ Bu "market maker seni kişisel olarak avlıyor" demek değil — **likidite arayışı**. (bkz. 11 #6)

## 3. Brooks'un bağlam kuralları (pratik kural, veri değil)

- "**Piyasa range'deyken yukarı ve aşağı kırılımların %80'i başarısız olur.**" (Brooks bunu kendisi "my 80% rule" diye sunuyor; veri seti yayımlanmış değil)
- "Trend dönüş denemelerinin %80'i başarısız olur." → Trendde, trend tersi sweep'ler daha düşük olasılık.
- Range'de: **BLSHS** — dipte al, tepede sat, scalp; **range'in orta üçte birinde işlem açma**.
- "Breakout mode": sıkışık range — kırılım her iki yöne de olabilir; ikinci sinyali bekle.
- "**Failed failure**": başarısız kırılım da başarısız olursa → orijinal kırılım yönünde devam; ikinci sinyal olduğu için daha güvenilir.

## 4. Grimes'ın Failure Test kuralları (en net, en uygulanabilir tanım)

**Giriş:** Bir bar desteğin altına/direncin üstüne gider ve **tekrar içeride kapanır** → kapanışta veya sonraki açılışta gir. İki barlık versiyon: bar dışarıda kapanır, sonraki bar içeride kapanır.

**Bağlam (3 tip):**
1. Range içinde (range ucunda) — en klasik.
2. Kurulu trendde trend extreme'inde → **trend tersi** (agresif).
3. Trend yönünde: karmaşık (iki bacaklı) pullback'in dibindeki pivotta failure test → trend yönlü giriş.

**Kalite kontrol listesi:**
- [ ] **Pivot herkesin gördüğü bir seviye mi?** "Sadece senin bildiğin gizemli seviyenin değeri yok" — stopların orada olmasını istiyorsun. İç (minor) pivotlar değil, **anlamlı** swing'ler.
- [ ] **Seviye gerçekten delindi mi?** Stopları alacak kadar. 50$'lık hissede 2-3 cent değil, 0.5-1$; ES 5dk'da 1-2+ tick.
- [ ] Piyasa gap'li mi? Gap stopun ötesine açılabilir.

**Risk:** Trend tersi failure test'lerde **riski yarıya indir**. Sebep: uzun vadede gap/kayma ile **planlanan riskin 3-5 katı** kayıp kaçınılmaz. Yarım risk ayrıca stop olunca **2. giriş** hakkı verir (iki yarım kayıp = bir normal kayıp) — çoğu failure test önce stopu alıp sonra döner.

**Stop yerleri (3 seçenek):**
1. Önceki extreme'de (en mantıklı).
2. Extreme'in **ötesinde tampon** — Grimes'a göre **en az mantıklı ve en tehlikeli**: "Ne kadar uzak yeterince uzak, bilinemez" + momentumda vurulursa kötü kayma.
3. Extreme'in birkaç tick **içinde** — ince piyasalarda kaymayı önlemek için.
→ Hangisini seçersen seç, **tutarlı ol**.

**Girişten sonra ne görmelisin:**
- ✅ **Fiyat reddi**: hızla seviyeden uzaklaşma.
- ❌ Seviyenin dibinde **sıkışma / sessizleşme** = kötü işaret (seviyeye karşı baskı var, kırılım devam edebilir) → pozisyonu küçült veya scratch et (**zaman stopu**).
- 1-2 inside bar normal, ama kırılımlarına dikkat (LTF üçgen olabilir).

**Kâr:** Bir kısmını **1R**'de al.

**Zaman dilimi:** Günlükte failure test aylarca/yıllarca sürecek tepe/dip yapabilir; 5dk'da daha önemsiz — HTF dönüş noktasıyla örtüşmedikçe. Duygusal, parabolik, 3. itkideki hareketlerin sonunda daha anlamlı.

## 5. Wyckoff Spring / Upthrust detayları

**Spring tipleri (klasik tipoloji, Villahermosa):**
| Tip | Delme | Hacim | Okuma |
|---|---|---|---|
| #1 / Terminal shakeout | Derin | Ani artış, geniş bar | Geri çekmek için güçlü talep gerekir |
| #2 | Orta | Artan | Arz kaldı → ardışık testler beklenir |
| #3 | Hafif | Azalan, dar bar | Klasik okumada testsiz alınabilir |

Villahermosa: **"Hiçbir spring onaysız işlem yapılmaz."** A+ spring: büyük delme + niyetli mumlarla hızlı dönüş + dönüş mumu SOS bar.

**Test (onay):** Spring bölgesine geri dönüş **daralan bar + azalan hacim** ile, spring dibinin **üstünde** kalarak.

**Giriş/Stop:**
- Güçlü spring: dönüş mumunun tepesinin üstüne buy-stop; stop shakeout dibinin altı.
- Zayıf spring: testi bekle, test tetiğinde gir.
- Stop **tam dibe değil** — ikinci bir sweep için pay bırak (Grimes'ın 2. seçeneğiyle çelişiyor; bu bir **tasarım tercihi**, test edilmeli).

**Geçersizlik:**
- Fiyat range **dışında kalıcı** yerleşirse → spring değil, gerçek kırılım.
- Test **yüksek hacim + genişleyen bar** ile gelirse veya shakeout dibinin altında tekrar kapanırsa → işlem yok.
- Geri alım sonrası fiyat range direncine ulaşamıyorsa → spring değil, secondary test.

**UT/UTAD:** Spring'in tersi (range tepesi üstü → içeri dönüş). Wyckoff Analytics: UT bir "boğa tuzağı", ama büyük oyuncular UT'den short açanları da art arda UT'lerle stop edebilir → **Faz D ve LPSY beklemek** çoğu zaman daha güvenli.

## 6. Tradeciety: Stop pocket ve stop run (tepe formasyonu okuma)

1. Güçlü trendde **uyarı işaretleri birikimi**: büyük ters mumlar (önceki trendde görülmemiş oranda), daha alçak tepeler, her alçak tepeden sonra daha sert satış.
2. Destek kırılınca kırılım traderları short açar → stopları kırılım seviyesinin hemen üstünde = **stop pocket**.
3. Fiyat retest ile stop pocket'a gelir. Eğer stoplar tetiklenip yine de yükseliş gelmezse (**alıcı yok**) → arkasından ardışık kırmızı mumlar = **stop run** sonrası devam.
4. **İlk kırılım değil, stop pocket'ın temizlendiği retest** daha güvenli giriş.
> Yorum (en beğenilen): "Stop pocket fikri en çok akılda kalan kısım — ilk kırılımı short etmek yerine retestin kırılımcıların stoplarını temizlemesini beklemek."

## 6b. Tradeciety: "Price action nasıl tahmin edilir" bağlam okuması (d7HVkAvGK_E)

Kontrol listesi (her grafikte sırayla):
1. **Genel trend**: itki ve düzeltme dalgaları nasıl oluşuyor? Düşüş dalgası hızlı ve büyük, yükseliş yavaşsa → aşağı trend baskın. (Brooks'un "always in" fikrine yakın.)
2. **Flip bölgeleri**: eski destek direnç oldu mu (ya da tersi)?
3. **Trend çizgisi yerine önceki tepe/dip kırılımı**: trend çizgileri daha öznel. Bayrakta çizginin kırılmasını değil, **önceki tepenin alınmasını** bekle.
4. **Başarısız devam + ani güçlü ters satış**: yükselen trendde devam kırılımı denenir ama başarısız olur, ardından **o trendde görülmemiş güçte** satış gelir → büyük değişim işareti, özellikle bir **fake-out / liquidity grab** bağlamında.
5. **Tepe ve diplerdeki zayıflık**: piyasa önceki tepeyi almakta zorlanıyor mu? Güçlü kırılım mumundan sonra devam gelmeyip çift tepe oluşuyorsa → duygu değişiyor olabilir.
6. **Uzun yatay faz = birikim**: düşüş trendinde normal düzeltmeden uzun süren yatay hareket. Dirence yaslanan **yükselen dipler** = "pressure pattern" / kırılım birikimi. Bu bağlamda kırılımın devam şansı yüksek.
7. **LVN reddi**: pullback düşük hacim düğümüne (06 §6) girip reddedilirse ve öncesinde zayıflık birikimi varsa → güçlü sinyal.
8. "**Çok erken giren** (FOMO), gerçek ipuçlarını beklemediği için genelde fake-out'larda cezalandırılır." Geç görünen ama teyitli giriş, erken ve teyitsiz girişten iyidir.

## 6c. Tradeciety: "Klasik kırılımı değil, kirli retest'i işle" (7umy17Ng0pQ)

- Rolf'un iddiası: 15 yılın başında klasik kırılım işlemleri iyi çalışıyordu, ama "**son 5-6 yılda** genel kırılımlar o kadar başarılı değil". Bu kişisel gözlem, veri değil. Yine de Brooks'un range'de %80 başarısızlık kuralıyla aynı yönde.
- Formasyon: Kırılım sonrası güçlü mumlarla **stop bölgesine derin bir retest** gelir (kırılımcıların stoplarının olduğu yer). Stop bölgesine değer değmez reddedilir. Son parça **momentum teyidi**: tercihen güçlü bir ters mumla aşağıda kapanış.
- Stop bölgesine giden güçlü mum ve hemen ardından gelen ret, iyi bir retest sinyalinin başlangıcı. Ama **teyit kapanışı gelene kadar erken**.
- Hedef: formasyonun önceki dibi, arz-talep bölgesi ya da hangi hedef aracını kullanıyorsan o.

## 6d. Trader Dante: absorpsiyon, ATR ve "ilk sorun bölgesi" (BX54B-9lHME)

> Eski prop trader. Bund futures 5dk, Market Delta footprint, market profile ve DOM. Yan tarafta FX majörleri, emtia ve endeksler 1 saatlik swing.

**Yaklaşım:** Basit S/R ve kırılım + retest. Swing tepesinin üzerinden momentumla almaya çalışanlar veya bir formasyona girip **tuzağa düşenler** gerçek zamanlı tespit edilir, onlara karşı işlem yapılır. Hedefler: bu trader'ların pozisyondan "kusmaya" (zorla çıkmaya) zorlanacağı ve stoplarının olduğu yerler.

**İpucu 1: Seviyede ne aradığını bil (footprint örneği)**
- "**Kumdaki çizgi**" direnci: tüm tepeler aynı bölgede. Kırılımda alım yapma, **retest'e bid ver**.
- Footprint'te ara: kırılım büyük agresif alım bloklarıyla geldi (683, 350, 700 lot vb.). Fiyat seviyeye yukarıdan geri gelince büyük satış blokları bid'e vuruyor (560, 300 lot), **ama fiyat seviyenin altına inemiyor** → **absorpsiyon** → long.
- Stop dar tutulabilir, çünkü işlem fikri "o kadar büyük satış seviyeyi kıramadı". Kırarsa fikir geçersiz.
- SFP versiyonu: Swing tepesinin üzerine çıkan **fitil büyük blok alımlarıyla** oluştuysa (alıcılar tuzakta) → sadece mum formasyonuna göre **daha yüksek olasılıklı** short.
- Footprint kullanmıyorsan sorun yok. Mesaj şu: seviyede **ne gördüğünde** işlem yapacağını önceden bil (mum formasyonu, 1-2-3 tetiği, ne olursa).

**İpucu 2: Nerede işlem yapacağını bil**
- Her gün önceki kapanıştan **günlük ATR yukarı ve aşağı** işaretlenir. "ATR çok güçlü bir araç." Fiyat ATR'yi aşınca **ortalamaya dönüş** işlemleri aranır, ama **sadece iyi seviyelerle çakışıyorsa**. Sadece ATR olduğu için alım/satım yapılmaz.
- **ATR'nin olabildiğince ötesindeki derin swing noktaları** daha yüksek olasılıklı.
- Market profile: önceki günün **değer alanı tepesi (VAH)** + kırılım gününün **düşük hacim bölgesi / single print'ler** aynı bölgeye denk geliyorsa güçlü bid bölgesi (06 §6). "Fiyat genelde düşük hacim bölgelerini reddeder."
- Önceden belirlenmiş birkaç seviyeye odaklan. Yoksa bütün gün grafiği incelersin ve iyi bölgeye gelindiğinde "beyin ölümü" yaşamış olursun.

**İpucu 3: Yaz** → günlük plan formu (bkz. 03).

**İpucu 4: Kaçırmaktan korkma**
- SFP oluştu: önceki tepenin üzerine çıkış ve altında kapanış. Ama **FTA (first trouble area, ilk sorun bölgesi)**, yani önceki tepeler ve spike öncesi destek, girişe çok yakın → RR yok → **işlem yok**.
- "Piyasa sürekli alıcı ve satıcı arıyor, **reklam veriyor**. Sen trader değil **likidite sağlayıcısısın**. Her güçlü yeşil mumda içeri dalan, TV'de her reklamdaki ürünü alan enayi gibidir." "**Seçici olduğum için para kazanıyorum.**"

**İpucu 5: Korkma (aşağılanma korkusu)**
- Herkes boğa iken short açmak gibi, kalabalığa ters setup'lardan çekinme. "Başkalarının ne düşündüğünü umursayarak kimse para kazanmadı."
- "**En iyi işlemler genelde alması en rahatsız edici olanlardır.** Hiç düşünmeden alınacakmış gibi görünenlerde çok daha fazla sıkıştırıldım."
- Örnek: FTSE'de güzel bir seviye (%61 Fib + önceki dipler). Twitter'da "kesin düşecek" diyen kalabalık var → beklendi. Fiyat seviyenin üstüne çıktı, reddedildi, altına döndü, tekrar yükselmeyi denedi, başarısız oldu → **1 saatlikte bearish outside bar** = sinyal. Stop tepenin üstünde.
- **Hedef mantığı**: "Piyasanın ATR'yi aşacağına kumar oynama. Sırf ben short'tayım diye outside day olacak değil." İlk hedef = günlük ATR sınırı + o bölgedeki önceki swing dibi. Orada gap kapanışı için short açmaya hevesli momentum satıcılarından bir **likidite havuzu** oluşur → onlardan geri al.

**Dante'nin setup'ları (Chat With Traders 39, DpUAgOr0QTU, ~2015).** Bunlar kendi beyanı, hiçbiri test edilmedi:
- "**Piyasa işlem yapılabilecek yere gitmek zorundadır**": Normalden fazla alıcı ve satıcıyı çekmek için hangi seviyeyi test etmeli?
- **Birçok kez test edilmiş dirençte fiyat durup hemen altında sessizce işlem görüyorsa** çoğu kişi "direnç güçlü, momentum bitti" diye short açar. Dante ise bunu genelde alım fırsatı olarak görür. Piyasa o bölgenin üstüne **yoklama** yapıp short'ların stoplarını ve kırılım alıcılarını çeker. "**Yoklama, kırılım değil**": doğru yönü bilenler bile 200 tick'lik kırılım bekleyip tuzağa düşer. Bu yüzden range'in içinde, teyitten önce pozisyon alıyor: "teyit geldiğinde çoğu zaman iş işten geçmiştir."
- **Favori setup'ı**: Pazar akşamı forex açılışında büyük gap. Fiyat gap yönünde patlar ve önemli bir swing tepesini kırar ama üstünde kapanamaz (**müzayede başarısızlığı**, failure test). Ardından gap kapanışına doğru fade. Dante bunun beklentisinin "çok yüksek" olduğunu söylüyor, ama kanıtı yok.
- "**Piyasa meraklıdır**": Yükselmeden önce desteğin altında satıcı var mı diye bakması gerekir. Sweep mantığının sözlü ifadesi (§2).
- **Duyarlılık ve fiyat çelişkisi**: Grafik ve profesyonellerin duyarlılığı çok bearish, ama fiyat aşağı kıramıyorsa long ara, en azından short olma. Örnek: Bund kilit swing dibini geniş bir düşüş günüyle kırdı, ertesi gün devam edemedi.
- Dante Fibonacci de kullanıyor. Grimes'ın testine göre Fib'in tek başına avantajı yok (04, README #9). Bu bir "bağlam seviyesi" olarak kullanılabilir, kanıt değil.

## 7. Likidite = hedef, giriş değil (DD Finance'ın sağlam tespiti)

- Eşit tepeler/dipler (EQH/EQL, "kul") ve yakın zamanlı ilişkili swing'ler (ilişkili likidite) = **hedef** bölgeleri.
- "Sen market maker değilsin" — likidite bölgesine körü körüne limit emirle girmek yerine, sweep **sonrası** yapı değişimi/onay ile gir.
- Yapı yukarıysa hedef yukarıdaki likidite, aşağıysa aşağıdaki.

## 8. SFP (Swing Failure Pattern) — kısa tanım

Fiyat son swing high'ın üstüne **fitil** atar, üstünde **kapanış yok**, geri döner. Tersi dipte. Trend tersi bir işlemdir, güvenli değildir (DD Finance). = Grimes failure test'in tek bar versiyonu.

## 8b. ⚠️ GERÇEK VERİ TESTİ: Filtresiz sweep avantaj göstermiyor (`arastirma/verify_pdh_sweep.py`, `verify_pdh_sweep_byside.py`)

**Test edilen setup**: Fiyat önceki seansın tepesini (PDH) ya da dibini (PDL) deler, sonra ilk bar seviyenin **içinde kapanır** → bu kapanışta ters yöne gir. Stop sweep uç noktası, hedef 1R ve 2R, hedef olmazsa seans sonunda çık. Aynı barda stop ve hedef → önce stop varsayıldı. Brooks'un "**ikinci giriş**" versiyonu da test edildi: ikinci kez dışarı çıkıp ikinci kez içeride kapanınca gir. Brooks'a göre bunun swing yapma ihtimali ~%60.

**Veri**: SPY, QQQ, IWM. 1 saatlik barlarda ~2 yıl (~1.260 sinyal), 5 dakikalık barlarda ~60 gün (~105 sinyal). Sadece normal seans, **maliyet yok**.

| | 1R hedef, karar verilen işlemlerde WR | 2R hedef WR | İşlem başına ortalama R |
|---|---|---|---|
| Rastgele yürüyüş temeli | %50 | %33 | 0 |
| 1 saatlik, ilk giriş (3 ETF) | %43-50 | %21-29 | **-0,13 ile -0,03** |
| 1 saatlik, ilk giriş, tarafa göre (2R) | | | short: -0,19 ile +0,07 / long: -0,06 ile -0,04 |
| 1 saatlik, **ikinci giriş** (Brooks), 2R | | | **-0,09 ile +0,03** |
| 5 dakikalık, ilk giriş (küçük örneklem) | %28-43 | %11-27 | -0,47 ile -0,12 |

**Sonuç:**
1. "Seviyeyi süpür ve içeride kapan, ters yöne gir" **tek başına bir avantaj değil**. Sonuçlar rastgele yürüyüşten ayırt edilemiyor, maliyet eklenince **negatif**. İkinci giriş de mekanik haliyle sıfır civarında. Brooks'un "%60" rakamı bu basit tanımla **desteklenmedi**.
2. Bu, sweep fikrinin yanlış olduğu anlamına gelmiyor. Avantaj varsa, **bağlam filtrelerinden** gelmek zorunda. Bu filtreler de ayrıca test edilmeli:
   - HTF rejimi: range günü mü trend günü mü? (Brooks: "range günü %80 kırılım başarısız" / "trend günü %80 dönüş başarısız", 04 §6b)
   - Sinyal barı kalitesi: güçlü ters gövde, ucuna yakın kapanış.
   - Delme derinliği ve hacim/absorpsiyon (Grimes, Wyckoff spring tipleri, Dante'nin footprint örneği).
   - Günün saati: açılış 18 barlık uçlar (04 §6b-2).
   - Uzun seri/klimaks sonrası (aşırı uzama).
   - HTF seviyesiyle çakışma (07).
3. Kısıtlar: 1 saatlik bar kaba bir çözünürlük, giriş bar kapanışında. Sadece 3 ABD endeks ETF'i. 2024-2026 boğa piyasası rejimi. Daha ince veri ve farklı piyasalarla (forex, altın, NQ futures) tekrarlanmalı. Script hazır, sembol ve aralık değiştirilerek kullanılabilir.
**Filtreli test** (`arastirma/verify_sweep_filters.py`, 3 ETF birlikte, 1.220 sinyal, 2R hedef, maliyetsiz, verinin ilk ve ikinci yarısında ayrı kontrol):

| Grup | N | Ortalama R | 1. yarı | 2. yarı | Yorum |
|---|---|---|---|---|---|
| Tümü | 1.220 | -0,05 | -0,04 | -0,06 | Avantaj yok |
| **Sığ delme** (<0,10 × günlük ATR) | 405 | **-0,14** | -0,20 | -0,09 | **Tutarlı kayıp** (~2,2 standart hata) |
| Derin delme (≥0,10 ATR) | 815 | ~0,00 | +0,05 | -0,04 | Başa baş |
| **Zayıf sinyal barı** | 736 | **-0,09** | -0,09 | -0,09 | **Tutarlı kayıp** |
| Güçlü sinyal barı (gövde ≥%50, uygun %30'luk dilimde kapanış) | 484 | +0,02 | +0,04 | -0,00 | Başa baş |
| Rejime uygun / rejime karşı (50 günlük SMA) | 565 / 655 | -0,03 / -0,06 | | | Anlamlı fark yok |
| İlk saat / sonrası | 792 / 428 | -0,03 / -0,07 | | | Anlamlı fark yok |
| En iyi kombinasyonlar (güçlü bar + herhangi rejim, derin + rejime uygun) | 195-366 | +0,01 ile +0,03 | | | Sıfır, maliyetle negatif |

**Sonuç:**
- Bu çözünürlükte (1 saatlik) ve bu piyasalarda **hiçbir filtre pozitif avantaj yaratmadı**.
- Ama iki filtre **kaybedenleri tutarlı şekilde ayırıyor**: (a) **seviyeyi zar zor delen** sweep'ler (Grimes'ın "seviye gerçekten delindi mi?" sorusu, §4) ve (b) **zayıf sinyal barları** (Brooks'un sinyal barı kalitesi). Bunlar her iki yarıda da negatif. → **Pratik kural**: Sığ delme ya da zayıf sinyal barıyla sweep işlemi alma. Bu tek başına kazandırmaz ama kaybettiren işlemleri eler.
- Çoklu test uyarısı: ~14 grup test edildi. +0,02-0,03'lük "en iyi" gruplar şans eseri olabilir ve yarılar arasında tutarlı değiller. Negatif gruplar ise iki yarıda da tutarlı, bu yüzden güven daha yüksek.
- Sıradaki hipotezler (test edilmedi): daha ince zaman dilimi (5 dakika, uzun veri gerekiyor), HTF seviye çakışması, hacim/absorpsiyon (futures verisi), seans açılışında 18 bar sonrası, forex ve altın.

**Grimes'ın "rastgele seviye" testi** (RandomSRLevels videosu 5mPp7_fajvo + `arastirma/verify_random_levels.py`):
- Grimes'ın deneyi: Fiyatı gizle, grafiğe **rastgele** yatay çizgiler çek, sonra 9 aylık 5 dakikalık veride bu çizgilerin etrafındaki fiyat hareketine bak. "Tick'ine kadar testler", "tutunan seviyeler", "kırılınca gelen volatilite"... hepsi **anlamlı görünüyor**. "Bu seviyelerin piyasa açılmadan önce senin favori tekniğinle hesaplandığını söyleseler inanırdın. Senin seviyelerin rastgele seviyelerden gerçekten daha iyi mi?"
- **Sayısal test**: SPY, QQQ, IWM, 1 saatlik, ~2 yıl. Önceki gün tepe/dibine (açılış önceki günün aralığındayken) ilk dokunuşta: fiyat seviyeden 0,25 × günlük ATR **geri döndü mü**, yoksa önce 0,25 ATR **içinden mi geçti**?

| | Dönüş oranı |
|---|---|
| **Gerçek PDH/PDL** | **%43,7** (429/982) |
| **Rastgele seviyeler** (açılışa aynı uzaklık ölçeğinde) | **%44,6** (450/1.010) |
| Rastgele yürüyüş teorisi | %50 |

- **Sonuç**: Bu piyasalarda ve bu çözünürlükte PDH/PDL **rastgele bir seviyeden daha fazla tepki almıyor**. İki tür seviyede de fiyat dokunduktan sonra dönmekten çok **devam etme** eğiliminde (%50'nin altı, muhtemelen dokunuş anındaki momentum yüzünden). Bu, filtresiz sweep testinin (yukarıda) neden avantaj göstermediğini de açıklıyor. **Seviyenin kendisi sihirli değil.**
- ⚠️ Kısıtlar: 1 saatlik barlar, tek eşik (0,25 ATR), sadece ilk dokunuş, 3 ABD ETF'i. Başka seviye tipleri (haftalık uçlar, hacim profili POC/VAH, HTF swing'ler) ve başka piyasalar test edilmedi. Aynı script bu testlere uyarlanabilir.
- **Bu bilgi tabanı için anlamı**: Bir seviye tipine işlem yapacaksan, önce **"benim seviyelerim rastgele seviyelerden daha iyi tepki alıyor mu?"** testini yap. Replay uygulamana bir "rastgele seviye" modu ekle: kör çizilmiş çizgilerle aynı setup'ı işle ve sonuçları karşılaştır.

4. **Ders (Grimes, 14 §6)**: "Sweep" ile kazanıyorsan, kazancın gerçekten sweep'ten mi yoksa farkında olmadan kullandığın başka bir filtreden mi (bağlam, saat, seviye kalitesi) geldiğini bilmelisin. Replay'de her sweep işlemine bu filtreleri **etiket olarak** yaz ve hangi etiketin EV'yi taşıdığını ölç.


**✔ 42. tur: Dante'nin SFP tanımıyla filtresiz test** (`arastirma/verify_sfp.py`).
- **Kurgu**: 1 saatlik veri, ~2 yıl, 9 piyasa (EURUSD, GBPUSD, USDJPY, ES, NQ, altın, petrol, ZN, BTC).
- **Salınım noktası**: ±5 barın en yüksek ya da en düşük değeri.
- **SFP**: en son alınmamış salınım noktası kırılıyor ve bar onun gerisinde kapanıyor.
- **İşlem kuralları**: SFP barının kapanışında giriş, stop barın uç noktasının ötesinde, hedef 2R, en fazla 48 bar. Maliyet yok.

| | Ortalama R | İsabet | n |
|---|---|---|---|
| **SFP (filtresiz)** | **-0,028** | %33 | 3.731 |
| Rastgele bar, aynı yön ve aynı stop mesafesi | -0,005 | ~%34 | — |
| Fark | -0,023 (se 0,032) | | |
| "Derin" salınımlarda SFP (salınım ≥ 3 ATR) | +0,011 | | 802 |
| "Sığ" salınımlarda SFP | -0,039 | | 2.929 |

- **Filtresiz SFP'nin avantajı yok.** Rastgele girişten ayırt edilemiyor, maliyetle birlikte negatif. Bu, endekslerdeki PDH/PDL süpürme bulgusunun (yukarıda) forex, emtia, tahvil ve kriptoda tekrarı.
- Dante'nin kendisi de "Herkes her SFP'yi işliyor, **seçici olmalısın**" diyor. Bu test onun haklı olduğunu gösteriyor: avantaj varsa formasyonda değil, filtrede ve bağlamda (Dante'nin bias'ı, HTF seviyesi, zaman).
- Daha uzun salınımlarda biraz daha iyi (+0,01'e karşı -0,04). Fark anlamlı değil, ama yön Dante'nin "uzun salınım daha önemli" görüşüyle uyumlu.
- **Senin için sonuç**: süpürme ya da SFP tek başına bir giriş sinyali değildir. Filtreni (bağlam, seviye, saat) replay'de kör olarak kaydet ve bu temel çizgiyle karşılaştır (13 §5).

## 8c. ✔ "Seviyeye sert gelen tutunur, sürüklenen kırar" ("drift of death") testi (Trader Dante, NDkE6RHke9U)

**İddia**: "Seviyeler, fiyat onlara agresif gelirse çok daha büyük olasılıkla tutunur. Yavaş sürüklenerek gelirse kırılır. Sezgiye tamamen ters, kendin test et." (Asya seansındaki sürüklenme hariç.) Gerekçe: hızlı düşüşte boğalar emirlerini çeker, yavaş düşüşte yeni trader'lar "momentum bitti" deyip önüne geçer.

**Test** (`arastirma/verify_dante_drift.py`, 1 saatlik, 730 gün, 4 parite ve 4 vadeli, Asya saatleri hariç): Seviye önceki günün dibi ve tepesi, günün ilk dokunuşu. Yaklaşma hızı, dokunuştan önceki 4 barda katedilen mesafe (ATR cinsinden). Sonuç: fiyat seviyeden 1 ATR uzaklaşıyor mu (tutundu), yoksa 1 ATR içeri mi giriyor? Kontrol: aynı uzaklıkta rastgele seviyeler.

| Seviye | Yavaş (sürüklenme) | Orta | Hızlı |
|---|---|---|---|
| Önceki gün tepe/dibi (n=2.438) | **%52,9** | %51,8 | **%42,6** |
| Rastgele seviye (n=2.184) | %53,6 | %51,5 | %46,2 |

- **İddianın tersi çıktı**: hızlı gelen fiyat seviyeyi daha sık **kırıyor** (−10 puan, ~4 standart hata). 8 sembolün 7'sinde aynı yön, sadece petrolde ters.
- **Etkinin çoğu rastgele seviyelerde de var** (−7 puan). Yani bu bir "seviye" özelliği değil, 1 saatlik ölçekte genel bir kısa vadeli momentum: hızlı hareket biraz daha devam etme eğiliminde.
- Dante'nin örneklerindeki gibi 1 tick'lik SFP'ler ve hacim okuması bu basit testte yok. Ama "sert gelen tutunur" kuralı tek başına kullanılırsa veride ters çalışıyor.
- **Senin için**: bu, "kendin test et" denen bir iddianın testte ters çıkabileceğine iyi bir örnek. Replay uygulamasında yaklaşma hızını otomatik etiketleyip kendi işlemlerinde de ölç (13 §5).
## 9. Sentez — test edilebilir bir "sweep setup" tanımı

```
BAĞLAM: HTF'de range (veya trend extreme + aşırı uzama/3. itki)
SEVİYE: Herkesin göreceği swing / range ucu / eşit tepe-dip (minor pivot değil)
TETİK:  Bar seviyeyi en az X (ATR'nin %Y'si) deler VE seviyenin içinde kapanır
        (opsiyon: 2 bar versiyonu; opsiyon: LTF'de MSS/CHoCH onayı)
HACİM (opsiyon): Sweep barında yüksek hacim + kapanış barın ortası/üstü = absorpsiyon
GİRİŞ:  Kapanışta / sonraki açılışta / LTF onayında
STOP:   Sweep extreme'i (tutarlı tek kural seç: extreme / extreme+tampon / extreme−birkaç tick)
RİSK:   Trend tersi ise normal riskin 1/2'si; 1 tekrar giriş hakkı
HEDEF:  Kısmi 1R; kalan range ortası (EQ) → karşı uç / karşı likidite
ZAMAN STOPU: N bar içinde ret yoksa (seviyede sıkışma) çık
GEÇERSİZ: Range dışında kabul (ardışık kapanış), test yüksek hacim+geniş bar
```
→ Bu tanımı replay/backtest ile **100+ örnekte** R olarak ölç. Brooks'un %80'i, Villahermosa'nın eşikleri vb. **senin piyasanda/zaman diliminde** doğrulanmadan kabul edilmez.
