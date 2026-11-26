# 03 — İşlem Planı (Trading Plan) Şablonu

> Güven seviyesi: **YÜKSEK** (konsensüs + mantık). Kaynak: AlgoCoinism "İyi Bir İşlem Planı Nasıl Hazırlanır?" (0YOD3MwxONY), Lance Beggs / Brooks yaklaşımlarıyla tutarlı.

İşlem planı = işleme girmeden **sakin kafayla** yazılmış cevap listesi. Plan hazırsa işlem sırasında karar vermezsin, sadece uygularsın.

## Dört soru

1. **Neden giriyorum?** → His değil, **kontrol edilebilir şartlar** listesi. Hepsi varsa giriş; biri eksikse işlem yok.
   - Örnek: (a) fiyat HTF destek bölgesinde, (b) o seviyede alt fitilli mum kapandı (red), (c) üst zaman diliminde yön aşağı değil.
2. **Nerede yanılmış olurum?** → Stop = fikrin geçersiz olduğu yer. **İlk karar stop, sonra giriş.**
3. **Ne kadar riske ediyorum?** → Sabit % risk → lot hesabı (bkz. 02).
4. **Ne zaman HİÇ işlem açmam?** (en az konuşulan, en önemli kısım)

## Giriş tipi (plana yaz)

- **Limit emir**: fiyatı sen seçersin, daha iyi RR, ama onay mumunu beklemeden girersin.
- **Kapanış + market emir**: daha fazla onay, ama fiyat uzaklaşmış olabilir.
- **Stop emir (kırılım girişi)**: momentum teyidi, ama sahte kırılım riski.

## Hedef

- Tahmini sayı değil, grafikte fiyatın karşılaşacağı **sonraki seviye** (direnç, likidite havuzu, HVN, range ucu).
- Kural önerisi: hedef stop mesafesinin **en az 1.5 katı** değilse işlem yok (maliyetler dahil düşün).
- **Ama R/R'yi piyasaya dayatma** (Dante, CWT 39): "Bu işlem sadece 1:1, bana 2:1 öğretildi. Stopu sıkılaştırayım ya da hedefi büyüteyim." Bu, piyasa yapısını yok saymaktır: "**Piyasa senin R/R'ini umursamaz.**" Stop yapının ötesine, hedef bir sonraki seviyeye konur. R/R bu ikisinden **çıkar**, uygun değilse işlem alınmaz. Avantaj = R/R ve isabet oranı birlikte (01). Dante yüksek isabetle 1:1'i, hatta 0,9R'yi kabul ediyor. Ama yüksek isabet iddiası günlükle kanıtlanmalı.
- **Girişte karar ver: bu işlem koşturulacak mı, yoksa seviyeden seviyeye mi?** (Dante) İki işlem tipi var. (a) Üst zaman diliminde büyük hareket için hazır bir piyasa: alt zaman diliminde gir, gün boyu ya da daha uzun taşı. (b) Gün içi bir seviyeden sonrakine. Yönetim zorluğunun çoğu, nereye gideceğine dair beklenti olmadan girmekten kaynaklanır.

## İşlem açmama koşulları (kontrol listesi)

- [ ] Fiyat range'in **ortasında** (ne destek ne direnç; yanılma noktası belirsiz)
- [ ] Stop çok uzak (lot çok küçülür ya da hedef gerçekçi olmaz)
- [ ] RR < 1.5
- [ ] Yön belirsiz / grafik karışık
- [ ] Günlük kayıp limitine ulaşıldı
- [ ] Giriş kaçırıldı — fiyat gitti, aynı stopla girmek RR'yi bozar → **peşinden koşma**
- [ ] Yüksek etkili haber yaklaşıyor (plana göre)
- [ ] Duygusal durum kötü (intikam, sıkıntı, yorgunluk)

## Stop yönetimi

- Zarar yönünde **asla** taşınmaz.
- Kâr yönünde taşıma (breakeven, trailing) kuralları **önceden** yazılır. (Not: erken breakeven'a çekmek WR'ı artırıp ortalama kazancı düşürür — bunu da backtest et.)

