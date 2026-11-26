# 12 — Strateji Haritası: 13 Yaklaşım ve Zayıf Yanları

> Güven seviyesi: **YÜKSEK** (tanımlar standart, zayıf yanlar dürüstçe verilmiş).
> Kaynak: AlgoCoinism "Tüm Trading Stratejileri Tek Videoda!" (5txNIi7jwaM).

Tüm stratejiler 3 soruya cevap verir: **Yön nereye? Tepki nerede? Kim alıyor, kim satıyor?**

| # | Yaklaşım | Mantık / Giriş | Zayıf yanı |
|---|---|---|---|
| 1 | Trend takibi (MA / trend çizgisi) | Fiyat MA üstünde → long; MA'ya / çizgiye geri çekilmede gir | Yatay piyasada sürekli whipsaw |
| 2 | Kırılım (breakout) | Sıkışma (range/üçgen/kama) dışında kapanış + hacim artışı; stop bandın içine | **Sahte kırılım** (fiyat aşar, arkası gelmez) |
| 3 | Geri çekilme (pullback) | Sert hareket → düzeltme sonu (MA, eski direnç→destek) → daha iyi fiyat, yakın stop | Düzeltme bazen trendin sonudur |
| 4 | Yatay aralık (range) | Alt bantta al, üstte sat, stop aralık dışı | Kırılım anında herkes aynı anda stop olur |
| 5 | Ortalamaya dönüş | RSI 70/30, Bollinger dışı → ortalamaya dönüş | Güçlü trendde RSI uzun süre 70+ kalır |
| 6 | Destek / direnç | Geçmiş dönüş seviyelerinde tepki ara; **çizgi değil bant** | Her testte zayıflar |
| 7 | Fibonacci | %38.2 / 50 / 61.8 geri çekilme | Çok oran var → her dönüşün yakınında "bir" seviye bulunur; tek başına kullanma |
| 8 | Mum formasyonları | Engulfing, pin bar (hammer / shooting star), doji | Bağlamsız anlamsız; Bulkowski verisinde çoğu mumun tek başına avantajı zayıf |
| 9 | Grafik formasyonları | Çift tepe/dip, OBO, fincan-kulp; boyun çizgisi kırılımında gir | Yoruma açık, formasyon bittikten sonra net görünür |
| 10 | SMC | Yapı (BOS/CHoCH) + likidite (eşit tepe/dip) + OB/FVG'ye geri çekilme | Çok öznel — iki kişi aynı grafiğe farklı bölgeler çizer |
| 11 | Hacim / hacim profili / Wyckoff | Hacim teyidi, POC/VA, birikim-dağıtım evreleri | Kriptoda hacim borsalara dağınık; forex spot'ta merkezi hacim yok (tick volume) |
| 12 | Emir akışı (order flow) | DOM, footprint, delta; **absorpsiyon** (çok satış geliyor ama fiyat düşmüyor) | Hızlı, veri gerektirir (futures'ta mümkün) |
| 13 | Momentum (MACD, RSI uyumsuzluk) | Kesişim, uyumsuzluk = güç azalıyor | Gecikmeli; uyumsuzluk uzun süre erken uyarı verir |
| + | Kural tabanlı / algoritmik | Yukarıdakilerden birini net kurala döker, backtest eder | Geçmişte çalışan gelecekte çalışmayabilir (overfitting) |

## Vade

Aynı yaklaşım 1 dakikada da günlükte de uygulanır; değişen hız ve stop büyüklüğü. Düşük zaman dilimi = daha fazla maliyet/gürültü oranı.

## Piyasalar farklıdır: aynı araç her yerde çalışmaz (Grimes + gerçek veri testi)

> Kaynak: Adam Grimes, Chat With Traders bölüm 115 ("Hand Traders vs. System Traders", dfRPZfkrDKk, ~2016).

Grimes: "**Klasik teknik analizin yalanlarından biri**, aynı sistemin, formasyonun ve indikatörün her piyasada ve zaman diliminde çalıştığıdır." Ona göre günlük grafikte **hisseler emtialardan daha çok ortalamaya döner**. Bu yüzden trend takibi emtia ve dövizde yaygındır, hisselerde değildir. "20 günlük tepeyi al, 20 günlük dibi sat" sistemi emtiada biraz kazandırır, hisselerde kaybettirir. Momentum ile ortalamaya dönüş dengedeyken fiyat rastgele yürür. Avantaj, bu güçlerden birinin baskın geleceği noktalardadır.

**Test** (`arastirma/verify_breakout_by_asset.py`, günlük, 2005+, maliyetsiz). Sistem: 20 günlük Donchian, dur-ve-ters-çevir. P&L ATR biriminde.
| Grup | Kırılım L/S, Sharpe (tümü / 2005-14 / 2015+) | Sadece long kırılım | Al-tut (referans) |
|---|---|---|---|
| 30 büyük ABD hissesi | **+0,03** / +0,02 / +0,04 | +0,38 | **+0,55** |
| 13 emtia ETF'i | +0,08 / **+0,19** / +0,02 | +0,11 | +0,08 / **-0,14** / +0,20 |
| 7 majör döviz paritesi | **-0,06** / -0,02 / -0,10 | -0,03 | +0,01 |

Kırılım sonrası 20 günlük getiri, sembolün kendi eğilimi çıkarıldıktan sonra her üç grupta da ~0. Ham kırılım sinyalinin tek başına yön avantajı yok.

**Sonuç:**
1. **Hisselerde Grimes haklı.** Kırılım sistemi maliyetsiz sıfır, maliyetle negatif. Sadece long versiyonu bile al-tut'un gerisinde kalıyor (Sharpe 0,38'e karşı 0,55). Trend filtresi hisselerin yukarı eğiliminin bir kısmını kaçırıyor. Not: bugünün büyük hisseleri seçildiği için hayatta kalma yanlılığı var, long tarafı lehine.
2. **Emtiada iddia 2005-14 için doğru.** Trend al-tut'u geçmiş (+0,19'a karşı -0,14), düşen emtia piyasasında short tarafı kazandırmış. **2015 sonrasında avantaj kaybolmuş** (+0,02'ye karşı al-tut +0,20). Bu, trend takibinin 2010'larda zayıfladığı yönündeki genel literatürle uyumlu (ör. Hurst, Ooi ve Pedersen'in çok piyasalı yüzyıllık trend çalışmaları). Tek bir Donchian sistemiyle birkaç ETF, çeşitlendirilmiş ve volatiliteye göre ölçeklenmiş bir futures portföyünün yerini tutmaz.
3. **Dövizde** bu basit kırılım sistemi zarar ettirdi.
4. **Genel ders:** Bir stratejiyi "piyasadan bağımsız" sanma. Her piyasayı ayrı test et ve **al-tut temel çizgisiyle** karşılaştır. Avantajlar hem piyasaya hem rejime bağlı. Hiçbiri bu testte Sharpe 0,2'yi geçmedi.

## Kısa vadeli ortalamaya dönüş (Connors RSI-2) ve gece etkisi: yayımlandıktan sonraki test (24. tur)

> Kaynaklar: Connors ve Alvarez, *Short Term Trading Strategies That Work* (2008). Connors'ın CMT podcast röportajı (iEcp7hzXqhY). Quantified Strategies'in "6 Connors stratejisi" backtest'i (gX8FjjKR7ec). Gece etkisi: Cooper, Cliff ve Gulen (2008).

**A) RSI(2)** (`arastirma/verify_swing_candidates.py`, `verify_rsi2_portfolio.py`). Kural:
- **Giriş**: kapanış 200 günlük ortalamanın üstünde ve RSI(2) < 10 ise kapanışta al.
- **Çıkış**: kapanış 5 günlük ortalamanın üstüne çıkınca ya da en fazla 10 gün sonra.
- Ortalama tutma süresi ~3,5 gün.

| | 2009 öncesi (yayım öncesi) | **2009+ (yayım sonrası)** |
|---|---|---|
| 8 endeks ETF'i, stopsuz, işlem başına (1R = 1 ATR) | +0,45R, isabet %77 | **+0,33R (se 0,05)**, isabet %72. 8 sembolün 8'inde pozitif. |
| 2 ATR stopla (1R = 2 ATR) | — | +0,109R (se 0,022). Rastgele "200 günlük ortalamanın üstü" girişinde +0,035R. |
| Portföy, %1 risk, açık risk sınırı 3r | — | Sinyallerin **%37'si atlanıyor**. Yıllık **%2,9**, maksimum düşüş %14. **SPY al-tut %14,3.** |
| İki aşamalı challenge, %1 / %2 risk | — | Geçti **%11** / %36, kaldı %21 / %54. Avantajı olmayan referans %32. |

- **Yayından sonra da çalışıyor, ama zayıflayarak.** "Yükselen bir endekste kısa vadeli aşırı satımı al" fikri 04 §5b'deki pullback bulgusuyla aynı mekanizma: hisse endekslerinde kısa vadede ortalamaya dönüş ve yukarı eğilim.
- **Stop beklentiyi düşürüyor.** ATR başına +0,33'ten ~+0,22'ye. Connors: "Stoplar test sonuçlarını kötüleştirir, rolleri psikolojik." Ama stopsuz pozisyonun gap riski açık uçlu. Connors'ın çözümü sabit dolar riskli haftalık call opsiyonu: kayıp en fazla 1R, gece ve hafta sonu gap'i dahil. Bu da Van Tharp'ın R kavramı.
- **Prop için uygun değil.** Sinyaller tüm endekslerde aynı günlerde kümeleniyor, yani tek bahis. Yılda bağımsız işlem sayısı az. %1 riskte challenge'ı bir yılda geçme ihtimali sadece %11. Quantified Strategies de aynı şeyi söylüyor: "Altı Connors stratejisini portföy olarak işleyemezsin, çok benzerler ve birbirini tamamlamıyorlar."

**B) Gece etkisi**: kapanışta al, ertesi açılışta sat. Maliyet 1 bp.
| | ≤2008 | 2009-2017 | **2018+** |
|---|---|---|---|
| SPY gece / gün içi Sharpe | 0,84 / -0,27 | 0,44 / 0,58 | **0,61 / 0,15** |
| QQQ | 0,72 / -0,63 | 0,90 / 0,53 | 0,64 / 0,21 |
| IWM | 0,83 / -0,47 | 0,58 / 0,26 | **0,86 / -0,45** |

