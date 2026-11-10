"""Tangga grid deterministik (lapisan L5 di docs/06) untuk emiten kelompok tertentu.
BUKAN rekomendasi: hanya menghitung level dari data EOD Yahoo + ekspor IDX (lihat README alat).
Pakai: python tangga_grid.py data [kelompok=elite]  -> data/tangga.csv + data/tangga.md
"""
import json, math, csv, sys, statistics as st, datetime as dt
from pathlib import Path
D = Path(sys.argv[1]); KELOMPOK = sys.argv[2] if len(sys.argv) > 2 else "elite"

BIAYA = 0.004  # beli 0,15% + jual 0,25%
N_LEVEL = 5

def tick(p):
    return 1 if p < 200 else 2 if p < 500 else 5 if p < 2000 else 10 if p < 5000 else 25

def bulat_tick(p, ke_bawah=True):
    t = tick(p)
    return (math.floor(p / t) if ke_bawah else round(p / t)) * t

def muat(kode):
    r = json.load((D / "yahoo" / f"{kode}.json").open(encoding="utf-8"))["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    bar = [(t, o, h, l, c) for t, o, h, l, c in zip(r["timestamp"], q["open"], q["high"], q["low"], q["close"])
           if None not in (o, h, l, c) and c > 0]
    return bar

def swing_low(lows, w=5):
    """indeks lembah lokal: low terendah dalam jendela ±w hari"""
    out = []
    for i in range(w, len(lows) - 1):
        a = lows[max(0, i - w): i + w + 1]
        if lows[i] == min(a):
            out.append(i)
    return out

agregat = {r["kode"]: r for r in csv.DictReader((D / "idx_agregat.csv").open(encoding="utf-8"))}
metrik = {r["kode"]: r for r in csv.DictReader((D / "metrik.csv").open(encoding="utf-8"))}
elite = [k for k, r in metrik.items() if r["kelompok"] == KELOMPOK]
elite.sort(key=lambda k: -float(metrik[k]["skor"] or 0))

hasil = []
for k in elite:
    bar = muat(k)
    tgl = dt.datetime.fromtimestamp(bar[-1][0] + 7 * 3600, dt.timezone.utc).date()
    c = [b[4] for b in bar]; h = [b[2] for b in bar]; l = [b[3] for b in bar]
    p = c[-1]
    ma50 = sum(c[-50:]) / 50; ma200 = sum(c[-200:]) / 200
    ret = [math.log(c[i] / c[i - 1]) for i in range(len(c) - 60, len(c))]
    sig = st.pstdev(ret)
    tr = [max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1])) for i in range(len(c) - 14, len(c))]
    atr = sum(tr) / 14
    hi252 = max(h[-252:]); lo252 = min(l[-252:]); lo60 = min(l[-60:])
    # support: lembah lokal 250 hari terakhir di bawah harga
    idx = [i for i in swing_low(l) if i >= len(l) - 250]
    sup = sorted({bulat_tick(l[i]) for i in idx if l[i] < p * (1 - 0.5 * sig)}, reverse=True)
    # langkah grid = sigma harian, dibulatkan ke kelipatan tick, min 3 tick dan > biaya
    t = tick(p)
    # kelipatan tick HARGA (bukan tick angka langkah)
    step = max(3 * t, math.floor(p * sig / t) * t)
    if step / p < 2.5 * BIAYA:
        step = math.ceil(p * 2.5 * BIAYA / t) * t
    # L1 = support terdekat bila dalam 1,5 langkah dari harga; selain itu harga - 1 langkah
    l1 = sup[0] if sup and p - sup[0] <= 1.5 * step else bulat_tick(p - step)
    lv = [l1]
    for _ in range(N_LEVEL - 1):
        nxt = lv[-1] - step
        # tempel ke support bila dalam setengah langkah
        dekat = [s for s in sup if abs(s - nxt) <= 0.4 * step and s <= lv[-1] - 0.7 * step]
        lv.append(dekat[0] if dekat else bulat_tick(nxt))
    lv = [bulat_tick(x) for x in lv]
    def dasar(x):
        tags = []
        if any(abs(x - s) <= tick(x) * 2 for s in sup): tags.append("support")
        if abs(x - lo60) <= max(tick(x) * 2, 0.005 * x): tags.append("low 60h")
        if abs(x - lo252) <= max(tick(x) * 2, 0.005 * x): tags.append("low 52mg")
        return "+".join(tags) or "langkah σ"
    ag = agregat[k]; m = metrik[k]
    net = float(ag["net_asing_16okt_m"])
    rem = []
    if p < ma200: rem.append("<MA200")
    if p < ma50: rem.append("<MA50")
    if net < 0: rem.append("asing jual")
    if m["gerbang"] != "lolos": rem.append("gerbang")
    hasil.append(dict(
        kode=k, tgl=str(tgl), harga=p, ma50=round(ma50), ma200=round(ma200), sig=sig, atr=round(atr),
        hi252=hi252, lo252=lo252, lo60=lo60, step=step, tick=t,
        lv=lv, dasar=[dasar(x) for x in lv], net=net, gerbang=m["gerbang"], skor=m["skor"],
        per=float(m["per"]), pbv=float(m["pbv"]), roe=m["roe"], yld=float(m["yield12"]), rem=rem,
        sup=sup[:4],
    ))

