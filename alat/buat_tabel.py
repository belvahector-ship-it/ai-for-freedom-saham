"""Ubah metrik.csv menjadi tabel Markdown untuk docs/05 (dua tabel per kelompok).

Pemakaian: python buat_tabel.py <folder_data> > keluaran.md
Kelompok akhir:
  elite      : 16 emiten contoh pilihan pembuat repo (semua ditampilkan, termasuk yang gugur)
  bluechip   : 30 kapitalisasi terbesar non-elite, lolos gerbang, nilai transaksi median >= Rp20 M/hari
  calon      : peringkat kapitalisasi 31-100 non-elite, lolos gerbang, laba tumbuh > 0, ROE >= 10%
"""
import csv
import math
import sys
from pathlib import Path

SIKLUS = {"FIN": "kredit/bunga", "ENE": "komoditas", "BAS": "komoditas", "KPR": "defensif",
          "KES": "defensif", "KNP": "siklikal", "IND": "siklikal", "INF": "infrastruktur",
          "PRO": "siklikal", "TRA": "siklikal", "TEK": "pertumbuhan"}


def f(v, n=1, pct=False):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return "–"
    if math.isnan(x):
        return "–"
    if pct:
        x *= 100
    return f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def pilih(rows):
    el = [r for r in rows if r["kelompok"] == "elite"]
    bc = [r for r in rows if r["kelompok"] == "bluechip_kand" and r["gerbang"] == "lolos"
          and float(r["nilai_med_m"]) >= 20000]
    ca = [r for r in rows if r["kelompok"] == "calon_kand" and r["gerbang"] == "lolos"
          and r["laba_tumbuh"] not in ("", "nan") and float(r["laba_tumbuh"]) > 0
          and float(r["roe"]) >= 10]
    return [("16 emiten elite (contoh pilihan pembuat repo)", el),
            ("Bluechip (lolos saringan)", bc), ("Calon bluechip (lolos saringan)", ca)]


def tabel(judul, rs):
    rs = sorted(rs, key=lambda r: -float(r["skor"]) if r["skor"] not in ("", "nan") else 0)
    out = [f"### {judul} — A. Fundamental & kepemilikan", "",
           "| Kode | Sektor · siklus | Harga | Kap. (Rp T) | PER | PBV | ROE % | Laba Δ % | Yield 12 bln % | Publik % | Pemegang >5% (total) % |",
           "|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for r in rs:
        out.append(f"| {r['kode']} | {r['sektor']} · {SIKLUS.get(r['sektor'], '')} | {f(r['harga_idx'], 0)} | {f(r['mcap_t'], 1)} | "
                   f"{f(r['per'])} | {f(r['pbv'], 2)} | {f(r['roe'])} | {f(r['laba_tumbuh'], 0, True)} | {f(r['yield12'], 1, True)} | "
                   f"{f(r['publik'])} | {f(r['besar5'])} |")
    out += ["", f"### {judul} — B. Pasar, arus asing & kecocokan grid", "",
            "| Kode | Nilai/hari (Rp M) | Partisipasi asing % | Net asing sejak 16 Okt (Rp M) | σ harian % | Tick % | Jarak min % | Spread (tick) | VR(5) | ER(60) | vs MA200 % | Turun dr puncak % | Gerbang | Skor |",
            "|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|--:|"]
    for r in rs:
        out.append(f"| {r['kode']} | {f(float(r['nilai_med_m']) / 1000, 1)} | {f(r['asing_partisipasi'], 0, True)} | "
                   f"{f(float(r['net_asing_16okt_m']) / 1000, 0)} | {f(r['sigma_hari'], 2, True)} | {f(r['tick_pct'], 2, True)} | "
                   f"{f(r['jarak_min'], 2, True)} | {f(r['spread_tick'])} | {f(r['vr5'], 2)} | {f(r['er60'], 2)} | "
                   f"{f(r['vs_ma200'], 0, True)} | {f(r['dd_252'], 0, True)} | {r['gerbang']} | {f(r['skor'])} |")
    return "\n".join(out)


def main():
    rows = list(csv.DictReader((Path(sys.argv[1]) / "metrik.csv").open(encoding="utf-8")))
    print("\n\n".join(tabel(j, rs) for j, rs in pilih(rows)))


if __name__ == "__main__":
    main()
