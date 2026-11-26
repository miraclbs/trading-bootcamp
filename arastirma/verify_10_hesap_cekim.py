"""Hedef: challenge'ı geç + fonlu hesabı %10 büyüt + çek. Kaç hesap gerekir? (2026-11-27, kullanıcı sorusu)

Model: FTMO 2 aşamalı (+%10, +%5, statik -%10, günlük -%5). Fonlu hesapta hedef +%10'a, -%10'a inmeden ulaşmak.
Günde 1 işlem, RR 2, kazanma olasılığı (1+e)/3 → maliyet sonrası e R/işlem. Hesaplar bağımsız (art arda alınır,
aynı işlem kopyalanmaz). Ödeme: %10 × 100.000 $ × %80 kâr payı = 8.000 $ + ücret iadesi (540 €).
Kur varsayımı: 1 € = 1,12 $ (540 € ≈ 605 $).
"""
import math
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rng = np.random.default_rng(271127)
N, K = 200_000, 2.0
FEE_EUR, EURUSD = 540.0, 1.12
FEE = FEE_EUR * EURUSD
PAYOUT = 0.10 * 100_000 * 0.80


def sim(e, r, funded_target=0.10):
    p = (1 + e) / (1 + K)
    state = np.zeros(N, np.int8); eq = np.zeros(N); days = np.zeros(N, np.int32)
    passed = np.zeros(N, bool); ok = np.zeros(N, bool); d_ok = np.full(N, -1)
    for t in range(20000):
        act = (state >= 0) & (state <= 2)
        if not act.any():
            break
        win = rng.random(N) < p
        eq = np.where(act, eq + np.where(win, K * r, -r), eq)
        days += act
        dead = act & ((eq <= -0.10) | ((r >= 0.05) & ~win))
        tgt = np.select([state == 0, state == 1, state == 2], [0.10, 0.05, funded_target], 9)
        hit = act & ~dead & (eq >= tgt)
        passed |= hit & (state == 1)
        done = hit & (state == 2)
        ok |= done; d_ok = np.where(done, days, d_ok)
        state = np.where(dead, -1, state)
        state = np.where(hit & (state < 2), state + 1, state)
        state = np.where(done, 3, state)
        eq = np.where(hit, 0.0, eq)
    return passed.mean(), ok.mean(), d_ok[ok]


print(f"Ödeme 8.000 $ + iade {FEE:.0f} $, ücret {FEE_EUR:.0f} € ≈ {FEE:.0f} $. Hesaplar bağımsız.\n")
for r in (0.005, 0.01, 0.02):
    print(f"=== işlem başına risk %{r * 100:.1f} ===")
    print(" avantaj | geçer | geçer+%10 çeker | geçenlerin çekme payı | n %90 / %95 / %99 | ort. ücret | "
          "medyan gün (çekene) | çekim başına net $ | deneme başına net $")
    for e in (-0.10, -0.05, 0.0, 0.10, 0.20):
        pp, s, d = sim(e, r)
        ns = [math.ceil(math.log(1 - t) / math.log(1 - s)) if 0 < s < 1 else (1 if s >= 1 else 0) for t in (.9, .95, .99)]
        fees = 1 / s if s > 0 else float("inf")
        net_cycle = PAYOUT + FEE - FEE * fees          # art arda al, ilk çekimde dur
        ev = s * (PAYOUT + FEE) - FEE                  # tek deneme
        med = int(np.median(d)) if len(d) else -1
        print(f"  {e:+.2f}  | %{pp * 100:4.1f} | %{s * 100:5.1f}          | %{s / pp * 100:4.0f}                  | "
              f"{ns[0]:3d} / {ns[1]:3d} / {ns[2]:3d}    | {fees:5.1f}     | {med:5d}               | "
              f"{net_cycle:+8.0f}         | {ev:+6.0f}")
    print()
