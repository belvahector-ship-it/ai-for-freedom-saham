"""Ambil harga harian 2 tahun dari Yahoo Finance (chart API publik) untuk daftar kode IDX.

Pemakaian: python ambil_yahoo.py <folder_keluaran> KODE1 KODE2 ...
Kode IDX otomatis diberi akhiran .JK; ^JKSE (IHSG) dan IDR=X (kurs) dipakai apa adanya.
Data mentah TIDAK diunggah ke repo (lisensi Yahoo); simpan di folder lokal.
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

URL = "https://query1.finance.yahoo.com/v8/finance/chart/{}?range=2y&interval=1d&events=div,split"


def ambil(simbol: str) -> dict:
    req = urllib.request.Request(URL.format(simbol), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main() -> None:
    keluar = Path(sys.argv[1])
    keluar.mkdir(parents=True, exist_ok=True)
    for kode in sys.argv[2:]:
        simbol = kode if kode.startswith("^") or "=" in kode else f"{kode}.JK"
        try:
            data = ambil(simbol)
            (keluar / f"{kode.replace('^', '').replace('=', '_')}.json").write_text(json.dumps(data))
            print("ok", kode)
        except Exception as e:  # noqa: BLE001
            print("gagal", kode, e)
        time.sleep(1)


if __name__ == "__main__":
    main()