## Pozisyon yönetimi: Brandt'ın kuralları ve acemi hataları (TraderLion 2025)

"**Seni trader yapan giriş değil, çıkış emirleridir.** Setup bir çift buz pateni gibidir. Kaymayı bilmiyorsan işe yaramaz."

**Brandt'ın yönetimi:**
- **Piramit (pozisyona ekleme) yok.** En büyük pozisyon her zaman ilk giriştir. Long'da piramit ortalama maliyeti yükseltir ve geri çekilmelere karşı kırılganlaştırır. (Bu Brandt'ın tercihi. Bazı başarılı traderlar ekleme yapıyor, ama acemi için risk.)
- **Asimetri fırsatı**: Büyük formasyonun sonunda küçük bir "fırlatma formasyonu" oluşursa → boyut **küçük formasyonun riskine**, hedef **büyük formasyonun potansiyeline** göre hesaplanır.
- Hedefin ~**%70**'ine gelince (özellikle retest olduysa) pozisyonun **yarısına kadar** kâr alınır. Kalan yarı **8 günlük hareketli ortalama** ile takip edilir: 8 günlüğün altında tam bir bar + ertesi gün devam. 2x hedefe 4-5 günde ulaşılırsa kâr alınır.
- Zararlı işlemlerden ortalama **1 hafta içinde** çıkılır. Kârlılar ortalama ~2 hafta tutulur, bazıları 2-3 ay.

