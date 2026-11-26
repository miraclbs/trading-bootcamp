# -*- coding: utf-8 -*-
"""
verify_birikim.py  --  bilgi/18-servet-ve-yatirim.md icin hesaplar

Kullanim:
    python verify_birikim.py [shiller_csv_yolu]

Bolumler
  A. Deterministik bilesik faiz tablolari (aylik 300$, reel getiriler, SWR geliri)
  B. Hedef gelir icin gereken aylik yatirim, 10 yilda 300$ ile emeklilik testi
  C. Tasarruf orani -> calisma yili (Mr. Money Mustache tablosunun yeniden hesabi)
  D. Tarihsel ABD verisi (Shiller, S&P 500 + temettu + CPI, 1871-2023/06):
       reel getiri, kotu donemler, tarihsel aylik 300$ birikim dagilimi,
       guvenli cekim orani (SWR) testi, getiri sirasi riski
  E. Turkiye: TUFE ve USD/TRY (2015-2025) -> dolarin ve S&P 500'un TL bazinda reel getirisi
     (USD/TRY: TCMB yil sonu gosterge kuru; TUFE: TUIK Aralik yillik;
      S&P 500 toplam getiri: yaygin yayimlanan yillik rakamlar, 2025 = %17,9)

Varsayimlar
  * Tum tutarlar BUGUNUN DOLARI (reel). Getiriler enflasyondan arindirilmis reel getiri.
  * Katkilar her ay sonunda yapilir; aylik getiri = (1+yillik)^(1/12)-1 (efektif yillik).
  * Vergi, komisyon, fon gideri YOK (gercekte bunlar getiriyi dusurur).
  * Shiller CSV: https://raw.githubusercontent.com/datasets/s-and-p-500/main/data/data.csv
    (Robert Shiller'in verisinden turetilmis aylik seri; fiyatlar aylik ortalama,
     temettu yillik tutar, CPI). Arg verilmezse URL'den okunur.
  * Tahvil getirisi (SWR testi icin) 10 yillik faizden yaklasik hesaplanir:
    her ay kuponu y0 olan 10 yillik par tahvil alinir, bir ay sonra y1 ile fiyatlanir.
"""
import sys
import math
import numpy as np
import pandas as pd

SHILLER_URL = "https://raw.githubusercontent.com/datasets/s-and-p-500/main/data/data.csv"


def fmt(x):
    return f"{x:,.0f}"


# ---------------------------------------------------------------------------
# A. Deterministik bilesik faiz
# ---------------------------------------------------------------------------
def fv_monthly(pmt, years, r_annual, growth_annual=0.0):
    """Aylik katki (ay sonu), yillik efektif reel getiri, katki her yil growth kadar artar."""
    rm = (1 + r_annual) ** (1 / 12) - 1
    bal = 0.0
    contrib = 0.0
    for y in range(years):
        c = pmt * (1 + growth_annual) ** y
        for _ in range(12):
            bal = bal * (1 + rm) + c
            contrib += c
    return bal, contrib


