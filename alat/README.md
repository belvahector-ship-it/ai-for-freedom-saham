# Alat: mengulang matriks di docs/05

Semua skrip **hanya membaca data dan menghitung statistik deskriptif**. Tidak ada koneksi broker, tidak ada order, dan tidak ada backtest.

| Skrip | Fungsi |
|---|---|
| `ambil_yahoo.py` | Harga harian 2 tahun dari Yahoo (`.JK`, `^JKSE`, `IDR=X`) |
| `hitung_metrik.py` | Menggabungkan data Yahoo dan ekspor IDX → `metrik.csv` (gerbang + skor) |
| `buat_tabel.py` | `metrik.csv` → tabel Markdown untuk docs/05 |
| `tangga_grid.py` | `metrik.csv` + `idx_agregat.csv` + Yahoo → tangga grid L5 per emiten (`tangga.csv`, `tangga.md`) untuk docs/07 |

## Ekspor data IDX (manual, lewat browser)
Endpoint IDX menolak permintaan langsung dari skrip (403), jadi data diambil dari **tab idx.co.id yang dibuka di browser sendiri** lewat konsol (`fetch` ke path relatif). Beri jeda **≥ 3 detik** antar-permintaan, karena IDX membalas 429/503 kalau terlalu cepat.

1. `GET /primary/TradingSummary/GetStockSummary?length=9999&start=0&date=YYYYMMDD`
   Satu permintaan memuat semua saham pada satu tanggal: Close, Volume, Value, ForeignBuy/Sell, ListedShares, Bid/Offer dan volumenya. Agregasikan 60 hari terakhir per kode menjadi `idx_agregat.csv` dengan kolom `kode,kelompok,close,mcap_t,nilai_med_m,asing_part,net_asing_16okt_m,net_asing_60h_m,amihud,spread_tick_med,depth_m_med,hari_jatuh,n_hari` (nilai dalam juta rupiah).
2. `GET /primary/ListedCompany/GetCompanyProfilesDetail?KodeEmiten=XXXX&language=id-id`
   Ambil `PemegangSaham` (jumlahkan kategori "Lebih dari 5%", "Masyarakat…", dan flag `Pengendali`) serta `Profiles` (sektor, papan) → `idx_profil.csv`: `kode,peng,gt5,n5,pub,tre,sek,papan,tgl`.
3. `GET /primary/DigitalStatistic/GetApiDataPaginated?urlName=LINK_FINANCIAL_DATA_RATIO&periodQuarter=4&periodYear=2026&type=yearly&isPrint=False&cumulative=false&pageSize=1500&pageNumber=1`
   Ulangi dengan `periodYear=2025&periodQuarter=3` → `idx_rasio.csv`: `kode,fs,eps,bv,roe,der,npm,eps25,laba,laba25`.

Lalu jalankan:
```bash
python ambil_yahoo.py data/yahoo BBRI BMRI ... ^JKSE IDR=X
python hitung_metrik.py data 2026-11-09
python buat_tabel.py data > tabel.md
python tangga_grid.py data elite
```
Data mentah (Yahoo dan IDX) **tidak** disertakan di repo. Ambil sendiri dan patuhi ketentuan penggunaan masing-masing sumber.
