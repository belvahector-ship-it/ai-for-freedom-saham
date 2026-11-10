# 05 · Matriks faktor emiten dan skor kecocokan grid

> **Contoh pilihan pembuat repo untuk bahan belajar. BUKAN saran, ajakan, atau rekomendasi membeli/menjual saham.** Skor di bawah mengukur *kecocokan statistik dengan mekanisme grid* pada data 1 Jul–9 Nov 2026, **bukan** kualitas investasi dan **bukan** prediksi. Lihat [DISCLAIMER](../DISCLAIMER.md).

Status: **Tahap 2.** Data per 9 Nov 2026 (harga penutupan IDX). Tanpa backtest. Tanda `[P]`, `[H]`, `[N]`, dan `[SARAN AI]` sama seperti di [01](01-anatomi-grid.md).

## 1. Semesta dan saringan
| Kelompok | Definisi | Kandidat → lolos |
|---|---|---|
| **Elite** | 16 emiten contoh pilihan pembuat repo: BMRI, BBRI, BBNI, BNGA, BJTM, BJBR, TLKM, ACES, ARNA, BFIN, TAPG, ASII, AKRA, POWR, SMSM, SSMS | 16 → **11 lolos gerbang** (semua ditampilkan) |
| ***Bluechip*** | 30 kapitalisasi terbesar di luar elite → lolos gerbang + nilai transaksi median ≥ Rp20 M/hari | 25 → **9** |
| **Calon *bluechip*** | Peringkat kapitalisasi 31–100 di luar elite → lolos gerbang + laba tumbuh > 0 + ROE ≥ 10% | 67 → **20** |

Urutan kapitalisasi diambil dari daftar stockanalysis.com (8 Nov 2026). Semua angka lain berasal dari IDX dan Yahoo.

**Gerbang keras** (gagal satu = tidak layak grid) `[SARAN AI]`:
1. Nilai transaksi median 60 hari ≥ Rp5 M/hari (*order book* cukup dalam, lihat [03](03-orderbook-depth.md)).
2. Porsi saham publik ≥ 15%.
3. Laba tidak turun > 30% dan tidak rugi. Grid tidak boleh "membeli diskon" dari fundamental yang runtuh.
4. Bukan di papan FCA atau Akselerasi.

**Skor kecocokan grid (0–100)**, berbasis persentil di dalam semesta 108 emiten. Bobotnya `[SARAN AI]` dan bersifat sewenang-wenang, jadi ubah sendiri di `alat/hitung_metrik.py`:
| Komponen | Bobot | Ukuran | Alasan |
|---|--:|---|---|
| Likuiditas | 25% | log nilai transaksi median | *Order book* dalam = order grid tidak menggeser harga |
| Bolak-balik (*range-bound*) | 25% | VR(5) rendah dan *Efficiency Ratio* 60 hari rendah | Grid untung dari harga yang bolak-balik, bukan tren |
| Rem tren | 20% | posisi harga terhadap MA200 | Di bawah MA200 = rezim tren turun |
| Ayunan per biaya | 15% | σ harian ÷ (0,4% + 1 tick) | Ayunan harus jauh lebih besar dari biaya |
| Tekanan asing | 15% | jual bersih asing sejak 16 Okt ÷ kapitalisasi | Arus asing satu arah = tren terjadwal (MSCI) |