- Endeks getirisinin büyük kısmı **gece** oluşuyor, bu yayından sonra da sürüyor. IWM'de 2018 sonrası gün içi bacak yıllık **-%8,5**: küçük şirket endeksinde gün içi long taşımak zarar.
- **Prop için pratik değil.** Futures prop firmalarının çoğu gece pozisyonu yasaklıyor (seans sonunda düz olma kuralı). CFD'de gecelik finansman (swap) yıllık faiz kadar, %5 faizde ~2 bp/gece, ve gece getirisi ~3 bp/gece. Avantajın çoğunu yiyor. Kendi futures hesabında finansman fiyatın içinde olduğu için daha uygulanabilir.


**✔ 37. tur: zaman bazlı test** (`arastirma/verify_rsi2_timesplit.py`).
- **Kurgu**: 21 endeks ve ülke ETF'i, 3.627 işlem. Her RSI-2 işlemi, aynı sembolde ve aynı 5 yıllık dönemde, aynı süre tutulan 5 rastgele "SMA200 üstü" günle karşılaştırıldı.

| Dönem | n | RSI-2 (R) | Rastgele (R) | **Fark (se)** |
|---|---|---|---|---|
| 2003-09 | 1.062 | +0,38 | +0,19 | +0,19 (0,05) |
| 2010-14 | 787 | +0,18 | +0,03 | +0,15 (0,07) |
| 2015-19 | 649 | +0,17 | +0,11 | +0,06 (0,08) |
| 2020+ | 1.129 | +0,33 | +0,10 | **+0,23 (0,05)** |
| **2015+** | 1.778 | +0,27 | +0,10 | **+0,17 (0,04)** |