def section_a():
    print("=" * 78)
    print("A1. Aylik 300$ (bugunun dolari), reel getiri; nihai deger ve SWR ile aylik gelir")
    print("=" * 78)
    years_list = [10, 15, 20, 25, 30]
    rates = [0.03, 0.05, 0.07, 0.09]
    print(f"{'Yil':>4} {'Yatirilan':>10} | " + " | ".join(f"{'%'+str(int(r*100))+' reel':>26}" for r in rates))
    print(f"{'':>4} {'':>10} | " + " | ".join(f"{'deger / %3,5 / %4 aylik':>26}" for _ in rates))
    for n in years_list:
        row = []
        for r in rates:
            fv, c = fv_monthly(300, n, r)
            row.append(f"{fmt(fv):>10} / {fmt(fv*0.035/12):>5} / {fmt(fv*0.04/12):>5}")
        print(f"{n:>4} {fmt(c):>10} | " + " | ".join(f"{s:>26}" for s in row))

    print()
    print("A1b. Katkinin nihai degerdeki payi (%7 reel): erken donemde kaldirac 'ne kadar yatirdigin'")
    for n in years_list:
        fv, c = fv_monthly(300, n, 0.07)
        print(f"  {n:>2} yil: katkilar {fmt(c)}$, buyume {fmt(fv-c)}$ -> katki payi %{100*c/fv:.0f}")

    print()
    print("=" * 78)
    print("A2. Katkiyi her yil reel %5 artirmak (300$ ile baslayip)")
    print("=" * 78)
    for r in [0.05, 0.07]:
        print(f"  Reel getiri %{int(r*100)}:")
        for n in years_list:
            fv0, c0 = fv_monthly(300, n, r)
            fv1, c1 = fv_monthly(300, n, r, 0.05)
            last = 300 * 1.05 ** (n - 1)
            print(f"   {n:>2} yil: sabit {fmt(fv0):>9}$ (gelir %4: {fmt(fv0*0.04/12):>5}$/ay) | "
                  f"+%5/yil {fmt(fv1):>9}$ (gelir %4: {fmt(fv1*0.04/12):>5}$/ay), "
                  f"son yil aylik katki {fmt(last)}$, toplam yatirilan {fmt(c1)}$")

    print()
    print("A3. Kaldirac karsilastirmasi (10 yil): getiriyi +2 puan artirmak mi, katkiyi artirmak mi?")
    base, _ = fv_monthly(300, 10, 0.05)
    hi_r, _ = fv_monthly(300, 10, 0.07)
    hi_c, _ = fv_monthly(600, 10, 0.05)
    print(f"  300$/ay %5: {fmt(base)}$ | 300$/ay %7: {fmt(hi_r)}$ (+%{100*(hi_r/base-1):.0f}) | "
          f"600$/ay %5: {fmt(hi_c)}$ (+%{100*(hi_c/base-1):.0f})")
    base30, _ = fv_monthly(300, 30, 0.05)
    hi_r30, _ = fv_monthly(300, 30, 0.07)
    print(f"  30 yilda: 300$/ay %5: {fmt(base30)}$ | 300$/ay %7: {fmt(hi_r30)}$ (+%{100*(hi_r30/base30-1):.0f})")


# ---------------------------------------------------------------------------
# B. Hedef gelir icin gereken aylik yatirim; "10 yilda 300$ ile emeklilik"
# ---------------------------------------------------------------------------
def required_pmt(target_capital, years, r):
    unit, _ = fv_monthly(1.0, years, r)
    return target_capital / unit


def solve_rate(pmt, years, target):
    lo, hi = -0.5, 3.0
    for _ in range(200):
        mid = (lo + hi) / 2
        fv, _ = fv_monthly(pmt, years, mid)
        if fv < target:
            lo = mid
        else:
            hi = mid
    return mid


def years_to_target(pmt, r, target):
    rm = (1 + r) ** (1 / 12) - 1
    bal, m = 0.0, 0
    while bal < target and m < 12 * 200:
        bal = bal * (1 + rm) + pmt
        m += 1
    return m / 12


def section_b():
    print()
    print("=" * 78)
    print("B1. Bugunun parasiyla hedef aylik gelir icin gereken aylik yatirim")
    print("=" * 78)
    for swr in [0.04, 0.035]:
        print(f"  Cekim orani %{swr*100:.1f}:")
        for inc in [1000, 2000]:
            cap = inc * 12 / swr
            parts = []
            for n in [10, 15, 20, 30]:
                for r in [0.05, 0.07]:
                    parts.append(f"{n}y@%{int(r*100)}: {fmt(required_pmt(cap, n, r))}$")
            print(f"   {inc}$/ay gelir -> sermaye {fmt(cap)}$ | " + ", ".join(parts))

    print()
    print("B2. '10 yilda aylik 300$ ile emekli olmak' testi")
    for r in [0.05, 0.07]:
        fv, c = fv_monthly(300, 10, r)
        print(f"  %{int(r*100)} reel, 10 yil: {fmt(fv)}$ -> %4 ile {fmt(fv*0.04/12)}$/ay")
    for inc in [1000, 2000]:
        cap = inc * 12 / 0.04
        rr = solve_rate(300, 10, cap)
        print(f"  10 yilda {fmt(cap)}$ (={inc}$/ay) icin 300$/ay ile gereken reel getiri: yilda %{rr*100:.0f}")
        for r in [0.05, 0.07]:
            print(f"     300$/ay %{int(r*100)} reel ile bu sermayeye ulasma suresi: {years_to_target(300, r, cap):.1f} yil")


# ---------------------------------------------------------------------------
# C. Tasarruf orani -> calisma yili (MMM)
# ---------------------------------------------------------------------------
def years_to_fi(s, r, swr=0.04):
    """Net gelir=1/yil. Harcama=(1-s). Hedef=(1-s)/swr. Aylik katki s/12. 0'dan baslar."""
    if s <= 0:
        return float("inf")
    target = (1 - s) / swr
    rm = (1 + r) ** (1 / 12) - 1
    bal, m = 0.0, 0
    while bal < target and m < 12 * 150:
        bal = bal * (1 + rm) + s / 12
        m += 1
    return m / 12


