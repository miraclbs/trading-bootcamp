# 09 — Prop Firm / FTMO Challenge Matematiği

> Güven seviyesi: **YÜKSEK** (kendi simülasyonum: `arastirma/verify_ftmo.py`). Kurallar firmadan firmaya değişir — her zaman güncel kuralı firmanın sitesinden kontrol et.
> Model: +%10 hedef, −%10 statik maks. zarar (başlangıç bakiyesinden), −%5 günlük zarar, günde 2 işlem, 60 gün, risk başlangıç bakiyesinin %'si olarak sabit.

## 1. Simülasyon sonuçları (20.000 deneme / satır)

| Sistem | Risk/işlem | Geçme | Maks. zarardan düşme | Günlük limitten düşme | Süre doldu |
|---|---|---|---|---|---|
| **Avantajlı** WR40 RR2 (+0.20R) | %0.5 | %71.7 | %1.4 | 0 | %27 |
| | **%1** | **%85.7** | %11.9 | 0 | %2.5 |
| | %2 | %72.0 | %28.0 | 0 | 0 |
| | %3 | %36.2 | 0 | **%63.8** | 0 |
| **Zayıf avantaj** WR35 RR2 (+0.05R) | %1 | %57.5 | %36 | 0 | %6.6 |
| | %2 | %54.8 | %45.2 | 0 | 0 |
| **Avantajsız** WR33 RR2 (~−0.01R) | %1 | **%43.5** | %49.4 | 0 | %7.1 |
| | %2 | **%47.2** | %52.8 | 0 | 0 |
| WR55 RR1 (+0.10R) | %1 | %73.3 | %10 | 0 | %16.7 |
| | %2 | %72.4 | %27.4 | 0 | 0 |

## 1b. İki sınırlı problem ve trailing drawdown (Mulham ve ImanTrading videoları + `arastirma/verify_prop_trailing.py`)

**Gerçek hesap büyüklüğü = izin verilen maksimum zarar.** 50k futures hesabı aslında 2.000$'lık bir hesaptır, 100k FTMO hesabı 10.000$'lık. "50k ürünün adıdır. 2.000$ kaç hatayı kaldırabileceğini söyler."

**Challenge = iki sınırlı bir problem**: üst sınıra (hedefe) alt sınırdan (maksimum zarar) önce değmek. Challenge'ın **kendi RR'ı** vardır: futures 50k'da +3.000 / -2.000 = 1,5:1. FTMO tipinde her faz ~1:1, ama iki faz var. Stratejin bu yapının içine sığmalı.

**Avantajsızken geçme ihtimali (kumarbazın iflası formülü):** `P(geçme) ≈ Zarar_sınırı / (Zarar_sınırı + Hedef)`.
- 50k: 2000/(2000+3000) = **%40**. Simülasyon: 0,5/1/2 risk ile %40,5 / %40,3 / %39,7. **Avantaj yoksa risk boyutu sonucu değiştirmez.**
- Negatif avantaj (WR %40, 1:1): risk 250$ → %0,8, 500$ → %7,5, 1000$ → %19,3. **Kumarda büyük bahis şansı artırır.** Mulham'ın tablosuyla (1/7/19) birebir aynı. → "**Geçme şansını kârlı bir sistemle asla karıştırma.**"

**Aynı EV (+0,15R), farklı varyans + drawdown tipi** (50k, +3000/-2000, 60 gün, günde 3 işlem, geçme oranı):

| Risk/işlem | Strateji | Statik | Gün sonu trailing | Gün içi trailing |
|---|---|---|---|---|
| 250$ (%0,5; 8R alan) | A: WR %65, RR 0,77 (düşük varyans) | **93,4%** | 88,2% | 86,9% |
| | B: WR %55, RR 1,09 | 87,5% | 78,1% | 75,1% |
| | C: WR %35, RR 2,29 (yüksek varyans) | 70,3% | 55,1% | 51,4% |
| 500$ (%1; 4R alan) | A | 83,6% | 70,0% | 65,7% |
| | B | 73,5% | 61,2% | 55,1% |
| | C | 56,3% | 45,3% | 40,1% |
| 1000$ (%2; 2R alan) | A | 66,9% | 56,4% | 48,2% |
| | B | 59,5% | 51,0% | 43,8% |
| | C | 43,9% | 40,1% | 35,0% |

Çıkarımlar:
1. **Dar challenge'da düşük varyans kazanır.** Kişisel hesapta soru "Bu para kazandırır mı?" iken prop'ta soru "Hedefe zarar sınırından **önce** ulaşır mı?" Yüksek RR / düşük WR stratejisi kârlı olsa bile kayıpları önce gelirse hesap ölür.
2. **Trailing drawdown** (özellikle gün içi, en yüksek özsermayeyi takip eden) geçme oranını **10-20 puan** düşürür. Gün sonu trailing daha affedicidir. Çoğu futures prop'ta trailing, taban başlangıç bakiyesine ulaşınca durur (ör. 52k'da durur).
3. Pozitif EV'de **küçük risk** (≥8R alan) geçme oranını en çok artırır. Ama süre sınırı ve aşırı küçük risk "zaman aşımı" riskini büyütür (bkz. §1).
4. **Kurallar katman katman geçme oranını düşürür**: maksimum zarar → günlük zarar → trailing → tutarlılık kuralı (consistency) → minimum gün, haber yasağı vb. Kişisel hesapta kârlı bir strateji fonlu hesapta başarısız olabilir.
5. **Sıra önemlidir** (Mulham): Aynı 10 işlem, 6 kazanç ve 4 kayıp. Kazançlar önce gelirse geçer, kayıplar önce gelirse kalır. Backtest'teki güzel eğri olası sıralamalardan sadece biri. Monte Carlo ile **kötü sıralamada da hayatta kalıyor musun** diye sor.
6. Belirli bir 4 işlemlik grubun tamamen kayıp olma ihtimali `(1-WR)^4`: WR %45 → %9,2, %55 → %4,1, %65 → %1,5. Ama 100 işlemde **en az bir** uzun seri görme ihtimali çok daha yüksek (01 §5).

**Tutarlılık kuralı (consistency) etkisi** (ImanTrading): %50 tutarlılık kuralında tek günün kârı toplam kârın yarısını geçemez → 3.000$ hedef en az 2 günde (≥1.500$/gün) tamamlanmalı. Avantajsız ve "tüm drawdown'u stop olarak kullanan" bir modelde tek işlemin kazanma ihtimali 2000/(2000+1500) = %57,14, iki gün üst üste = **%32,65**. 25k / 1.250 DD / 1.500 hedef hesapta %62,5² = **%39,06**. Matematik doğru, bkz. §5 uyarıları.

**Fiyat/değer metriği** (ImanTrading): `Değerlendirme ücreti / maksimum zarar × 100` = her 100$ "gerçek fon" için ödenen ücret. Sadece **aynı kurallı, aynı plandaki** hesap boyutlarını karşılaştırmak için kullan. Hesabın "kolaylığı" için `Maksimum zarar / Hedef` oranına bak: büyükse daha kolay (50k: 0,67; bazı 25k: 0,83; 150k 4,5k/9k: 0,5).

## 1c. Gerçek getiri hunisi: ödeme ekran görüntüsü yalan söylemez ama eksik söyler (Mulham)

Örnek: 100 challenge × 150$ = **15.000$**. 86'sı değerlendirmede kalır, 14'ü fonlanır, 8'i hiç ödeme almaz, **6'sı** 2.000$ ödeme alır = **12.000$**. Net **-3.000$** (challenge başına -30$). "6 ödeme olmasına rağmen grup para kaybetti."
- **Senin sorman gereken tek soru**: "Bu boyutta, bu kurallar içinde işlem yapılan stratejim, **tüm denemelerin maliyetini karşılayıp** üstüne para bırakacak kadar ödeme üretiyor mu?"
- Kendi hunini takip et: satın alınan challenge sayısı ve toplam ücret, geçenler, fonlu hesapta ödemeye ulaşanlar, toplam ödeme. Net sonuç = ödemeler − tüm ücretler (aktivasyon ücreti, reset ücretleri dahil).

**Sektör çapında veri (Finance Magnates, ~300.000 hesap, firmalar arası analiz):** Trader'ların **%14**'ü challenge'ı geçip fonlu hesaba ulaşıyor. Bunların **~%45**'i ödeme alıyor → tüm trader'ların yalnızca **~%7**'si ödeme alıyor. Bu veri bağımsız denetimden geçmiş değil. **FTMO resmi bir aşama bazlı geçme oranı yayımlamıyor**, dolaşımdaki "FTMO %10-12" rakamları topluluk tahminleri. Aynı firmanın geçme oranı "kombine sayısına mı kişiye mi bakıyorsun" sorusuna göre %17 ile %52 arasında değişebiliyor. Kaynaklar: [Finance Magnates](https://financemagnates.com/forex/analysis/exclusive-only-7-of-300000-prop-trading-accounts-achieved-payouts), [TradeInformer: FTMO finansalları](https://tradeinformer.com/prop-weekly/what-ftmo-tells-us-about-prop-firm-finances), [thepropfirmguide](https://thepropfirmguide.com/prop-firm-statistics/). → Mulham'ın 100'de 6 ödeme örneği (%6) bu %7 ile **tutarlı**.

## 1d. Optimal risk ancak FONLU AŞAMA dahil hesaplanırsa anlam kazanır (SharpeEdge + Photon + `arastirma/verify_optimal_risk_ev.py`)

**Çatışma:** Photon Trading (QtdcgmLsoBI): "%0,5 ile %98 geçersin ama 100-150 işlem (7-12 ay) sürer. %3 ile %50-67 geçersin ama 1-3 ayda fonlanırsın → **agresif ol**." SharpeEdge (DTVjwgob_E8): "Kaldıracı 10'a çıkarınca 3 günde geçip 5 günde kaybediyorsun, ödeme 0, EV negatif. 1 yıllık EV kaldıraç 2-3'te maksimum."

**Kendi modelim**: FTMO tipi 2 faz (+%10, +%5), %10 statik maksimum zarar, %5 günlük zarar, 500$ ücret (ilk ödemede iade), fonlu hesapta ~ayda bir (10 işlemde bir) %80 kâr payı ödemesi ve bakiyenin 100k'ya dönmesi, hesap kaybedilirse yeni challenge. Yılda 120 işlem (ayda ~10, Photon'un varsayımı). 6.000 deneme.

| Risk/işlem | İyi avantaj WR40/2R (+0,2R), günde 1 işlem: ortalama net / zararda biten | Aynı strateji **günde 2 işlem** | Canlıda WR 5 puan düşük (WR35, +0,05R) | Maliyet sonrası avantajsız (WR30, -0,1R) |
|---|---|---|---|---|
| %0,25 | -481$ / %99 | -485$ / %99 | -501$ / %100 | -522$ / %100 |
| %0,5 | +1.119$ / %66 | +1.032$ / %67 | -343$ / %93 | -742$ / %100 |
| **%1** | **+9.654$ / %23** | +8.648$ / %24 | +2.159$ / %61 | -839$ / %90 |
| %1,5 | +17.727$ / %13 | +15.870$ / %12 | +5.620$ / %44 | -420$ / %79 |
| **%2** | **+26.623$ / %7** | **+24.777$ / %7** | +10.073$ / %32 | +712$ / %66 |
| %3 | +46.551$ / %4 | **-1.155$ / %63** | +20.859$ / %18 | +5.243$ / %50 (medyan +300$) |
| %5 | -36.417$ / %100 | -29.883$ / %92 | -39.508$ / %100 | -42.516$ / %100 |