- **RSI-2 avantajı pullback'ten farklı olarak 2015 sonrasında da sürüyor.** Fark dört dönemin dördünde de pozitif. Ama zayıf bir 2015-19 dönemi var.
- İşlem başına avantaj gerçek. Ama portföy düzeyinde sınırlı kalıyor: az işlem, kümelenme ve sadece endeks (yukarıdaki %2,9 yıllık getiri ve %11 challenge sonucu geçerli).
- **Emtiada trailing stop** (03) de zaman testinden geçti (`verify_trailing_robustness.py`). 2015 sonrasında ETF'lerde +0,07R ve futures'ta +0,07R, sabit hedefle ~0.
- **RSI-2 başka piyasalarda ve satışta (2026-11-27, `verify_rsi2_genis.py`, README #89).**
  - Alış yönü 2015+ rastgeleye göre: endeks +0,28R (se 0,06), büyük ABD hisseleri +0,10 (0,05), sağlık +0,11 (0,08), emtia ~0, parite ~0.
  - Kripto −0,19 ve Türk hisseleri −0,12: bu piyasalarda düşüşü almak rastgeleden kötü, çünkü trend yapıyorlar.
  - Satış aynası (SMA200 altı, RSI(2) > 90) hiçbir grupta maliyet öncesi bile anlamlı kâr etmiyor.
  - İlişkisiz piyasalarda sinyaller SPY ile yalnız %13-15 çakışıyor, ama orada avantaj yok. → RSI-2 endeks alışına özgü. Emtia, kripto ve döviz için trend takibi kullan.
- Yani zaman testinden geçen iki işlem başı avantaj kaldı: **endekste RSI-2** ve **emtiada trailing çıkış**. 12 ay momentumunun 2015 sonrası Sharpe'ı da 0,61.
**Genel ders (20. ve 24. tur; ⚠️ 36. turda pullback avantajının 2015 sonrası ~0 olduğu bulundu, 04 §5b):** Hisse endekslerinde günlük grafikteki iki gerçek avantaj (pullback ve RSI-2) **işlem başına pozitif**, ama:
1. Sinyaller endeksler arasında aynı günlerde kümeleniyor.
2. Uzun ağırlıklı oldukları için asıl getiri yukarı eğilimden geliyor ve **al-tut'un gerisinde** kalıyorlar.
3. Yılda yeterince bağımsız işlem üretmiyorlar, bu yüzden prop challenge'ı için yetersizler.

Prop için gereken ~10-15R/yıl, ya **birbiriyle ilişkisiz çok sayıda piyasada** ya da **düşük maliyetli yüksek sıklıkta** bir avantaj ister. Prop challenge'ı, avantajı küçük olanlar için yapısal olarak zor bir oyun (09 §4h).

**Güncelleme (25. tur):** Birbiriyle ilişkisiz piyasalar yolu denendi. Endekste RSI-2 + emtiada kırılım ve trailing stop portföyü, %0,5 riskte iki aşamalı challenge'ı 3 yıllık süreyle %93 geçiyor. Ama medyan süre ~2 yıl ve kollar seçim yanlılığı taşıyor. Tahvil ve döviz kolları negatif çıktı (09 §2 madde 7).

## Çeşitlendirilmiş trend takibi: Clenow'un 12 ay kuralı ve Parker'ın dersleri (26. tur)

> Kaynaklar: Andreas Clenow, Top Traders Unplugged #91 (grIHdA5pMhE); Jerry Parker (Turtle, Chesapeake Capital), Real Vision (B894C3Z6Pq0). Akademik adı **zaman serisi momentumu** (Moskowitz, Ooi ve Pedersen 2012).

**Clenow:**
- **"Karmaşıklık ancak karşılığı çok iyi ödeniyorsa eklenir."** 10 indikatörün birlikte sinyal vermesi büyük ihtimalle aşırı uyumdur. EMA mı SMA mı tartışması "yuvarlama hatası". "Kurumsal tarafta kimse 10 indikatörü optimize etmiyor, bu perakendenin yanılgısı."
- **Kıyas modeli**: "Dünkü fiyat bir yıl öncekinden yüksekse long, değilse short." 50-100 futures piyasasında, volatiliteye göre boyutlanınca kitabındaki modelden bile iyi sonuç veriyor. "**Bunu geçemiyorsan sorunun var.**" Tek bir ya da beş piyasada ise "her şey olabilir".
- **Volatilite tabanı**: Ocak 2015'te İsviçre merkez bankası (SNB) EUR/CHF tabanını kaldırınca, yapay olarak düşük volatilite nedeniyle aşırı büyük pozisyon taşıyan fonlar bir günde %25-30 kaybetti. → Volatiliteye göre boyutlandırmada **taban volatilite** kullan. Parker da aynı şeyi söylüyor. **Aynı riski taşıyan pozisyonları ayrı ayrı alma**: CHF futures ve EUR/CHF aynı bahis.
- **Hisselerde trend takibi ≠ futures'ta trend takibi.** Hisselerin iç korelasyonu yüksek, özellikle düşüşte hep birlikte kaybediyorlar. Sıralama gerekiyor, endeks rejim filtresi gerekiyor ("düşen piyasada hisse alma"). Hisse short'lamak çoğu kişi için "ahmakça bir iş": ani sıçramalar ve satın alma haberleri var.
- **Trend yönünde "karşı trend" girişi**: Trend takipçilerinin stoplarının toplandığı yerden, yani son uç noktadan 3 ATR geri çekilmede trend yönünde gir. Bu, 04 §5b'deki pullback bulgusuyla aynı mantık.
- **Gerçekçi beklenti**: "Uzun vadede yıllık %10-15 bileşik getiri çok iyi sayılır. %50-100'ü kimse sürdüremedi." Perakendecinin ana hatası, "bir hedge fon çalışanını kovduracak" kadar risk almak. Elliott dalgaları ve Fibonacci "çürütülemeyen safsatalar".

**Parker:**
- "**Sistemine uy ve küçük işlem yap.**" Trader sorunlarının kökü aşırı büyük boyut. Turtle programında yüzde 200'lük getiriler, bir günde %60 kayıp. Chesapeake'i kurunca hedefi düşürdü.
- **Kısa vadeli trend 1990'ların sonundan itibaren çalışmadı.** Geriye bakış süresi uzatıldı, pozisyon tutma süresi 6-12 aya çıktı. "Bunun sebebi kesikli piyasa, stop avı ve tüm o oyunlar."
- "Zamanın %60'ında yanılıyoruz. Dev kazananlar kurtarıyor." Paul Tudor Jones'un Japonya short'u: büyük kazançtan önce 5 kez küçük kayıp. "Trendin döneceğini tahmin etmeye çalışırken, kârın bir kısmını geri vermekten daha çok para kaybedilir."
- Portföy kabaca 25% tahvil, 25% emtia, 25% hisse, 25% döviz. Long ve short birlikte. Piyasalar **geçmiş performansa göre değil, çeşitlendirme katkısına göre** ağırlıklandırılıyor.

**✔ Test** (`arastirma/verify_tsmom.py`, 19 ETF ve döviz paritesi, 2005+, aylık yeniden dengeleme, volatiliteye göre boyut, taban volatilite %5, maliyet 5 bp × devir):
| Kural | Sharpe 2005+ | 2005-14 | **2015+** | Maksimum düşüş |
|---|---|---|---|---|
| **12 ay** | **0,55** | 0,48 | **0,61** | %8 (yıllık volatilite 4,2%) |
| 3 ay | 0,40 | 0,46 | 0,33 | %10 |
| 1 ay | 0,02 | 0,17 | **-0,12** | %16 |
| *SPY al-tut* | *0,60* | | | *%55* |

- Sınıflara göre 12 ay kuralının Sharpe'ı: emtia 0,64, hisse 0,43, tahvil 0,23 (2015+ 0,05), döviz ~0.
- **SPY ile günlük korelasyon -0,02.** Al-tut ile aynı Sharpe'ı çok daha küçük düşüşle veriyor, ve ikisi birbirini çeşitlendiriyor.
- **Parker'ın gözlemi doğrulandı**: geriye bakış süresi kısaldıkça avantaj kayboluyor, 1 aylık kural 2015 sonrasında negatif. 03'teki 20 günlük kırılım bulgusu da bununla tutarlı.
- **Prop testi** (iki aşama, aşama başına 3 yıl, yol yıllık volatiliteye ölçeklendi):

  | Yıllık volatilite | Geçti | Kaldı | İki aşamayı geçme süresi (medyan) |
  |---|---|---|---|
  | %4 | %23 | %0 | ~3 yıl |
  | **%6** | **%70** | **%4** | ~2,4 yıl |
  | %8 | %70 | %23 | ~1,8 yıl |
  | %10 | %63 | %37 | ~1,2 yıl |

  Bu, 25. turdaki kollu portföyle (09 §2 madde 7) aynı tablo: **gerçek, çeşitlendirilmiş avantaj challenge'ı yüksek ihtimalle geçirir ama 1,5-3 yıl sürer.**

**✔ 12 ay momentumu + SPY al-tut karışımı** (27. tur, `arastirma/verify_tsmom_blend.py`). Her bacak yıllık %10 volatiliteye ölçeklendi, ağırlıklar risk ağırlığı:
| SPY risk ağırlığı | Sharpe 2005+ | 2015+ | Maksimum düşüş |
|---|---|---|---|
| %0 (sadece momentum) | 0,55 | 0,61 | %19 |
| %30 | 0,74 | 0,85 | %13 |
| **%50** | **0,82** | **0,95** | **%13** |
| %70 | 0,77 | 0,92 | %20 |
| %100 (sadece SPY) | 0,60 | 0,75 | %33 |

- **İlişkisiz iki avantajı birleştirmek en büyük iyileşme.** Sharpe 0,55-0,60'tan 0,82'ye çıkıyor, düşüş yarıya iniyor.
- **Prop testi**: %50 karışım, yıllık %8 volatilite → iki aşamalı challenge **%89 geçti, %11 kaldı**, medyan ~560 gün. Sadece momentumda %70 / %23.
- **⚠️ Uygulama çekinceleri**:
  - (1) SPY bacağı ex post volatiliteye ölçeklendi, yani hafif ileriye bakma var.
  - (2) Prop hesabında SPY long'u **CFD ile tutulur**. CFD long'larında gecelik finansman ~faiz + %2-3 markup. Örneğin %5 faizde nominalin ~%7'si, %10 volatilite bacağında (~0,5× kaldıraç) yılda ~%3,5. SPY bacağının getirisinin yarısından fazlası gider. Futures'ta finansman fiyatın içinde ve sadece faiz farkı kadar.
  - (3) FTMO **Standart** fonlu hesapta hafta sonu pozisyon taşınamaz. Bu kurulum **Swing** hesap tipi ister (09 §4i).
  - (4) Test edilen ETF'lerin bir kısmı (emtia ETF'leri) teminat faizini getiriye dahil ediyor. Prop simüle hesabında nakit faizi yok.
  - (5) Sadece 2005-2026, yani tek bir uzun boğa piyasası.