**Acemilerin pozisyon yönetimi hataları (Brandt'ın topluluğundan):**
1. **Kırılımı önceden tahmin etmek**: Range içinde, kırılımdan önce, 2-3 günlük bir rallide almak → stop ol, tekrar dene, tekrar stop ol → gerçek kırılım geldiğinde yorgun düşüp kaçırmak. "Range'de işlem yapacaksan dibinden al." Kırılımı da sonra alabilirsin.
2. **Stopu çok erken başa başa çekmek**: 8 kayıptan sonra 1-2 günlük kârı korumak için stopu başa başa çekmek. Başa baş fiyatı formasyon sınırının **üstündedir**, retest'e yer bırakmaz → stop ol → piyasa yeni zirve yapar → "boğa piyasasında haklıyken para kaybetmek".
3. Bir hafta iyi gidip çıkmak, sonra fiyat devam edince tekrar atlamak ve stop olmak → hareketin büyüklüğünden faydalanamamak.
4. **Anlatıya kilitlenmek** ("altında sadece long olunur").
5. **Aşırı işlem yapmak ve aşırı risk** (%5-15).
- Brandt ve Dante'nin ortak gözlemi: "Tetiği çekmesi en kolay, en rahat hissettiren işlemler genelde **en kötü performansı** gösteriyor." Hiç beklentisi olmadığı piyasalar ise sürpriz kazançlar getiriyor.

### Brandt'ın 3 günlük trailing stop kuralı ve "seçim mi yönetim mi?" testi

**Kural** (Diary of a Professional Commodity Trader'dan, ChartWizards -WaAMAEAjOs):
1. Hareketin **en yüksek gününü** belirle (short'ta en düşük gün).
2. Sonraki bir gün o günün **dibinin altında kapanırsa**, stopu bu kapanış gününün dibinin hemen altına çek.
3. Yeni bir en yüksek gün oluşursa süreç baştan başlar.

Kural tamamen fiyata dayalı, öznel değil. Brandt bunu "son gün kuralı" (ilk stop) ile birlikte kullanıyor.

**Brandt'ın iddiası** (TraderLion, R1sNTB2Vh7w): "İşlem seçimi bir trader'ın avantajının belki %5-10'u. Oyun işlem yönetiminde ve risk yönetiminde oynanır."

**Test** (`arastirma/verify_brandt_exits.py`, günlük, 2005+, maliyetsiz). Tüm girişlerde ilk stop 1 ATR, gap'te açılış fiyatından çıkış.
| Grup | Giriş | Sabit 2R hedef / 20 gün | **Brandt 3 günlük trailing** | 10 günlük dip trailing |
|---|---|---|---|---|
| Emtia ETF'leri | 20 günlük kırılım | +0,04R | **+0,13R** (PF 1,20) | +0,10R |
| Emtia ETF'leri | **Rastgele gün, rastgele yön** | +0,04R | **+0,11R** | **+0,16R** |
| Endeks ETF'leri | 20 günlük kırılım | -0,04R | -0,09R | -0,12R |
| Endeks ETF'leri | Rastgele | -0,06R | -0,04R | -0,08R |
| Majör pariteler | 20 günlük kırılım | -0,06R | -0,06R | 0,00R |
| Majör pariteler | Rastgele | -0,08R | -0,09R | -0,01R |

**Sonuç:**
1. **Trend yapan piyasada (emtia) Brandt haklı.** Trailing stop'la "kazananı koşturmak", sabit hedefe göre sonucu 3-4 katına çıkarıyor. **Rastgele yönlü girişler bile** kırılım girişleri kadar iyi. Bu basit testte giriş seçiminin katkısı ~0. Avantaj çıkıştan, yani trendin kalın kuyruğunu tutmaktan geliyor.
2. **Ortalamaya dönen piyasada (hisse endeksleri) tersi geçerli.** Trailing stop sonucu kötüleştiriyor. Sabit hedef daha az kötü, ama burada kırılım girişi de rastgele giriş de negatif. Endekste işe yarayan, düşüşü almak (04 §5b).
3. **"Kârı koştur" evrensel bir kural değil, piyasanın karakterine bağlı.** Çıkış yöntemini piyasaya göre seç ve test et. Aynı sonuç 12'deki kırılım bulgusunda da çıkmıştı.
4. **Sağlamlık kontrolü** (18. tur, `arastirma/verify_trailing_robustness.py`). Rastgele yönlü girişler, 5 farklı rastgele tohumla tekrarlandı.
   - **Emtia ETF'leri**: sabit 2R -0,03R, Brandt trailing +0,06R (se 0,017), 10 günlük dip +0,08R. Trailing **12 sembolün 12'sinde** sabit hedeften iyi, iki dönemde de pozitif.
   - **Emtia futures** (12 kontrat, vade geçişi gap'i olan 387/16.700 işlem çıkarıldı): sabit -0,03R, Brandt trailing +0,03R (se 0,015), 12 kontratın 9'unda daha iyi. Fark daha küçük ve 2005-14 döneminde ~0.
   - Bulgunun yönü sağlam. Büyüklüğü ise 17. turdaki tek tohumlu sonuçtan küçük (+0,11R yerine +0,03 ile +0,06R). Bu, çok sayıda rastgele tekrarın neden gerekli olduğunu gösteriyor. Doğal gaz, mısır, buğday, kakao ve sığır gibi sert dönüş yapan piyasalarda trailing de negatif.
5. **Sınırlamalar**: 20 günlük kırılım, Brandt'ın seçici yatay formasyonlarının (önce haftalık, %8-15 genişlik) kaba bir temsilcisi. Testte maliyet yok. Emtia ETF'lerinde gap'ler nedeniyle -13R'ye varan kayıplar var, bu yüzden "en kötü kayıp" sınırı için büyük gap riski olan araçlarda boyutu küçült.


**Brandt'ın erken çıkış kuralları** (Words of Rizdom, 02tMCQLFIjg):
- **İddia**: "İşlemlerimin %15'i kârın %85'ini getiriyor. Bu büyük kazananlar hemen çalıştı ve geri dönmedi. Onlardan herhangi bir zararlı kapanışta çıksaydım çok kaybetmezdim. Kaybedenlere aynısını yapınca toplam sonuç tamamen değişiyor."
- **Kuralları**:
  - "Cuma öğleden sonra zarardaki pozisyonu hafta sonuna taşımayız."
  - "Bir işlem stopa değmeden iki gün üst üste zarardaysa keser kaçarız."

**Test** (`arastirma/verify_brandt_early_exit.py`):
- **Kurgu**: 20 günlük kapanış kırılımı ve rastgele yönlü girişler. Brandt 3 günlük trailing stop, 1 ATR ilk stop. Günlük veri, 2005+, maliyetsiz.
- **Hücreler**: işlem başına fark (R) / büyük kazananlardan (en iyi %15) ne kadarının erken kesildiği.

| Filtre | Emtia ETF kırılımı | Emtia vadeli kırılımı |
|---|---|---|
| Temel (filtre yok) | +0,073R | +0,075R |
| İlk zararlı kapanışta çık | **-0,030** / %30 | -0,019 / %31 |
| İki ardışık zararlı kapanışta çık | -0,001 / %8 | -0,009 / %10 |
| Cuma günü zarardaysa çık | -0,009 / %9 | +0,001 / %9 |

- **Mekanik kırılımlarda desteklenmedi.** İlk zararlı kapanışta çıkmak büyük kazananların **%30'unu** kesiyor ve sonucu kötüleştiriyor. İki gün ve Cuma kuralları ise nötr: zarar da yok fayda da.
- Pareto kısmı doğru, hatta daha uç: en iyi %15'lik işlem net kârın ~%800'ünü getiriyor, geri kalanı toplamda zararda (12, 03).
- **Brandt'ın girişleri seçici klasik formasyonlar**: yatay sınırlı, %15'ten dar, 6-26 haftalık yapılar. Onun işlemlerinde kazananlar gerçekten "hemen çalışıyor" olabilir. Bu tür bir kuralı benimsemeden önce **kendi işlem kaydında** "hiç zararlı kapanışı olmayan kazanan oranı"nı ölç.
- Hafta sonu kuralı prop için ayrıca anlamlı: FTMO Standard hesapta hafta sonu pozisyon zaten yasak (09 §4i).

**Brandt'ın kendi kırılım kuralları ve mekanik test** (Chat With Traders, bIi6YzPt9bE; `arastirma/verify_brandt_box.py`):
- **Kurallar**:
  - Haftalık grafikte **yatay** formasyon: dikdörtgen ya da dik açılı üçgen. Çapraz çizgili formasyonlar (kanal, simetrik üçgen, kama) yok.
  - Süre **8-14 hafta**, genişlik fiyatın **%15'i** içinde.
  - 14 günlük **ADX 12'nin altında**, 10'a yakın (sıkışma).
  - Giriş: sınırın **30 günlük ATR'nin yarısı** kadar ötesine buy-stop emri, karşılığında otomatik stop emri.
  - İlk stop: kırılım gününün dibi ("son gün kuralı").
  - Pozisyonu **8 günlük ortalama** ile yönetiyor: "Gümüş 40'tan 120'ye 8 günlük ortalamayı kırmadan gitti."
  - Risk her işlemde **%0,6-0,7**, tek seferde girer, piramit yok. 1-2 hafta içinde kısmi kâr alır.
  - "**Dikdörtgende avantaj yoktur.** Grafik sadece riskin tanımlandığı yeri gösterir. Avantajım risk yönetiminden, duygu yönetiminden ve süreçten gelir."
- **Test kurgusu**: günlük veri, 2005+, maliyetsiz. Kutu = son 60 günün tepe ve dibi. Çıkış 8 günlük ortalamanın gerisinde kapanış ya da stop. Tablodaki değerler işlem başına ortalama R ve standart hatası (se).

| Grup | Tam kurallar (genişlik ≤%15, ADX<15) | Filtresiz 60 günlük kırılım | Rastgele giriş, aynı çıkış |
|---|---|---|---|
| Emtia vadelileri | +0,63 (se 0,25, n=180) | +0,30 (se 0,07) | +0,07 |
| Majör pariteler | -0,10 | -0,01 | +0,02 |
| Endeks ETF'leri | +0,13 | -0,05 | **+0,17** |
| Emtia, vade geçişi boşlukları çıkarılmış, **2015+** | +0,11 (se 0,22, n=89) | **+0,16** (se 0,09) | +0,07 |

**Sonuçlar:**
1. **Brandt'ın sözü veriyle uyumlu: formasyonun kendisinde sağlam bir avantaj yok.** Sıkışma filtreleri (ADX, genişlik) tüm dönemde ortalamayı artırıyor gibi görünüyor, ama bu küçük bir 2005-14 örnekleminden geliyor (n=41, se 0,64). 2015 sonrasında filtresiz kırılımdan iyi değil.
2. **Piyasa her şeyi belirliyor.**
   - Emtiada kırılım ve trailing çıkış pozitif, rastgele girişten ~+0,1R iyi. Bu fark iki dönemde de var ama gürültü sınırında.
   - Paritelerde sonuç sıfır. Endekslerde kırılım rastgeleden kötü.
   - 17. ve 18. turlarla ve 12'deki "piyasalar farklıdır" bulgusuyla tutarlı.
3. **Kârın kaynağı kuyruk**: brüt kazancın %75-85'i işlemlerin en iyi %15'inden geliyor. Brandt'ın "15/85" gözlemiyle aynı.
4. **Prop için**:
   - Bu tarz (haftalarca tutulan emtia kırılımları) **Swing hesap** gerektirir (09 §4i).
   - İşlem sıklığı düşük (Brandt'ta yılda 125-150).
   - Dar stop (kırılım günü dibi) R'yi büyütür, ama gerçek maliyet ve kayma bu R'nin önemli bir kısmını yer. Testte maliyet yok.
### "Her şeyi 1R'de al" (Grimes, Desire To TRADE ZHoPjGvQk4Y) ve test

**Grimes'ın iddiası**:
- "Kendi işlemlerimi elle ~200 saat inceledim. Her şeyi **1R hedefte** almak, trailing stop'larımdan hem **daha düzgün bir sermaye eğrisi** hem de **daha fazla para** verdi. 2R daha iyi değildi."
- S&P gün içi işlemlerinde riski hedefin 3 katıydı. Gün içi bir formasyonda 0,5R hedef iyi çalıştı.
- "Herkesin söylediği 1:5 oran bana hiçbir anlam ifade etmiyor."

**Hızlı formasyon testi** (Grimes):
- Formasyonu 1:1 stop ve hedefle sisteme dök. Hedef **%50'den sık** vuruluyorsa avantaj var.
- Ama karşılaştırma %50 ile değil, "**boş ya da eğilim olasılığı**" ile yapılmalı: aynı oranlarla rastgele girişte isabet.
- **RR ile isabet birbirinden ayrılamaz.** Hedefi küçültürsen isabet kendiliğinden artar.
- Formasyonların bir **tahmin ufku** vardır. 5 barlık küçük bir formasyonu haftalık stoplarla işlersen sinyal gürültüye dönüşür.

**✔ Test** (`arastirma/verify_grimes_targets.py`):
- **Kurgu**: momentum sonrası ilk pullback sinyalleri, 21 endeks ve ülke ETF'i ile 30 hisse, günlük, 2005+, maliyetsiz, ilk stop 1 ATR.
- **Temel çizgi**: aynı yönde rastgele trend günü girişi.

| Endeks ETF'leri, long | Pullback: ortalama R / isabet / ortalama÷std | Rastgele trend günü: ortalama R / isabet | Fark | Fark 2015+ |
|---|---|---|---|---|
| Hedef 0,5R | -0,003 / %66 / -0,004 | -0,015 / %66 | +0,01 | -0,03 |
| **Hedef 1R** | +0,130 / **%56** / +0,131 | +0,059 / **%53** | +0,07 (se 0,03) | **+0,02** |
| Hedef 2R | **+0,223** / %41 / **+0,151** | +0,131 / %38 | +0,09 | +0,04 |
| Brandt 3 gün trailing | +0,195 / %36 / +0,093 | +0,028 / %34 | +0,17 | +0,09 |
| 10 gün trailing | +0,188 / %27 / +0,067 | +0,042 / %26 | +0,15 | +0,11 |

30 hissede (long) de aynı tablo:
- 1R: +0,116, ortalama÷std 0,117.
- 2R: +0,188 / 0,129.
- 10 günlük trailing: +0,313 / 0,103.

**Sonuçlar:**
1. ✔ **RR ve isabet iç içe**: hedef 0,5R'de %66, 1R'de %56, 2R'de %41, trailing'de %27-36.
2. ✔ **Hisselerde "boş olasılık" %50 değil, ~%53** (yukarı eğilim). Pullback'in 1:1 isabeti %56, yani fark sadece +3 puan. Grimes'ın "eğilim olasılığı" kavramı doğru ve gerekli.
3. ✘ **"1R en iyisi" bu mekanik versiyonda desteklenmedi.**
   - 1R, trailing'den daha düzgün (işlem başına ortalama÷std 0,13'e karşı 0,07-0,09), bu kısım doğru.
   - Ama 2R hem daha çok kazandırıyor hem daha düzgün.
   - Trailing işlemleri çok daha uzun sürüyor. Zaman başına getiri ölçülmedi, kısa hedefler sermayeyi daha az bağlar.
   - Grimes'ın bulgusu kendi takdirli girişleri ve trailing tarzıyla ilgili, bu test onu birebir ölçmüyor.
4. ⚠️ **2015 sonrasında pullback'in rastgele girişe üstünlüğü hedefli çıkışlarda ~0** (+0,02 ve +0,04). Bu, zaman bazlı testle aynı sonuç (04 §5b).
5. **Pratik**: Çıkış seçimi piyasa karakterine göre yapılır (yukarıdaki Brandt testi). Kendi işlem kaydında Grimes'ın yaptığı **"aynı girişler, farklı çıkış" pro forma analizini** yap (13 §5 madde 10). İsabeti her zaman aynı RR'deki rastgele girişin isabetiyle karşılaştır.

### Kademeli kâr alma (scale out) ve test (Trader Dante, "Should I Scale Out Of Trades?", CDOuxZTsq5o)

**Dante**: "Kademeli çıkmıyorum. Çoğu trader için matematiksel olarak sağlam olmayan bir hamle, P&L'yi işlemek. Hedefin 50 tick ise neden 10, 20, 25'te parça satıyorsun? Kimse kaybedenden kademeli çıkmıyor. Kademeli çıkış iyiyse neden zararda da yapmıyorsun? Rahat hissettiren şey bu oyunda işe yaramaz. Kendi günlüğünle test et."

**Test** (`arastirma/verify_scale_out.py`, aynı girişler farklı çıkışlar, 1R = 1 ATR, maliyetsiz):

| Giriş seti | Tamamı 2R'de | 1/3'ü 0,5R, 1R, 2R'de | + zararda 1/3'ü -0,5R'de kes | Trailing (10 gün dibi) | Yarısı 2R'de + trailing |
|---|---|---|---|---|---|
| RSI-2 endeks long (n=793) | +0,100R (sd 1,44) | +0,058R (sd 0,92) | **+0,007R** | +0,296R (sd 2,77) | +0,199R (sd 1,91) |
| Emtia 20 günlük kırılım (n=2.905) | +0,071R (sd 1,41) | +0,033R (sd 0,92) | **0,000R** | +0,185R (sd 3,06) | +0,128R (sd 1,99) |
| Rastgele giriş (n=832) | -0,04R | -0,05R | -0,08R | -0,03R | -0,04R |

- **Avantajlı iki girişte kademeli çıkış beklentiyi yaklaşık yarıya indiriyor.** Oynaklığı da ~%36 azaltıyor, ama ortalama/oynaklık oranı iyileşmiyor (0,070'e karşı 0,063; 0,051'e karşı 0,036). Aynı oynaklık azalmasını, sağ kuyruktan vazgeçmeden **daha küçük boyutla** da elde edersin.
- **Zararda da kademeli çıkmak avantajı tamamen siliyor** (+0,007R ve 0,000R). Dante'nin simetri argümanı doğru: bu, pozisyonun bir kısmına daha sıkı stop koymakla aynı şey.
- **Rastgele girişte hiçbir çıkış avantaj yaratmıyor** (Grimes, 10 §6l).
- Bu iki avantajda kârın büyük kısmı kuyruktan geliyor. Trailing ve "yarısı hedefte, yarısı trailing" en iyi oran. RSI-2'de trailing'in yüksek sonucu kısmen endeksin yukarı yönünden geliyor (10 §6o).
- ⚠️ Günlük barlarla yaklaşık test. Aynı barda stop ve hedef görüldüğünde yazı-tura kullanıldı; bu, yakın hedefleri biraz cezalandırır. Maliyet eklenmedi; gerçekte kademeli çıkış komisyonu artırır.
- **Pratik**: kademeli çıkışı rahatlık için değil, kendi kaydında "aynı girişler, farklı çıkış" karşılaştırmasıyla kanıtlarsan kullan. Replay uygulamasındaki çıkış karşılaştırma modu tam bunun için (13 §5 madde 10). Holden'ın "kısmi kâr beyni geri çekilme moduna sokar" gözlemiyle de uyumlu (13 §3e).

## İşlem sonrası

- "Plana uydum mu?" → evet/hayır. Kazanç/kayıp ikincil.
- Ekran görüntüsü (giriş + çıkış), R sonucu, setup etiketi, duygu notu → günlüğe (bkz. 10).
- 1 ay aynı kurallarla işlem yap → sonra değerlendir: hangi koşulda plana uyamadın, hangi kuralı çiğnedin?

## Plan = kazanç garantisi değil

İyi planlanmış işlem de kaybeder. Plan sadece **kaybın ne kadar olacağını önceden bilmeni** ve duygusal kararları engellemeyi sağlar.

## Günlük plan formu (Trader Dante'nin prop'tan kalma formu, BX54B-9lHME)

Her sabah, seans öncesi:
1. **Günün verileri/haberleri** + o verinin **önceki etkisi** (örn. "geçen sefer altın önce hareket etti" ya da "beklentiden iyi geldi ama piyasa düştü, iyi haberi görmezden geldi").
2. **Teknik seviyeler**: piyasanın altında bid vereceğin seviyeler, üstünde offer vereceğin seviyeler.
3. **Günün beklentisi**: örn. "nötr, günlük bull flag içindeyiz, testere bekliyorum".
4. Gün sonunda: **ne oldu** ve **çıkarımlar**. Nasıl işlem yaptım?

Neden işe yarar? Dante'nin öğrencilerinden örnek: Sabah iki büyük seviye yazmış. Fiyat **iki seviyeden de mükemmel döndü**, ama öğrenci günlük zarar limitine takıldı. Sebep: plandaki seviyeleri değil, plana hiç yazılmamış 4-5 başka seviyeyi ve kırılımı işlemiş. "Piyasanın insafına kalmışlar. Her momentum parçasının peşine atlıyorlar." Gün içinde yeni yapı oluşabilir, ama büyük seviyelerini önceden bilirsen fiyat oraya gelince hazır olursun.

## FTA (first trouble area, ilk sorun bölgesi) kontrolü

Hedefi belirlemeden önce: fiyatın lehine giderken karşılaşacağı **ilk** engel nerede (önceki tepe/dip, spike öncesi destek, VAH/VAL, HVN)? FTA girişe çok yakınsa ve RR < plan eşiği ise setup ne kadar "güzel" görünürse görünsün **işlem yok** (Dante'nin 4. ipucu).

## Şablon (kopyala-kullan)

```
SETUP ADI:
PİYASA / SEANS:
HTF BAĞLAM (yön, kilit seviye):
GİRİŞ ŞARTLARI (hepsi zorunlu):
  1.
  2.
  3.
GİRİŞ TİPİ: limit / kapanış / stop-emir
STOP KURALI (geçersizlik noktası + tampon):
HEDEF KURALI (sonraki seviye; min RR):
RİSK %:
YÖNETİM (BE / kısmi / trailing):
İŞLEM YOK KOŞULLARI:
GÜNLÜK / HAFTALIK LİMİT:
```