**Yorum, dikkatli oku:**
1. **Çok küçük risk (≤%0,5) ayda ~10 işlemle zaman kaybettirir**: bir yılda nadiren fonlanırsın. Photon'un "zaman maliyeti" argümanı **doğru**.
2. **%1-2 risk, avantajı olan biri için en sağlam bölge**: işlem sıklığı değişse bile (günde 1 ya da 2) sonuç bozulmuyor.
3. **%3 sadece günde ≤1 işlem varsa iyi, bu da kırılgan**. Günde 2 işlemde iki kayıp = %6 > %5 günlük limit → ortalama zarara döner (%63'ü zararda). Photon'un hesap makinesinde günlük limit yok, bu yüzden %3+ önerisi FTMO tipi günlük limitli hesaplarda **eksik ve tehlikeli**. %5: her tek kayıp günlük limiti patlatır.
4. SharpeEdge'in bulgusuyla uyumlu: optimum **"orta"** risk (temel riskin 2-3 katına kadar), aşırı agresif risk fonlu aşamayı öldürür.
5. ⚠️ **Model iyimser**: işlem maliyeti, kayma, tutarlılık kuralı, minimum gün, ödeme reddi, kural değişiklikleri ve davranışsal bozulma (tilt) **yok**. Bu yüzden negatif avantajlı bir trader bile %3'te "ortalama" pozitif görünüyor. Bu, firmanın zarar tarafını ücret karşılığında üstlenmesinden doğan **opsiyon benzeri çarpık getiri**. Ama aynı satırda **trader'ların yarısı zararda**, medyan +300$. Ortalama nadir büyük ödemelerle şişiyor. Gerçek dünyadaki huni (Mulham: 100 challenge'dan 6 ödeme, grup zararda) bu modelden daha güvenilir. **Bu tablo "avantajsız da kazanırsın" demek değil, riskin fonlu aşamadaki etkisini göstermek içindir.**
6. Photon'un doğru uyarıları: (a) **canlı WR'ı backtest'ten 5-10 puan düşük varsay** (tablo: WR 5 puan düşünce %1 risk +9.654$'dan +2.159$'a iniyor); (b) ≥%3 risk alıyorsan **en az 3 deneme bütçele**; (c) **challenge ortasında riski değiştirme** (hedefe yaklaşınca artırmak ya da düşüşte paniğe kapılıp %0,25'e inmek).

**SharpeEdge'in yöntem dersleri (kendi verinle uygulanacak):**
- Simülasyonu **işlem sonuçlarıyla değil, mum bazlı getirilerle** yap. Bir işlem sonunda +2R kapansa bile içinde -0,9R'lik bir düşüş (MAE) yaşadıysa, o düşüş günlük ya da maksimum zarar limitini ihlal edebilir. Toplam işlem getirisi bunu gizler. → Replay uygulamanda **her işlemin MAE'sini** kaydet.
- **Blok bootstrap Monte Carlo**: getirilerin ardışık bloklarını örnekleyerek binlerce alternatif yol üret. Bu yöntem çarpıklık, basıklık, otokorelasyon ve rejim davranışını korur (i.i.d. yazı-tura modelinden daha gerçekçi).
- **Örneklem dışı (out-of-sample) getiri kullan**: optimize ettiğin dönemin getirileriyle simüle edersen sonuçlar şişer.
- Metrikler:
  - `P(geçme)`
  - `EV/challenge = P(geçme) × E[ödeme] − ücret × (1 − P(geçme)) − aylık maliyetler` (ücret geçince iade ediliyorsa)
  - `Geçme maliyeti = (ücret + aylık maliyet) / P(geçme)`
  - `Verimlilik = EV / geçme maliyeti`
  - `P(iflas) = (1 − P(geçme))^(bütçe / ücret)`
- Fonlu aşamada "bu hesap patlamadan önce ne kadar para çekebilirim?" sorusu ve ödeme zamanlaması (aylık, en erken fonlanmadan 1 ay sonra) modellenmeli.
- SharpeEdge'in kendi stratejisi (%1 risk): %84 geçme, ortalama 130 günde fonlanma. Kaldıraç 2'de ~%85 geçme, 67 gün. Kaldıraç 10'da %36 geçme ve hesap ortalama 2 gün yaşıyor.

**FTMO'nun resmi önerisi** (Kbb8FiKUXnE, firma kaynağı, çıkar çatışmasını göz önünde tut):
- Risk **%0,5-1,5**. Scalper (günde ~5 işlem) **%0,25-0,5**. Swing (haftada 1-2 setup) %1-1,5.
- %2 riskle 5 ardışık kayıp = %10 = 2 aşamalı challenge'ın maksimum zararı.
- Plan **9-10 ardışık kaybı** maksimum zarar limitine değmeden kaldırmalı (yani %10 limitte ≤%1 risk).
- "%60 WR'da bile 4'lü kayıp serisi ihtimali %70": işlem sayısı belirtilmemiş. Kendi hesabım: 50 işlemde %54, 100 işlemde %80. Yani ~75 işlem için doğru.
- "Günlük zarar limiti güvenlik ağı değil, katı bir limit. Planın ona **yaklaşmamak** üzerine kurulmalı."

## 1e. Pratik risk formülleri ve geçme süresi (Wilksey, Kimmel Trading + `arastirma/verify_round3.py`)

**Beklenen geçme süresi** (Wilksey, mEnKHRWvzl4): `Beklenen işlem ≈ Hedef (R) / EV (R)`. Örnek: EV +0,2R ve %1 risk (hedef 10R) → ~50 işlem. "Phase 1'de 6-12 ay takılanların sebebi bu."
- ⚠️ İncelik (simülasyonla doğrulandı): Bu formül sınırsız zamandaki ortalamadır. **Geçenlerin** ortalama işlem sayısı daha düşüktür, çünkü geçen yollar şanslı yollardır.
- WR %30, RR 3 (+0,2R), +%10 / -%10 statik:

| Risk | Geçme | Geçenlerde ortalama işlem | Medyan |
|---|---|---|---|
| %1 (10R/10R) | **%77,7** | 30 | 22 |
| %2 (5R/5R) | **%63,5** | 8,4 | 6 |

Wilksey'nin iddiası (%77 / %63, ~30 / ~10 işlem) **birebir doğrulandı**. "Riski ikiye katlamak hesap kaybetme ihtimalini ikiye katlamaz. Risk sınır olasılığını değiştirir, **avantajı değil**."

**Kimmel'in formülleri** (NZfUe30eUMs):
- "Konservatif" %0,25: 10% limitte 40 ardışık kayıp gerekir. Ama FTMO phase 1 için 40R kazanmak gerekir → aylarca sürer. Kimmel de önermiyor: "Bu kadar düşük risk istiyorsan hesap boyutun ya çok büyük ya da stratejine güvenmiyorsun → **hesabı küçült**."
- "**Normal**": `risk = (maksimum zarar / 2) / haftalık işlem sayısı`. Hesabı kaybetmek için **2 hafta boyunca tüm işlemlerin** kaybetmesi gerekir. FTMO %10, haftada 5 işlem → %1; 10 işlem → %0,5; 3 işlem → %1,67. Hiç trading'den para kazanmadıysan **en fazla %1**.
  - ⚠️ Simülasyon (%1 risk, hedef 10R): hesap kaybetme ihtimali WR %30/RR3 → **%22**, WR %40/RR2 → **%13**, WR %50/RR1,5 → %3,4, WR %55/RR1,2 → %2,5. "Kârlı trader 2 hafta üst üste kaybetmez" varsayımı **düşük WR'lı stratejilerde tutmaz**.
- "**Agresif**": `risk = (günlük limit − %1-2 tampon) / günlük işlem sayısı`. FTMO %5, 2 işlem/gün → (5−2)/2 = %1,5. Bu yapısal olarak doğru bir kural: **risk × günlük maksimum işlem sayısı < günlük limit − tampon** (§1d'deki "%3 günde 2 işlemde çöker" bulgusunun çözümü). Kimmel'e göre sadece uzun süredir kârlı, birden fazla ödeme almış, başka geliri olan ve küçük hesap boyutunda işlem yapanlar için.
- "**Kârlı değilsen prop firm'e gitme.** Kârlı trader'ların ödemelerini sağlayan likidite olursun." (DD Finance, Brandt ve Beggs ile tutarlı.)

**Risk = yerine koyma maliyeti, ego değil** (Wilksey):
- **Çekirdek hesaplar**: en güvendiğin, uzun vadeli, pahalı ve zor firmalar. Kaybedersen en zor challenge'a geri dönersin. → **%0,3-0,75** risk (en güvenlisi %0,5). Amaç ödeme sürekliliği: "%1-2 al, tekrarla."
- **"Çekim" hesapları**: ucuz, kolay değiştirilebilir hesaplar. → %1-1,5 risk, daha büyük ama daha seyrek ödemeler.
- ⚠️ Bu bilgi tabanının notu: "Ucuz / yeni / itibarı oturmamış firma" ödeme reddi ve batma riski taşır (Diamant ve Dante'nin de uyarısı). Bu ayrım ancak **avantajı kanıtlanmış** bir trader için mantıklı. Yeni başlayan için tek ve güvenilir bir firmada %0,5-1 daha sağlıklı.

## 1f. Kurala bağlı dinamik risk: düşüşte azalt (Kimmel'in "Top 5" videosu + `arastirma/verify_dynamic_risk.py`)

Videodaki öneriler (cUMPvlLtArM, ödeme iddiaları doğrulanmamış):
- **Kyle**: "Başlangıç bakiyesine göre neredesin? Kaybedersen riski yarıya indir. Kazanırsan aynı tut ya da ikiye katla. Düşüşte riski azaltmak özsermaye eğrisini düzleştirir ve A+ setup'ları bulana kadar hayatta kalmanı sağlar."
- **Dan Chong**: "Önce **kavram kanıtı**: backtest ve örneklem testleriyle avantajını kanıtla. En kötü şey, işe yaramayan bir stratejiyle **şans eseri** kazanıp ödeme almak ve sonraki 5 yılı aynı şeyi yaparak geçirmektir. 4+ kayıptan sonra riski düşür, başa başa dönünce geri yükle."
- **Paladin** (bir prop firmanın, SFT'nin kurucu ortağı → çıkar çatışması): "Tepedekilerin %2-3 riskini kopyalama. Challenge'ı maaşınla alıyorsan %0,5-1 risk."
- **Pasquali**: "Sabır. 3-5 yıllık bir kariyer gibi gör. Bir günde geçmeye çalışanlar aşırı kaldıraç kullanıyor. Daha yüksek zaman dilimi zihnini sakinleştirir."
- **Andrew NFX**: "%4-4,5 risk, tek ya da iki işlemde geç, 4 hesap al." → **Firmaların çoğundan banlanmış**. Hayatta kalan yanlılığına örnek, takip etme (§4b).

**Simülasyon** (phase 1: +%10 / -%10 statik, temel risk %1, 300 işlem sınırı, 30.000 deneme):

| Strateji | Sabit %1 | Başlangıcın altındaysa %0,5 (Kyle) | Her kayıpta yarıya, kazançta %1'e dön | ≥4 ardışık kayıpta %0,5, başa başta %1 (Dan) | Üstteyken %2, alttayken %0,5 |
|---|---|---|---|---|---|
| WR %30 / RR 3 (+0,2R) | %77,6 (medyan 22 işlem) | **%88,6** (38) | %86,2 (56) | %86,2 (33) | %83,5 (31) |
| WR %40 / RR 2 (+0,2R) | %87,6 (29) | **%95,3** (42) | %92,6 (58) | %94,4 (39) | %93,2 (33) |
| WR %55 / RR 1,2 (+0,21R) | %97,5 (38) | %99,4 (47) | %98,6 (55) | %99,4 (41) | %98,7 (33) |
| WR %33 / RR 2 (avantajsız) | %46,5 | %42,9 | %42,2 | %44,0 | %43,6 |

**Çıkarımlar:**
1. **Avantaj varsa**, düşüşte riski kurala bağlı azaltmak hesap kaybetme oranını **yarıya veya daha aşağıya** indiriyor (WR %40: %12,4 → %3,6). Sebep: challenge bir bariyer problemi. Tabana yaklaşınca küçük risk sana daha fazla R cinsinden "alan" verir, pozitif sürüklenme de gerisini yapar.
2. **Bedeli zaman**: medyan işlem sayısı ~%30-90 artıyor. En iyi denge **"≥4 ardışık kayıpta riski yarıya indir, başa başa dönünce geri yükle"** (Dan Chong'un kuralı): geçme oranı yüksek, süre artışı küçük.
3. **Avantaj yoksa hiçbir boyutlandırma kuralı işe yaramıyor** (~%43-46). Pozisyon boyutu avantaj **yaratmaz**, sadece dağılımı değiştirir.
4. **Photon'un "challenge ortasında riski değiştirme" uyarısıyla çelişmiyor**. Ayrım şu: **önceden yazılmış, mekanik** bir risk merdiveni iyi. Korkuyla, hırsla ya da "hedefe yaklaştım" düşüncesiyle anlık değiştirmek kötü. Kuralı plana yaz (03) ve replay'de test et.

## 2. Çıkarımlar

1. **Challenge geçmek bir şey kanıtlamaz.** Avantajı SIFIR olan biri %1-2 riskle ~%45 ihtimalle geçiyor. "Geçtim, demek ki stratejim çalışıyor" = yanılgı. Kanıt, funded aşamada ve **yüzlerce işlemlik** R-kaydında.
2. **Avantajın varsa ideal risk ~%1** (bu kurallar altında). %0.5 çok yavaş (süre dolma), %2+ maks. zarar riskini büyütür.
3. **%3+ risk + günde 2 işlem = günlük limit katili.** İki kayıp = −%6 > −%5. Risk/işlem × günlük maks. işlem sayısı < günlük limit olmalı.
4. **Avantajın yoksa risk artırmak geçme şansını biraz artırır** (%43→%47) — bu yüzden "full port at, kaybedersen sadece fee gider" stratejisi kumar mantığıdır: prop firmalar bu davranıştan para kazanır.
5. "Challenge al, kaybet, yenisini al, sonunda geçersin" (Yusuf Trades röportajı) = **negatif/sıfır EV'li biri için kumar**, pozitif EV'li biri için ise maliyet. Fark: senin R-kaydın.
6. **Gerçek veriyle kanıtlanmış ama küçük bir avantaj da challenge'ı kurtarmaz** (⚠️ 36. tur: bu pullback avantajı 2015 sonrası rastgele girişten ayırt edilemiyor, 04 §5b) (`arastirma/verify_pullback_portfolio.py`, 04 §5b). Bu bilgi tabanının sembol dışında tekrarlanan tek avantajı endekslerdeki pullback long'u (işlem başı +0,1 ile +0,18R, yılda ~35 alınan işlem). 241 farklı başlangıç tarihiyle FTMO tipi kurallarda denendi: %1 statik riskte **%48 geçti, %25 kaldı, %27'si 1 yılda bitmedi**. Aynı sayıda rastgele long girişte sırasıyla %56 / %24 / %20. Yani avantajı olmayan referansla (~%50) aynı. **Challenge'ı geçmek için gereken yıllık R = hedef / risk.** %10 hedef ve %1 risk için 10R gerekiyor. İşlem başı +0,1R'lik bir sistem bunun için ~100 işlem ister. Yılda 35 işlemle 3 yıl eder. → Prop için bir setup seçerken **işlem başı R × yıllık işlem sayısı ≥ 10-15R/yıl** olmalı. Korelasyonlu işlemleri tek işlem say. Gün içi sıklık bunu sağlayabilir, ama maliyeti R cinsinden hesapla (04 §5b: 1 saatlik FX'te ~0,10R).
7. **✔ Çok piyasalı swing portföyü: bu bilgi tabanının ilk olumlu prop tablosu** (25. tur, `arastirma/verify_multiasset_portfolio.py`, 2009+, maliyetli, günlük piyasa değerlemesi). Kurulum:
   - **Kollar**: (EQ) SPY/QQQ RSI-2 long. (CMD) 8 emtia ETF'inde 20 günlük kırılım + Brandt 3 günlük trailing. (RATES) TLT/IEF kırılım + 10 günlük dip stopu. (FX) 6 majör parite, aynı kural.
   - **Risk sınırları**: kol başına en fazla 2r, toplamda en fazla 6r açık risk.

   | Kol | Yılda işlem | Ortalama R | R/yıl (sınırlardan önce) |
   |---|---|---|---|
   | EQ | 18 | +0,18 | +3,2 |
   | **CMD** | 113 | +0,12 | **+13,8** |
   | RATES | 30 | -0,07 | -2,0 |
   | FX | 55 | -0,07 | -4,0 |

   Kollar arası aylık R korelasyonu -0,18 ile +0,35, yani gerçekten ilişkisiz.

   | Portföy (iki aşamalı challenge) | Risk | 1 yıl süreyle: geçti / kaldı / bitmedi | **3 yıl süreyle: geçti / kaldı** | İki aşamayı geçme süresi (medyan) | Yıllık getiri / maksimum düşüş |
   |---|---|---|---|---|---|
   | Dört kol birlikte | %1 | %20 / **%80** / %0 | — | — | %9,3 / %39 |
   | **EQ + CMD** | **%0,5** | %31 / %2 / %67 | **%93 / %7** | **~750 gün** | %4,8 / %14 |
   | EQ + CMD | %0,75 | %51 / %22 / %27 | %69 / %31 | ~426 gün | %6,9 / %21 |
   | Sadece CMD | %0,5 | %29 / %6 / %66 | %64 / %26 | ~560 gün | %5,0 / %15 |
   | *Avantajı olmayan referans* | | | *~%32* | | |

   **Dersler:**
   - (a) **R/yıl tek başına yetmez, düşüş derinliği de önemli.** Emtia kolu yılda ~14R üretiyor, ama trend takibinin uzun kayıp serileri %1 riskte %33 düşüş yaratıyor ve %10 zarar sınırını deliyor. Challenge'ı geçmenin ölçüsü **"getiri / maksimum düşüş" (Calmar benzeri)**. Brandt'ın "en kötü kayıp" ve "kazanç/acı oranı" metrikleri bu yüzden önemli (10 §6b).
   - (b) **Negatif kolları eklemek çeşitlendirme değil, zarar.** Dört kol birlikte %1 riskte %80 kalıyor. Kollar ilişkisiz ama ikisinin beklentisi negatif. Ayrıca toplam açık risk 6r'ye kadar çıkınca kötü bir günde **günlük %5 limiti** tetikleniyor.
   - (c) **Kazanan formül: gerçek avantaj + düşük risk + zaman.** %0,5 risk ve sadece pozitif kollarla geçme ihtimali %93, ama **~2 yıl** sürüyor. Fonlu aşamada beklenti yıllık ~%5 (%0,5 risk) ile ~%7 (%0,75 risk). Bu, "ayda %10" pazarlamasından çok uzak, ama gerçekçi. Hertzberg'in "kalıcı olanlar dünyayı yakmıyor" tespitiyle (§4h) ve SharpeEdge'in fonlu aşama bulgusuyla (§1d) uyumlu.
   - (d) **⚠️ Seçim yanlılığı**: EQ ve CMD, RATES ve FX'in negatif çıktığı **görüldükten sonra** seçildi. CMD'nin kuralı da bu bilgi tabanının kendi 2005+ verisinde bulunmuştu, yani sembol dışı değil. Gerçek beklenti tablodakinden düşüktür. EQ (RSI-2) ise yayımlandıktan sonraki bir dönemde test edildiği için daha güvenilir.
   - (e) **Pratik engeller**:
     - Futures prop firmalarının çoğu gece pozisyonu yasaklıyor, swing burada imkânsız.
     - CFD firmalarında (FTMO vb.) emtia sepeti sınırlı: DBA ve CPER gibi tarım ve bakır ETF'lerinin karşılığı olmayabilir.
     - Haftalarca tutulan pozisyonlarda gecelik swap maliyeti var, testte yok.
     - Hafta sonu taşıma kuralı firmaya ve hesap tipine göre değişiyor.
     - → Bu portföyü uygulamadan önce **kendi firmanın ürün listesi ve swap'larıyla** yeniden test et.

## 3. Pratik kurallar (FTMO tarzı hesaplar için)

- Risk/işlem: **%0.5–1** (başlangıç bakiyesinin).
- Günlük kendi limitin firmanın limitinden **sıkı** olsun: örn. firma −%5 → sen −%2 (2 kayıp) ve dur.
- Maks. zarara yaklaşınca riski **düşür** (örn. −%6'dan sonra %0.5'e in), artırma.
- Hedefe yaklaşınca da riski düşürmek mantıklı (kalan mesafe küçük, kayıp asimetrik).
- Haber saatleri, hafta sonu tutma, lot limitleri, "tutarlılık kuralı" gibi firma kurallarını önceden oku — çoğu hesap strateji yüzünden değil **kural ihlali** yüzünden kaybedilir.
- Küçük hesapla başla (10k), kanıtla, sonra büyü (röportajdaki doğru tavsiye). Büyük hesap → psikolojik baskı → kural ihlali.

## 4. Sektör uyarıları (2024–2026)

- Röportajdaki iddia: 2024'te MetaQuotes'un bazı prop firmalara lisansı kesmesiyle birçok CFD prop firma kapandı; firmalar "çok vaat edip az ödüyor". Firma seçerken: ödeme geçmişi, şirket yaşı, düzenleyici yapı, Trustpilot değil **bağımsız** ödeme kanıtları.
- Futures prop'larda (Topstep vb.) "live'a geçirme", hesap kapatma gibi kural değişiklikleri olabiliyor.
- YouTube'daki prop firm röportajları çoğunlukla **sponsorlu/affiliate** — kazanç iddiaları doğrulanmamış, kaybedenler video çekmez (hayatta kalan yanlılığı).

## 4b. "Tam agresyon" ve Martingale'e dayalı challenge yaklaşımlarının analizi (ImanTrading, _DvBJEbYR2U)

Videonun tezi: "Değerlendirme gerçek hesap değil, 80$'lık bir masraf. Maksimum agresyon (tüm drawdown'u stop olarak kullanmak) rastgele işlemlerle bile yavaş yaklaşımdan daha iyi geçme oranı verir. Büyük kazananlar ya 2 günde geçiyor ya da yeni hesap alıyor."

| Doğru olan | Neden dikkatli olmalısın |
|---|---|
| Avantaj sıfırsa tam agresyon geçme oranını maksimize eder (yukarıdaki matematik) | Bu **trading becerisi değil**, firmanın fiyatlamasına karşı bir bahis. Senin hedefin trader olmaksa (14) seni hiçbir şey öğretmeden yakar |
| Değerlendirme ücreti sınırlı bir kayıptır | Firmalar buna karşılık veriyor (videonun kendi itirafı): "sorumlu trader programları" (aylık hesap sınırı), tutarlılık kuralları, ödeme tamponları, aktivasyon ücretleri, ödeme öncesi (AI) mülakatlar, değerlendirmede izin verip fonlu hesapta Martingale/haber kumarını yasaklama. → **Ödeme reddi riski**. "Ödemenin reddedilmesi aklımdan bile geçmemeli" (Iman'ın kendi sözü) |
| Martingale "sonuçların dağılımını değiştirir, avantaj yaratmaz" | Kişisel hesapta yıkıcı. Fonlu hesapta çoğu firmada **yasak**. Psikolojik olarak "kaybını geri alma" refleksini besler (08) |
| "Zarar sınırına 100$ kaldıysa büyük haberde yazı-tura at" (asimetrik bahis) | Saf kumar. Birçok firmada haber yasağı var. Bu bilgi tabanının disiplin ilkeleriyle çelişir → **önerilmez** |
| Büyük kazananlar en çok harcayanlar, "harcama-ödeme farkı" önemli | Hayatta kalan yanlılığı: Discord'da "doğrulanmış ödeme alanlar" görünür, çok harcayıp hiç alamayanlar görünmez. Mulham'ın hunisinde grup **zararda** (§1c) |

**Iman'ın videosundaki sağlam pratik tavsiyeler** (alınabilir):
- **Hazır olana kadar hiçbir şey satın alma**, ücretsiz simde öğren.
- **Küçük başla** (25k). İlk ödemeni almadan pahalı planlara (günlük ödeme, yüksek getiri) geçme. İlk ödemeden önce kâr payı oranı (%80 / %90) öncelik değil.
- **Aylık değerlendirme bütçesi** koy. Tilt halinde arka arkaya reset satın alma tuzağı gerçek. "Umutsuzluk, öfke, üzüntü ya da coşku anında kendine güvenme."
- **Fonlu hesaba girmeden önce ödeme planını yaz**: hemen maksimum ödeme mi, hesabı büyütmek mi? (Duygusal öngörü hatası: "+1.000$ ya da -1.000$'dayken ne hissedeceğini bilemezsin.") Iman ilk ödemede çekebildiği kadarını çekmiş, sonra büyütmeye geçmiş.
- Günlük maksimum zarar eşiğini kendi verinle bul ("Belli bir günlük kayıptan sonra toparlamaktan çok daha fazla kaybetme eğilimindeydim").
- Yeni ve küçük, kötü itibarlı firmalardan kaçın: "Ödemen reddedilirse kolaylığın bir anlamı yok."
- Gerçekçilik: Iman'ın Discord'unda işi olmayan kârlı trader'lar neredeyse sadece **üniversite öğrencileri**. Iman'ın kendi canlı hesap toplamı ~10.000$. "Başarı bir kursta satın alınamaz."
- ⚠️ Çıkar çatışması: Iman kendi sitesinde firmaları sıralıyor ve affiliate indirim kodu kullandırıyor.

**Bu bilgi tabanının tavsiyesi:** Prop firmayı **kanıtlanmış pozitif EV'li bir sistemi** düşük maliyetle sermayeye çevirmek için kullan (%0,5-1 risk, düşük varyanslı uygulama, tüm kurallara uyum). "Avantajsız challenge kumarı" ile trader olunmaz. Firmalar kuralları zaten buna göre değiştiriyor.

## 4c. Trailing drawdown mekaniği: gün sonu vs gün içi (Kejvi Dema, t4PFBbaZF4I)

| | **Gün sonu (EOD) trailing** | **Gün içi (intraday) trailing** |
|---|---|---|
| Neyi takip eder | **Gerçekleşmiş** kapanış bakiyesini | **Gerçekleşmemiş** özsermayeyi, tick tick |
| Ne zaman güncellenir | Günde 1 kez, seans bitince (genelde 16:15 NY) | Sürekli, işlem açıkken bile |
| Aşağı iner mi | Hayır (sadece yukarı ya da sabit) | Hayır |
| Nerede durur | Genelde **başlangıç bakiyesinde** (ya da +100$) kilitlenir | Aynı |
| Fiyat | **Daha pahalı** | Daha ucuz |
| Kime uygun | Kazananları uzun tutan, swing yapan | Scalper (daha az zarar görür) |

- **Taban delinirse açık pozisyonlar hemen tasfiye edilir**, kapanış beklenmez.
- **Kritik örnek (50k, 2.000$ trailing)**: İşlem gün içinde +2.000$'a çıkıp +1.000$'da kapanırsa, gün içi trailing'de taban zirveyle birlikte 50.100$'a kilitlenmiştir. Kalan alan sadece **~900$**. Gün sonu trailing'de taban sadece 1.000$ yükselir (49.000$), alan **2.000$** kalır.
- **Çıkarım**: Gün içi trailing'de bir işlemin **MFE'si (maksimum lehte hareket) tabanı belirler**. Kârdan geri dönen her işlem alanını kalıcı olarak daraltır. → Gün içi trailing'li hesapta kısmi kâr al ya da kâr hedefini yakın tut. Replay uygulamanda her işlemin MFE ve MAE değerlerini kaydet ve trailing tipine göre simüle et (§1b'deki simülasyonda gün içi trailing geçme oranını en çok düşüren tipti).

## 4d. Ödeme reddi: kural riski ve korunma kontrol listesi (Blue Edge Financial DVniIqCxcxg, Day Trading & Jesus 7gxYw8aejS8)

**Teşvik uyumsuzluğu** (Blue Edge): Prop firmalar gelirlerinin büyük kısmını **challenge ücretlerinden** kazanır. Model, çoğu kişinin kaybetmesi üzerine kuruludur. Fonlu bir trader'ın büyük ödemeleri doğrudan bu gelirden çıkar → ödemeleri inceleme ve geciktirme için gerçek bir finansal baskı var. "Bu FTMO'yu dolandırıcı yapmaz, ama teşvik yapısı seninle tam uyumlu değil."

**Vaka 1: FTMO'nun belirsiz kuralı.** Reddit ve Facebook'taki raporlara göre (bunlar anekdot, doğrulanmadı) trader'lar "işlem başına %1 maksimum risk" gerekçesiyle ödeme reddi veya hesap kapatma aldı. FTMO'nun sitesinde %1 sadece "en iyi uygulama önerisi" olarak geçiyor. Yasaklı uygulamalar bölümündeki ifade şöyle: "gerçek piyasada makul şekilde tekrarlanamayacak uygulamalar, **diğer simüle işlemlerine göre belirgin şekilde daha büyük pozisyonlar** açmak dahil". "**Belirgin şekilde**" için eşik yok → takdir firmada, ve bu takdiri **sen işlemi yaptıktan ve ödeme istedikten sonra** kullanıyor.
- → **Pozisyon boyutunu tutarlı tut.** Tek bir işlemde normal boyutunun birkaç katına çıkmak, "tam agresyon" ve Martingale (§4b) sadece yasak kurallarla değil, bu belirsiz maddelerle de **ödeme reddi** riski taşır. §1f'deki "düşüşte riski yarıya indir" kuralı boyutu küçültür, büyütmez. Bu yüzden bu açıdan güvenli tarafta.

**Vaka 2: Apex'in ödeme dönemi mantığı** (Tyler, e-posta yazışmasından öğrendiği ve sitede yazmayan süreç; firmaya özgü, kurallar değişebilir):
- Ödeme talebi için **8 işlem günü** gerekiyor, bunların 5'i >50$ kârla kapanmalı. 50k hesapta bir tampon (buffer) bakiyesi var (videoda 52.600$).
- "**%30 kuralı**": açık bir işlemin gerçekleşmemiş zararı belirli bir eşiği (kâr bakiyesine göre %30) aşarsa "gelişigüzel / kumar tarzı işlem" sayılıp ödeme reddediliyor.
- Kural ihlali olan bir dönemin kârı, sonraki temiz döneme eklenip istenirse **o talep de reddediliyor**. Firma önceki döneme de bakıyor. Çözüm: Önce **sadece içinde bulunulan temiz dönemin** kârını iste. Onaydan sonra önceki ihlaller "sıfırlanıyor" ve birikmiş tutar çekilebiliyor.
- Ders: "Kuralları takip ettim ama reddedildim" şikâyetlerinin bir kısmı, **yazılı olmayan süreç mantığından** kaynaklanıyor. Her firmanın ödeme sürecini destek ekibine **yazılı olarak** sor.

**Firma seçmeden ve işlem yapmadan önce kontrol listesi** (Blue Edge + bu bilgi tabanı):
- [ ] **Yasaklı uygulamalar** sayfasını oku, sadece işlem hedeflerini değil. Dil ne kadar belirsizse firma o kadar takdir yetkisi saklıyor.
- [ ] Son 1-2 yılın **kural değişikliği kaydını** iste. Vermiyorlarsa kırmızı bayrak.
- [ ] Trustpilot'un **genel puanına değil son 30 yoruma** bak. Ödeme reddi şikâyetleri bir desen oluşturuyor mu?
- [ ] "Firma adı + payout denied" araması yap (Reddit, YouTube, X). Son dönemdeki desen önemli.
- [ ] **Tek firmaya bağımlı kalma**. Blue Edge kurucusu MyForexFunds kapanınca 4-5 hesabını birden kaybetti. Brandt da aracı kurumlar için aynı şeyi söylüyor (02 §6b).
- [ ] Ödeme sürecini (dönem uzunluğu, tampon, minimum gün, tutarlılık, haber ve gece taşıma kuralları) **yazılı olarak** teyit et.
- [ ] Pozisyon boyutunu ve stilini challenge ile fonlu hesap arasında **tutarlı** tut.
- ⚠️ Her iki video da kendi ürününü tanıtıyor (Blue Edge'in "Prop Farming Blueprint"i, Tyler'ın Apex affiliate kodu). "1.600 üye 100k+ fonlu" iddiası doğrulanmadı.
- **Fiyat hatası ve gecikme arbitrajı = yasaklı ve ödeme reddi sebebi.** Trader Dante (CWT 39) 2004-06'da spread-bet kurumlarının fiyat gecikmesinden (haberde bir kurum 6-8 sn geç fiyatlıyordu) ve algoritma hatalarından (sahte 1$'lık petrol sıçramaları) "bedava para" kazandığını anlatıyor. Kurumların biri kazancı **hesaptan geri aldı**, açıklar da kapatıldı. Dante: "Meşru bir strateji değil." Bugün prop firmaların yasaklı uygulamalar listesinde gecikme arbitrajı, fiyat beslemesi hatalarını sömürmek ve "gerçek piyasada tekrarlanamayan" işlemler açıkça yer alıyor. Simüle hesaptaki bir fiyat hatasından gelen kâr, **ödeme reddinin en net gerekçesidir**. Bir "açık" görürsen kâr değil hesap kaybı bekle.

## 4e. Tutarlılık kuralı (consistency) hesabı (Kimmel, oXCUgAmapr8)

- Tanım (futures prop'larda yaygın): Ödeme çekerken **en yüksek kârlı günün kârı, toplam kârın belirli bir yüzdesini geçemez**. Örnekler: MyFundedFutures %40, Apex %30 (oranlar değişebilir, güncel kuralı kontrol et).
- Formül: `Gereken toplam kâr = en büyük günün kârı / oran`. `Kalan gereken kâr = gereken toplam − mevcut toplam`.
  - Örnek: Toplam kâr 10.000$, en büyük gün 5.000$, oran %40 → gereken toplam 12.500$ → **2.500$ daha** kazanmalısın (o "büyük gün" seni kural dışına itti).
- Sonuç: **Tek bir büyük gün ödemeyi geciktirir.** Daha fazla işlem günü, daha fazla varyansa maruz kalmak demek. Pratikte günlük kârı da sınırlamak (örneğin günlük hedefe ulaşınca durmak) tutarlılık kuralını kolaylaştırır. Bu da prop hesapta "büyük günü uzatma" içgüdüsüne karşı bir argüman.
- Bazı firmalarda haftalık minimum işlem kuralı var (Kimmel tek micro kontratla işlem açıp bunu karşılıyor).
- Tutarlılık kuralı varsa ImanTrading'in "avantajsız tam agresyon" matematiği de değişir: tek günde hedefin tamamına ulaşmak yasak olduğu için en az 2 gün gerekir (§1b).

## 4f. Prop firm yerine ya da sonrası: yatırımcı sermayesi (Jason Graystone, vGammwZiyNk)

> Graystone prop firm challenge'larına eleştirel bakıyor. Kendi yazılımını (Trader Performance OS) tanıtıyor, ilkeler yine de sağlam.

- "**Sermaye trading becerisi yaratmaz.** Var olan becerinin finansal sonuçlarını büyütür." İyi süreç + daha fazla sermaye = fırsat. Kötü süreç + daha fazla sermaye = daha fazla paranın o sürece maruz kalması.
- **Gerçek bir işlem kaydı**: ekran görüntüleri değil, hatırladığın işlemlerin tablosu değil, ChatGPT ile mükemmelleştirilmiş bir backtest değil. Olması gerekenler: net tanımlı strateji, anlamlı örneklem, forward test, uygun olduğunda **bağımsız olarak doğrulanabilir** canlı kayıt. Metrikler: WR, ortalama kazanç ve kayıp, EV, DD, işlem sıklığı ve **kurallara uyum**. "Kârlı bir stratejiye sahip olmak ile kârlı bir stratejiyi uygulayabilen biri olmak arasında büyük fark var. Yatırımcı ikisiyle de ilgilenir."
- "**Haklı güven**": Kendi kanıtın olunca motivasyon videolarına ya da Lamborghini gösterenlere ihtiyacın kalmaz. "Kanıta dayalı güven ile umuda dayalı heyecan tamamen farklı."
- **Yatırımcı gibi düşün**: Yatırımcının ilk sorusu "%20 kazandırır mısın?" değil, "**Ne kadar kaybedebilirim?**" Tarihsel en kötü DD gelecekteki maksimum DD değildir. Senaryoları tarihsel en kötüden de kötü kur. "Sadece yukarı yönle ilgileniyorsan başkasının sermayesini yönetmeye hazır değilsin."
- **Sınırlar**: şeffaflık ile müdahale farklı şeyler. Yatırım yetki belgesi (mandate), belgelenmiş risk limitleri, raporlama takvimi, hangi koşulda işlem durur, fesih ve çekim koşulları. Strateji doğasına uygun bir yatırım ufku (örn. 2-3 yıl).
- **Yapı ve hukuk**:
  - **İşlem yetkisini saklamadan (custody) ayır.** Yatırımcının parası **kendi adına** hesapta kalsın, sen sadece tanımlı bir işlem yetkisiyle işlem yap. Asla kendi kişisel hesabına para aktarılmasın.
  - Birçok ülkede başkasının parasını ücret karşılığı yönetmek **lisans gerektiren** bir faaliyettir. Videodaki örnek İngiltere ve FCA. Türkiye'de portföy yönetimi SPK düzenlemesine tabidir (genel bilgi, bu oturumda ayrıca doğrulanmadı).
  - Yatırım teklifiyle insanlara yaklaşmak da "finansal tanıtım" kurallarına takılabilir. Bir sözleşme şablonu lisansın yerini tutmaz → **profesyonel hukuki danışmanlık** al.
- **Performans ücreti ve high-water mark** (hesabı doğruladım): 250k, 1. yıl +%12 → 30k kâr, %20 ücret = 6k → yatırımcı 274k. 2. yıl -%10 → 246,6k, **ücret yok**. 3. yıl +%18 → 290.988 → ücret sadece önceki zirvenin (274k) üstündeki 16.988'in %20'si = **~3.398** → yatırımcı ~287.590. "Yatırımcı kazanmadan sen kazanmazsın."
- **Sunum**: Kim olduğun, piyasalar, üst düzey yaklaşım, kanıt (özsermaye eğrisi, aylık sonuçlar, maksimum DD, ortalama risk, sıklık, **zorlanılan dönemler**), yapı, kimin varlıkları sakladığı, raporlama, ücretler, fesih. "En kötü kayıp dönemini açıklayabilen birine, sadece en iyi ayını anlatabilenden daha çok ilgi duyarım."
- **Gerçekçilik**: Kârlı herkes yatırımcı bulamaz. Stratejinin kapasitesi sınırlı olabilir, sonuçlar yeterince sağlam olmayabilir, hukuki ve operasyonel maliyetler işi ekonomik olmaktan çıkarabilir. "Dış sermaye, piyasanın sana kârlı olduğun için borçlu olduğu bir ödül değil."
- Bu bilgi tabanı için anlamı: Prop firm de yatırımcı da **önce kanıtlanmış bir R kaydı** ister. Replay ve günlük kayıtların (10, 13) bu kaydın temelidir.

## 4g. "17 milyon $ ödeme" roundtable'ı: futures prop pratiği (Words of Rizdom, ps5In64-2So, 2,5 saat)

> Konuklar: Trader Kane, Desi Trades, Vince (ilk 7 haneli futures prop ödemesi), JadeCap/Kyle (2,5 M$ rekor ödeme) ve iki trader daha. Ödemeler **kendi beyanları**. Panel tanım gereği kazananlardan oluşuyor (**hayatta kalma yanlılığı**). Sponsorlar Alpha Prime ve Tradezella. Bazı konuklar "kumar" pratiklerini açıkça savunuyor. → Kanal **SEÇİCİ**. Aşağıda kanıtla tutarlı olanlar ve uyarılar ayrıldı.

**Kanıtla tutarlı, uygulanabilir olanlar:**
- **Ortak payda strateji değil.** Hiçbiri belirli bir setup'ı başarı sebebi olarak göstermedi. Saydıkları şunlar: kendi verisi ("50 kayıpta bile modelimi değiştirmem, veri arkamda"), ısrar, düşüşte boyut küçültme kuralları, kişisel günlük zarar limiti. Bu, 08 ve 14 ile tutarlı.
- **Trailing drawdown varken tampon oluşana kadar küçük ve "hedeften önce" kapat.** Fiyat hedeften hemen önce dönerse trailing seviye yukarı çekilmiş kalır (§4c). Tampon oluşunca normal yönetime dön. Bir konuğun kuralı: "Hesabı patlatmadan önce kendine 5 işlem payı bırakırsan büyük ihtimalle patlatırsın." **Hesapla doğrulandı** (`arastirma/verify_streak_buffer.py`): %55 isabetle 100 işlemde en az bir **5'li kayıp serisi ihtimali %65**, 250 işlemde %93. 10'lu seri ihtimali %2-4. → **Tampon en az 10R** olmalı (isabet %45 ise 12R).
- **Kopya işlem = tek bahis.** 20 hesabı birbirine kopyalamak çeşitlendirme değildir. Kazancı da kaybı da ve **challenge ücretini 20 ile çarpar**. Örnek: Vince "20 hesap × günde 416$ = günde 8.333$, 120 günde 1 milyon" planını 82 günde tamamladığını söylüyor. Ama aynı panelden biri ödeme gününe 10 gün kala 20 hesapta +380k$'ı tek seferde kaybetti, bir diğeri ödemeden önceki iki günde ~1 M$ kaybetti. Konukların çoğu yeni başlayana **önce tek hesap, bir ödeme al, sonra büyüt** diyor. Bu, 14 §3f'deki "boyutu hak et" ilkesiyle aynı. Avantaj yoksa 20 hesap, beklenen kaybı 20 katına çıkarır (§1b).
- **Firma riskini dağıt.** Vince 8 firmada 8 ayrı kopya grubu kullanıyor, firmalar arasında kopya yapmıyor: "Bir firma batarsa yedisi devam eder." Bu §4d'deki "tek firmaya bağımlı kalma" maddesiyle aynı.
- **Kâr koruma kuralları** (konukların kişisel kuralları, test edilmedi):
  - Günlük zirveden %30 geri verince dur.
  - +400$'da, sonra +1.000$'da stopu kârı koruyacak yere çek.
  - Günde 2 kayıpta dur. 1 kazanç 1 kayıpta üçüncü işleme izin var.
  - "3 net kazanç ya da 3 net kayıpta dur": 3 net kayıp günlük zarar limitine denk.
  - Avantaj yokken bu kurallar beklentiyi değiştirmez (02 §4b'deki optional stopping). İşlevleri varyansı ve tilt'i sınırlamak. Önceden yazılı devre kesici olarak değerli (02 §7, §1f).
- **Zarara ortalama yapma (DCA) = fonlu hesapların bir numaralı ölüm sebebi** (Vince'in gözlemi). Başarılı trader'lar kazanana yapıyla ekliyor, yani yükselen bir dip oluşunca. Eklemeyi önce mikro kontratla öğreniyorlar. Bir konuğun yöntemi kırılımda 1 kontrat ekleyip stopu ortalama girişe çekmek: "eklenen risk sıfır". Bu, Brandt'ın piramit kurallarıyla tutarlı (03).
- **Büyük bir kazanç ya da kazanç serisinden sonra ara ver.** Neredeyse tüm konukların en büyük kayıpları **sıcak bir seriden hemen sonra** gelmiş. Desen hep aynı: aşırı güven → boyut büyütme → 2-3 büyük kayıp. Örnekler: "Günün erken saatindeki büyük kazanç benim için en kötüsü. Tampon var, trend var diye tekrar girdiğimde en kötü kayıplarımı aldım." "Dopaminim bu kadar fırlıyorsa boyutum fazla demektir." Çözüm: büyük kazançtan sonra ekrandan kalk, planlı tatil yap, ödemeyi **hesaptan çek** ve vergiyi ayır.
- **Güven derecelendirmesi** (bir konuğun yöneticisinden aktarılan anekdot): Veteran trader'lar işlemlerine 1-10 arası güven puanı vermiş. **10 verdikleri işlemler en kötü kaybedenleri arasında çıkmış.** Aşırı güven boyutu büyütüp tutma süresini uzatıyor. → **Günlükte güven puanı sütunu tut ve EV'yi güven gruplarına göre karşılaştır.** Dante'nin "sezgi boyutu" vakasıyla aynı mekanizma (02 §4c).
- **Yeni firma seçimi**: Kurallar "fazla kolay" görünüyorsa dikkat et. Yeni firmalar pazar payı kazanmak için başta ödeme yapar, sonra kuralları değiştirir. Örneğin bir firma "canlı hesap" verdi ama maksimum 2 mikro kontratla. **En az 6 ay bekle**, ödeme reddi şikâyetlerine ve müşteri desteğine bak, köklü firmalarla başla.
- **Kişisel canlı hesapta sadece bir günde kaldırabileceğin kadar para tut.** Örnek: bir konuk 500k$'lık hesapta 50 mini NQ ile zarardaki pozisyonu taşıdı, gün -130k$ kapandı. Sonra canlı futures hesabını 100k$ ile sınırladı. Bir başkası otel Wi-Fi'ında bağlantı kopunca ödemeye hazır 350k$'ı kaybetti. Ders: **altyapı riski**. Hız testi yap, kablolu bağlantı kullan, telefonda yedek erişim olsun.
- **Boyut toleransı kademeli büyür** ("spor salonu gibi"). Kişilik limiti gerçek, herkes 6 haneli riske uygun değil. "Biraz terletecek kadar ama günün geri kalanını mahvetmeyecek kadar."

**Uyarılar (kanıtsız veya bu bilgi tabanıyla çelişen):**
- "**Challenge'ları haber anında büyük boyutla geçiyorum**", "3.000$ koyarsam en az 30k$ çıkacağım garanti" (iki konuk). Hiçbir şey garanti değil. Haber anında büyük boyut varyansı artırır, avantaj eklemez. Avantaj yoksa geçme ihtimali ≈ DD/(DD+hedef) (§1b). Ayrıca birçok firma haber işlemini yasaklıyor ya da sınırlıyor, ve "kumar tarzı işlem" ödeme reddi sebebi (§4d, Apex'in %30 kuralı). Bunu yapanlar zaten kârlı ve ücreti "gözden çıkarılmış" sayan kişiler. Yeni başlayan için model olamaz.
- "**Tutarlılık kuralını yok say, ödemeyi geciktirip oran düşene kadar işlem yapmaya devam et**." Aynı panelde bunu yapan kişi oranı geri kazanmaya çalışırken 380k$ kaybetti. Kane ise kurala saygı duyuyor: "Tavanı olan bir hesapta günde 10k yapmak enerji israfı. Küçük ve düzenli kazanç al, devam et." §4e'deki hesap ve "boyutu tutarlı tut" kuralı geçerli.
- **Simülasyon dolumlarını sömürmek.** Örnek: sim hesapta tek kontratlık likiditeye 27 mini silver limit emri tamamen doluyor. Bu, gerçek piyasada tekrarlanamaz. §4d'deki yasaklı uygulamalar ve ödeme reddi kapsamına girer. **Replay uygulaması için çıkarım**: limit emirleri fiyat seviyeye değince değil, **seviyenin içinden geçince** doldur, büyük emirlerde kısmi dolum uygula. Aksi halde backtest gerçekte olmayan dolumlarla iyimser olur.
- "Prop firm kayıpları sınırlar, öğrenmenin en ucuz yolu" (çoğunluk görüşü). Kısmen doğru: 100-200$'lık ücret, ilk canlı hesabı birkaç günde patlatmaktan ucuz. Ama ücretleri seri halde ödemek de para kaybıdır (§1c huni). Kane: "Challenge'larda kumar oynayan, o alışkanlıkları canlı hesaba taşır."
- Panelde "retail'in %20-30'u 3-5 yıl kalırsa başarır" tahmini dile getirildi. **Kanıtı yok.** Akademik veriler (08 §1) çok daha karamsar.
- Bir konuk her sabah üç sohbet botuna (Gemini, Grok, Perplexity) günün beklentisini sorduğunu ve "alarm verici derecede isabetli" olduklarını söylüyor. Kanıtı yok, 10 §6c'deki çoklu test ve sonuç yanlılığı tuzağına açık.

## 4h. Sektörün iç verisi ve beklenti kalibrasyonu (Justin Hertzberg / FPFX Tech, Titans of Tomorrow ucF91qWKYBE; Blueberry Funded CEO'su, Diamant Trades PwPT-ETipm8)

> Hertzberg, 150'den fazla prop firmasına altyapı sağlayan FPFX Tech'in kurucusu. Söyledikleri kendi şirketinin verisine dayanıyor, bağımsız olarak doğrulanmadı. Bu %7 rakamı muhtemelen 1. bölümdeki Finance Magnates rakamıyla **aynı ankete** ait (FPFX anketi bir sektör yayınına verildi). Yani iki ayrı kaynak sayılmamalı.

**Rakamlar:**
| Kaynak | Challenge'ı geçen | Ödeme alan | Diğer |
|---|---|---|---|
| FPFX anketi (10 firma, ~300 bin aktif hesap) | **%14** | **%7** (geçenlerin yarısı) | Ortalama ödeme **hesabın %4'ü**. Fonlu hesapta ortalama kalış **22 gün**. |
| Blueberry Funded CEO'su (iki aşamalı) | **~%12** | Geçenlerin %30'u → tüm adayların ~%3,6'sı | Ödeme alanların %30'u ikinci ödemeye ulaşıyor (~%1,1). "Prop firmalarının %90-95'i 2 yıl içinde batıyor" (kendi iddiası). |

**Firma ekonomisi** (Hertzberg'in örneği): 100k$'lık challenge ~500$. 100 satış = 50.000$ gelir. 14 kişi fonlanır, 7 kişi ortalama 4.000$ ödeme alır = 28.000$. Bu, ödeme işleme, platform, pazarlama, affiliate ve personel maliyetlerinden **önceki** hesap. "Rakamlar müthiş görünür, ama gelir ve ödemeyi ayırınca bunun zor bir oyun olduğunu görürsün."

**✔ Kalibrasyon: sektör oranı hangi beklentiye karşılık geliyor?** (`arastirma/verify_industry_calibration.py`, FTMO tipi iki aşama: +%10 / +%5 hedef, -%10 maksimum zarar, işlem +2R/-1R)
| İşlem başı beklenti | %1 risk | %2 risk | %3 risk |
|---|---|---|---|
| -0,20R | %3 | %9 | %14 |
| **-0,10R** | **%12** | %17 | %21 |
| -0,05R | %20 | %23 | %26 |
| **0 (avantaj yok)** | **%32** | %28 | %31 |
| +0,05R | %44 | %34 | %37 |
| +0,10R | %58 | %42 | %42 |
| +0,20R | %79 | %56 | %52 |

**Çıkan dersler:**
1. **Ortalama challenge adayı rastgeleden kötü işlem yapıyor.** Yazı tura atan biri iki aşamayı %32 ihtimalle geçerdi, gerçek oran %12-14. Bu, işlem başına **~-0,1R** (%1 risk) ya da ~-0,2R (%3 risk) beklentiye denk geliyor. Bu seviye, gün içi işlemin R cinsinden maliyetiyle (04 §5b: 1 saatlik FX'te ~0,10R) ve aşırı işlemle tutarlı. Akademik veriler de aynısını söylüyor (08 §1).
2. **Risk artırmak sadece negatif beklentide işe yarıyor.** -0,2R'de %1 → %3 riskle geçme oranı %3'ten %14'e çıkıyor, +0,1R'de %58'den %42'ye düşüyor. "Agresif ol, hızlı geç" tavsiyesi (§4b) bu yüzden **kumar mantığı**: avantajın yoksa varyansı artırmak şansını büyütür. Avantajın varsa seni yavaşlatır ve düşürür.
3. **Hedef**: Bu tabloya göre anlamlı bir geçme olasılığı (%50+) için %1 riskte işlem başı **≥ +0,07R** (net) gerekiyor. Bu, 09 §2 madde 6'daki "yılda 10-15R" ölçütüyle birlikte okunmalı.

**Kim kalıcı ödeme alıyor?** (Hertzberg, yüz binlerce hesabın verisinden):
- "Kalıcı kârlı prop trader'ını gösteren şey, kalıcı kârlı kendi hesabıyla işlem yapan trader'ı gösterenle aynı": **aşırı kaldıraç yok, aşırı işlem yok**, çoğunlukla **swing**, pozisyonu 1-3 gün tutan.
- "Kısa vadeli trader spread ve komisyonla kendini doğrar." Kalıcı olanlar "dünyayı yakmıyor, ayda %3-4 yapıyor ama tekrar tekrar."
- "**En büyük ödemeler**, kaldıraçla şans eseri tutturan, topa sert vuran trader'lardan geliyor." Yani büyük ödeme ekran görüntüsü beceri kanıtı değil (§1c).
- Firmalar alışkanlık haline gelmiş kumarcıyı işaretliyor: 25$'lık challenge alıp maksimum kaldıraçla art arda patlatanlar. Hertzberg firmalara bu müşterileri **yasaklamalarını** öneriyor. Haber işlemleri bir firmada 60 günde ödemelerin %30'unu oluşturmuştu, "yazı tura atmak". Bu yüzden firmalar haber kuralları ekliyor.
- Firmaların risk araçları: gecikme arbitrajı, istatistiksel arbitraj, firmalar arası ters pozisyon ve "zehirli akış" tespiti. Toplam net pozisyonu hedge ediyorlar, bazı hesapları gerçek piyasaya yönlendiriyorlar (A-book). "Tüm trader'ların tersini almak" maliyet ve varyans yüzünden işe yaramıyor: ancak %1-2 getiriyor, o da büyük riskle.

**Firma güvenliği için ek işaretler** (§4d listesine ek):
- [ ] "Ödemeleri geçici durdurduk", "broker ya da likidite sorunu" açıklamaları → **en net kırmızı bayrak**.
- [ ] Anlamsız kampanyalar ("1 alana 1 bedava", "%75 indirim") → nakit sıkıntısındaki firmanın para toplaması.
- [ ] Son 6 ay içinde kurulmuş firma. Hertzberg'e göre bunların ~%90'ı "teknik olarak batık": eski yükümlülükleri yeni satışla ödüyor.
- [ ] Tek platforma ve tek brokere bağımlılık. MetaQuotes 2024 başında MT4/MT5'i prop firmalarına kapatınca aylık satışı 15M$'dan 4M$'a düşen firmalar bir anda batık duruma düştü.
- [ ] Blokzincir cüzdanlarından "milyonlarca dolar ödeme" gösteren takip siteleri **manipüle edilebilir**: para cüzdanlar arasında döndürülebilir. Hertzberg'e göre en büyük 3-4 firmanın aylık satışı 10-20M$. "Ayda 8M$ ödüyoruz" iddiaları akla yatkın değil.
- [ ] Sağlıklı yeni firma: lansmanda 150-300 bin $ nakit rezerv ve satış dursa bile yükümlülükleri karşılayacak bir rezerv formülü.

## 4i. FTMO'nun güncel resmi kuralları: gece, hafta sonu, haber, limitler (ftmo.com, 2026-11-22'de okundu)

> Kaynak sayfalar: ftmo.com/en/trading-objectives/, /faq/can-i-hold-positions-overnight-or-over-the-weekend/, /faq/can-i-trade-news/, /faq/what-is-the-swing-account-type-and-how-does-it-work/, /forbidden-trading-practices/. Kurallar değişebilir, işlem yapmadan önce yeniden kontrol et.

| Konu | Standart hesap tipi | Swing hesap tipi |
|---|---|---|
| Değerlendirme aşaması (Challenge/Verification) | Gece, hafta sonu ve haber **serbest** | Serbest |
| Fonlu aşama (FTMO Account): gece ve hafta sonu | "**2 saatten uzun piyasa kapanışlarında** pozisyon tutmak yasak", kapanıştan önce kapat. Pratikte günlük kısa aralar sorun değil, **hafta sonu taşımak yasak**. | "Gece veya hafta sonu pozisyon tutmada **kısıt yok**" |
| Fonlu aşama: haber | Seçili haberlerden **2 dk önce ve 2 dk sonra** emir yok | Kısıt yok |

- **İki aşamalı program**: hedefler **%10 ve %5**, günlük maksimum zarar **%5**, maksimum zarar **%10 (sabit)**. En az **4 işlem günü**. Süre sınırı yok (sitede "No time limit").
- **Günlük maksimum zarar tam olarak nasıl hesaplanıyor?** (Trading Objectives sayfası, 2026-11-22)
  - "Limit her gün 00:00 CE(S)T'de yeniden hesaplanır." Formül: **gece yarısı kaydedilen bakiye − başlangıç sermayesinin %5'i** (tek aşamalıda %3).
  - **Varlık değeri (equity) = bakiye + açık pozisyonların K/Z ± swap − komisyon.** Equity bu limitin altına düştüğü anda kural ihlal edilmiş sayılır.
  - FTMO'nun örneği (100 bin $, iki aşamalı):
    - 1. gün limit 95.000 $.
    - Gece bakiyesi 102.000 $ olunca 2. gün limit 97.000 $.
    - Gece bakiyesi 101.000 $ olunca 3. gün limit 96.000 $.
  - **Sonuç 1: Limit kapalı bakiyeye göre yukarı kayar.** Kâr kapatıldıkça günlük limit de yükselir, yani kâr "kilitlenmez".
  - **Sonuç 2: Gece taşınan açık zarar o günün payını baştan yer.** Gece yarısı −%3 açık zararla girersen o gün sadece %2 hareket alanın kalır.
  - Gece taşınan açık kârın tampon gibi davranması sayfada açıkça yazmıyor, formülden çıkan bir yorum. Önemliyse destekle teyit et.
  - Parabolik bir harekette lot sabit kalırsa kuyruk günleri ikiye katlanır (02 §6b-3).
- **Tek aşamalı program**: hedef %10, günlük maksimum zarar **%3**, maksimum zarar %10 ve **trailing**. Trailing'in geçme oranına etkisi için §1b ve §4c'ye bak.
- **Yasaklı uygulamalar**: "aşırı kaldıraç, aşırı pozisyon, tek yönlü bahisler, hesap döndürme" ve "**diğer simüle işlemlerine göre belirgin şekilde büyük pozisyonlar**". Haber civarında gap işlemi de yasak. Ayrıca bir tutarlılık (en iyi gün) kuralı var (§4e).
- **Swap**: Hesap değeri formülünde "± Swaps" geçiyor, ama ücret tablosu yayımlanmamış. Gecelik finansmanın uygulandığını varsay, kendi enstrümanların için platformdan kontrol et.
- **Bu bilgi tabanı için anlamı**: 25-27. turdaki swing ve trend portföyleri (§2 madde 7, 12) haftalarca pozisyon taşıyor. FTMO'da **Swing hesap tipi** gerekiyor. Değerlendirmede kısıt yok, ama fonlu aşamada Standart hesapta uygulanamaz. Gün içi ve gecelik (hafta sonu hariç) stratejiler Standart hesaba uygun.

## 4j. "Geçen ve kalan hesapların verisi" ne söyler, ne söylemez? (PipBack WWulQ4Mi0fM + seçilim simülasyonu; FTMO röportajı gMk5QKiUNRo)

> PipBack'in kurucusu, bir CFD prop firmasıyla bağlantılı olduğunu söylüyor. ⚠️ Kanal **challenge satışından komisyon alan bir "cashback" sitesi**, yani çıkar çatışması var.

**Videonun verileri** (firmanın kendi verisi, doğrulanamaz):

| | Geçen hesaplar | Kalan (ihlal) hesaplar |
|---|---|---|
| 1. aşamayı geçme oranı | %22 | — |
| Günlük işlem sayısı | 2,5-3 | 8-9 |
| Ortalama RR | ~2,5 | 1'in altında |
| Hesabın bitmesi | ~9 gün | 5-7 gün |

Diğer iddialar:
- Kalan trader'ların bazı haftalarda **%50'ye kadarı stop ve TP kullanmıyor**.
- Kalanların **%70'i scalper**. Bunlar stop mesafesinden bağımsız **sabit lot** kullanıyor.
- Kalanlar haberin çıktığı anda işleme giriyor.
- Kalanlar en çok altın ve Nasdaq işliyor. Geçenler de bunları işliyor, fark risk yönetiminde.
- Geçenlerin %60-80'inin isabeti %50'nin üzerinde.
- Firmada swing hesapları normal hesaplardan daha kârlıydı.
- "Negatif RR" ifadesi yanlış. RR negatif olamaz, kastedilen 1'in altında.

**✔ Simülasyon: bu "kazanan profili"nin ne kadarı sadece şanstır?** (`arastirma/verify_pass_vs_breach.py`, 40.000 trader)
- **Kurgu**:
  - Trader'lar risk (%0,25-4), günlük işlem sayısı (1-10) ve TP:SL oranı (0,5-3) bakımından farklı.
  - İşlem başına maliyet 0,05R.
  - 1. aşama kuralları: +%10 hedef, -%10 maksimum zarar, -%5 günlük zarar.
- **Senaryo A, kimsenin avantajı yok**:
  - 30 gün sınırıyla geçme oranı **%19**. Firmanın %22'sine çok yakın.
  - Geçenlerin gerçekleşen isabeti **%65**, kalanların **%21**. Geçenlerin işlem başına sonucu **+0,87R**, kalanlarınki **-0,51R**.
  - Hedefi 2,5R ve üstü olan geçenlerin **%47-58'inin** isabeti %50'nin üzerinde, oysa bu trader'ların gerçek isabeti ~%27.
  - → "Geçenlerin %60-80'i %50+ isabetle 2,5R alıyor" verisi **şansla tamamen üretilebiliyor**. Bu bir beceri kanıtı değil, sonuca göre seçilmiş bir gruptur (seçilim/hayatta kalma yanlılığı).
- **Senaryo B, trader'ların %20'si gerçekten iyi** (maliyetten sonra +0,15R):
  - Becerikli trader'ların payı geçenler arasında %20'den **%38-40**'a çıkıyor. Yani **geçenlerin ~%60'ı yine de şanslı ama becerisiz**.
  - Geçmek, beceri hakkında zayıf bir sinyal.
- **Hangi kollar gerçekten nedensel?**
  - **İşlem başına risk**:
    - Avantajı olmayan trader'da risk arttıkça geçme oranı artıyor: %0,25 riskte %0-7, %4 riskte %33-34.
    - Becerikli trader'da tersi: süre sınırı yokken %0,5 riskte **%93** geçiyor, %4 riskte %51.
    - (23. turdaki "risk artırmak sadece negatif beklentili trader'a yarar" bulgusunun aynısı.)
  - **İşlem sıklığı**:
    - Sabit 0,05R maliyetle süre sınırı yoksa günde 1 işlemle %31, günde 10 işlemle %22 geçiyor.
    - Gerçek veride 3'e karşı 9 işlemlik fark, maliyetin tek başına üreteceğinden çok daha büyük. Bu, gerçek **davranış** farklarına işaret ediyor: intikam işlemi, plansız işlem, dar stoplu scalping'de daha yüksek maliyet.
  - **TP:SL oranı**: avantaj yokken düşük RR (0,5) biraz daha kötü (%10-14). Hedefe ulaşmak için daha çok işlem gerekiyor, dolayısıyla daha çok maliyet ödeniyor.
- **Sonuç: kendine "geçenler gibi işlem yap" deme. Kontrol edebildiğin kollara bak**:
  1. Avantajın varsa düşük risk.
  2. Az ve planlı işlem.
  3. Stop mesafesine göre lot. Sabit lot büyük kayıplar üretir (02 §1, §6b-3).
  4. Haber anında işleme girme.
  5. Her işlemde stop.

  Bunların hepsi bilgi tabanının önceki bulgularıyla uyumlu. Geçme/kalma istatistiğindeki isabet ve RR farkı ise çoğunlukla sonucun kendisi.

**FTMO röportajı: Leo, GBPUSD, toplam ~200 bin $ ödeme** (FTMO'nun kendi kanalı, ⚠️ hayatta kalanlardan seçilmiş bir örnek, firma challenge satıyor):
- **Geçmiş**:
  - 2019'da sinyal grupları ve "dolandırıcı influencer'larla" başlamış. Aşırı kaldıraç ve intikam işlemi gibi bütün hataları yapmış.
  - İlk ödemesini **4 yıl sonra** (Mart 2023) almış. Bu sırada FTMO'da müşteri hizmetlerinde çalışıyormuş.
  - "Strateji 2020-21'den beri aynı, değişen zihniyet."
- **Yöntem**:
  - Tek parite (GBPUSD), 15 dakikalık grafik.
  - Sadece Londra ve New York seanslarının ilk 3 saati. FOMC, NFP ve CPI'da işlem yok.
  - Asya tepe/dibinin süpürülmesinden sonra ikili tepe/dip, boyun çizgisi kırılımı ve yeniden test.
  - Hedef formasyonun 3 katı ya da günün tepesi/dibi. RR ~3,5, isabet %50'nin altında.
  - 400 bin $'lık **Swing** hesapta +100 bin $ kazanmış, maksimum düşüş ~%3.
  - **Limit emir koyup bilgisayarı kapatıyor, işlemi yönetmiyor**: "Backtest'te yönetmiyorsan canlıda da yönetme." 13'teki replay ilkesiyle aynı.
- **Backtest ve günlük**:
  - TradingView replay ile "10 yıldan fazla" backtest yapıp Google Sheets'te kaydetmiş.
  - Kayıpları "sistem kaybı" ve "kendi hatam" diye ayırmış: "Kayıplarımın çoğu hataydı: plan dışı parite, saat dışı işlem." Bu, Dante'nin yöntemiyle aynı (10 §6h).
  - Pariteyi "en kârlı paritem" diye seçmiş. Carver'a göre bu **piyasa seçme yanlılığı** (10 §6j).
- **✘ İddia: "Asya seanslarının %80'inde iki uç da süpürülür."** Test edildi (04 §6b-5): GBPUSD'de iki uç sadece **%44** günde süpürülüyor. **En az bir uç ise %99**. Ve bu, aynı saat-volatilite profiline sahip rastgele modelden (%47) farksız. Süpürmeden sonra karşı uca gitmede de rastgeleden fark yok.
- **✘ İddia: "20-30 işlem, olasılıkların işlemesi için yeterli."**
  - Bu ancak çok büyük bir avantajla doğru. RR 3,5 ve +0,75R/işlemde 30 işlemlik dilimin zararda bitme olasılığı %2.
  - Gerçekçi bir +0,2R avantajda (RR 3,5, isabet %27) 30 işlemlik dilimin **%28**'i, 100 işlemlik dilimin **%17**'si zararda biter.
  - → Yüzlerce işlem gerekir (10 §3, 11 #63).
- ✔ **Kumarhane benzetmesi doğru**: Avrupa ruletinde tek yeşil kasaya ~%2,7 avantaj verir (kırmızının olasılığı 18/37 = %48,6).
- ✔ **"Teknik analiz tek bir işlemin riskini azaltmaz"** (Douglas ile aynı).
- ✔ **Bakiyeye bakma, yüzde düşün.**

## 4k. Phidias firma verisi: 20.000 ve 50.000 trader (N3bpg-Hiqos, Mfwc6j8pJIc)

> Phidias, bir futures prop firması. Video tamamen kendi ürünlerinin reklamı ("25K statik hesap 55 $"). Veriler firmanın kendi beyanı, doğrulanamaz. Diğer firmaların verileriyle (FPFX §4h, PipBack §4j) **aynı yönde** oldukları için not edildi.

**Firmanın verisi:**
- **Swing trader'ların başarı oranı, sadece gün içi işlem yapanlardan %83 yüksek.** PipBack'in "swing hesaplar daha kârlı" ve FPFX'in "kalıcı ödeme alanlar 1-3 gün tutuyor" verisiyle aynı yönde.
- **Değerlendirmeyi acele etmeden geçenlerin ödemeye ulaşma şansı 3 kat.** Minimum gün sayısında geçmeye uğraşmayanlar kastediliyor. Simülasyonlarımızla tutarlı: yüksek riskle hızlı geçenler fonlu hesapta çabuk düşüyor (§4j, 23. tur).
- **Statik düşüş limitli hesaplarda başarı, trailing limitlilerin 2 katı.** Gün içi trailing limitte açık kâr da tamponu yiyor. Mekanik için §4c.
- **"Günlük zarar limitine takılıp günü kapatılanların ertesi gün hesabı patlatma olasılığı belirgin şekilde yüksek."**
  - Firma bunu "güvenlik ağı tuzaktır, günlük limit yok" diye pazarlıyor. Bu **nedensellik ters çevrilmiş** bir yorum.
  - Günlük limite takılmak, zaten yüksek riskle ve duygusal işlem yapan trader'ın işareti. Limitin kendisi sebep değil.
  - Doğru ders: limite takıldığın günün ertesi günü (intikam eğilimi) için **önceden** kural koy, ör. ertesi gün yarım boyut ya da ilk işlemden önce mola (13 §3, 08). Ayrıntı 11 #65'te.
- **Ödeme tamponu**: kârın bir kısmının (ör. 50K hesapta 2.600 $) çekilemez tutulması. Firmayı seçerken ödenebilir kârı bu tampondan sonra hesapla.

**Firma seçim çerçevesi** (makul):
- "Firma, sen **başarılı olunca mı**, yoksa **sadece başarısız olunca mı** para kazanıyor?"
- Kırmızı bayraklar:
  1. Ödemeler başlayınca kuralları değiştirmek (§4, §4d).
  2. Gün içi trailing limit ve sıkı günlük limit, yani ilan edilenden küçük gerçek düşüş payı.
  3. Geç ödeme ya da çekilemeyen tampon.
  4. Fonlu trader'ı sonsuza dek simülasyonda tutmak.
- ⚠️ Videonun kendisi bu çerçeveyi kendi ürününü satmak için kullanıyor. Çerçeveyi her firmaya, Phidias dahil, kendin uygula.

**✘ "En iyi %5 kazananın isabeti %70, demek ki yüksek isabetli strateji daha iyi"** (Mfwc6j8pJIc):
- **Taban oran yok.** Tüm trader'ların ya da kaybedenlerin ortalama isabeti verilmemiş.
- Video kaybedenlerin **de** yüksek isabetli strateji kullandığını kendisi söylüyor. Yani isabet kazananı kaybedenden **ayırmıyor**.
- En çok kazananlar sonuca göre seçilmiş bir grup. §4j simülasyonunda avantajı olmayan trader'larda bile geçenlerin gerçekleşen isabeti %65 çıkıyor.
- Videonun kendi vardığı sonuç doğru olan: fark **zararların küçük tutulmasında**, yani risk yönetiminde. Yüksek isabet psikolojik olarak kolay olabilir ama tek başına avantaj değil. Ayrıntı 11 #64'te.

## 4l. Ödeme politikası ve hesap tipi: erken küçük ödeme, statik ve trailing limit (Kimmel 90ozA2Ts4FU, NinjaTrader Prop GVdkt_EI26Q + simülasyon)

**Kimmel'in "tek seferde bir" (OAT) sistemi** (200+ ödeme aldığını söylüyor, doğrulanmamış; FundedNext affiliate'i ve mentorluk satışı var):
- **Döngü**:
  - Challenge'larda yüksek risk ve hızlı döngü, fonlu hesapta temkinli risk.
  - Fonlu hesapta **ilk küçük ödemeyi mümkün olan en kısa sürede kilitle**. Ör. 100K hesapta 500 $'lık ödeme ücreti geri getirir ve sıradaki challenge "risksiz" olur.
  - Para geri gelince yeni challenge'a geç.
- **Partiler halinde işle**:
  - Fonlu hesapların ~%30'unu aynı anda işle (ör. 3 hesap, %1 risk). Diğerleri yedekte beklesin.
  - Kâr kilitlenince ödeme tarihini beklerken sonraki partiye geç.
  - Tutarlılık kuralı olmayan futures hesaplarında minimum gün şartını küçük kârlı günlerle (150 $) doldur.
- **Düşüşteyken partiyi bırakma.** Ödeme ya da hesap kaybı olana kadar aynı partide kal. Partiden partiye atlamak "kumar döngüsünü" başlatır. Bu, makul bir davranış kuralı.
- **İddia**: "Kârlı olmasan bile prop firmalarından para kazanabilirsin." Örnek: bir partide -%10 kaybedip diğerinde +%2 kazanınca 6.000 $ ödeme alırsın, 3.000 $ ücretten sonra +3.000 $.

**NinjaTrader Prop videosu**: başlıkta "100+ ödeme analizi" yazıyor ama videoda analiz yok. Ödeme mekaniğini temel düzeyde anlatıyor:
- Futures'ta kâr payı %80-90. Net kâr, komisyon ve ücretler düşüldükten sonra hesaplanır.
- Şartlar: minimum işlem günü, çekim eşiği ve o an kural ihlali olmaması. Eşiği geçtikten bir saat sonra günlük limite takılırsan ödeme alamazsın.
- **Ödemeden sonra bakiye düşer.** Bazı firmalarda düşüş tabanı yerinde kalır, yani tampon küçülür.

**FTMO'nun yayımladığı rakamlar** (ftmo.com, 2026-11-22):
- Geçme ya da ödeme oranı **yayımlanmıyor**. ftmo.com/en/statistics/ sayfası yok (404).
- Sadece toplam rakamlar var: "4,5 milyon+ müşteri", "650 milyon $+ ödeme".
- Kabaca **müşteri başına ~144 $ ödeme** ediyor. 100K challenge ücreti 540 $. Müşterilerin bir kısmı ücretsiz deneme kullanıcısı da olabilir.
- Yani ortalama müşteri, ödediği ücretin altında ödeme alıyor. Bu, sektör verisiyle (§4h) tutarlı.

**✔ Simülasyon** (`arastirma/verify_payout_policy.py`):
- **Kurgu**: 100K hesap, %80 kâr payı, RR 2, günde 1 işlem, ~2 haftada bir ödeme kontrolü, 500 işlemlik (~2 yıl) ufuk, hücre başına 20.000 yol.
- **A = FTMO tipi**: başlangıçtan -%10 statik limit, ödemeden sonra bakiye başlangıca döner.
- **B = futures tipi**: gün sonu trailing %5, +%0,2'de kilitlenir, %5,2'lik tampon çekilemez.

| İşlem başına avantaj | Risk | A, eşik +%0,5: ortalama ödeme / P(≥1 ödeme) | A, eşik +%5 | B (trailing %5 + tampon) | 2 aşamayı geçme | Deneme başına net EV (A, +%0,5) |
|---|---|---|---|---|---|---|
| -0,10R | %1 | 3.942 $ / %59 | 3.289 $ / %35 | 785 $ / %15 | %12 | **-30 $** |
| -0,05R | %1 | 5.838 $ / %67 | 5.314 $ / %46 | 1.110 $ / %20 | %21 | +780 $ |
| 0 | %1 | 8.879 $ / %75 | 8.560 $ / %58 | 1.720 $ / %25 | %33 | +2.563 $ |
| +0,10R | %0,5 | 19.728 $ / %95 | 19.482 $ / %90 | 6.057 $ / %51 | %79 | **+15.503 $** |
| +0,10R | %1 | 20.250 $ / %86 | 22.235 $ / %78 | 3.582 $ / %37 | %61 | +12.106 $ |

**Sonuçlar:**
1. **Erken ve küçük ödeme** en az bir ödeme alma olasılığını belirgin şekilde artırıyor (avantaj yokken %58'den %75'e, ücret iadesi de buna bağlı). Ama **beklenen toplam ödemeyi neredeyse değiştirmiyor** (8.560 $'a karşı 8.879 $).
   - Teori de bunu söylüyor: avantajı olmayan rastgele bir yolda, statik taban ve sıfırlanan bakiyeyle, beklenen toplam çekim ≈ kâr payı × tampon. Burada 0,8 × 10.000 $ = 8.000 $ artı küçük taşma (opsiyonel durma teoremi).
   - Negatif avantajda erken çekim biraz yardım ediyor. Pozitif avantajda yüksek risk ve yüksek eşikle biraz daha iyi.
   - → Kimmel'in kuralı **nakit akışını ve ücret iadesini güvenceye alır, beklenen değeri artırmaz.** ✔ kısmen.
2. **Hesap tipi en büyük kol.**
   - Aynı %10 büyüklükte trailing ve çekilemez tampon, ödemeleri yarıya indiriyor: avantaj yokken 8.766 $'dan 3.499 $'a, +0,1R'de 20.098 $'dan 12.008 $'a.
   - Tipik futures hesabındaki %5'lik tampon bunu bir yarıya daha indiriyor (1.697 $ / 3.588 $).
   - Phidias'ın "statik limit 2 kat başarılı" verisiyle (§4k) aynı yönde. **Firma seçerken statik limit ve çekilebilir kâr ilk kriter.**
3. **"Kârlı olmasan da kazanırsın" iddiası yarı doğru ve tehlikeli.**
   - Modelde statik limitli firmada, sabit riskle disiplinli işlem yapan **sıfır avantajlı** trader deneme başına +1,9-2,6 bin $ pozitif beklenti görüyor. Bu, firmanın zarar tarafını ücret karşılığında üstlenmesinden doğan opsiyon (§1d).
   - Ama gerçekçi ortalama trader (-0,10R, sektör kalibrasyonu §4h, bu modelde %12 geçme) **~0 ya da negatif**. Trailing limitli firmalarda negatif.
   - Model iyimser: tutarlılık kuralı, ödeme reddi, kural değişikliği, tilt ve sapma yok. Bu tablo "avantajsız da kazanırsın" demek değil (§1d uyarısı geçerli).
4. **Kimmel'in parti sistemi beklenen değeri değiştirmez.**
   - Aynı işlemleri birden fazla hesapta aynı anda açmak, tek ve büyük bir bahistir. Hepsi birlikte kazanır ya da kaybeder (02 §6c).
   - Yedekte bekleyen hesaplar sadece zamanı böler, gelir akışını yumuşatır.
   - Bazı firmalarda aynı işlemi hesaplar arasında kopyalamak kısıtlı (§4g). Önce kendi firmanın kuralını kontrol et.
5. **Sınama sırası**: "Challenge'da yüksek, fonlu hesapta düşük risk" stratejisi henüz ayrı test edilmedi (§1d sadece tek risk düzeyini inceliyor).

## 4m. "Challenge'da yüksek, fonlu hesapta düşük risk" ve FTMO'nun Monte Carlo yazısı (simülasyon)

**FTMO blog yazısı** ("How to Use Monte Carlo Simulations to Pass the FTMO Challenge", 2026-07-31):
- Geçmiş işlemlerini binlerce kez karıştırıp alternatif sermaye eğrileri üret ve stres testi yap. Bu yöntem doğru (10 §6d-f, §6k).
- "%2 riskle 5 ardışık kayıp %10 maksimum zarar limitini doldurur." Aritmetik doğru.
- "Riski %2'den %0,5-1'e indirmek geçme olasılığını örneğin %15'ten %85'e çıkarabilir." Rakamın girdileri verilmemiş.
- Kendi uyarısı: "Günlük zarar limiti açık zararları da sayar, simülasyon bunu modellemeli" (§4i).

**✔ Test** (`arastirma/verify_split_risk.py`). Ayarlar: 2 aşama, statik %10 limit, RR 2, günde 1 işlem, süre sınırı yok. İki aşamayı geçme oranı:

| Avantaj (R/işlem) | %0,5 risk | %1 | %2 | %3 |
|---|---|---|---|---|
| -0,10 | %3 | %12 | %17 | %22 |
| 0 | %32 | %34 | %28 | %31 |
| +0,10 | %79 | %61 | %41 | %42 |
| +0,20 | %96 | %82 | %55 | %52 |

- **FTMO'nun "%15'ten %85'e" örneği ancak gerçek bir avantajla mümkün** (yaklaşık +0,2R'nin üstü).
- **Avantajı olmayan trader için riski düşürmek geçme oranını DÜŞÜRÜR** (-0,10R'de %22'den %3'e). Düşük risk sadece avantajı olana yarar. 23. turun "risk artırmak sadece negatif beklentili trader'a yarar" bulgusunun öbür yüzü.

**Kimmel'in "challenge'da yüksek, fonlu hesapta temkinli risk" önerisi.** Kurgu: 250 işlemlik trader yılı, ücret 540 $ (ilk ödemede iade), 2 haftada bir %80 kâr payı ödemesi. Hesap kaybedilince yeni challenge alınıyor.

| +0,10R avantaj | Fonlu risk %0,5 | Fonlu %1 | Fonlu %2 |
|---|---|---|---|
| Challenge riski %1 | +7.149 $ / %17 / 134 gün | +13.515 $ / %19 / 103 g | +16.907 $ / %27 / 49 g |
| Challenge riski %2 | +10.060 $ / %6 / 198 g | **+21.571 $ / %4 / 168 g** | +34.680 $ / %7 / 101 g |
| Challenge riski %3 | +11.120 $ / %4 / 219 g | +25.140 $ / %2 / 196 g | +46.592 $ / %2 / 135 g |

(Hücreler: yıllık ortalama net / zararda biten yıl oranı / fonlu hesapta geçirilen gün)

**Sonuçlar:**
1. ✔ **Challenge'da daha yüksek risk** (%2-3) her avantaj düzeyinde daha iyi. Sebep **zaman**: %0,5 riskle bir yılda nadiren fonlanılıyor. Photon'un zaman maliyeti argümanı (§1d) da bunu söylüyordu.
   - ⚠️ Bu sadece günde ≤1 işlem açılırsa geçerli. Günde 2 işlemde %3 riskle iki kayıp %6 eder, %5 günlük limiti aşar (§1d).
2. ✘ **Fonlu hesapta temkinli risk bu modelde ortalama kazancı DÜŞÜRÜYOR.** Avantajı olan trader'da bile %2 fonlu risk, %0,5'in 3 katı kazandırıyor. Sebep yapısal: fonlu hesapta zarar firmanın, kâr trader'ın. Getiri opsiyon gibi dışbükey (§1d, §4l). Volatilite arttıkça opsiyonun değeri artar.
   - Avantajı olmayan trader bile %2-3 challenge ve %2 fonlu riskle modelde pozitif görünüyor. Bu, **modelin bilerek dışarıda bıraktığı** şeyleri gösteriyor:
     - Firmanın "aşırı kaldıraç / diğer işlemlere göre çok büyük pozisyon" yasağı ve ödeme reddi (§4i, §4d).
     - Tutarlılık kuralı (§4e).
     - Ölçeklendirme planı: kârlı fonlu hesap büyür, model bunu kaçırıyor.
     - Yüksek riskte davranışın bozulması (tilt): gerçek avantaj küçülür.
     - Kural değişiklikleri.
3. **Pratik denge** (bu modelin ve önceki turların birlikte söylediği):
   - Avantajın kanıtlıysa (≥200 işlemlik canlı ya da replay kaydı) challenge'da **%1-2**, fonlu hesapta **%1** civarı.
   - Ör. +0,1R'de challenge %2 ve fonlu %1: yılda ortalama +21,6 bin $, zararda biten yıl %4, 168 fonlu gün. Kural ve davranış riskleri içinde kalır.
   - Fonlu hesapta %2 ve üstü riskle modeldeki ek kazanç, gerçekte ödeme reddi ve tilt riskiyle ödenir.
   - Avantajın kanıtlı değilse, hiçbir risk ayarı onu yaratmaz. Modeldeki "pozitif ortalama" firmanın opsiyonunu sömürmekten ibaret ve medyan ile gerçek sektör verisi (%7 ödeme alan, §4h) bunu desteklemiyor.

## 4n. FTMO ölçeklendirme planı, kâr tamponu ve "hesap döndürme" yasağı (simülasyon)

**Resmi kurallar** (ftmo.com/en/scaling-plan, 2026-11-22):
- Şartlar:
  - 1 ya da 2 aşamalı challenge'la alınmış hesap (Instant hesap hariç).
  - En az **4 ay**.
  - O 4 ayda **en az %10 net kâr**.
  - Aynı dönemde **en az 2 işlenmiş ödeme**.
  - Ölçeklendirme anında pozitif bakiye.
- Ödül: **her 4 ayda hesap %25 büyür** (tüm hesaplar toplamında 2 milyon $'a kadar), kâr payı %90 olur (2 aşamalıda; 1 aşamalı zaten %90).
- Ödeme talebi ilk işlemden **14 gün sonra ya da sonraki herhangi bir günde** yapılabiliyor, 1-2 iş gününde ödeniyor.
- %10 / 4 ay ≈ **yılda %30**. Yüksek bir çıta.

**✔ Simülasyon** (`arastirma/verify_scaling_plan.py`):
- **Kurgu**: tek fonlu hesap, ~3 yıl (750 işlem), RR 2, günde 1 işlem.
- **Risk tanımı**: güncel hesap büyüklüğünün yüzdesi.
- **Ödeme kuralı**: 10 işlemde bir, kârın tamamı çekiliyor.

| Avantaj | Risk | 3 yılda ortalama ödeme (ölçeklendirmeli) | En az 1 büyüme | 3 yıl sonunda hesap ayakta | Ölçeklendirmesiz |
|---|---|---|---|---|---|
| 0 | %0,5-2 | ~8.000 $ | %1-12 | %0-3 | ~8.000 $ |
| +0,10R | **%0,5** | **27.644 $** | %45 | %29 | 24.074 $ |
| +0,10R | %2 | 13.432 $ | %4 | %0 | 13.680 $ |
| +0,20R | **%0,5** | **71.595 $** | %82 | %69 | 54.107 $ |
| +0,20R | %1 | 50.691 $ | %48 | %2 | 40.974 $ |
| +0,30R | %0,5 | 134.126 $ | %97 | %92 | 87.844 $ |

**Kâr tamponu bırakmak** (ölçeklendirmesiz, 3 yıl):
- Kural: her ödemede sadece belirli bir tamponun **üstündeki** kâr çekiliyor.
- Hücreler: ortalama ödeme / 3 yıl sonunda hesabın ayakta olma olasılığı.

| | Tampon 0 | Tampon %3 | Tampon %5 | Tampon %10 |
|---|---|---|---|---|
| Avantaj 0, %1 risk | 8.788 $ / %0 | 8.576 $ / %0 | 8.489 $ / %0 | 8.565 $ / %3 |
| +0,10R, %1 risk | 20.533 $ / %0 | 26.160 $ / %3 | 29.491 $ / %8 | **36.462 $ / %27** |
| +0,20R, %1 risk | 49.339 $ / %5 | 69.268 $ / %22 | 80.030 $ / %37 | **95.621 $ / %69** |
| +0,20R, %0,5 risk | 54.473 $ / %71 | 56.699 $ / %90 | 55.945 $ / %95 | 52.658 $ / %98 |

**Sonuçlar:**
1. **Avantajı olmayan trader için fonlu hesabın değeri ≈ kâr payı × tampon (~8.000 $), ne yaparsa yapsın.** Risk, ödeme eşiği, ölçeklendirme ya da tampon fark etmiyor (opsiyonel durma, §4l). Ölçeklendirmeye neredeyse hiç ulaşamıyor.
2. **Avantajı olan trader için hesabın ömrü her şey.**
   - Kârın tamamını her seferinde çekersen tampon hep %10'da kalır. Hesap yukarıda kârla "sıfıra yansıyan", aşağıda -%10'da sona eren bir yürüyüş olur, yani avantaja rağmen **eninde sonunda kaybedilir**. %1 riskte 3 yılda ayakta kalma olasılığı %0-5.
   - Çözüm iki kol:
     - **Düşük risk**: %0,5'te +0,2R ile %69-71 ayakta.
     - **Kârın bir kısmını tampon olarak bırakmak**: %1 riskte %10 tamponla ödemeler 49 bin $'dan 96 bin $'a çıkıyor, ayakta kalma %5'ten %69'a.
3. **Ölçeklendirme planı sadece güçlü avantaj ve düşük riskle anlamlı.**
   - +0,2R'de %0,5 riskle ödemeleri %32 artırıyor (54 bin $'dan 72 bin $'a).
   - +0,1R'de etkisi küçük (+%15). %2 riskte neredeyse hiç işlemiyor.
4. **§4m ile çelişki nasıl çözülür?**
   - §4m'nin modeli hesap kaybedilince **yeni challenge alıp devam ediyordu**. Orada yüksek fonlu risk kazandırıyordu, çünkü her yeni hesap firmanın ~8.000 $'lık opsiyonu.
   - Bu "yüksek risk, hesap yak, yenisini al" döngüsü FTMO'nun yasak listesinde açıkça var: "aşırı kaldıraç, aşırı pozisyon, tek yönlü bahis, **hesap döndürme (account rolling)**" (§4i). Gerçekte ödeme reddi ve yasaklanma riski taşır.
   - **Sürdürülebilir yol** tek bir hesabı uzun süre yaşatmaktır: kanıtlı avantaj, düşük risk (%0,5-1), kârın bir kısmını tampon olarak bırakmak ve ölçeklendirme.
5. **Kimmel'in "ilk küçük ödemeyi hemen al" önerisi** (§4l) avantajı olmayan trader için en iyisi, avantajı olan trader için ise **en kötüsü**. Avantajın varsa ilk ödemelerden sonra tampon biriktir.

## 4o. Resmi firma istatistikleri ve "koridor" matematiği (Topstep açıklaması + Syndicate001 -BF_X7tSkQY + simülasyon)

**Topstep'in kendi yayımladığı 2025 istatistikleri** ("2025 Trader Performance Statistics", topstep.com/disclosures-notices ve /risk-disclosure, 2026-11-22'de okundu):

| Ölçüm | Değer |
|---|---|
| Başlatılan Trading Combine'ların başarıyla tamamlanan oranı | **%16,8** (combine başına) |
| En az bir combine'da fonlu seviyeye geçen **kişi** oranı | **%51,8** (çok sayıda deneme sayesinde) |
| Fonlu seviyedeki kişilerden **ödeme alan** | **%33,3** |
| Express fonlu hesaptan Live hesaba çağrılan | **%0,71** |

- Kaba hesap: kişilerin ~%17'si (0,518 × 0,333) en az bir ödeme almış. Ama combine başına ücret ödendiği için çoğu kişi birden fazla combine almış.
- FPFX'in platform verisi (300.000 hesap, %7 ödeme alan, §4h) ile aynı mertebe.
- Videoda diğer firmalar için anılan rakamlar (firma beyanları, doğrulanmadı): Take Profit Trader %36 geçme, MyFundedFutures ~%20 geçme ve fonlananların ~2/5'i ödeme alıyor, Earn2Trade <%9, The Funded Trader %5-10 geçme ve ~1/5 ödeme. 2020'den beri 80+ prop firması kapanmış (karşı taraf riski, §4).

**Koridor matematiği** (video, ★★★★):
- Challenge, bakiyenin ortasından başladığı bir koridordur: yukarıda kâr hedefi (50K'da +3.000 $), aşağıda maksimum zarar (-2.000 $).
- Avantajı olmayan rastgele yürüyüşte önce hedefe ulaşma olasılığı = **alt duvara uzaklık / koridor genişliği** = 2.000 / 5.000 = **%40**.
- Bu sonuç isabete, setup'a ya da indikatöre bağlı değil. Sadece koridorun şekline bağlı. Firma kuralları (trailing) ve işlem maliyetleri bunu aşağı çeker.
- Challenge, aslında kendi sürecin üzerine alınmış bir **alım opsiyonu**. Fiyatı = deneme ücreti / gerçekçi geçme oranı + aktivasyon ücreti. Ör. 80 $ / %20 → ~400 $ + aktivasyon.

**✔ Tekrar** (`arastirma/verify_corridor.py`, avantaj yok, 1:1, 300 $ risk, günde 2 işlem, 40.000 yol):

| Senaryo | Videonun iddiası | Bu simülasyon |
|---|---|---|
| Statik limit, maliyetsiz | %40 (bölünmeli işlemlerle ~%38) | **%41,6** |
| Gün sonu trailing (başlangıçta kilitlenen) | ~%25 | **%29,1** |
| Trailing + işlem başına riskin %3'ü maliyet | ~%15 ("Topstep'in %16,8'i") | **%20,3** |
| Aynı, ama +0,06R gerçek avantaj (1:1'de +3 puan isabet) | "neredeyse 2 kat" | **%38,2** |
| +0,20R avantaj | — | %81,6 |

**Geometri taraması** (avantaj yok, trailing): hücreler maliyetsiz geçme / %3 maliyetle geçme.

| Hedef | 0,25R (isabet %80) | 0,5R | 1R | 2R | 4R (isabet %20) |
|---|---|---|---|---|---|
| Geçme | %26,5 / **%4,8** | %28,0 / %13,2 | %29,0 / %20,3 | %29,1 / %24,4 | %29,5 / **%26,8** |

**Risk boyutu** (avantaj yok, trailing + maliyet, 1:1):

| İşlem başına risk | 100 $ | 200 $ | 285 $ (düşüşün 1/7'si) | 600 $ |
|---|---|---|---|---|
| Geçme | %7,8 | %16,1 | %19,6 | %27,5 |

**Sonuçlar:**
1. ✔ **Ortalama combine, maliyet ödeyen avantajsız bir strateji gibi davranıyor.** Bizim modelde %20, Topstep'in gerçeği %16,8. 23. turdaki sektör kalibrasyonuyla (ortalama trader ≈ -0,1R, §4h) aynı sonuç.
2. ✔ **Yüksek isabetli, dar hedefli scalping, maliyet yüzünden koridoru geçemiyor.**
   - Maliyetsiz her geometri ~%28. Maliyet eklenince 0,25R hedefte %5, 4R hedefte %27.
   - Sebep: dar hedef aynı mesafeyi daha çok işlemle kat eder ve her işlem maliyet öder.
   - Bu, §4j'deki PipBack verisiyle (kalanların %70'i scalper) ve 11 #71 ile uyumlu.
   - **Geometriyle yardım almak istiyorsan hedefi küçültme, işlem sayısını azalt.**
3. ✔ **Avantaj yokken çok küçük risk zarar** (100 $ riskle %7,8, çünkü maliyet ve süre birikir). Ama avantaj yoksa hiçbir risk düzeyi beklentiyi pozitif yapmaz (§4m).
4. ✔ **Küçük ama gerçek bir avantaj yapı tarafından büyütülür.** +0,06R ile geçme %20'den %38'e çıkıyor. "Yapı avantaj yaratmaz, sadece büyütür. Avantajın yokluğunu da aynı sadakatle büyütür."
5. **Videonun karar tablosu** (makul):
   - Gerçek avantaj ve kurala uygun strateji → hesap ekle.
   - Avantajsız ama kurala uygun → ücreti sabit bütçeli bir prim gibi gör, bütçe bitince dur.
   - Gerçek avantaj ama kurallarla çatışıyor (büyük tek gün, derin düşüş) → önce stratejiyi yeniden tasarla.
   - Avantajsız ve elle, hisle işlem → **ödemeyi bırak.**

## 4p. FTMO 1 aşamalı ve 2 aşamalı challenge karşılaştırması (resmi kurallar + simülasyon)

**1 aşamalı hesabın resmi kuralları** (ftmo.com/en/trading-objectives, 2026-11-22):
- **Hedef**: %10, tek aşama.
- **Günlük maksimum zarar %3**: gece yarısı bakiyesinden hesaplanır.
- **Maksimum zarar %10, gün sonu trailing**: "Önceki herhangi bir işlem gününde 00:00'da ulaşılan en yüksek bakiye (ya da daha yüksekse başlangıç sermayesi) eksi %10." "Limit sadece yükselebilir, asla düşmez." Başlangıç bakiyesinde durmuyor, yeni zirvelerle yükselmeye devam ediyor.
- **Tutarlılık** (12 Ekim 2026 ve sonrası siparişlerde): en iyi gün toplam kârın %50'sini geçemez. İhlal sayılmaz, kural sağlanana kadar işleme devam edersin.
- **Ücret**: 2 aşamalıda ilk ödemede iade ediliyor, 1 aşamalıda iade yok (FAQ). Kâr payı 1 aşamalıda baştan %90.

**✔ Simülasyon** (`arastirma/verify_one_step.py`, RR 2, 30.000 yol, süre sınırı yok, sadece kapanmış işlemlerle günlük limit, yani iyimser). Hücreler: geçme (geçmenin medyan süresi).

| Avantaj | Risk | Günde 1 işlem, 2 aşamalı | Günde 1 işlem, **1 aşamalı** | Günde 2 işlem, 2 aşamalı | Günde 2 işlem, **1 aşamalı** |
|---|---|---|---|---|---|
| -0,10R | %1 | %11,8 (63 g) | %20,5 (29 g) | %10,7 | %20,2 |
| 0 | %1 | %33,9 (66 g) | %38,3 (31 g) | %31,7 | %38,9 |
| +0,10R | %0,5 | %79,3 (196 g) | %74,9 (109 g) | %79,5 | %75,6 |
| +0,10R | %1 | %61,3 (62 g) | %59,8 (30 g) | %60,3 | %60,1 |
| +0,20R | %1 | %81,8 (52 g) | %76,2 (27 g) | %81,5 | %77,8 |
| +0,10R | **%1,5** | %48,6 | %53,9 | %47,6 | **%9,7** |
| +0,20R | **%1,5** | %66,3 | %67,4 | %65,9 | **%13,2** |

**Sonuçlar:**
1. **Geçme oranları benzer, 1 aşamalı yaklaşık 2 kat hızlı.**
   - Avantajı olmayan trader 1 aşamalıda biraz daha çok geçiyor (%38'e karşı %31-34).
   - Teori de bunu söylüyor: zirveden %10 düşmeden %10 kazanma olasılığı = e⁻¹ = %37.
   - Gerçek avantajı olan trader düşük riskle 2 aşamalıda biraz daha iyi (%79'a karşı %75).
2. ⚠️ **1 aşamalının en büyük tuzağı %3'lük günlük limit.**
   - Günde 2 işlem ve %1,5 riskte iki kayıp = %3 = ihlal. Geçme oranı +0,2R avantajla bile %66'dan **%13'e** çöküyor.
   - Kural: **işlem başına risk × o gün açabileceğin en fazla işlem sayısı < %3**. Gün içi açık zarar da sayıldığı için güvenli tarafta kal: ör. günde en fazla 2 işlem ve %1 risk.
3. **Tutarlılık kuralı** bu stratejilerde neredeyse etkisiz (±1-2 puan). Tek büyük gün kazancına dayanan stratejilerde önemli olur (§4e).
4. ⚠️ **Fonlu aşamada trailing limit hiç düşmüyorsa ödeme tamponu yer.**
   - Ör. 110 bin $ zirvede limit 100 bin $ olur. 9 bin $ çekersen bakiye 101 bin $'a iner, tampon %1 kalır.
   - **40. tur güncellemesi**: Trading Objectives sayfasının 1 aşamalı bölümü şöyle diyor: "Bir ödül çekilip yeni bir FTMO hesabı verildiğinde maksimum zarar limiti **tamamen sıfırlanır**, ilk gün limiti başlangıç sermayesinin %90'ına döner." Yani 1 aşamalıda ödemeden sonra tampon yine %10 olur, bu tuzak büyük ölçüde ortadan kalkıyor.
   - Aynı sayfada Instant hesapla ilgili blokta "Ödül çekilince maksimum zarar limiti **sıfırlanmaz**" yazıyor. Sayfa blokları karışık olduğu için satın almadan önce destekle yine teyit et.
   - Trailing ve çekilemez tampon modelimizde ödemeleri yarıya indiriyordu (§4l).
5. **Hangisini seçmeli?**
   - Kanıtlı avantaj ve düşük riskle uzun bir fonlu kariyer hedefliyorsan: statik limit, iade edilen ücret ve ölçeklendirme için **2 aşamalı** (§4n).
   - Hız istiyorsan ve günlük işlem sayını sıkı sınırlayabiliyorsan 1 aşamalı da olur. Ama günlük %3 limit ve trailing yapı hata payını daraltır.
## 4q. JadeCap (Kyle Ng): 4,5 milyon $ prop ödemesi, süreç ve firma riski (Chat With Traders #304, WgBFlbLZeeU)

> JadeCap, en büyük tek prop ödemesini (2,5 milyon $, Apex) almış ICT tabanlı forex ve futures trader'ı. Ödemeler büyük ölçüde kamuya açık sertifikalarla görüldü. ⚠️ Yine de hayatta kalanlardan biri, sonuçları seçilmiş bir örnek. Sponsor: Plus500.

**Yol** (kendi anlatımı):
- 2011'de 5.000 $'lık hesaplarla başlamış. **Yıllarca hesap patlatmış**:
  - Stopu genişletmek.
  - "Haftada %20" kovalamak.
  - Aşırı analizden doğan çok sayıda küçük kayıp: "beş küçük işlem bir tam stop ediyordu".
  - Ara verip aynı hatalara dönmek.
- **On yıl boyunca her düşüşte strateji değiştirmiş.** "Yeni bir şey öğrenmek bir sonraki işlemin olasılığını değiştirmiyor."
- Dönüm noktası:
  - Sadeleşmek: haftada **2-3 işlem**, iş yerinde ekrana daha az bakmak.
  - Pozisyon boyutu ve işlem yönetimine odaklanmak.
  - Maaşının 2-3 katını kazanana ve **2-3 yıllık gider** biriktirene kadar işini bırakmamak.
- **Prop firmalarına geçmeden önce ~10 yıl deneyimi vardı.** "Kârlı kullanan tanıdıklarımın hepsinin yıllarca deneyimi var. Yeni başlayan için kötü alışkanlıkları besleyebilir."

**Prop dersleri:**
1. **Prop, sermaye sıçrama tahtası.** "1.000 $'a 200 bin $'lık hesap, gerçekte 20 bin $'lık düşüş payı." 400K FTMO hesabında ~40 bin $ pay. "Fonlanmak 2-4 bin $'a mal oldu. Kendi hesabımı 40-50 bin $'a çıkarmaktan çok daha kolaydı."
2. **Hesaplar simüle. Ödemeler başarısız trader'ların ücretinden.** "Diğer trader'lara karşı bir yarışma." FPFX ve Topstep verisiyle uyumlu (§4h, §4o).
3. **Firmalar arasında çeşitlendir.**
   - Batan firmalar oldu, ona borcunu ödemeyenler oldu.
   - Hesap sayısı arttıkça **işlem başına riski %1-2'den %0,25-0,5'e indirmiş**. Düşüşler sığlaşmış, kazancı artmış.
   - ⚠️ Aynı işlemi tüm hesaplarda açmak tek bir büyük bahistir (02 §6c). Hesap başına riski düşürmek toplam riski makul tutmanın yolu.
4. **Prop kuralları "güvenlik tamponu" gibi disiplin öğretti.**
   - "Kişisel hesapta kimse %10-20-30 risk almamı engellemiyordu."
   - Düşüşte **sermaye eğrisini yataylaştırmayı** öğrenmiş: boyutu küçültmek, doğru setup'ı beklemek. Önceden düşüşte riski artırıp çukuru derinleştiriyormuş.
5. **İki yaklaşım**:
   - Çok agresif ("bozuk slot makinesi").
   - Çok temkinli: o, sermaye tabanı genişken bunu yapmış.
   - Agresif yaklaşımda "kumar oynuyor" diye ödeme reddi riski var. **Her firmanın kurallarını tek tek oku.**
   - Büyük ödemesinden sonra firma kuralları değiştirmiş. Belirsiz kurallarla sorun yaşamış (§4d).
6. **Sektör uyarıları**:
   - Kredi kartıyla borçlanıp challenge alan ve "kumarhane gibi" kullanan kullanıcılar var.
   - Firmaların tek gelir kaynağı ücretler. Trader'lar iyileştikçe ödeme yükü batırabilir (CFD firmalarının batması). Düzenleme riski de var.
7. **Süreç**:
   - Pazar akşamı haftalık hazırlık (ekonomik takvim).
   - FOMC haftasında Pazartesi ve Salı ya hiç işlem yok ya küçük işlem. Karar sonrası Çarşamba ve Perşembe yön aranır.
   - Her sabah 15 dakika meditasyon.
   - %80 teknik, %20 temel.
   - Piyasalar arası analiz (tahvil, kur, emtia) uyumsuzsa beklemek.
8. **Yılda 1-2 ay "hiçbir şey tutmuyor"**:
   - Ya ara verir ya önemsiz boyutla işlem yapar.
   - Stop olduktan sonra aynı fikre tekrar girmek "çok nadiren" işe yarıyor. İlk stop zaten fikrin geçersizlendiği yer.
9. **Genç haline tavsiyesi**: "Doğru pozisyon boyutu ve sabır. Haftada 1-3 işlem yap ve her birini didik didik incele. Haftada 30-50 işlemden kimse bir şey öğrenemez."

**Bilgi tabanıyla karşılaştırma:**
- ✔ Haftada birkaç işlem, yüksek zaman dilimi bağlamı, düşüşte boyut küçültme ve firma çeşitlendirmesi önceki bulgularla tutarlı (§4j-4o, 02).
- ⚠️ ICT "seans likiditesi" iddiası (Asya ya da Londra dibi süpürülünce ters yöne dön) mekanik olarak test edildi ve **rastgeleden ayırt edilemedi** (04 §6b-5, 11 #44, #61). JadeCap'in başarısı büyük ölçüde **yüksek zaman dilimi makro trendlerinden** gelmiş görünüyor: Ukrayna savaşından sonra 1,5 yıl EUR short. Takdir, boyut yönetimi ve deneyim de etkili. Süpürme kuralının kendisi kanıt değil.
## 4r. Peter Brandt'ın prop firması uyarısı (Words of Rizdom, 02tMCQLFIjg)

> 50 yıllık futures trader'ı. Röportaj sponsorlu (bir prop firması ve bir günlük uygulaması). Brandt kendisinin hiçbir firmadan para almadığını söylüyor.

**Eleştirileri:**
1. **"Ödemeli simülasyon (sim-for-payout) trading değil, oyun."**
   - ABD'deki online poker ve spor bahisleriyle aynı kategoride. Brandt yasal olup olmadığından emin değil, düzenlenip vergilendirilmesi gerektiğini düşünüyor.
   - Firma bir borsa değil, **kasaya karşı** oynuyorsun.
   - Kurallar başarısızlık için optimize edilmiş: günlük kapanış zorunluluğu, art arda "kârlı gün" şartları.
2. **Kurallar trader'ı kalıba sokuyor.** "Market Wizards'taki 71 trader'dan ikisi aynı işlem yapmıyor. Herkes deneme yanılmayla kendi yolunu bulur." Gün içi zorunluluğu ise "kârı koştur" ilkesiyle çelişiyor.
3. **Şeffaflık yok.** İngiltere'de forex kurumları kârlı müşteri oranını açıklamak zorunda, prop firmaları değil.
   - Brandt'ın tahmini: "1.000 hesaptan belki %1'i yıl sonunda kârlı, belki %0,5'i gerçek paraya geçiyor."
   - Topstep'in resmi verisi tahmini doğruluyor: Express fonlulardan Live hesaba geçen **%0,71** (§4o).
   - Bazı firmalar trader'ları gerçek hesaba taşıdığını söylüyor ama taşımıyor. Brandt'a göre bu dolandırıcılık. Topstep'i bu konuda doğru yaptığı için anıyor.
4. **Olumlu yanı**: kuralları çözen biri bir "problem çözücüdür". Bu kişileri gerçek sermayeye taşıyan firmalar değerli.
   - Brandt'ın önerdiği model: ödemesiz simülasyonda bir yıl özgürce öğren. Sonra kazanılan ödemenin bir kısmıyla kendi hesabında, kendi kurallarınla gerçek işlem yap.

**Pratik ölçütleri:**
- **İşi ne zaman bırakmalı?**
  1. Hesaptaki paranın tamamı **kâr** olmalı: eşinin parası, miras ya da ikinci ipotek olmamalı.
  2. Hesaptan ayrı **2 yıllık yaşam gideri** biriktirilmiş olmalı.
  3. Hesap, gerçekçi yıllık kazancının **3 katı** olmalı. Ör. yılda 100 bin $ gerekiyorsa 300 bin $ kâr.
  - (JadeCap: 2-3 yıllık gider ve maaşın 2-3 katı, §4q.)
- **Öğrenme süresi**: "Yönü sezmek 3 yıl, süreci oturtmak 3-4 yıl daha. Toplam 5-6 yıl, ve çoğu kişi o noktaya gelmeden sermayesini bitirir." Brandt'ın ilk işlemi 1974, ilk kârlı yılı 1979.
- **Risk**:
  - Bugün işlem başına en fazla %1, genellikle %0,6-0,8. 1987'de %5-10 riske ederek %600 yapmış: "şanstı, bugün beni korkutuyor".
  - %30-38'lik düşüşler yaşadıktan sonra "aynı doları tekrar tekrar kazanmaktan" bıkıp riski küçültmüş. Bugün %2-3 düşüş rahat, %5 şok etkisi yaratır. Düşüşü kapanmış işlemlerin net değerinden ölçüyor. 4 zararlı yılı var.
- **Başarı ölçütü** (Schwager): yıllık getiri / en kötü düşüş ≥ **3 olağanüstü, 4 dünya klası**. Bu bilgi tabanının "getiri / maksimum düşüş prop'ta asıl kısıt" bulgusuyla aynı (§2).
- **"Sızıntı" (leakage) ölçüsü**: kural ihlallerinin parasal maliyetini kaydet. Brandt'ın hedefi yılda ≤ 1.000 baz puan.
- **Gün içinde gördüğü işleme o gün giremez**: kapanışı bekleyip ertesi gün girer. Bu onun FOMO tamponu. Emirleri saat 4'te girip ekranı kapatıyor.
- **Bakiyesine haftalarca bakmıyor.** "Bakiyene sürekli bakıyorsan bu kötü bir işarettir."
- **"Bir sonraki işlemin kaybedeceğini varsay."** İsabet ~%50. Beklentileri en yüksek işlemleri çoğu zaman en kötüleri oluyor.
- **Kurallarını yılda bir kez** değiştiriyor, ilkeye dayalı ve küçük adımlarla. Ör. bu yıl haftalık grafik kurallarına 50 baz puanlık yeni bir dilim açmış. "Geçen yıl şunu yapsaydım" türü optimizasyon yok (10 §6j).
- **Sevdiği formasyonlar**:
  - Yatay sınırlı formasyonlar: yükselen üçgen, dikdörtgen.
  - Simetrik yapı.
  - Sıkışma fiyatın %15'inden dar.
  - Süre 6-8 ile 26 hafta arası, en iyisi 12 hafta.
  - COT verisine sadece 2 standart sapmalık uç değerlerde bakıyor.
- **Sosyal medya**: "Büyük gününün ekran görüntüsünü paylaşanı hemen takipten çık." 5 iyi kaynak seç ve onlara bağlı kal.

## 4s. Futures prop hesaplarının ödeme matematiği (Ashton, "The Prop Firm Payout Math Nobody Shows You", 1pL6BgWc4hg)

> Küçük bir kanal. Sayılar kendi simülasyonundan ve firma kurallarından. Hesaplar doğru ve bu bilgi tabanının bulgularıyla uyumlu.

- **50K esnek değerlendirme** (2.000 $ maksimum zarar, 3.000 $ hedef, %50 tutarlılık):
  - Avantaj yokken bir günde 1.500 $'a 2.000 $ kayıptan önce ulaşma olasılığı = 2.000/3.500 = **%57,14** (koridor formülü, §4o).
  - Tutarlılık için bunu iki ayrı günde yapmak gerekir: 0,5714² = **%32,65**. Bu, maliyetsiz geçme oranı.
- **Risk boyutu avantaja bağlıdır**: avantajın pozitifse daha düşük risk geçme oranını artırır. Negatifse azaltır, çünkü daha çok işlem yapılır, daha çok maliyet ödenir ve negatif beklenti daha uzun süre işler (§4m, 11 #68).
- **Önemli kurallar**:
  - Günlük limit "sert" mi (hesap biter, ör. Apex, Alpha Funded) yoksa "yumuşak" mı (sadece o gün kilitlenir)?
  - **Gün içi trailing yerine gün sonu trailing** seç.
  - Tutarlılık kuralı değerlendirmede mi var, fonlu hesapta mı?
- **"1.000 $ nasıl 450 $ olur?"**
  - Fonlu hesapta kârın **%50'si** çekilebilir (Lucid Flex), minimum ödeme 500 $, 5 "nitelikli gün" (≥100 $) şartı var, kâr payı %90.
  - Yani 1.000 $ kâr ettiğinde banka hesabına 450 $ geçer.
  - Bazı hesaplarda çekilemez tampon var. Ör. Alpha Funded 50K Instant: 1.500 $ tampon, 7 gün ≥250 $. İlk 500 $ için 2.000 $ kâr gerekir (§4l).
- **Avantajsız trader için ödeme zinciri** (onun simülasyonu, Alpha Instant modeli):
  - İlk ödeme %21,8.
  - İkinci ödeme **%6,8**.
  - Üçüncü ödeme **%2,3**.
  - Hesap başına ortalama net +265 $, maliyet ve kayma hariç.
  - Bu, fonlu hesabın "opsiyon" değerinin (§4l) ve Topstep'in "fonlananların 1/3'ü ödeme alıyor" verisinin (§4o) aynı yönde bir başka modeli.
- **"Ödemeyi hemen al mı, tamponda biriktir mi?"** Kendi simülasyonlarında biriktirmek uzun vadede daha kârlı. §4n ile aynı sonuç: avantajı olan için kâr tamponu hesabın ömrünü uzatır.
  - Sermayesi kısıtlı olan için ise erken ödeme yeni değerlendirmelere yatırım imkânı verir.
- **Seçim yöntemi**:
  - Firmanın tüm kurallarını yaz.
  - **Kendi işlem geçmişinle** farklı risk boyutlarını simüle et.
  - "Geçme oranı"nı değil, **ödemeye kadar satın alınan hesap sayısını** ve net nakit sonucunu ölç (ücret, tekrarlı ödemeler, kötü senaryolar dahil).
## 4t. Prop programını kim kullanmalı, kim kullanmamalı? (Lance Breitstein, hAwuIvMZkmQ)

> Breitstein, Trillium'da 10 yıldan fazla trader yetiştirmiş ve 100 milyon $+ gerçek kâr ettiğini söylüyor. Topstep'in kurucusuyla yaptığı görüşmeden sonra görüşleri yumuşamış. Her şeyden önce yalnızca **likiditesi ve sermayesi sağlam, saygın** firmaları kastediyor. Sektörde batan ve kullanıcısını dolandıran firma çok.

**Fayda gören 3 tip:**
1. **Yapı ve topluluk isteyen trader ya da hobici.**
   - Günlük limitler aşırı boyutu, zarardakine eklemeyi, intikam işlemini ve "kötü günde durmamayı" engeller. "100 $'lık simülasyon hesabını patlatmak, 100.000 $'lık birikimi patlatmaktan iyidir."
   - Küçük bir ücret ciddiyet getirebilir, ama **sabit bir eğitim gideri** olarak görülmeli, kayıp kovalama aracı olarak değil.
2. **Kanıtlı avantajı olan ama sermayesi olmayan trader.**
   - Firmanın ekonomisini kaybedenlerin ücretleri sübvanse ediyor. Kuralları gerçekten yenebiliyorsan kaldıraç çok cazip.
   - Ama bu kitle kullanıcıların belki **%1**'i. Breitstein kendini "beklenen değer maksimalisti" olarak tanımlıyor: kurallar sana pozitif beklenti veriyorsa kullanmakta sorun yok.
3. **Affiliate pazarlamacı**: en çok kazanan muhtemelen o. Arabaları ve ödemeleri gösteren kişiye "Gelirinin ne kadarı trading'den, ne kadarı referans komisyonundan?" diye sor. Bazıları komisyondan çok daha fazla kazandığını açıkça söylüyor.

**Zarar gören 3 tip:**
1. **Avantajı olmayan ve hesap üstüne hesap yakan trader** (en kalabalık grup). Hesap başına düşük ücret toplam kaybı küçük gösteriyor. "Kanıtlı bir avantajın yoksa birkaç ay **ücretsiz simülasyonda** işlemlerini kaydet, bir oyun kitabı oluştur, tutarlılık göster. Sonra satın al."
2. **Her gün sadece ES ya da NQ işleyen trader.**
   - Bunlar dünyanın en rekabetçi ve verimli piyasaları. Çoğu gün istisnai bir fırsat yok.
   - "Çalıştığım 5 firma ve 500'den fazla profesyonel trader'dan hiçbiri her gün düzenli ES ve NQ işlemiyordu."
   - Profesyonel, o gün **"oyunda" olan şeye** gider: kazanç sürprizi, FDA haberi, short squeeze, emtia arz şoku.
3. **Simülasyonun gerçeğe taşınmayan alışkanlıkları.**
   - Ücret aşağı tarafı sınırladığı için "kocaman pozisyonla geçmeye çalışmak" değerlendirme için rasyonel olabilir, ama profesyonel bir trader için **berbat bir alışkanlık**.
   - Simülasyonda likidite, kayma ve piyasa etkisi yok.
   - Çok kazanan trader firma için bir yük olabilir. Sonunda hesap limiti, ödeme kısıtı ya da daha küçük canlı hesapla karşılaşabilir: "Kasayı yenersin, kasa ne kadar kazanabileceğine sınır koyar." Gerçek bir prop firmasında bu olmaz.

**Bu bilgi tabanıyla tutarlılık**:
- "Avantajın yoksa ödeme" (§4o).
- "Yüksek risk ile hesap döndürme değerlendirmede rasyonel görünür ama yasak ve kötü alışkanlık" (§4m-4n).
- "Ücret değil, ödemeye kadar gereken hesap sayısı" (§4s).
- Brandt'ın eleştirisi (§4r).

## 4u. ✔ "Küçük hesap challenge'ı" (2.000 $ → 50.000 $) ve prop'a etkisi (Breitstein, LbSn-awZmm4 + simülasyon)

**Breitstein'ın iddiaları**:
- Hiçbir ciddi firmada (Trillium, SMB, Jane Street) başarılı bir trader alım gücünü %99 küçültüp küçük hesap büyütmeyi denemez. Profesyonelin kariyeri **daha fazla sermayeyi sorumlu yönetmeyi** kanıtlamak üzerine kurulur.
- Bu challenge'lar içerik için var. "2.000 $ üzerinde sorumlu bir %20 getiri viral olmaz." Viral olmak için aşırı risk, yoğunlaşma, kaldıraç ya da "home run" denemesi gerekir.
- Küçük hesapta kullanılan yöntemler (kaldıraç, likiditesi olmayan stiller) ölçeklenmez. "Yüzde getiri tek başına umurumda değil."
- Bellafiore (SMB): "Bir iyi işlem yap, sonra bir iyi işlem daha."

**Simülasyon** (`arastirma/verify_small_account.py`, RR 2, mevcut bakiyenin f'si kadar bileşik risk, 250 işlem ≈ 1 yıl. Başarı = bakiye %10'a düşmeden 25 kat):

| İşlem başı beklenti | Risk %1 | %3 | %5 | %10 | %20 | %33 |
|---|---|---|---|---|---|---|
| 0 (avantaj yok) | %0 | %0 | %0,1 | %1,7 (%67 batış) | %3,1 (%96 batış) | %2,9 (%97 batış) |
| +0,10R (iyi) | %0 | %0 | %1,6 | %14 (%28 batış) | %14 (%82 batış) | %8 |
| +0,20R (çok iyi) | %0 | %0,3 | %15 | %47 (%6 batış) | %39 (%54 batış) | %19 |

- **Bir yılda 25 kat, güçlü bir avantajla bile işlem başına ≥%5-10 risk ister.** %1-3 riskte imkânsıza yakın.
- **Avantajsız 31-36 kişiden biri** %20-33 riskle 25 kata ulaşır, geri kalanların %96-97'si batar. YouTube'da görülen başarı, görünmeyen batmış denemelerin hayatta kalanıdır.
- **Aynı risk prop hesabında** (FTMO 2 aşamalı tipi, günde 2 işlem): +0,20R avantajla %1 riskte geçme %87. %5 ve üstü riskte **%40**, yani avantajsız birinin %1 riskteki oranının (%49) bile altında. **Küçük hesap alışkanlığı prop'ta avantajı siler.**

**Sonuç**: Küçük hesap challenge'ı bir beceri kanıtı değil, bir risk seçimidir. Prop'a hazırlık olarak ters alışkanlık öğretir. Doğru ölçü yüzde getiri değil, getiri / düşüş (§4r) ve ölçeklenebilirlik.

## 4v. The5ers CEO'su: ödeme alan trader'ların davranışı ve firma risk yönetimi (Saul Lokier, Titans of Tomorrow dFZgmVGUmlM + simülasyon)

> Kaynak bir firma sahibi (çıkar çatışması var) ve sponsorlu bir kanal. Verisini yayımlamıyor, gözlemlerini anlatıyor. Aşağıdakiler bu tabandaki bağımsız bulgularla tutarlı olanlar.

**Ödeme alan ve büyük hesaplara çıkan trader'lar** (firmanın kendi hesap verisinden gözlemler):
- Çoğu **swing trader**: daha az işlem, işlemi koşturma, daha büyük RR. Scalper değiller. "Uzun vadede kârlı scalper olmak çok daha fazla beceri, sabır ve ekran süresi ister, çoğu trader henüz orada değil." (Phidias ve FPFX verisiyle uyumlu, §4h, §4k.)
- Stop kullanıyorlar, kayıplarla yaşıyorlar, tek bir stratejide ustalaşmışlar ("strateji atlamayı çoktan bırakmışlar").
- **Düşük efektif kaldıraç**: 1:100 erişimleri olsa da 1:10-1:20 kullanıyorlar. %1-2 risk için daha fazlası gerekmiyor.
- **Doğal deney (2021)**: aynı program 1:6 ve 1:30-1:50 kaldıraçla açıldı. Düşük kaldıraçtakiler daha iyi performans gösterdi. Yüksek kaldıraca geçen trader'lar düşük kaldıraçlı programa dönünce daha iyi yaptı. Belirsiz profilli fonlu trader'lardan birkaç hafta düşük kaldıraçla işlem yapmaları istendi, bunlar daha uzun yaşadı ve daha çok ödeme aldı. ⚠️ Kendi kendine seçilme var, kontrollü deney değil. Yine de §4m-4n'deki "düşük risk avantajı olanı uzun yaşatır" sonucuyla aynı yönde.
- **"Ödeme alma becerisi, trading becerisi değil"**: firma, toplam P&L'si negatif trader'lara da ödeme yapıyor (2K ödeme, sonra 5-10K kayıp). Bu trader ücret / ödeme oranında kârda, trading'de zararda. (§4l: statik limitli hesapta sıfır avantajlı trader modelde de pozitif çıkabiliyor.)

**Kaybedenlerin iki davranışı**:
1. Düşüşteyken **tek bir çok büyük işlem** açıp günlük ya da toplam limiti patlatmak.
2. Hedefe ~%2 kala **"hızlı bitireyim" diye büyük işlem** açmak.
- Tutarlı lot ve riskle işlem yapanlar daha iyi ve sonunda ödeme alıyor. Lot büyütüp küçültenlerin sonucu tahmin edilemiyor.

**Simülasyon** (`arastirma/verify_rescue_finish.py`, +%10 hedef, -%10 statik, -%5 günlük, RR 2, günde 2 işlem, taban risk %1; geçme olasılığı):

| İşlem başı beklenti | Sabit %1 | Kurtarma (-%6'da %3) | Bitirme (hedefe ≤%2 kala %3) | İkisi | Tilt (2 kayıptan sonra 2 kat) |
|---|---|---|---|---|---|
| -0,10R (maliyet sonrası tipik) | %26,2 | **%30,9** | %22,2 | %25,9 | **%33,6** |
| 0 | %51,4 | %53,8 | %46,8 | %49,8 | %49,7 |
| +0,10R | %74,9 | %73,9 | %71,9 | %71,5 | **%65,2** |
| +0,20R | %89,2 | %86,4 | %88,1 | %86,1 | **%77,2** |

- **Teori (Dubins-Savage)**: lehine bir oyunda hedefe ulaşma olasılığını küçük bahis, aleyhine bir oyunda **cesur bahis** en büyütür. Simülasyon aynen bunu gösteriyor.
- **Avantajı olmayan ya da negatif olan** trader için kurtarma işlemi ve tilt geçme olasılığını birkaç puan **artırıyor**. Bu davranışın neden bu kadar yaygın olduğunu açıklıyor: çoğunluk negatif avantajlı ve "cesur oyun" onlar için matematiksel olarak doğru. Yine de çoğu kaybediyor (%31-34).
- **Avantajı olan trader için** her sapma zararlı: tilt geçmeyi 10-12 puan, kurtarma 1-3 puan düşürüyor.
- **Hedefe yakın büyük işlem herkese zarar**: hedefe %2 kala zaten %1 riskli tek bir kazanç (+%2) yetiyor. %3'lük kayıp hedeften 3 puan uzaklaştırıyor.
- **CEO'nun gözlemi** ("bunu yapanlar batıyor") seçilimle de açıklanır: bunu yapanların çoğu zaten avantajsız. Kural aynı: **avantajını kanıtladıysan boyutu sabit tut. Hedefe yakınken boyutu büyütme.**

**Firma tarafı** (iş modeli bilgisi):
- Herkesin tersine işlem açmak, çift komisyon, çift spread ve likidite sağlayıcı ücreti yüzünden kârsız (11 #77 ile aynı).
- Eskiden (2016) %50 kâr payı, daha küçük maksimum zarar ve pahalı programlar vardı. Firma tüm işlemleri piyasaya gönderebiliyordu (A-book). Rekabetle fiyatlar düştü ve pay trader lehine arttı. Sadece B-book ve sadece ücret gelirine dayanan model "sürdürülebilir değil". Bugün makine öğrenmesiyle trader profili çıkarılıp A-book, B-book ya da ters pozisyon (C-book) kararı veriliyor.
- **Ödeme iddiaları**: büyük firmaların yılda 10-30 milyon $ ödemesi inandırıcı. Küçük firmaların aynı iddiaları, kripto cüzdanları arasında para gezdirilerek şişirilebilir (FPFX'ten Hertzberg de aynı uyarıyı yaptı, §4h).
- **Düzenleme**: CySEC, sektöre bir yatırımcı mevduatı girmediği için prop firmalarını düzenlemeyi kabul etmemiş. Anlık fonlama (instant funding) ücretin çekilebilir düşüşü karşılaması gerektiği için mevduata benziyor.
- CEO'nun kendi stili: 1 dakikalık grafikte arz/talep bölgesine kademeli giriş, isabet %80+, RR ≤1, kâr tam, zarar kısmi. "En verimli yol değil, kişiliğime uyuyor." İsabet ile RR'nin ters ilişkisi (README #45) burada da görülüyor.

## 4w. "Döner kapı" (revolving door) stratejisi: prop'u avantajsız "oyun" olarak oynamak (Waqar Asim, 8FXbZRS4Gq4 + simülasyon)

> Kanal satış kodları (firma indirim linkleri) ve kurs satıyor. "Konuştuğum bütün prop milyonerleri" örneklemi tanım gereği kazananlardan oluşuyor (hayatta kalma yanlılığı). Kanal **BIRAKILDI**, ama iddialar bu tabanın prop modeliyle test edilebildiği için incelendi.

**İddialar**:
1. "Prop'tan milyon kazananların hiçbiri sağduyulu, uzun vadeli bir stratejiyle kazanmadı. Hepsi prop'a özel agresif kurallarla oynadı. Bazılarının çalışan bir stratejisi bile yoktu."
2. Milyonerler değerlendirmelere 200-400 bin $ harcamış. Ücret/ödeme oranı 2023-24'te 1:10'du, şimdi 1:3-1:4 (daha çok kısıt, daha çok ödeme reddi).
3. **Döner kapı**: 5 fonlu hesabı haftalık aralıklarla aç (kopya işlem), +%3'te ödemeyi kilitle, düşüşteki hesabı "çöpe at", 2. aşamayı geçmeye %1 kalmış yedek hesapları devreye sok. "Başa baş bir trader bile kazanır: kazanç dönemleri büyür, kayıp dönemleri küçülür."
4. **Değerlendirmede tek işlemde maksimum günlük zararı (%4-4,5) riske at**, 1-2 işlemde geç.
5. "Fonlanıp ödeme alamayanların çoğu hesabı ilk haftada patlatıyor."

**Simülasyon** (`arastirma/verify_revolving_door.py`, FTMO tipi 100K: 1. aşama +%10, 2. aşama +%5, statik -%10, ücret 540 $; fonlu: %1 risk, RR 2, +%3'te tüm kârı çek, kâr payı %80):

| İşlem başı beklenti | Fonlu hesabın değeri (0'dan) | -%3'ten | Değerlendirme %1 risk: geçme / fonlu hesap başı maliyet | %4,5 risk: geçme / maliyet |
|---|---|---|---|---|
| -0,10R (maliyet sonrası tipik) | 4.193 $ | 2.498 $ | %11,8 / 4.569 $ | **%20,0** / 2.700 $ |
| 0 | 7.900 $ | 5.555 $ | %32,1 / 1.680 $ | %26,7 / 2.021 $ |
| +0,10R | 16.059 $ | 12.860 $ | **%58,1** / 930 $ | %34,5 / 1.567 $ |
| 0, ama ±0,3R'lik seriler (rejim) | 10.412 $ | 8.056 $ | %29,8 / 1.811 $ | %26,0 / 2.078 $ |

Fonlu hesap başına net değer ve ücret dolarına düşen ödeme:

| Beklenti | Hesabı limite kadar tut | -%3'te çöpe at |
|---|---|---|
| -0,10R, %1 değerlendirme | -375 $ (0,92 kat) | -2.824 $ (0,38 kat) |
| -0,10R, %4,5 değerlendirme | **+1.493 $** (1,55 kat) | -956 $ (0,65 kat) |
| 0, %1 değerlendirme | +6.220 $ (4,7 kat) | +734 $ (1,4 kat) |
| +0,10R, %1 değerlendirme | +15.130 $ (17 kat) | +2.372 $ (3,6 kat) |

**Sonuçlar**:
- **"Başa baş trader da kazanır" modelde doğru, ama sebebi strateji değil firmanın yapısı.** Avantajı sıfır bir fonlu hesabın değeri ≈ kâr payı × tampon (0,8 × 10.000 $ ≈ 7.900 $), §4l'deki opsiyonel durma sonucuyla aynı. Ücretten sonra hesap başına +6.200 $. Bu, firmanın bedava verdiği zarar tamponunun değeri. Firmaların kurallarla (tutarlılık, "kumar tarzı işlem", ödeme reddi, hesap sınırı) kapattığı açık da tam olarak bu. Konuşmacının kendisi de oranın 1:10'dan 1:3-4'e düştüğünü söylüyor.
- **Gerçekçi maliyetli trader (-0,10R)** hesabı tutup %1 riskle değerlendirmeye girerse zararda (-375 $). Değerlendirmede %4,5 risk ("cesur oyun") onu +1.493 $'a çıkarıyor. Yani bu tavsiye matematiksel olarak tam da **negatif avantajlı** trader'a yarıyor (§4v, Dubins-Savage). **Avantajı olan trader'ın** geçme oranını ise %58'den %35'e düşürüyor.
- **"Düşüşteki hesabı at"** her senaryoda ücret dolarına düşen ödemeyi 2,5-5 kat düşürüyor. Fonlu hesabın tamponu bedava verilmiş bir opsiyon, onu -%3'te atmak opsiyonu çöpe atmak demek. Tek bir "at ve yenile" kararı bile sadece hesap sınırı doluysa ve yeni fonlu hesabın maliyeti düşükse anlamlı olabilir. Avantajı negatif trader için her durumda zararlı.
- **Kademeli açma ve kopya işlem beklenen değeri değiştiremez**: toplamın beklentisi, hesapların beklentilerinin toplamıdır. Aynı sinyaller tüm hesaplara kopyalandığı için hesaplar çeşitlendirilmiş değil, tamamen ilişkilidir (§4g). Kademelendirme sadece aynı anda risk altındaki sermayeyi azaltır.
- **"+%3'te kilitle" beklentiyi değiştirmez** (§4l, opsiyonel durma). Sadece en az bir ödeme alma olasılığını artırır.
- **Seriler (rejim) varsa** çöpe atma biraz daha az zararlı, ama yine de tutmanın çok altında (3.028 $'a karşı 10.412 $).
- **Kurallar**: "tek işlemde maksimum günlük zarar", "hesap yak, yenisini al" ve hesaplar arası kopya ile risk yığma FTMO'nun yasak listesinde: aşırı kaldıraç, aşırı pozisyon, tek yönlü bahis, hesap döndürme (§4i, §4n). Konuşmacının önerdiği firmalar arasında FTMO da var. Bu stratejiyle alınan ödemeler **reddedilebilir**.

**Bu tabanın tavsiyesi değişmedi**: prop'u kanıtlanmış bir avantajı düşük maliyetle sermayeye çevirmek için kullan. Avantajı olan trader için hesabı tutmak, düşük risk ve tampon bırakmak en değerli yol (§4n). "Oyun" stratejileri avantajsızlar için firmanın bedava opsiyonunu sağmaya çalışmak demek: kural ihlali ve ödeme reddi riski taşıyor, ve avantaj kazandırmıyor.

## 4x. Zamco: 1,3 milyon $ prop ödemesinin içinden (Titans of Tomorrow, jw-HOnDexEc)

> İngiltere'nin en çok ödeme alan prop trader'larından biri, kendi beyanı. Son derece açık sözlü bir röportaj. Burada "nasıl yapılır" olarak değil, **bu tür başarıların gerçek yüzü** olarak alındı.

**Sayılar** (beyan):
- 8 yıl trading. İlk 6-6,5 yıl zararda: kendi parasından ~80 bin $ kayıp. İlk ödeme 18 ay önce.
- CFD prop firmalarına ~300 bin $ ücret, karşılığında 1,3 milyon $ ödeme (~1:4). Futures firmalarına 50-100 bin $, karşılığında 600-700 bin $ (~1:7).
- 2025'te ~1,03 milyon $. **Ekim-Aralık 2025, yılın kârının %60-70'i** (yarım milyon $). "Piyasa koşulları stratejime çok uygundu."
- Strateji: en basit trend devamı (yapı kırılımı, verimsizlik/FVG retest'i). Altın, DAX, Nasdaq. 1 dakikalık grafikte giriş, gün boyu tut.

**Nasıl oynadı**:
- **Değerlendirmede** izin verilen maksimum günlük zararı tek işlemde riske attı (ör. %4), geniş stop, 1:2-2,5 hedef. İki kazanç = fonlandı. Fonlu hesapta riski düşür, tek iyi işlem = ödeme, sonra bekle.
- 1-1,5 milyon $ fonlamayı kopya işlemle yönetti (2,6 milyonda hesapları unutmaya başladı). Futures'ta 20 hesaba kopya.
- Günlük limiti beklemek yerine hesabı **bilerek patlatıp** yenisini alarak düşüşü "sıfırladı". "Bu benim aptallığım."
- Ödemeden sonra firmalar riskini %1 ile sınırladı. Bazı firmalarda yasaklandı.

**Görmezden gelinmemesi gerekenler** (kendi sözleri):
- **Sağlık**: 2-4 saat uyku, gece 1'de 8 saat ekrana kilitlenme, kanlanmış gözler, baş ağrısı, yemek yiyememe, sürekli kusma hissi. "Trading'den nefret ediyorum, zehirli bir şey, ama bırakamıyorum."
- **Bağımlılık**: kişisel hesapta 1:500 kaldıraçla 2.000 $'ı iki haftada 350.000 $'a çıkardı, 250 bin çekti, kalan 100 bini 20-30 dakikada kaybetti. "Bağımlı olabilirim. Kişisel hesabı yavaş büyütecek psikolojim yok." Prop'un dış kuralları onu durdurduğu için prop'ta kazanabildiğini söylüyor.
- **Hiç tatmin yok**: 1 milyon $'ın üstünde bile "zengin olmadım, geride kaldım" hissi. "Yalnızca işlemdeyken bir şey hissediyorum."
- **Firma seçim ölçütü**: "Risk kuralları gevşekse (tek işlemde %3+ izin) iyi firma." Avantajı olan bir trader için bu ölçüt tersine işler. Önemli olan statik limit, ödeme güvenilirliği ve kurallarla uyumlu bir strateji (§4l).
- "Prop'ta birkaç yıllık fırsat kaldı, kurallar sıkılaşıyor."

**Test** (10 §6o): Ekim-Aralık 2025'te altında **becerisiz rastgele long** girişler, RR 2 ile işlem başına +0,22R ve %58 isabet verdi. Short'lar -0,31R. Yani bu dönemin olağanüstü sonucunun önemli bir kısmı altının tarihi yükselişindeki yönden gelebilir. Beceriyle ayırt etmek için yön eşleştirilmiş kıyas gerekir.

**Bu tabanla tutarlılık**: değerlendirmede maksimum risk (§4w, §4v), hesap döndürme yasağı (§4n), hayatta kalma yanlılığı (§4j), kumar ile trading sınırı (08 §8). Kendisinin de söylediği gibi bu yol bir "oyun". Ödemelerin bir kısmı firmanın tamponundan, bir kısmı bir rejimden geliyor, ve bedeli sağlık.

## 5. "Demo mu, küçük ücretli hesap mı?"

- Röportaj: "Demo yapma, 19$'lık 2.5k hesap al" → psikolojik baskıyı erkenden yaşamak için mantıklı bir argüman **ama** ancak sistemin önce replay/backtest'te R-kaydıyla pozitif EV gösterdiyse. Sırayla: backtest/replay (100+ işlem) → demo/forward test (kuralları canlı hızda uygulayabiliyor musun) → küçük gerçek/prop hesap.