def section_c():
    print()
    print("=" * 78)
    print("C. Tasarruf orani -> finansal bagimsizliga kadar calisma yili (0'dan, %4 cekim)")
    print("=" * 78)
    print(f"{'Tasarruf':>9} | {'%3 reel':>8} | {'%5 reel (MMM)':>13} | {'%7 reel':>8}")
    for s in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]:
        print(f"{'%'+str(int(s*100)):>9} | {years_to_fi(s,0.03):>8.1f} | {years_to_fi(s,0.05):>13.1f} | {years_to_fi(s,0.07):>8.1f}")


# ---------------------------------------------------------------------------
# D. Tarihsel ABD (Shiller)
# ---------------------------------------------------------------------------
def load_shiller(path):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df[(df["Dividend"] > 0) & (df["Consumer Price Index"] > 0)].copy()
    df = df.sort_values("Date").reset_index(drop=True)
    # ardisik aylari koru
    gaps = df["Date"].diff().dt.days.fillna(31)
    if (gaps > 32).any():
        cut = gaps[gaps > 32].index[0]
        df = df.iloc[:cut]
    P = df["SP500"].values
    D = df["Dividend"].values
    C = df["Consumer Price Index"].values
    Y = df["Long Interest Rate"].values / 100.0
    nom = (P[1:] + D[:-1] / 12) / P[:-1] - 1
    real = (1 + nom) * C[:-1] / C[1:] - 1
    # tahvil yaklasimi
    T = 10.0
    bond_nom = []
    for i in range(len(Y) - 1):
        y0, y1 = Y[i], Y[i + 1]
        t = T - 1 / 12
        price = (y0 / y1) * (1 - (1 + y1) ** -t) + (1 + y1) ** -t if y1 > 0 else 1.0
        bond_nom.append(price - 1 + y0 / 12)
    bond_nom = np.array(bond_nom)
    bond_real = (1 + bond_nom) * C[:-1] / C[1:] - 1
    dates = df["Date"].values[1:]  # getirinin bittigi ay
    return pd.DataFrame({"date": dates, "eq": real, "bond": bond_real})


def ann(x_months):
    return np.prod(1 + x_months) ** (12 / len(x_months)) - 1