**Clenow'dan ek notlar** (Zerodha "In The Money" #06, oUKqTaSe9oQ, ilk yarı):
- "**Görüşlerimle değil, matematiğimle işlem yaparım.** 5-6 yıldır bu boğa piyasasının çok uzadığını, her an çökebileceğini düşünüyorum, ve yanıldım. Matematiğim long."
- **2008** trend fonları için "tarihin en kârlı yılı" ama en stresli yılıydı. Fon günde %15-20 sallanınca "sorumlu olan herkes modeli ezip riski düşürdü". Daha çok kazanılabilirdi ama "o riski almazsın". **Modeller o volatiliteye göre tasarlanmamıştı. Hazırlıklı olmadığın bir şey olursa harekete geç.** Ayrıca nakit için karşı taraf riski vardı: her öğleden sonra hangi bankanın 24 saat içinde batma ihtimalinin en düşük olduğunu inceleyip gecelik mevduat yapmak.
- **1980-2000'lerin rüzgârı**: Yüksek ve düşen ABD faizi trend fonlarına iki yönden kazandırdı: tahvil fiyatlarının yükselmesi ve nakdin yüksek faizi. "O dönem bitti." Eski getirileri bugüne taşıma.
- **Giriş kuralı ikincil, portföy kurgusu birincil.** "Kırılım mı hareketli ortalama mı tartışması anlamsız." Hangi piyasalar evrende, nasıl etkileşiyorlar, her birine ne kadar risk veriliyor, bunlar daha önemli. Tek başına para kaybettiren bir piyasa bile, diğerleri kaybederken kazandırıyorsa (çarpıklığı iyileştiriyorsa) portföye girebilir. Ama 25. turdaki tahvil ve döviz kollarının korelasyonu pozitifti (+0,09 / +0,35), yani bu koruma değeri yoktu.
- "**Tek bir enstrümanda trend takibi** (en iyi Nasdaq trend sistemi nedir?) büyük bir hata. Endüstride 50-100 kontrat işlenir."
- Klasik indikatörler "kalem kağıtla hesaplanabilsin diye sadeleştirilmiş", onları kopyalamak için bir sebep yok.
- **Kripto**: "Temel değeri sıfır, ama psikolojiyle hareket ettiği için trendleri var. İşlem yapılabilir, yeter ki hikâyeye inanma."

