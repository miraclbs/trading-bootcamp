# 07 — Çoklu Zaman Dilimi (Top-Down / Time-Frame Alignment)

> Güven seviyesi: **ORTA-YÜKSEK** — kavram evrensel (Elder'in "Triple Screen"inden beri), ama "RR'ı 2:1'den 5:1'e çıkarır" gibi iddialar **kanıtsız**.
> Kaynaklar: Mulham Trading "Trading is hard until you apply these 2 concepts" (FxHBdSCDKdM), DD Finance backtest videosu, Yusuf Trades röportajı (HTF bias).

## Fikir

- **Büyük resim (HTF)**: yön/bias + kilit seviye (bölge).
- **Küçük resim (LTF)**: o bölgede tetik (yapı değişimi / onay mumu) + dar stop.
- HTF seviyeden gelen LTF yapı **geçerlidir**; HTF seviyesi olmayan yerdeki LTF BOS'lar çoğu zaman devam etmez (Mulham'ın ana tespiti — mantıklı ama test edilmeli).

## Kombinasyonlar (işlem tarzına göre seç)

| Tarz | HTF (bağlam) | Orta (yapı) | LTF (giriş) |
|---|---|---|---|
| Swing | Haftalık | Günlük | 4H / 1H |
| Gün içi | Günlük / 4H | 1H | 15m / 5m |
| Scalp | 1H | 15m | 1m–3m |

Kural: zaman dilimleri arası oran ~4–6×. Çok fazla zaman dilimi = analiz felci ve çelişkili sinyal.

## İki kullanım şekli

1. **HTF seviye → LTF tetik**: Fiyat 4H kilit bölgeye gelir → 15m'de MSS/CHoCH (yön değişimi) veya engulfing → giriş, stop LTF yapı noktasının ötesine.
2. **HTF yapı içinde LTF devam**: 4H'de geçerli BOS sonrası range oluştu → 15m'de bu range'in indirim bölgesinden (alt yarı) long tetik ara.

## Karşı görüş: Grimes "MTF bir moda kelime" diyor (Tz_l1OBJRK4)

- "**Çoklu zaman dilimine ihtiyacın yok.**" Birkaç gün ya da hafta grafik incelemesiyle tek bir günlük grafikten haftalığın nasıl göründüğünü çıkarabilirsin. Grimes iki zaman dilimini sadece yüzlerce grafiği hızlı taramak için "koltuk değneği" olarak kullanıyor.
- "MTF trading, sanki tüm sorunları çözüyormuş gibi insanlara **satılan bir moda kelime**. Çözmüyor. Trading'in özü tek zaman diliminde yakalanabilir."
- **Gerçek tehlike: işlem ortasında plansız zaman dilimi değiştirmek.**
  - Scalp olarak girip zaman dilimini sürekli büyüterek **scalp'te büyük kayıp** yemek.
  - Haftalık bir işleme girip 5 dakikalık grafikteki hareketi beğenmediği için birkaç saat sonra çıkmak. "Saçmalık."
  - → Hangi zaman diliminde işlem yaptığını bil, o zaman dilimine uygun riski ve bilgiyi kullan ve ona sadık kal.
- Brandt'ın rutini de bununla uyumlu: haftalık → günlük, intraday nadiren ve sadece zamanlama için.

**Sentez:** MTF bir **bağlam ve zamanlama aracı** olarak faydalı (Mulham, Brandt, Beggs'in 3 zaman dilimi). Ama sihirli bir avantaj değil (Mulham'ın "RR'ı 5:1'e çıkarır" iddiası kanıtsız, 11 #8). En önemli kural: **işlem zaman dilimini girişten önce belirle ve işlem boyunca değiştirme.** Değiştireceksen planın parçası olsun.

## Uyarılar

- LTF'ye inmek stopu daraltır → RR yükselir **ama WR düşer** (gürültü). RR artışı bedava değil — bkz. 01 §3.
- "Kilit seviye" tanımın (order block, FVG, S/R, engulfing, VAH/VAL...) önemli değil, **tutarlı ve test edilmiş** olması önemli. Mulham bunu doğru vurguluyor: hangi seviye tipini seçersen seç, aynı kuralla uygula.
- HTF bias yanlışsa LTF'deki her "mükemmel" setup stop olur. HTF bias'ı da kuralla tanımla (örn. günlük kapanış son swing high üstünde = bullish).