**Definisi ukuran**:
- **VR(5)** = *variance ratio* Lo–MacKinlay pada 1 tahun. Nilai < 1 condong balik ke rata-rata mingguan; > 1 condong tren ([Lo & MacKinlay 1988, doi:10.1093/rfs/1.1.41](https://doi.org/10.1093/rfs/1.1.41)).
- **ER(60)** = |perubahan harga 60 hari| ÷ jumlah |perubahan harian|. Mendekati 0 berarti bolak-balik; mendekati 1 berarti lurus satu arah. Ukuran ini dari Kaufman, *Trading Systems and Methods* [tanpa DOI — buku].
- **Jarak min** = maks(biaya 0,4% + 1 tick, σ harian).
- **Laba Δ** = laba periode terbaru disetahunkan dibanding laba 9 bulan 2025 disetahunkan. Ukuran ini bebas efek *split*, tetapi **terpengaruh musiman** `[H]`.
- **Partisipasi asing** = (beli + jual asing) ÷ (2 × volume).
- **Pemegang >5% (total)** dipakai karena kolom "pengendali" di profil IDX kosong untuk bank BUMN (dikuasai negara lewat Danantara).

## 2. Temuan
1. **Jarak grid yang realistis saat ini ≈ σ harian, yaitu 1,6–5,9% (median 3,3%)**, jauh di atas batas biaya 0,4% + tick. Grid 1% akan terisi berkali-kali dalam sehari tanpa sempat berbalik. Angka 1% di [01](01-anatomi-grid.md) hanya batas bawah biaya, bukan jarak yang disarankan `[H]`.
2. **Saham dividen yang bagus belum tentu cocok untuk grid.** 5 dari 16 emiten elite gugur di gerbang: SMSM, BJTM, BJBR, ARNA (nilai transaksi < Rp5 M/hari) dan BNGA (publik 8,5%). Contohnya BJTM: yield 11,5% dan PBV 0,33, tetapi σ harian hanya 1,2% dengan transaksi Rp2,7 M/hari. Saham ini cocok ditahan, bukan di-grid `[H]`.
3. **Kebanyakan saham lolos memang bolak-balik di horizon mingguan.** VR(5) < 1 pada 33 dari 51 saham (median 0,91). Di elite, 14 dari 16. Ini syarat perlu, bukan syarat cukup. **42 dari 51 berada di bawah MA200**, sehingga rezimnya tren turun dan sifat bolak-baliknya terjadi **di dalam tren turun** `[H]`.
4. **Bank besar dan TLKM menanggung arus jual asing terbesar.** Fundamentalnya baik (BMRI PER 5,4, ROE 21%; BBRI PER 7,0), tetapi komponen "tekanan asing" menekan skornya. Grid di saham-saham ini pada skenario B atau C ([04](04-kondisi-bursa-2026.md#5-skenario-bersyarat-sampai-juni-2027-saran-ai)) berarti melawan penjual yang terjadwal `[SARAN AI]`.
5. **Saringan calon *bluechip* condong ke komoditas.** 9 dari 20 adalah energi atau bahan baku, dengan laba melonjak (TINS +584%, MEDC +417%, PTBA +216%). Lonjakan seperti ini **siklikal**. Lapisan LLM perlu memeriksa harga komoditas dan apakah laba itu berulang (lihat [06](06-arsitektur-llm-pivot.md)) `[SARAN AI]`.
6. **Valuasi murah, tetapi itu bukan sinyal grid.** Median PER saham lolos 8,1× (elite 7,0×). Valuasi murah membantu bertahan saat barang menumpuk, tetapi tidak menghentikan tren turun yang digerakkan arus `[H]` + `[SARAN AI]`.

## 3. Batasan (R8: yang harus diperiksa)
- **Laba Δ** membandingkan periode yang berbeda panjangnya (H1 atau 9M 2026 vs 9M 2025) dan terpengaruh musiman. Cocokkan dengan laporan keuangan per emiten.
- **EPS dan nilai buku** berasal dari *Financial Data & Ratio* IDX (EPS disetahunkan). PER dan PBV dihitung ulang dengan harga 9 Nov.
- **Yield 12 bulan** dari data dividen Yahoo (disesuaikan *split*). Cek ke pengumuman dividen IDX.
- **Net asing** = (volume beli asing − jual asing) × harga penutupan harian. Ini perkiraan, bukan nilai transaksi persis, dan mencakup seluruh pasar.
- **Spread dan *depth*** hanya dari snapshot bid/offer **saat penutupan**, bukan intrahari.
- **Porsi publik** dari profil IDX (komposisi terakhir yang dilaporkan). Data pengendali dan afiliasi baru dari BEI-KSEI ([04 §2](04-kondisi-bursa-2026.md#2-peta-kejadian-2026)) belum dipakai.
- Data mentah tidak diunggah. Cara mengulang: `alat/ambil_yahoo.py` → ekspor IDX (lihat `alat/README.md`) → `alat/hitung_metrik.py` → `alat/buat_tabel.py`.

## 4. Tabel
Diurutkan menurut skor di dalam kelompok. Harga, nilai, dan arus asing per 9 Nov 2026. "–" = data tidak tersedia atau tidak bermakna (misalnya laba 2025 negatif).

### 16 emiten elite (contoh pilihan pembuat repo) — A. Fundamental & kepemilikan

| Kode | Sektor · siklus | Harga | Kap. (Rp T) | PER | PBV | ROE % | Laba Δ % | Yield 12 bln % | Publik % | Pemegang >5% (total) % |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| ASII | IND · siklikal | 5.150 | 208,5 | 7,0 | 0,70 | 10,0 | -12 | 7,6 | 47,8 | 50,1 |
| TAPG | KPR · defensif | 1.905 | 37,8 | 8,4 | 3,09 | 37,0 | 31 | 10,6 | 17,0 | 82,1 |
| POWR | INF · infrastruktur | 955 | 15,4 | 10,1 | 1,15 | 11,3 | 33 | 7,7 | 15,9 | 83,8 |
| ACES | KNP · siklikal | 342 | 5,9 | 7,4 | 0,88 | 11,9 | 26 | 9,4 | 40,0 | 60,0 |
| BBRI | FIN · kredit/bunga | 2.820 | 423,1 | 7,0 | 1,30 | 18,6 | 14 | 12,3 | 46,8 | 52,7 |
| AKRA | ENE · komoditas | 1.340 | 26,9 | 8,9 | 1,66 | 18,7 | 34 | 7,5 | 33,1 | 64,6 |
| BMRI | FIN · kredit/bunga | 3.710 | 342,8 | 5,4 | 1,14 | 21,2 | 21 | 14,6 | 40,5 | 59,5 |
| SSMS | KPR · defensif | 960 | 9,1 | 6,7 | 3,16 | 47,4 | 35 | 8,7 | 29,2 | 70,8 |
| BBNI | FIN · kredit/bunga | 3.380 | 124,8 | 6,0 | 0,72 | 12,1 | 7 | 10,3 | 40,5 | 59,4 |
| TLKM | INF · infrastruktur | 2.050 | 203,1 | 11,6 | 1,51 | 12,9 | 1 | 10,9 | 40,6 | 58,7 |
| SMSM | KNP · siklikal | 1.645 | 9,5 | 8,0 | 2,04 | 25,4 | 7 | 8,8 | 41,4 | 50,5 |
| BJTM | FIN · kredit/bunga | 492 | 7,3 | 4,7 | 0,33 | 7,1 | 3 | 11,5 | 48,8 | 51,1 |
| BJBR | FIN · kredit/bunga | 710 | 7,4 | 5,2 | 0,37 | 7,1 | 37 | 12,0 | 24,4 | 75,5 |
| BFIN | FIN · kredit/bunga | 725 | 10,9 | 6,3 | 0,96 | 15,1 | 13 | 9,7 | 44,4 | 51,1 |
| BNGA | FIN · kredit/bunga | 1.510 | 37,6 | 6,2 | 0,66 | 10,6 | -15 | 10,7 | 8,5 | 91,4 |
| ARNA | IND · siklikal | 498 | 3,7 | 7,8 | 1,87 | 23,9 | 22 | 9,0 | 37,0 | 20,4 |

### 16 emiten elite (contoh pilihan pembuat repo) — B. Pasar, arus asing & kecocokan grid

| Kode | Nilai/hari (Rp M) | Partisipasi asing % | Net asing sejak 16 Okt (Rp M) | σ harian % | Tick % | Jarak min % | Spread (tick) | VR(5) | ER(60) | vs MA200 % | Turun dr puncak % | Gerbang | Skor |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|--:|
| ASII | 208,7 | 69 | 526 | 2,86 | 0,49 | 2,86 | 1,0 | 0,62 | 0,07 | -6 | -30 | lolos | 76,0 |
| TAPG | 27,2 | 43 | -22 | 3,57 | 0,26 | 3,57 | 1,0 | 0,81 | 0,04 | 8 | -22 | lolos | 72,0 |
| POWR | 6,4 | 28 | 28 | 3,70 | 0,52 | 3,70 | 1,0 | 0,62 | 0,11 | 22 | -7 | lolos | 68,2 |
| ACES | 7,7 | 42 | 11 | 2,38 | 0,58 | 2,38 | 1,0 | 0,71 | 0,04 | -6 | -26 | lolos | 63,0 |
| BBRI | 527,7 | 45 | -4.289 | 3,06 | 0,35 | 3,06 | 1,0 | 0,83 | 0,09 | -13 | -30 | lolos | 61,9 |
| AKRA | 20,9 | 56 | -182 | 3,25 | 0,37 | 3,25 | 1,0 | 0,79 | 0,04 | -2 | -15 | lolos | 60,7 |
| BMRI | 515,0 | 49 | -2.823 | 2,78 | 0,27 | 2,78 | 1,0 | 0,87 | 0,12 | -15 | -31 | lolos | 58,7 |
| SSMS | 10,0 | 24 | 27 | 4,67 | 0,52 | 4,67 | 1,0 | 1,35 | 0,05 | -17 | -47 | lolos | 58,1 |
| BBNI | 123,7 | 46 | -415 | 2,74 | 0,30 | 2,74 | 1,0 | 1,00 | 0,07 | -11 | -27 | lolos | 57,1 |
| TLKM | 341,9 | 66 | -1.879 | 3,58 | 0,49 | 3,58 | 1,0 | 0,76 | 0,20 | -27 | -48 | lolos | 54,0 |
| SMSM | 4,1 | 51 | -6 | 2,22 | 0,30 | 2,22 | 1,0 | 0,77 | 0,06 | -5 | -15 | likuiditas<Rp5M | 50,9 |
| BJTM | 2,7 | 15 | 6 | 1,18 | 0,41 | 1,18 | 1,0 | 0,91 | 0,14 | -8 | -19 | likuiditas<Rp5M | 46,3 |
| BJBR | 1,9 | 25 | 0 | 1,47 | 0,70 | 1,47 | 1,0 | 0,60 | 0,21 | -10 | -21 | likuiditas<Rp5M | 46,2 |
| BFIN | 13,1 | 37 | -8 | 3,33 | 0,69 | 3,33 | 1,0 | 0,91 | 0,17 | -9 | -29 | lolos | 46,0 |
| BNGA | 4,7 | 29 | -41 | 2,54 | 0,33 | 2,54 | 1,0 | 0,84 | 0,10 | -11 | -21 | likuiditas<Rp5M, publik<15% | 45,4 |
| ARNA | 1,7 | 35 | -6 | 1,20 | 0,40 | 1,20 | 1,0 | 1,10 | 0,00 | 0 | -11 | likuiditas<Rp5M | 42,3 |

### Bluechip (lolos saringan) — A. Fundamental & kepemilikan

| Kode | Sektor · siklus | Harga | Kap. (Rp T) | PER | PBV | ROE % | Laba Δ % | Yield 12 bln % | Publik % | Pemegang >5% (total) % |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| AMMN | BAS · komoditas | 3.590 | 260,3 | 11,4 | 2,32 | 20,2 | – | 0,0 | 25,3 | 73,6 |
| AADI | ENE · komoditas | 10.250 | 79,8 | 5,6 | 1,13 | 20,3 | 30 | 9,8 | 37,7 | 62,3 |
| ADRO | ENE · komoditas | 2.330 | 67,1 | 5,7 | 0,67 | 11,7 | 83 | 11,3 | 40,4 | 48,8 |
| INDF | KPR · defensif | 6.875 | 60,4 | 6,3 | 0,48 | 7,7 | -10 | 4,2 | 49,9 | 50,1 |
| ANTM | BAS · komoditas | 2.710 | 65,1 | 6,5 | 1,58 | 24,4 | 48 | 7,7 | 35,0 | 65,0 |
| BBCA | FIN · kredit/bunga | 5.325 | 649,9 | 11,1 | 2,31 | 20,9 | 4 | 7,2 | 44,6 | 54,9 |
| DSSA | ENE · komoditas | 705 | 135,8 | 25,1 | 2,49 | 9,9 | 58 | 0,0 | 22,1 | 59,9 |
| ICBP | KPR · defensif | 6.200 | 72,3 | 9,8 | 0,96 | 9,8 | -22 | 4,3 | 19,5 | 80,5 |
| PANI | PRO · siklikal | 3.710 | 67,5 | 29,4 | 1,98 | 6,7 | 145 | 0,1 | 16,3 | 83,8 |

### Bluechip (lolos saringan) — B. Pasar, arus asing & kecocokan grid

| Kode | Nilai/hari (Rp M) | Partisipasi asing % | Net asing sejak 16 Okt (Rp M) | σ harian % | Tick % | Jarak min % | Spread (tick) | VR(5) | ER(60) | vs MA200 % | Turun dr puncak % | Gerbang | Skor |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|--:|
| AMMN | 241,8 | 33 | 55 | 4,07 | 0,28 | 4,07 | 1,0 | 0,91 | 0,08 | -27 | -56 | lolos | 69,9 |
| AADI | 121,9 | 38 | -381 | 3,30 | 0,24 | 3,30 | 1,0 | 1,02 | 0,08 | 6 | -18 | lolos | 65,6 |
| ADRO | 88,1 | 39 | -335 | 2,69 | 0,43 | 2,69 | 1,0 | 0,77 | 0,05 | -4 | -18 | lolos | 61,6 |
| INDF | 37,3 | 68 | 102 | 1,58 | 0,36 | 1,58 | 1,0 | 0,98 | 0,10 | 1 | -8 | lolos | 61,4 |
| ANTM | 275,3 | 35 | -777 | 3,56 | 0,37 | 3,56 | 1,0 | 0,85 | 0,07 | -20 | -43 | lolos | 61,0 |
| BBCA | 816,6 | 60 | -3.814 | 3,13 | 0,47 | 3,13 | 1,0 | 0,83 | 0,16 | -17 | -39 | lolos | 55,4 |
| DSSA | 274,2 | 22 | 5 | 5,07 | 0,71 | 5,07 | 1,0 | 1,53 | 0,14 | -60 | -85 | lolos | 51,8 |
| ICBP | 35,7 | 50 | -183 | 2,55 | 0,40 | 2,55 | 1,0 | 0,92 | 0,20 | -13 | -30 | lolos | 45,5 |
| PANI | 25,7 | 23 | -20 | 3,58 | 0,27 | 3,58 | 1,0 | 1,02 | 0,32 | -48 | -75 | lolos | 43,2 |

### Calon bluechip (lolos saringan) — A. Fundamental & kepemilikan

| Kode | Sektor · siklus | Harga | Kap. (Rp T) | PER | PBV | ROE % | Laba Δ % | Yield 12 bln % | Publik % | Pemegang >5% (total) % |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| MEDC | ENE · komoditas | 1.180 | 29,7 | 4,9 | 0,66 | 13,3 | 417 | 5,1 | 24,7 | 73,0 |
| TINS | BAS · komoditas | 3.330 | 24,8 | 5,1 | 2,07 | 40,4 | 584 | 2,6 | 35,0 | 65,0 |
| KLBF | KES · defensif | 740 | 34,6 | 9,2 | 1,30 | 14,2 | 4 | 2,7 | 38,1 | 57,9 |
| MAPA | KNP · siklikal | 595 | 17,0 | 8,5 | 1,65 | 19,5 | 24 | 0,7 | 30,7 | 68,8 |
| PTBA | ENE · komoditas | 2.970 | 34,2 | 5,8 | 1,26 | 21,8 | 216 | 3,9 | 34,0 | 65,9 |
| ITMG | ENE · komoditas | 24.825 | 28,1 | 7,7 | 0,82 | 10,6 | 31 | 7,0 | 27,8 | 65,1 |
| INTP | BAS · komoditas | 5.850 | 20,1 | 8,1 | 0,88 | 10,9 | 22 | 8,0 | 41,0 | 54,7 |
| TOWR | INF · infrastruktur | 362 | 21,4 | 5,5 | 0,71 | 12,9 | 9 | 3,8 | 27,8 | 70,6 |
| ARCI | BAS · komoditas | 960 | 24,2 | 9,4 | 3,27 | 34,8 | 83 | 4,2 | 15,9 | 83,7 |
| CMRY | KPR · defensif | 4.140 | 32,9 | 15,3 | 4,75 | 31,1 | 7 | 4,8 | 19,3 | 5,6 |
| PTRO | ENE · komoditas | 2.090 | 21,1 | 32,0 | 3,67 | 11,5 | 150 | 0,0 | 30,1 | 69,8 |
| CPIN | KPR · defensif | 2.310 | 37,9 | 5,1 | 1,09 | 21,3 | 65 | 7,8 | 38,5 | 61,5 |
| TKIM | BAS · komoditas | 6.125 | 19,1 | 2,6 | 0,32 | 12,3 | 73 | 0,5 | 40,3 | 59,7 |
| AMRT | KPR · defensif | 940 | 39,0 | 11,0 | 2,04 | 18,5 | 31 | 6,0 | 44,7 | 52,9 |
| ISAT | INF · infrastruktur | 1.405 | 45,3 | 6,6 | 1,11 | 16,8 | 37 | 7,9 | 16,3 | 83,6 |
| IMPC | IND · siklikal | 740 | 40,6 | 51,1 | 11,27 | 22,0 | 37 | 0,7 | 20,9 | 74,4 |
| ULTJ | KPR · defensif | 2.050 | 21,3 | 11,7 | 2,54 | 21,7 | 49 | 6,3 | 17,9 | 23,8 |
| CUAN | ENE · komoditas | 354 | 39,8 | 15,4 | 3,48 | 22,6 | 97 | 0,0 | 19,5 | 80,4 |
| JPFA | KPR · defensif | 1.500 | 17,6 | 3,4 | 0,82 | 24,6 | 54 | 15,3 | 43,4 | 56,3 |
| MIKA | KES · defensif | 1.310 | 18,2 | 12,7 | 2,10 | 16,5 | 7 | 3,3 | 33,9 | 64,7 |

### Calon bluechip (lolos saringan) — B. Pasar, arus asing & kecocokan grid

| Kode | Nilai/hari (Rp M) | Partisipasi asing % | Net asing sejak 16 Okt (Rp M) | σ harian % | Tick % | Jarak min % | Spread (tick) | VR(5) | ER(60) | vs MA200 % | Turun dr puncak % | Gerbang | Skor |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|--:|
| MEDC | 70,5 | 30 | 124 | 3,66 | 0,42 | 3,66 | 1,0 | 0,82 | 0,05 | -19 | -41 | lolos | 72,2 |
| TINS | 176,7 | 36 | -474 | 3,74 | 0,30 | 3,74 | 1,0 | 0,72 | 0,06 | -12 | -32 | lolos | 67,2 |
| KLBF | 41,9 | 54 | 29 | 2,98 | 0,68 | 2,98 | 1,0 | 0,74 | 0,07 | -14 | -44 | lolos | 62,2 |
| MAPA | 9,2 | 55 | 67 | 3,57 | 0,84 | 3,57 | 1,0 | 0,83 | 0,05 | -6 | -25 | lolos | 62,0 |
| PTBA | 112,1 | 37 | -445 | 3,15 | 0,34 | 3,15 | 1,0 | 0,90 | 0,16 | 8 | -13 | lolos | 61,8 |
| ITMG | 40,0 | 47 | -328 | 1,98 | 0,10 | 1,98 | 2,0 | 0,95 | 0,02 | 1 | -17 | lolos | 58,5 |
| INTP | 6,5 | 68 | 43 | 2,41 | 0,43 | 2,41 | 2,0 | 0,97 | 0,10 | 9 | -22 | lolos | 57,8 |
| TOWR | 27,7 | 28 | 22 | 3,45 | 0,55 | 3,45 | 1,0 | 1,30 | 0,04 | -19 | -42 | lolos | 54,7 |
| ARCI | 35,2 | 26 | -24 | 4,34 | 0,52 | 4,34 | 1,0 | 0,86 | 0,11 | -29 | -53 | lolos | 54,4 |
| CMRY | 10,8 | 61 | -21 | 2,37 | 0,24 | 2,37 | 2,0 | 0,57 | 0,12 | -11 | -34 | lolos | 53,7 |
| PTRO | 185,0 | 18 | 123 | 4,52 | 0,48 | 4,52 | 1,0 | 1,24 | 0,42 | -60 | -84 | lolos | 53,2 |
| CPIN | 57,5 | 57 | 90 | 2,96 | 0,43 | 2,96 | 1,0 | 1,04 | 0,22 | -35 | -56 | lolos | 50,0 |
| TKIM | 12,7 | 36 | 12 | 3,21 | 0,41 | 3,21 | 1,0 | 1,31 | 0,15 | -17 | -45 | lolos | 46,7 |
| AMRT | 42,7 | 74 | -39 | 3,36 | 0,53 | 3,36 | 1,0 | 0,72 | 0,26 | -34 | -57 | lolos | 45,9 |
| ISAT | 111,2 | 47 | -236 | 3,70 | 0,36 | 3,70 | 1,0 | 1,01 | 0,32 | -33 | -49 | lolos | 45,5 |
| IMPC | 20,9 | 27 | 37 | 4,87 | 0,68 | 4,87 | 1,0 | 1,13 | 0,24 | -59 | -82 | lolos | 44,4 |
| ULTJ | 24,9 | 28 | -123 | 2,43 | 0,49 | 2,43 | 1,0 | 1,11 | 0,36 | 27 | -5 | lolos | 43,5 |
| CUAN | 251,6 | 24 | -19 | 4,53 | 0,56 | 4,53 | 1,0 | 1,31 | 0,37 | -65 | -87 | lolos | 43,0 |
| JPFA | 27,9 | 46 | -63 | 2,95 | 0,33 | 2,95 | 1,0 | 0,85 | 0,29 | -34 | -49 | lolos | 40,9 |
| MIKA | 5,7 | 58 | -94 | 3,05 | 0,38 | 3,05 | 2,0 | 0,90 | 0,28 | -30 | -51 | lolos | 32,8 |