# ---- keluaran
with open(D / "tangga.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["kode", "tgl", "harga", "ma50", "ma200", "sigma", "atr14", "step", "L1", "L2", "L3", "L4", "L5",
                "lo60", "lo252", "hi252", "net_asing_16okt_m", "gerbang", "skor", "rem"])
    for r in hasil:
        w.writerow([r["kode"], r["tgl"], r["harga"], r["ma50"], r["ma200"], round(r["sig"], 4), r["atr"], r["step"],
                    *r["lv"], r["lo60"], r["lo252"], r["hi252"], r["net"], r["gerbang"], r["skor"], ";".join(r["rem"])])

rp = lambda x: f"{x:,.0f}".replace(",", ".")
pc = lambda x: f"{x*100:+.1f}%".replace(".", ",")
with open(D / "tangga.md", "w", encoding="utf-8") as f:
    for r in hasil:
        p = r["harga"]
        f.write(f"\n### {r['kode']} · {rp(p)} ({r['tgl']}) · langkah Rp{rp(r['step'])} = {pc(r['step']/p)[1:]} (σ {pc(r['sig'])[1:]})\n")
        f.write(f"MA50 {rp(r['ma50'])} · MA200 {rp(r['ma200'])} · low60 {rp(r['lo60'])} · low52mg {rp(r['lo252'])} · net asing sejak 16 Okt Rp{rp(r['net']/1e3)} M · rem: {', '.join(r['rem']) or 'tidak ada'}\n\n")
        f.write("| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |\n|---|---:|---:|---|---:|---:|---:|\n")
        for i, x in enumerate(r["lv"]):
            jual = bulat_tick(x + r["step"])  # harga jual valid sesuai fraksi
            f.write(f"| B{i+1} | {rp(x)} | {pc(x/p-1)} | {r['dasar'][i]} | {rp(jual)} | {pc(jual/x-1-BIAYA)} | Rp{rp(x*100)} |\n")
    f.write("\n")
for r in hasil:
    p = r["harga"]
    print(f"{r['kode']:5} {p:>6.0f} ma50 {r['ma50']:>6} ma200 {r['ma200']:>6} sig {r['sig']*100:4.2f} step {r['step']:>4} "
          f"L {r['lv']} lo60 {r['lo60']:.0f} lo252 {r['lo252']:.0f} net {r['net']/1e3:>8.0f}M rem {','.join(r['rem'])} "
          f"sup {r['sup']} dasar {r['dasar']} skor {r['skor']} per {r['per']:.1f} pbv {r['pbv']:.2f} roe {r['roe']} y {r['yld']*100:.1f}")