def section_d(path):
    print()
    print("=" * 78)
    print("D. Tarihsel ABD verisi (Shiller): S&P 500 reel toplam getiri (temettu dahil)")
    print("=" * 78)
    r = load_shiller(path)
    eq = r["eq"].values
    bd = r["bond"].values
    dates = pd.to_datetime(r["date"])
    print(f"  Veri: {dates.iloc[0].strftime('%Y-%m')} -> {dates.iloc[-1].strftime('%Y-%m')} ({len(eq)} ay)")
    print(f"  Tum donem reel yillik: hisse %{ann(eq)*100:.2f}, 10y tahvil (yaklasik) %{ann(bd)*100:.2f}")
    m1900 = (dates >= "1900-02-01").values
    print(f"  1900-2023 reel yillik: hisse %{ann(eq[m1900])*100:.2f} (DMS 1900-2025 ABD: %6,6)")

    # yuvarlanan pencereler
    print("\n  D1. Yuvarlanan pencerelerde yillik reel getiri (S&P 500, temettu dahil)")
    logr = np.log1p(eq)
    cs = np.concatenate([[0], np.cumsum(logr)])
    for n in [10, 20, 30]:
        w = 12 * n
        a = np.exp((cs[w:] - cs[:-w]) / n) - 1
        i_min = int(np.argmin(a))
        start = dates.iloc[i_min] - pd.DateOffset(months=1)
        print(f"   {n} yil: en kotu %{a.min()*100:.1f} (baslangic {start.strftime('%Y-%m')}), "
              f"%5'lik dilim %{np.percentile(a,5)*100:.1f}, medyan %{np.median(a)*100:.1f}, "
              f"en iyi %{a.max()*100:.1f}, negatif pencere orani %{100*(a<0).mean():.1f}")

    # drawdown ve su alti sureleri
    print("\n  D2. Reel toplam getiri endeksinde dususler ve 'su alti' sureleri")
    idx = np.exp(np.cumsum(logr))
    peak = np.maximum.accumulate(idx)
    dd = idx / peak - 1
    print(f"   En buyuk reel dusus: %{dd.min()*100:.0f} ({dates.iloc[int(np.argmin(dd))].strftime('%Y-%m')})")
    episodes = []
    in_dd, start_i = False, 0
    for i in range(len(idx)):
        if dd[i] < 0 and not in_dd:
            in_dd, start_i = True, i
        elif dd[i] >= 0 and in_dd:
            episodes.append((start_i, i, dd[start_i:i].min()))
            in_dd = False
    if in_dd:
        episodes.append((start_i, None, dd[start_i:].min()))
    episodes.sort(key=lambda e: -((e[1] if e[1] is not None else len(idx)) - e[0]))
    for s, e, m in episodes[:4]:
        end_txt = dates.iloc[e].strftime('%Y-%m') if e is not None else "veri sonu"
        length = ((e if e is not None else len(idx)) - s) / 12
        print(f"   Zirve {dates.iloc[s-1].strftime('%Y-%m') if s>0 else '-'} -> toparlanma {end_txt}: "
              f"{length:.1f} yil, en dip %{m*100:.0f}")
    # 2000 sonrasi
    m2000 = (dates >= "2000-01-01").values
    sub = idx[m2000] / idx[m2000][0]
    rec = np.where(sub >= 1.0)[0]
    rec = rec[rec > 12]
    if len(rec):
        print(f"   Ocak 2000'de alan biri reel olarak {dates[m2000].iloc[rec[0]].strftime('%Y-%m')} tarihinde basa bas (temettu dahil)")

    # tarihsel DCA 300$/ay
    print("\n  D3. Tarihsel aylik 300$ (reel) S&P 500 birikimi: her baslangic ayi icin nihai reel deger")
    for n in [10, 20, 30]:
        w = 12 * n
        finals, starts = [], []
        for s in range(0, len(eq) - w + 1):
            bal = 0.0
            for k in range(w):
                bal = bal * (1 + eq[s + k]) + 300
            finals.append(bal)
            starts.append(dates.iloc[s])
        f = np.array(finals)
        i_min, i_max = int(np.argmin(f)), int(np.argmax(f))
        det, _ = fv_monthly(300, n, 0.07)
        print(f"   {n} yil (yatirilan {fmt(300*w)}$): en kotu {fmt(f.min())}$ ({starts[i_min].strftime('%Y-%m')} baslangic), "
              f"%10 {fmt(np.percentile(f,10))}$, medyan {fmt(np.median(f))}$, %90 {fmt(np.percentile(f,90))}$, "
              f"en iyi {fmt(f.max())}$ ({starts[i_max].strftime('%Y-%m')}) | %7 sabit varsayim {fmt(det)}$")
        print(f"        -> medyanin %4 cekimle aylik geliri {fmt(np.median(f)*0.04/12)}$, en kotunun {fmt(f.min()*0.04/12)}$; "
              f"yatirilandan az (reel zarar) biten pencere orani %{100*(f < 300*w).mean():.1f}")

    # SWR
    print("\n  D4. Guvenli cekim orani testi (30 yil, ilk sermayenin %x'i, enflasyona endeksli, aylik cekim)")
    w = 360
    for label, weq in [("%100 hisse", 1.0), ("%60/40", 0.6), ("%50/50", 0.5)]:
        port = weq * eq + (1 - weq) * bd
        res = []
        for rate in [0.03, 0.035, 0.04, 0.045, 0.05]:
            ok = 0
            tot = 0
            for s in range(0, len(port) - w + 1):
                bal = 1.0
                wd = rate / 12
                fail = False
                for k in range(w):
                    bal = bal - wd
                    if bal <= 0:
                        fail = True
                        break
                    bal *= (1 + port[s + k])
                ok += (not fail)
                tot += 1
            res.append(f"%{rate*100:.1f}: %{100*ok/tot:.0f}")
        # SAFEMAX
        lo, hi = 0.01, 0.10
        for _ in range(40):
            mid = (lo + hi) / 2
            allok = True
            for s in range(0, len(port) - w + 1, 1):
                bal = 1.0
                for k in range(w):
                    bal -= mid / 12
                    if bal <= 0:
                        allok = False
                        break
                    bal *= (1 + port[s + k])
                if not allok:
                    break
            if allok:
                lo = mid
            else:
                hi = mid
        print(f"   {label:<10} basari: " + ", ".join(res) + f" | tarihsel en kotu durumda guvenli oran ~%{lo*100:.2f}")

    # getiri sirasi riski
    print("\n  D5. Getiri sirasi riski: AYNI 30 yillik getiriler, duz ve ters sira, %100 hisse")
    w = 360
    for start in ["1966-01", "1929-01"]:
        s_idx = np.where(dates.dt.strftime("%Y-%m").values == start)[0]
        if not len(s_idx) or s_idx[0] + w > len(eq):
            continue
        s = s_idx[0]
        seq = eq[s:s + w]
        for rate in [0.04, 0.05]:
            for name, sq in [("duz", seq), ("ters", seq[::-1])]:
                bal, depleted = 1.0, None
                for k, x in enumerate(sq):
                    bal -= rate / 12
                    if bal <= 0 and depleted is None:
                        depleted = k / 12
                        bal = 0.0
                    bal *= (1 + x)
                txt = f"{depleted:.1f}. yilda bitti" if depleted is not None else f"son bakiye ilk sermayenin {bal:.2f} kati"
                print(f"   {start}, cekim %{rate*100:.0f}, {name} sira (yillik ort. ayni: %{ann(sq)*100:.1f}): {txt}")
    # en derin dususun bolumu
    i_dd = int(np.argmin(dd))
    pk = int(np.argmax(idx[:i_dd + 1]))
    rec_i = np.where(idx[i_dd:] >= idx[pk])[0]
    rec_txt = dates.iloc[i_dd + rec_i[0]].strftime('%Y-%m') if len(rec_i) else "yok"
    print(f"\n   En derin dusus bolumu: zirve {dates.iloc[pk].strftime('%Y-%m')}, dip {dates.iloc[i_dd].strftime('%Y-%m')} "
          f"(%{dd[i_dd]*100:.0f}), reel toparlanma {rec_txt}")


