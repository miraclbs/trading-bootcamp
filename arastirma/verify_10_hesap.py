"""10 hesap alırsak en az birini geçme olasılığı (2026-11-27, kullanıcı sorusu).

Model: FTMO 2 aşamalı (1. aşama +%10, 2. aşama +%5, statik -%10, günlük -%5, süre sınırı yok).
Günde 1 işlem, RR 2, kazanma olasılığı (1+e)/3 → maliyet sonrası işlem başına e R. Risk, başlangıç bakiyesinin %'si.
Hesap büyüklüğü (100K / 200K) yüzdeleri değiştirmez: geçme olasılığı aynı, ücret ve ödeme 2 kat.

10 hesap arasındaki bağ (q): her gün q olasılıkla bütün açık hesaplar AYNI işlemi alır (ortak sonuç),
1-q olasılıkla her hesap kendi bağımsız işlemini alır. q=0: tamamen bağımsız (ayrı zamanlarda ya da ilişkisiz
setup'larla). q=1: aynı işlemi 10 hesapta aynı anda açmak (tek büyük bahis).
"İlk ödeme": fonlu hesapta en az 10 işlem sonra bakiye ≥ +%1 iken, -%10'a inmeden önce (ücret bu ödemeyle iade).
"""
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(2026_11_27)
N, A, T, K = 20_000, 10, 3000, 2.0


def sim(e, r, q):
    p = (1 + e) / (1 + K)
    state = np.zeros((N, A), np.int8)          # 0: aşama 1, 1: aşama 2, 2: fonlu, 3: ödeme aldı, -1: kaybetti
    eq = np.zeros((N, A)); days = np.zeros((N, A), np.int16)
    passed = np.zeros((N, A), bool)
    for _ in range(T):
        act = (state >= 0) & (state <= 2)
        if not act.any():
            break
        common = rng.random(N) < p
        own = rng.random((N, A)) < p
        use_common = rng.random(N) < q
        win = np.where(use_common[:, None], common[:, None], own)
        eq = np.where(act, eq + np.where(win, K * r, -r), eq)
        days = np.where(act & (state == 2), days + 1, days)
        dead = act & ((eq <= -0.10) | ((r >= 0.05) & ~win))
        p1 = act & ~dead & (state == 0) & (eq >= 0.10)
        p2 = act & ~dead & (state == 1) & (eq >= 0.05)
        pay = act & ~dead & (state == 2) & (days >= 10) & (eq >= 0.01)
        passed |= p2
        state = np.where(dead, -1, state)
        state = np.where(p1, 1, state); state = np.where(p2, 2, state); state = np.where(pay, 3, state)
        eq = np.where(p1 | p2, 0.0, eq)
    paid = state == 3
    return passed.mean(), passed.any(1).mean(), passed.sum(1).mean(), paid.mean(), paid.any(1).mean()


print("FTMO 2 aşamalı, 10 hesap. Hücre: P(en az 1 geçer) / beklenen geçen sayısı / P(en az 1 ödeme)")
for r in (0.01, 0.02):
    print(f"\n=== işlem başına risk %{r * 100:.0f} ===")
    print(f"{'avantaj':>8} | {'tek hesap geçer / ödeme':>24} | " + " | ".join(f"{'q=' + str(q):^22}" for q in (0.0, 0.5, 0.8, 1.0)))
    for e in (-0.10, -0.05, 0.0, 0.10, 0.20):
        cells, single = [], None
        for q in (0.0, 0.5, 0.8, 1.0):
            p1, pany, npass, pay1, payany = sim(e, r, q)
            single = single or f"%{p1 * 100:4.1f} / %{pay1 * 100:4.1f}"
            cells.append(f"%{pany * 100:4.1f} / {npass:4.2f} / %{payany * 100:4.1f}")
        print(f"{e:+8.2f} | {single:>24} | " + " | ".join(cells))

print("\nKontrol (bağımsız formül 1-(1-p)^10):")
for p in (0.12, 0.14, 0.168, 0.33, 0.61):
    print(f"  p=%{p * 100:4.1f} → %{(1 - (1 - p) ** 10) * 100:4.1f}")