**Jerry Parker, The Meb Faber Show** (TjkdsSHW6oQ, 2017):
- **"Her şey tek bir soruya indirgeniyordu: Büyük kazananlar küçük kayıpların bedelini öder mi?"** Turtle kuralları karmaşık değildi: "Herkese kurallar öğretilebilir. Asıl soru, kurallara ~%100 uyup uyamayacağın."
- **Disiplin en az %50.** "Disiplin eksikliğinden kaçırdığım para, yöntemimin daha iyi olamamasından kaçırdığım paradan **çok daha fazla**. Örnekler: kuralı izlememek, kârdan erken çıkmak, sıradaki işlemi almamak. Çoğu insan için de böyle."
- **"Çoğu insan kazananı seçebilir, ama kazananı yönetemez."** Başarılıyı başarısızdan ayıran şey kazanandan erken çıkmamak. "Kârla cesur, zararla korkak ol." Bu, Richard Dennis'in 1983'teki sözü. "Kârı korumak için" sonradan eklenen kurallara "sistematik takdir" diyor ve sağlam olmadıklarını söylüyor.
- "**Büyük fonlar iyi fonlardan daha sık para kaybeder.** Çok sayıda vuruşta ıskalamadan büyük vuruş olmaz." İşlemlerin ~%40'ı kazanıyor. Petrol short'u: büyük düşüşten önce aynı işlemi bir düzine kez denemiş ve neredeyse her seferinde başarısız olmuş.
- **Piyasa sayısının marjinal faydası azalıyor.** 20 piyasadan 100'e çıkmak, ilk 20'nin verdiği kadar çeşitlendirme vermiyor: "bir tahvil piyasası daha, bir kur daha".
- **Teknik analiz ≠ trend takibi.** "TA; formasyonlar, grafik okuma, fincan ve tabaklar. Onu anlamıyorum ve katılmıyorum. Trend takibi tek giriş, tek çıkış ve stoplu sistematik bir yaklaşım." Meb Faber de CMT programının 3. seviyesinde "%90'ına inanmadım, nesnel backtest'i yok" diyor. Bu, 10 §7b'deki mum formasyonu bulgusuyla uyumlu.
- **Meb Faber**: Bir portföy optimizasyon aracına geçmiş verilerle hisse, tahvil, emtia ve trend takibini verirsen, en büyük ağırlığı trend takibine verir. Faber'in "Trinity" portföyü kabaca yarı al-tut, yarı trend. Bu bilgi tabanının bulgusuyla örtüşüyor: %50/%50 risk karışımı en iyi Sharpe'ı verdi. Faber'e göre opsiyon (put) sepeti almak negatif beklentili bir koruma, düşük faizde tahvilin koruması da garanti değil.
- **Öğrenme**: "Bir mentor bul, az parayla bir ustanın yanında çalış." Dennis'in mülakat sorusu "İşlem hakkında bilinebileceklerin yüzde kaçını biliyorsun?" idi. Çoğu "%90" dedi, işe alınan tek kadın Liz Cheval "çok az" dedi. "Turtle 2.0 kod yazmak."