# ---------------------------------------------------------------------------
# E. Turkiye
# ---------------------------------------------------------------------------
def section_e():
    print()
    print("=" * 78)
    print("E. Turkiye: dolar tutmanin TL bazinda reel sonucu (TUFE ile)")
    print("=" * 78)
    # TCMB gosterge kuru, yil sonu (simianx tablosu, kaynak TCMB)
    usd = {2015: 2.9181, 2016: 3.5192, 2017: 3.7719, 2018: 5.2810, 2019: 5.9400, 2020: 7.4194,
           2021: 13.3290, 2022: 18.6983, 2023: 29.4382, 2024: 35.2803, 2025: 42.8457}
    # TUIK yillik TUFE, Aralik
    cpi = {2016: 8.53, 2017: 11.92, 2018: 20.30, 2019: 11.84, 2020: 14.60, 2021: 36.08,
           2022: 64.27, 2023: 64.77, 2024: 44.38, 2025: 30.89}
    cum_cpi, cum_usd = 1.0, 1.0
    print(f"{'Yil':>5} {'USD/TRY deg.':>13} {'TUFE':>7} {'Dolarin reel getirisi (TL)':>28} {'100 TL nakdin reel degeri':>27}")
    for y in range(2016, 2026):
        du = usd[y] / usd[y - 1]
        pc = 1 + cpi[y] / 100
        cum_cpi *= pc
        cum_usd *= du
        print(f"{y:>5} {100*(du-1):>12.1f}% {cpi[y]:>6.1f}% {100*(du/pc-1):>27.1f}% {100/cum_cpi:>26.1f}")
    print(f"  2015 sonu -> 2025 sonu: fiyatlar x{cum_cpi:.2f}, dolar x{cum_usd:.2f}; "
          f"dolar nakdin reel degisimi %{100*(cum_usd/cum_cpi-1):.0f}; "
          f"yastik alti 100 TL'nin alim gucu {100/cum_cpi:.1f} TL")
    # S&P 500 toplam getiri (USD, temettu dahil, vergi/gider oncesi)
    spx = {2016: 11.96, 2017: 21.83, 2018: -4.38, 2019: 31.49, 2020: 18.40, 2021: 28.71,
           2022: -18.11, 2023: 26.29, 2024: 25.02, 2025: 17.9}
    cum_spx = np.prod([1 + spx[y] / 100 for y in range(2016, 2026)])
    tl = cum_spx * cum_usd
    print(f"  S&P 500 toplam getiri 2016-2025: USD x{cum_spx:.2f}; TL bazinda x{tl:.1f}; "
          f"TUFE'ye gore reel x{tl/cum_cpi:.2f} (yillik reel %{100*((tl/cum_cpi)**0.1-1):.1f})")
    print("  Yil yil S&P 500'un TL bazinda reel getirisi:")
    for y in range(2016, 2026):
        du = usd[y] / usd[y - 1]
        pc = 1 + cpi[y] / 100
        print(f"    {y}: %{100*((1+spx[y]/100)*du/pc-1):.1f}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else SHILLER_URL
    section_a()
    section_b()
    section_c()
    section_d(path)
    section_e()


if __name__ == "__main__":
    main()
