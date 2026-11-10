"""Hitung metrik deskriptif kecocokan grid per emiten (BUKAN backtest, BUKAN rekomendasi).

Masukan (folder data lokal):
  yahoo/<KODE>.json      harga harian 2 tahun (ambil_yahoo.py)
  idx_agregat.csv        agregat GetStockSummary IDX (likuiditas, asing, spread, depth)
  idx_profil.csv         pemegang saham & sektor (GetCompanyProfilesDetail IDX)
  idx_rasio.csv          EPS, nilai buku, ROE, DER (Financial Data & Ratio IDX)
Keluaran: metrik.csv + tabel markdown ke stdout.

Pemakaian: python hitung_metrik.py <folder_data> <tanggal_acuan YYYY-MM-DD>
"""
import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

BIAYA = 0.0040  # beli 0,15% + jual 0,25% (asumsi, termasuk PPh final 0,1%)


def tick(harga: float) -> float:
    """Fraksi harga BEI (tabel 2016; periksa ulang ke idx.co.id)."""
    if harga < 200:
        return 1
    if harga < 500:
        return 2
    if harga < 2000:
        return 5
    if harga < 5000:
        return 10
    return 25


def baca_yahoo(p: Path):
    r = json.loads(p.read_text())["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    rows = []
    for i, t in enumerate(r["timestamp"]):
        c, h, l = q["close"][i], q["high"][i], q["low"][i]
        if c is None or h is None or l is None:
            continue
        d = datetime.fromtimestamp(t + 7 * 3600, tz=timezone.utc).date()  # WIB
        rows.append((d, float(h), float(l), float(c)))
    div = [(datetime.fromtimestamp(v["date"] + 7 * 3600, tz=timezone.utc).date(), v["amount"])
           for v in (r.get("events", {}).get("dividends", {}) or {}).values()]
    return rows, div


def variance_ratio(logp: np.ndarray, k: int = 5) -> float:
    """VR(k) Lo-MacKinlay sederhana (tumpang tindih). <1 condong balik ke rata-rata, >1 condong tren."""
    r1 = np.diff(logp)
    rk = logp[k:] - logp[:-k]
    v1 = r1.var(ddof=1)
    return float(rk.var(ddof=1) / (k * v1)) if v1 > 0 else float("nan")


def efisiensi(close: np.ndarray, n: int = 60) -> float:
    """Efficiency ratio Kaufman: |perubahan bersih| / jumlah |perubahan harian|. Rendah = bolak-balik."""
    c = close[-(n + 1):]
    jalan = np.abs(np.diff(c)).sum()
    return float(abs(c[-1] - c[0]) / jalan) if jalan > 0 else float("nan")


def metrik_harga(rows, div, acuan, ihsg):
    rows = [x for x in rows if x[0] <= acuan]
    d = [x[0] for x in rows]
    h = np.array([x[1] for x in rows]); l = np.array([x[2] for x in rows]); c = np.array([x[3] for x in rows])
    lp = np.log(c)
    r = np.diff(lp)
    tr = np.maximum(h[1:] - l[1:], np.maximum(abs(h[1:] - c[:-1]), abs(l[1:] - c[:-1])))
    atr14 = tr[-14:].mean() / c[-1]
    ma200 = c[-200:].mean() if len(c) >= 200 else float("nan")
    puncak = c[-252:].max()
    awal26 = next((c[i] for i, x in enumerate(d) if x.year == 2026), c[0])
    # beta 1 tahun terhadap IHSG (tanggal sama)
    ih = dict(ihsg)
    pas = [(c[i], ih[x]) for i, x in enumerate(d) if x in ih][-253:]
    beta = float("nan")
    if len(pas) > 60:
        a = np.diff(np.log([p[0] for p in pas])); b = np.diff(np.log([p[1] for p in pas]))
        beta = float(np.cov(a, b)[0, 1] / b.var(ddof=1))
    dps12 = sum(v for t, v in div if 0 <= (acuan - t).days <= 365)
    return {
        "harga": c[-1],
        "sigma_hari": r[-60:].std(ddof=1),
        "atr14": atr14,
        "vs_ma200": c[-1] / ma200 - 1,
        "dd_252": c[-1] / puncak - 1,
        "ytd": c[-1] / awal26 - 1,
        "beta": beta,
        "vr5": variance_ratio(lp[-253:]),
        "er60": efisiensi(c),
        "yield12": dps12 / c[-1],
    }


def baca_csv(p: Path):
    with p.open(encoding="utf-8") as f:
        return {r["kode"]: r for r in csv.DictReader(f)}


def persentil(nilai, semua):
    s = sorted(x for x in semua if not math.isnan(x))
    return sum(1 for x in s if x <= nilai) / len(s) if s and not math.isnan(nilai) else float("nan")


def main():
    folder = Path(sys.argv[1]); acuan = datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
    ag = baca_csv(folder / "idx_agregat.csv"); pr = baca_csv(folder / "idx_profil.csv"); ra = baca_csv(folder / "idx_rasio.csv")
    ihsg_rows, _ = baca_yahoo(folder / "yahoo" / "JKSE.json")
    ihsg = [(x[0], x[3]) for x in ihsg_rows]
    hasil = []
    for kode in ag:
        p = folder / "yahoo" / f"{kode}.json"
        if not p.exists():
            continue
        rows, div = baca_yahoo(p)
        if len(rows) < 260:
            continue
        m = metrik_harga(rows, div, acuan, ihsg)
        a, f, q = ag[kode], pr.get(kode, {}), ra.get(kode, {})
        harga_idx = float(a["close"])
        tk = tick(harga_idx) / harga_idx
        m.update({
            "kode": kode, "kelompok": a["kelompok"], "harga_idx": harga_idx,
            "mcap_t": float(a["mcap_t"]), "nilai_med_m": float(a["nilai_med_m"]),
            "asing_partisipasi": float(a["asing_part"]), "net_asing_16okt_m": float(a["net_asing_16okt_m"]),
            "net_asing_60h_m": float(a["net_asing_60h_m"]), "amihud": float(a["amihud"]),
            "spread_tick": float(a["spread_tick_med"]), "depth_m": float(a["depth_m_med"]),
            "hari_jatuh": int(a["hari_jatuh"]),
            "tick_pct": tk, "jarak_min": max(BIAYA + tk, m["sigma_hari"]),
            "publik": float(f.get("pub") or "nan"), "pengendali": float(f.get("peng") or "nan"), "besar5": float(f.get("gt5") or "nan"),
            "sektor": f.get("sek", ""), "papan": f.get("papan", ""), "fs": q.get("fs", ""),
        })
        eps = float(q.get("eps") or "nan"); bv = float(q.get("bv") or "nan")
        m["per"] = harga_idx / eps if eps and eps > 0 else float("nan")
        m["pbv"] = harga_idx / bv if bv and bv > 0 else float("nan")
        m["roe"] = float(q.get("roe") or "nan")
        m["der"] = float(q.get("der") or "nan")
        # pertumbuhan laba (bebas efek split): laba periode terbaru disetahunkan vs laba 9 bulan 2025 disetahunkan
        laba, laba25 = float(q.get("laba") or "nan"), float(q.get("laba25") or "nan")
        bulan = int(q["fs"][5:7]) if q.get("fs") else 0
        if bulan and laba25 > 0 and not math.isnan(laba):
            m["laba_tumbuh"] = (laba / bulan) / (laba25 / 9) - 1
        else:
            m["laba_tumbuh"] = float("nan")
        hasil.append(m)

    # ---- skor kecocokan grid (deskriptif, bobot = SARAN AI, bukan rekomendasi) ----
    kol = lambda k: [x[k] for x in hasil]
    for x in hasil:
        gerbang = []
        if x["nilai_med_m"] < 5000:
            gerbang.append("likuiditas<Rp5M")
        if not math.isnan(x["publik"]) and x["publik"] < 15:
            gerbang.append("publik<15%")
        if not math.isnan(x["laba_tumbuh"]) and x["laba_tumbuh"] < -0.30:
            gerbang.append("laba turun>30%")
        if math.isnan(x["per"]):
            gerbang.append("rugi/EPS kosong")
        if x["papan"] in ("Pema", "Akse"):
            gerbang.append("papan FCA/akselerasi")
        x["gerbang"] = ", ".join(gerbang) or "lolos"
        s_lik = persentil(math.log1p(x["nilai_med_m"]), [math.log1p(v) for v in kol("nilai_med_m")])
        s_rng = 1 - (persentil(x["vr5"], kol("vr5")) + persentil(x["er60"], kol("er60"))) / 2
        s_tren = persentil(x["vs_ma200"], kol("vs_ma200"))
        rasio_biaya = x["sigma_hari"] / (BIAYA + x["tick_pct"])
        x["ayun_per_biaya"] = rasio_biaya
        s_biaya = persentil(rasio_biaya, [h["sigma_hari"] / (BIAYA + h["tick_pct"]) for h in hasil])
        tekan = x["net_asing_16okt_m"] / (x["mcap_t"] * 1e6)  # net asing (Rp M) / kapitalisasi (Rp M)
        x["tekanan_asing"] = tekan
        s_asing = persentil(tekan, [h["net_asing_16okt_m"] / (h["mcap_t"] * 1e6) for h in hasil])
        x["skor"] = round(100 * (0.25 * s_lik + 0.25 * s_rng + 0.20 * s_tren + 0.15 * s_biaya + 0.15 * s_asing), 1)

    hasil.sort(key=lambda x: (x["gerbang"] != "lolos", -x["skor"]))
    kolom = ["kode", "kelompok", "sektor", "papan", "harga_idx", "mcap_t", "nilai_med_m", "publik", "pengendali", "besar5",
             "asing_partisipasi", "net_asing_16okt_m", "net_asing_60h_m", "tekanan_asing", "per", "pbv", "roe", "der",
             "laba_tumbuh", "fs", "yield12", "sigma_hari", "atr14", "tick_pct", "jarak_min", "ayun_per_biaya",
             "spread_tick", "depth_m", "amihud", "hari_jatuh", "vs_ma200", "dd_252", "ytd", "beta", "vr5", "er60",
             "gerbang", "skor"]
    with (folder / "metrik.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(kolom)
        for x in hasil:
            w.writerow([x[k] if not isinstance(x[k], float) else round(x[k], 6) for k in kolom])
    print(f"{len(hasil)} emiten ditulis ke {folder / 'metrik.csv'}")


if __name__ == "__main__":
    main()