**✔ Parker'ın "endekste trend takibi büyük hata, tek hisselerde yap" iddiası** (`arastirma/verify_tsmom_stocks.py`, 12 ay momentumu, 2005+, %10 volatiliteye ölçekli):
| | Sharpe (2015+) | Maksimum düşüş | SPY ile korelasyon |
|---|---|---|---|
| SPY | 0,56 (0,44) | %25 | 0,50 |
| 4 endeks ETF'i | 0,54 (0,40) | %23 | 0,45 |
| **30 büyük hisse, long/short** | **0,45** (0,31) | %25 | **0,35** |
| 30 büyük hisse, sadece long | 0,77 (0,67) | %21 | 0,74 |

→ Tek başına bakınca **desteklenmedi**: tek hisselerde long/short trend endeksten daha düşük Sharpe veriyor. Sadece SPY ile korelasyonu daha düşük, bu kısım doğru. Sadece long versiyonun yüksek Sharpe'ı çoğunlukla piyasa betası (korelasyon 0,74) ve hayatta kalma yanlılığı. Parker'ın asıl argümanı, tek hisselerin 100 piyasalı bir portföy **içinde** çeşitlendirme sağlaması. Bu test onu tam ölçmüyor.

**"Trendi tanımlamanın yüz yolu var, hepsi aynı şeyi yapar"** (Carver, Zerodha #04, p0znNV4oWe8).
- **Carver'ın iddiaları**:
  - En basit yol "son N günde fiyat arttı mı?". Bu, üstel hareketli ortalama kesişimine (EWMAC) çok yakın sonuç verir.
  - Trend kuralını seçmeye uğraşmak "tam bir zaman kaybı". Kural eklemek Sharpe'ı en fazla birkaç yüzdelik değiştirir.
  - Trend **birkaç hafta ile bir yıl** arası tutma sürelerinde çalışır. Saatlik ya da birkaç günlük trend gürültüdür, dakikalarda ortalamaya dönüş görülür.
  - Yeni başlayana önerisi:
    - **Tek ucuz enstrüman** (SPY gibi) ve **tek kural** (EWMAC 16/64).
    - Çıkış için ayrı bir mantık değil, volatiliteye göre bir trailing stop. Ayrı giriş ve çıkış mantığı aşırı uyumdur.
    - Sonra enstrüman ekle; asıl kazanç oradan gelir.
  - **Short tarafa ayrı kural uydurma.** Hisselerde çok az düşüş dönemi var, istatistik yetmez. Sadece long ya da long/short tercihi, portföyde zaten hisse long olup olmamana bağlı.
  - **Gece etkisi** tek başına işlenemez (maliyet). Ancak zaten alacaksan bir icra eğilimi olarak kullanılabilir (24. tur bulgusuyla uyumlu).

**✔ Test** (`arastirma/verify_carver_zerodha.py`): 19 piyasa, 2005+. 11 kural, hepsi volatiliteye göre boyutlu, haftalık yeniden dengeleme, 5 baz puan maliyet.

| Kural | Sharpe 2005+ | Sharpe 2015+ | EWMAC 16/64 ile korelasyon |
|---|---|---|---|
| EWMAC 8/32 | -0,01 | -0,19 | 0,82 |
| EWMAC 16/64 | 0,29 | 0,18 | 1 |
| EWMAC 32/128 | 0,42 | 0,36 | 0,81 |
| EWMAC 64/256 | 0,26 | 0,14 | 0,55 |
| 20 günlük getiri | -0,04 | -0,32 | 0,62 |
| 63 günlük getiri | 0,12 | -0,19 | 0,88 |
| 126 günlük getiri | **0,49** | 0,27 | 0,76 |
| 252 günlük getiri | **0,47** | **0,46** | 0,53 |
| Donchian 20 | -0,31 | -0,44 | 0,50 |
| Donchian 55 | 0,02 | -0,20 | 0,83 |
| Donchian 120 | 0,23 | -0,07 | 0,90 |
| 11 kuralın ortalaması | 0,26 | 0,03 | 0,92 |

- ✔ **Aynı hızdaki kurallar neredeyse aynı şey**: EWMAC 16/64 ile 63 günlük getirinin korelasyonu 0,88, Donchian 120 ile 0,90. Kuralların ortalama korelasyonu 0,62, yavaş olanlar arasında 0,69.
- ✔ **Asıl fark hız.** ~1 aylık ve daha hızlı kurallar (EWMAC 8/32, 20 günlük getiri, Donchian 20) maliyetten sonra **sıfır ya da negatif**, 2015 sonrası daha da kötü. Parker ve Carver'ın "hızlı trend çalışmayı bıraktı" gözlemiyle uyumlu.
- **Ortalama almak ancak hızlar maliyete göre süzülürse işe yarıyor.** Hızlı kuralları da katınca ortalama 0,26'ya düşüyor.
- ✘ Ama "en basit kural EWMAC kadar iyi" kısmı hıza bağlı. Yavaş hızlarda (126-252 gün) basit getiri kuralı **en iyi** sonucu verdi. Komşu hızlar arasındaki 0,1-0,3'lük Sharpe farkları, 20 yılda bir Sharpe'ın standart hatası (~0,22) mertebesinde, yani muhtemelen gürültü.
- → **Senin için anlamı**: Giriş kuralının türüyle (EMA, kırılım, getiri) uğraşma. **Hızı** haftalar-aylar aralığında tut ve maliyeti hesaba kat. 15 dakikalık ya da 1 saatlik "trend takibi" bu kanıtlara göre gürültü bölgesinde.

**Hangi piyasalar? Man AHL makalesi** (Carver'ın özeti, Top Traders Unplugged #386, OVh3f8hmchA). Makale piyasaları üçe ayırıyor:
- **Geleneksel**: 30 yıl önceki klasik futures (endeks, tahvil, majör kur, temel emtia).
- **Alternatif.**
- **Ezoterik**: Çin vadelileri, fiziksel kripto, Alman elektriği, CDS gibi.

Bulgular:
- **Getirinin kaynağı farklı.** Geleneksel piyasalarda trend getirisinin ~%55'i ortak faktörlerden (risk iştahının açılıp kapanması) gelir, ~%45'i piyasaya özgüdür (idiosenkratik). Alternatif ve ezoterik piyasalarda oran ~1/3 faktör, ~2/3 piyasaya özgü.
- **Kısıtsız Sharpe optimizasyonu** ağırlığın sadece ~%30'unu geleneksel piyasalara veriyor. "Garip şeyler" çeşitlendirir.
- **Ama amaç kriz koruması ise** (sadece hisselerin düştüğü dönemlere göre optimize edilince) bu oran ~%50'ye çıkıyor. Krizde istenen şey tam da o ortak faktör: 2008'deki gibi hisse short, tahvil long.
- **Nakit verimliliği de hesaba katılınca** oran ~%70'e çıkıyor. Futures marjı düşük: Carver nakdinin ~%30'unu, tipik bir CTA ~%20'sini marj olarak kullanıyor.

→ **Prop/CFD trader için anlamı**:
- FTMO gibi firmaların sunduğu evren zaten büyük ölçüde geleneksel piyasalar: endeks, majör kur, altın, gümüş, petrol, doğalgaz.
- Bu, kriz dönemlerinde iyi, Sharpe açısından biraz eksik bir evren.
- Bu bilgi tabanının 19 piyasalık testleri de bu evrende yapıldı.
- Daha fazla "garip" piyasa ekleme imkânı sınırlı. Çeşitlendirmeyi piyasa sayısından çok **farklı sınıflardan** (metal, enerji, kur, endeks) almak gerekir.

### Parker ve Faber, ikinci bölüm (56. tur, "Does Trend Following Work?", 2oXvQ-8Bj9E) ve test

**Parker'ın ilkeleri** (Turtle programından gelen, Chesapeake'in kurucusu):
- ~100 piyasa, dört sınıfa yaklaşık eşit pay (emtia, faiz, kur, hisse), long ve short. Her pozisyon volatilitenin tersine boyutlanır: her işlemin portföye katkı potansiyeli eşit.
- En az 100 günlük bakış, ortalama tutma süresi ~1 yıl. Kayıpların ~%60'ı küçük. Kâr nadir büyük trendlerden (kakao) geliyor.
- Piyasa seçimi geçmiş performansa göre yapılmaz: "Kakaoda 50 küçük kayıp, sonra tüm zamanların en büyük trendlerinden biri." (Carver'ın "piyasa seçme" bulgusuyla aynı, 10 §6j.)
- "Stopu başa başa çekmek, backtest açısından en kötü fikirlerden biri. Duygudan geliyor." (02 §4b ile aynı.)
- "Günün tepesinden almaya çalış" kuralı: trader'ların nefret ettiği şey, ama ortalama işleme birkaç puan eklemiş. Duygusal rahatsızlık bir avantaj kaynağı olabilir.

**Test** (`arastirma/verify_parker_streak.py`, 30 vadeli, 2000+, 100 günlük kırılım, 50 günlük karşı uçta çıkış, 1R = 2 ATR, maliyetsiz): 1.575 işlem, ortalama **+0,24R**, isabet %38. **İşlemlerin en iyi %10'u brüt kazancın %67'si.**

| O piyasada önceki ardışık kayıp | İşlem | Ortalama R (se) | İsabet |
|---|---|---|---|
| 0 (son işlem kazandı) | 608 | +0,25R (0,18) | %37 |
| 1-2 | 627 | +0,16R (0,17) | %38 |
| 3-4 | 218 | +0,30R (0,26) | %43 |
| 5+ | 122 | +0,47R (0,50) | %38 |

- Ardışık kayıplardan sonraki işlemler **daha kötü değil**, iki dönemde de biraz daha iyi: 2000-2012'de +0,56R'ye karşı +0,23R, 2013 sonrası +0,25R'ye karşı +0,18R. Standart hatalar büyük, yani "beklenti birikir" kanıtlanmadı. Ama **"kaybettiren piyasayı bırak" kuralı veriyle desteklenmiyor** (11 #88).
- Faber'in **"ilk kârlı kapanışta çık"** örneği de test edildi: rastgele girişlerde isabet **%96**, ortalama **-0,05R**, en kötü %1 **-11,8R**, medyan tutma 2 gün, işlemlerin %7'si 60 günden fazla açık kalıyor. Yüksek isabet tek başına hiçbir şey söylemez (01 §3).

## Breitstein'ın iki swing stratejisi: mekanik versiyon testi (51. tur, k-X0164r66U)

**Stratejiler** (Breitstein: "Swing işlemlerimin çoğu bu ikisi"):
- **(A) Kapitülasyon, "V'nin sağ tarafı"**: Sürdürülemez hızla ivmelenen sert ve uzun bir düşüş, devasa hacim. Düşüş trendi kırılınca al. İlk stop dipte, sonra bir önceki günlük barın dibinden trailing. En iyi işlemi buydu: Ağustos 2024 Nikkei paniği, tek işlemde 10 milyon $.
- **(B) Devam (Kullamägi tarzı)**: "Oyunda" olan, sıcak temalı bir hissenin çok aylık kırılımı, ideal olarak katalizörle. Kırılım seviyesinden al. Stop seviyenin altında ya da günün dibinde. Trailing: önceki günlük barın dibi ya da 20 günlük ortalama. "Kurumlar bir temaya pozisyon alırken 20 dakika değil haftalarca alır."
- **Boyut**: "Stop 3 kat genişse boyut 3 kat küçük olmalı." Kendi hatası, gün içi boyutunda kalıp daha sonra gün içi stoplarla kendini silkelemekti (02 §6e).

**Test** (`arastirma/verify_breitstein_swing.py`, 50 likit ABD hissesi, günlük, long, maliyetsiz, kıyas: aynı hisselerde aynı stop ve çıkışla rastgele giriş):

| Kural | 2005-14 (rastgele) | 2015+ (rastgele) |
|---|---|---|
| A, önceki gün dibi trailing | -0,09R (+0,04R) | -0,06R (+0,03R) |
| A, 5 günlük ortalama çıkışı | -0,21R (+0,07R) | -0,14R (+0,04R) |
| B, önceki gün dibi trailing | -0,03R (+0,09R) | +0,05R (+0,07R) |
| B, 20 günlük ortalama çıkışı | +0,13R (+0,18R) | **+0,46R (+0,21R)**, işlem başına +%1,41 (+%0,32) |

- **A (kapitülasyon)**: Mekanik versiyonda avantaj yok, rastgele girişten kötü. Bu, Breitstein'ın takdirli seçimini temsil etmez: "oyunda" olmak, duygusal aşırılık, endeks paniği. Bu bilgi tabanındaki diğer bulgularla birlikte bakınca kapitülasyon alımının avantajı **tek hisselerde değil endekslerde** görülüyor (RSI-2, 10 §6n).
- **B (kırılım + hacim)**: Sadece **gevşek çıkışla** (20 günlük ortalama) ve sadece 2015 sonrasında rastgelenin üstünde: +0,25R fark, ~1,9 standart hata. Önceki gün dibi trailing'i avantajı tamamen yok ediyor. Brandt'ın "ilk zararlı kapanışta çık" testiyle aynı ders: sıkı çıkış büyük kazananları keser (03).
- ⚠️ **Hayatta kalma yanlılığı**: hisse listesi bugünün büyük şirketlerinden oluşuyor (NVDA, AVGO, LLY gibi), bu da kırılım sonuçlarını şişirir. Rastgele kıyas aynı hisselerde olduğu için yanlılığın bir kısmını dengeler, hepsini değil. B'nin 2015+ sonucunu **zayıf kanıt** say.
- **İlk denemede ileriye bakma hatası vardı**: kırılım seviyesinden giriş yapıp "gün seviyenin üstünde kapandı" filtresini kullanmak, başarısız kırılımları gizledi ve sahte +1,1R üretti. Kendi testlerinde **gün içi giriş + kapanış filtresi** kombinasyonundan kaçın (10).
- **Prop açısı**: B tipi hisse swing'i FTMO'da CFD ile ve hafta sonu taşıma kuralıyla (Swing hesap) sınırlı. Bilanço boşlukları -10R'ye ulaşabilir (02 §6e).

## Seçim kriteri

- Stratejinin "en iyisi" yok (DD Finance: "en çok kazandıran model" arayışı tembellik/pazarlama). Ölçüt: **senin uygulayabildiğin + test ettiğin + pozitif EV'li** olan.
- Basitlik vs bilgi genişliği tartışması (Yusuf: "az bil, çok kazan" / DD: "ne kadar çok bilirsen o kadar iyi yorumlarsın"):
  **Sentez (Brooks/Grimes ile tutarlı):** Bağlamı anlamak için geniş bilgi faydalı, ama **işlem yapmak için 1-2 iyi tanımlanmış setup** yeterli ve gerekli. Bir setup'ı kanıtlamadan diğerine atlama.
