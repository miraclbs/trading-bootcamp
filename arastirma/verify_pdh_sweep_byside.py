"""Breakdown of verify_pdh_sweep by side (PDH-sweep short vs PDL-sweep long) + 'second entry' variant.
Second entry (Brooks): after the first close-back-inside, price re-tests beyond the level again (or makes new extreme)
and closes back inside a SECOND time -> enter on that second close. Stop = sweep extreme at that time."""
import sys
import yfinance as yf
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def load(sym):
    df = yf.download(sym, period="730d", interval="1h", prepost=False, progress=False, auto_adjust=False)
    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)
    df = df.tz_convert("America/New_York").between_time("09:30", "15:59")
    return [g for _, g in df.groupby(df.index.date)]

def run(days, side, k, second):
    out = []
    for i in range(1, len(days)):
        prev, g = days[i-1], days[i]
        lvl = prev["High"].max() if side == "short" else prev["Low"].min()
        H, L, C = g["High"].values, g["Low"].values, g["Close"].values
        ext, closes_inside, armed, entry_i = None, 0, False, None
        for j in range(len(g)):
            beyond = H[j] > lvl if side == "short" else L[j] < lvl
            if beyond:
                ext = H[j] if (ext is None or side == "short" and H[j] > ext) else ext
                if side == "long":
                    ext = L[j] if (ext is None or L[j] < ext) else ext
                armed = True
            inside = C[j] < lvl if side == "short" else C[j] > lvl
            if armed and inside:
                closes_inside += 1
                armed = False
                if closes_inside == (2 if second else 1):
                    entry_i = j
                    break
        if entry_i is None or entry_i == len(g) - 1:
            continue
        e = C[entry_i]
        R = (ext - e) if side == "short" else (e - ext)
        if R <= e * 0.0003:
            continue
        res = None
        for j in range(entry_i + 1, len(g)):
            if side == "short":
                if H[j] >= ext: res = -1.0; break
                if L[j] <= e - k*R: res = float(k); break
            else:
                if L[j] <= ext: res = -1.0; break
                if H[j] >= e + k*R: res = float(k); break
        if res is None:
            res = ((e - C[-1]) / R) if side == "short" else ((C[-1] - e) / R)
        out.append(res)
    return out

for sym in ("SPY", "QQQ", "IWM"):
    days = load(sym)
    for second in (False, True):
        for side in ("short", "long"):
            r = run(days, side, 2, second)
            if r:
                wins = sum(1 for x in r if x == 2.0); losses = sum(1 for x in r if x == -1.0)
                print(f"{sym} {'2nd' if second else '1st'} entry {side:5s} 2R target: N={len(r):3d} | win {wins} loss {losses} "
                      f"| avg R {sum(r)/len(r):+.2f}")
