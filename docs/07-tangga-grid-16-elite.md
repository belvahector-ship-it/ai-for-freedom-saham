# 07 · Tangga grid 16 emiten elite: keluaran L5 di bawah rem L6

> **Contoh keluaran rumus untuk bahan belajar. BUKAN saran, ajakan, zona beli, harga wajar, atau target harga.** Level di bawah hanya menunjukkan *di mana mesin grid akan memasang order bila diizinkan*. Pada data 10 Nov 2026, mesin yang sama **tidak diizinkan memasang order beli baru**. Lihat [DISCLAIMER](../DISCLAIMER.md).

Status: **Tahap 3, contoh kerja.** Data tutup 10 Nov 2026. Tanpa backtest. Tanda `[P]`, `[H]`, `[N]`, dan `[SARAN AI]` sama seperti di [01](01-anatomi-grid.md).

## 1. Posisi dokumen ini dalam arsitektur
[06](06-arsitektur-llm-pivot.md) membagi bot menjadi lapisan. Dokumen ini adalah contoh nyata dua lapisan:
- **L5 mesin grid** (deterministik): menghitung jarak, level beli, dan pasangan jual dari σ dan *support*. Skrip: [`alat/tangga_grid.py`](../alat/tangga_grid.py).
- **L6 penjaga risiko** (aturan keras): memutuskan apakah tangga itu **boleh dipasang**. LLM di L3 hanya boleh membuatnya lebih hati-hati, tidak boleh melepas rem.

## 2. Rumus `[H]`
| Komponen | Aturan |
|---|---|
| Langkah | σ harian 60 hari × harga, dibulatkan ke bawah ke kelipatan **tick harga** (min. 3 tick; min. 2,5× biaya) |
| B1 | *Support* terdekat (lembah lokal ±5 hari dalam 250 hari) bila ≤ 1,5 langkah dari harga; selain itu harga − 1 langkah |
| B2–B5 | Level sebelumnya − 1 langkah; ditempel ke *support* bila selisihnya ≤ 0,4 langkah dan jarak dari level di atasnya ≥ 0,7 langkah |
| Jual | Level beli + 1 langkah, dibulatkan ke fraksi harga yang sah |
| Bersih/putaran | Langkah − biaya ±0,4% (beli 0,15% + jual 0,25%, lihat [01 §2](01-anatomi-grid.md#2-untung-per-grid-dan-biaya-di-idx-h)) |
| Modal | Contoh 1 lot (100 lembar) per level |

Data: harga harian Yahoo `.JK` (2 tahun) `[N]`; arus asing 16 Okt–9 Nov dan gerbang dari ekspor IDX `GetStockSummary` ([05](05-matriks-faktor-emiten.md)) `[H]`.

## 3. Rem global: semua JEDA `[H]` `[SARAN AI]`
IHSG 5.139 berada **di bawah MA200 6.751** pada awal Oktober dan awal November 2026. Aturan L6 no. 1 terpicu: `boleh_beli_baru = false` untuk **semua** emiten, sebagus apa pun fundamentalnya. Inilah yang membedakan grid dari "mencicil beli pisau jatuh": di tren turun kelima level terisi tanpa sempat terjual, dan rugi berjalannya hampir tidak bergantung pada jarak ([01 §4](01-anatomi-grid.md#4-jebakan-inventaris-saat-tren-turun)).

## 4. Ringkasan tangga (tutup 10 Nov 2026) `[H]`
| Kode | Harga | Langkah | Bersih/putaran | B1 | B2 | B3 | B4 | B5 | B5 vs harga | Modal 5 lot | Rem saham |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| POWR | 955 | 35 | 3,3% | 920 | 885 | 850 | 815 | 785 | −17,8% | Rp0,4 jt | — |
| ASII | 5.225 | 125 | 2,0% | 5.100 | 4.970 | 4.870 | 4.770 | 4.640 | −11,2% | Rp2,4 jt | <MA200 |
| ACES | 342 | 8 | 1,9% | 334 | 326 | 318 | 310 | 302 | −11,7% | Rp0,2 jt | <MA200 |
| TAPG | 1.910 | 65 | 3,0% | 1.820 | 1.755 | 1.690 | 1.600 | 1.535 | −19,6% | Rp0,8 jt | <MA50, asing jual |
| SSMS | 970 | 40 | 3,7% | 930 | 890 | 850 | 800 | 760 | −21,6% | Rp0,4 jt | <MA200, <MA50 |
| BBRI | 2.860 | 80 | 2,4% | 2.780 | 2.700 | 2.630 | 2.540 | 2.460 | −14,0% | Rp1,3 jt | <MA200, <MA50, asing jual |
| BMRI | 3.740 | 100 | 2,3% | 3.650 | 3.550 | 3.450 | 3.350 | 3.250 | −13,1% | Rp1,7 jt | <MA200, <MA50, asing jual |
| BBNI | 3.430 | 90 | 2,2% | 3.380 | 3.290 | 3.200 | 3.090 | 2.990 | −12,8% | Rp1,6 jt | <MA200, <MA50, asing jual |
| AKRA | 1.320 | 40 | 2,6% | 1.275 | 1.225 | 1.195 | 1.165 | 1.125 | −14,8% | Rp0,6 jt | <MA200, <MA50, asing jual |
| TLKM | 2.030 | 70 | 3,0% | 1.960 | 1.890 | 1.820 | 1.770 | 1.700 | −16,3% | Rp0,9 jt | <MA200, <MA50, asing jual |
| BFIN | 730 | 20 | 2,3% | 705 | 690 | 675 | 650 | 630 | −13,7% | Rp0,3 jt | <MA200, <MA50, asing jual |
| SMSM | 1.620 | 35 | 1,8% | 1.585 | 1.550 | 1.520 | 1.485 | 1.450 | −10,5% | Rp0,8 jt | <MA200, <MA50, asing jual, ❌ gerbang |
| BNGA | 1.520 | 35 | 1,9% | 1.485 | 1.450 | 1.415 | 1.380 | 1.345 | −11,5% | Rp0,7 jt | <MA200, <MA50, asing jual, ❌ gerbang |
| BJBR | 710 | 15 | 1,7% | 700 | 685 | 670 | 655 | 640 | −9,9% | Rp0,3 jt | <MA200, <MA50, ❌ gerbang |
| BJTM | 494 | 6 | 0,8% | 488 | 482 | 476 | 470 | 464 | −6,1% | Rp0,2 jt | <MA200, <MA50, ❌ gerbang |
| ARNA | 498 | 6 | 0,8% | 492 | 486 | 480 | 474 | 468 | −6,0% | Rp0,2 jt | <MA50, asing jual, ❌ gerbang |

"Gerbang" = gagal gerbang grid di [05](05-matriks-faktor-emiten.md) (nilai transaksi < Rp5 M/hari, dan BNGA juga publik < 15%). Tangganya tetap ditampilkan agar bisa dibandingkan, tetapi mesin **tidak akan memakainya**.

## 5. Membaca hasil `[SARAN AI]`
| Kelompok | Emiten | Ciri | Arti bagi bot |
|---|---|---|---|
| A · paling dekat aktif | POWR, ASII, ACES | Di atas atau tepat di MA50; asing **beli** bersih sejak 16 Okt (POWR +Rp28 M, ASII +Rp526 M, ACES +Rp11 M) | Kandidat pertama bila rem IHSG lepas |
| B · tren campur | TAPG, SSMS | TAPG di atas MA200 tapi di bawah MA50; SSMS paling liar (σ 4,6%), tangganya paling dalam (−21,6%) | Tunggu harga merebut MA50 |
| C · rem penuh | BBRI, BMRI, BBNI, AKRA, TLKM, BFIN | Di bawah MA200 dan MA50, asing jual bersih (BBRI −Rp4,3 T, BMRI −Rp2,8 T, TLKM −Rp1,9 T) | Arus keluar terjadwal (isu MSCI, [04](04-kondisi-bursa-2026.md)); TLKM B4 = terendah 52 minggu, B5 sudah di wilayah harga terendah baru |
| D · tidak layak grid | SMSM, BNGA, BJBR, BJTM, ARNA | Likuiditas < Rp5 M/hari; BJTM dan ARNA σ ±1,2% → untung bersih hanya ±0,8% per putaran | Dikeluarkan mesin. Saham dividen bagus ≠ cocok untuk grid |

## 6. Pemicu agar tangga boleh dipasang `[SARAN AI]`
1. **Global:** IHSG menutup di atas MA200 pada awal bulan (konfirmasi bulanan, aturan L6 no. 1).
2. **Per saham** (usulan tambahan, belum diuji): tutup di atas MA50 **dan** asing net beli 5–10 hari bursa berturut-turut.
3. **Kalender penahan:** sekitar keputusan MSCI (paling lambat Jun 2027) dan **1 Jan 2027**, saat ARB kembali simetris 20–25%. Penurunan harian bisa jauh lebih besar dari 7%, sehingga B1–B5 bisa terisi dalam satu hari ([02](02-migrasi-kripto-ke-saham.md)).
4. **Hitung ulang tiap hari:** σ, *support*, dan MA bergeser. Tangga dari tanggal lain tidak berlaku.

Contoh keluaran L3/L6 untuk satu emiten hari ini:
```json
{"tanggal": "2026-11-10", "emiten": "BMRI", "rezim": "tren_turun", "keyakinan": "tinggi",
 "pengali_jarak": 1.0, "boleh_beli_baru": false,
 "alasan": ["IHSG < MA200 dua awal bulan", "harga < MA50 dan MA200", "asing jual bersih sejak 16 Okt"],
 "sumber": ["Yahoo ^JKSE & BMRI.JK EOD 10 Nov", "IDX GetStockSummary 16 Okt-9 Nov"], "data_basi": false}
```

## 7. Batasan
- *Support* = lembah lokal harga historis, bukan jaminan pantulan. σ 60 hari memuat hari *crash* 16–19 Okt, sehingga langkah cenderung lebar.
- Tidak memperhitungkan *orderbook*, broker, atau insider (data itu ada di aplikasi broker, lihat [03](03-orderbook-depth.md)).
- Tidak ada backtest dan tidak ada klaim untung. Modal per lot hanya ilustrasi ukuran order.

## 8. Rincian per emiten `[H]`
Keluaran langsung `alat/tangga_grid.py` (urut skor grid di 05). "Dasar" menunjukkan asal level: `support`, `low 60h`, `low 52mg`, atau `langkah σ`.

### ASII · 5.225 (2026-11-10) · langkah Rp125 = 2,4% (σ 2,8%)
MA50 4.772 · MA200 5.462 · low60 3.920 · low52mg 3.920 · net asing sejak 16 Okt Rp526 M · rem: <MA200

| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |
|---|---:|---:|---|---:|---:|---:|
| B1 | 5.100 | -2,4% | langkah σ | 5.225 | +2,1% | Rp510.000 |
| B2 | 4.970 | -4,9% | langkah σ | 5.075 | +1,7% | Rp497.000 |
| B3 | 4.870 | -6,8% | support | 4.990 | +2,1% | Rp487.000 |
| B4 | 4.770 | -8,7% | support | 4.890 | +2,1% | Rp477.000 |
| B5 | 4.640 | -11,2% | langkah σ | 4.760 | +2,2% | Rp464.000 |

### TAPG · 1.910 (2026-11-10) · langkah Rp65 = 3,4% (σ 3,5%)
MA50 2.034 · MA200 1.766 · low60 1.645 · low52mg 1.255 · net asing sejak 16 Okt Rp-22 M · rem: <MA50, asing jual

| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |
|---|---:|---:|---|---:|---:|---:|
| B1 | 1.820 | -4,7% | support | 1.885 | +3,2% | Rp182.000 |
| B2 | 1.755 | -8,1% | langkah σ | 1.820 | +3,3% | Rp175.500 |
| B3 | 1.690 | -11,5% | support | 1.755 | +3,4% | Rp169.000 |
| B4 | 1.600 | -16,2% | support | 1.665 | +3,7% | Rp160.000 |
| B5 | 1.535 | -19,6% | langkah σ | 1.600 | +3,8% | Rp153.500 |

### POWR · 955 (2026-11-10) · langkah Rp35 = 3,7% (σ 3,7%)
MA50 948 · MA200 786 · low60 785 · low52mg 670 · net asing sejak 16 Okt Rp28 M · rem: tidak ada

| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |
|---|---:|---:|---|---:|---:|---:|
| B1 | 920 | -3,7% | langkah σ | 955 | +3,4% | Rp92.000 |
| B2 | 885 | -7,3% | langkah σ | 920 | +3,6% | Rp88.500 |
| B3 | 850 | -11,0% | langkah σ | 885 | +3,7% | Rp85.000 |
| B4 | 815 | -14,7% | langkah σ | 850 | +3,9% | Rp81.500 |
| B5 | 785 | -17,8% | support+low 60h | 820 | +4,1% | Rp78.500 |

### ACES · 342 (2026-11-10) · langkah Rp8 = 2,3% (σ 2,4%)
MA50 339 · MA200 362 · low60 308 · low52mg 308 · net asing sejak 16 Okt Rp11 M · rem: <MA200

| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |
|---|---:|---:|---|---:|---:|---:|
| B1 | 334 | -2,3% | langkah σ | 342 | +2,0% | Rp33.400 |
| B2 | 326 | -4,7% | langkah σ | 334 | +2,1% | Rp32.600 |
| B3 | 318 | -7,0% | support | 326 | +2,1% | Rp31.800 |
| B4 | 310 | -9,4% | support+low 60h+low 52mg | 318 | +2,2% | Rp31.000 |
| B5 | 302 | -11,7% | langkah σ | 310 | +2,2% | Rp30.200 |

### BBRI · 2.860 (2026-11-10) · langkah Rp80 = 2,8% (σ 3,0%)
MA50 3.069 · MA200 3.222 · low60 2.460 · low52mg 2.460 · net asing sejak 16 Okt Rp-4.289 M · rem: <MA200, <MA50, asing jual

| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |
|---|---:|---:|---|---:|---:|---:|
| B1 | 2.780 | -2,8% | langkah σ | 2.860 | +2,5% | Rp278.000 |
| B2 | 2.700 | -5,6% | langkah σ | 2.780 | +2,6% | Rp270.000 |
| B3 | 2.630 | -8,0% | support | 2.710 | +2,6% | Rp263.000 |
| B4 | 2.540 | -11,2% | support | 2.620 | +2,7% | Rp254.000 |
| B5 | 2.460 | -14,0% | support+low 60h+low 52mg | 2.540 | +2,9% | Rp246.000 |

### AKRA · 1.320 (2026-11-10) · langkah Rp40 = 3,0% (σ 3,2%)
MA50 1.421 · MA200 1.367 · low60 1.165 · low52mg 1.095 · net asing sejak 16 Okt Rp-182 M · rem: <MA200, <MA50, asing jual

| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |
|---|---:|---:|---|---:|---:|---:|
| B1 | 1.275 | -3,4% | support | 1.315 | +2,7% | Rp127.500 |
| B2 | 1.225 | -7,2% | support | 1.265 | +2,9% | Rp122.500 |
| B3 | 1.195 | -9,5% | support | 1.235 | +2,9% | Rp119.500 |
| B4 | 1.165 | -11,7% | support+low 60h | 1.205 | +3,0% | Rp116.500 |
| B5 | 1.125 | -14,8% | langkah σ | 1.165 | +3,2% | Rp112.500 |

### BMRI · 3.740 (2026-11-10) · langkah Rp100 = 2,7% (σ 2,8%)
MA50 4.010 · MA200 4.378 · low60 3.200 · low52mg 3.200 · net asing sejak 16 Okt Rp-2.823 M · rem: <MA200, <MA50, asing jual

| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |
|---|---:|---:|---|---:|---:|---:|
| B1 | 3.650 | -2,4% | support | 3.750 | +2,3% | Rp365.000 |
| B2 | 3.550 | -5,1% | support | 3.650 | +2,4% | Rp355.000 |
| B3 | 3.450 | -7,8% | langkah σ | 3.550 | +2,5% | Rp345.000 |
| B4 | 3.350 | -10,4% | langkah σ | 3.450 | +2,6% | Rp335.000 |
| B5 | 3.250 | -13,1% | langkah σ | 3.350 | +2,7% | Rp325.000 |

### SSMS · 970 (2026-11-10) · langkah Rp40 = 4,1% (σ 4,6%)
MA50 1.041 · MA200 1.150 · low60 800 · low52mg 650 · net asing sejak 16 Okt Rp27 M · rem: <MA200, <MA50

| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |
|---|---:|---:|---|---:|---:|---:|
| B1 | 930 | -4,1% | langkah σ | 970 | +3,9% | Rp93.000 |
| B2 | 890 | -8,2% | langkah σ | 930 | +4,1% | Rp89.000 |
| B3 | 850 | -12,4% | support | 890 | +4,3% | Rp85.000 |
| B4 | 800 | -17,5% | support+low 60h | 840 | +4,6% | Rp80.000 |
| B5 | 760 | -21,6% | langkah σ | 800 | +4,9% | Rp76.000 |

### BBNI · 3.430 (2026-11-10) · langkah Rp90 = 2,6% (σ 2,7%)
MA50 3.490 · MA200 3.774 · low60 2.830 · low52mg 2.830 · net asing sejak 16 Okt Rp-415 M · rem: <MA200, <MA50, asing jual

| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |
|---|---:|---:|---|---:|---:|---:|
| B1 | 3.380 | -1,5% | support | 3.470 | +2,3% | Rp338.000 |
| B2 | 3.290 | -4,1% | langkah σ | 3.380 | +2,3% | Rp329.000 |
| B3 | 3.200 | -6,7% | langkah σ | 3.290 | +2,4% | Rp320.000 |
| B4 | 3.090 | -9,9% | support | 3.180 | +2,5% | Rp309.000 |
| B5 | 2.990 | -12,8% | support | 3.080 | +2,6% | Rp299.000 |

### TLKM · 2.030 (2026-11-10) · langkah Rp70 = 3,4% (σ 3,5%)
MA50 2.297 · MA200 2.810 · low60 1.770 · low52mg 1.770 · net asing sejak 16 Okt Rp-1.879 M · rem: <MA200, <MA50, asing jual

| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |
|---|---:|---:|---|---:|---:|---:|
| B1 | 1.960 | -3,4% | langkah σ | 2.030 | +3,2% | Rp196.000 |
| B2 | 1.890 | -6,9% | langkah σ | 1.960 | +3,3% | Rp189.000 |
| B3 | 1.820 | -10,3% | langkah σ | 1.890 | +3,4% | Rp182.000 |
| B4 | 1.770 | -12,8% | support+low 60h+low 52mg | 1.840 | +3,6% | Rp177.000 |
| B5 | 1.700 | -16,3% | langkah σ | 1.770 | +3,7% | Rp170.000 |

### SMSM · 1.620 (2026-11-10) · langkah Rp35 = 2,2% (σ 2,2%)
MA50 1.670 · MA200 1.727 · low60 1.415 · low52mg 1.415 · net asing sejak 16 Okt Rp-6 M · rem: <MA200, <MA50, asing jual, gerbang

| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |
|---|---:|---:|---|---:|---:|---:|
| B1 | 1.585 | -2,2% | support | 1.620 | +1,8% | Rp158.500 |
| B2 | 1.550 | -4,3% | langkah σ | 1.585 | +1,9% | Rp155.000 |
| B3 | 1.520 | -6,2% | support | 1.555 | +1,9% | Rp152.000 |
| B4 | 1.485 | -8,3% | langkah σ | 1.520 | +2,0% | Rp148.500 |
| B5 | 1.450 | -10,5% | langkah σ | 1.485 | +2,0% | Rp145.000 |

### BJTM · 494 (2026-11-10) · langkah Rp6 = 1,2% (σ 1,2%)
MA50 509 · MA200 537 · low60 466 · low52mg 466 · net asing sejak 16 Okt Rp6 M · rem: <MA200, <MA50, gerbang

| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |
|---|---:|---:|---|---:|---:|---:|
| B1 | 488 | -1,2% | support | 494 | +0,8% | Rp48.800 |
| B2 | 482 | -2,4% | support | 488 | +0,8% | Rp48.200 |
| B3 | 476 | -3,6% | langkah σ | 482 | +0,9% | Rp47.600 |
| B4 | 470 | -4,9% | support+low 60h+low 52mg | 476 | +0,9% | Rp47.000 |
| B5 | 464 | -6,1% | support+low 60h+low 52mg | 470 | +0,9% | Rp46.400 |

### BJBR · 710 (2026-11-10) · langkah Rp15 = 2,1% (σ 1,5%)
MA50 752 · MA200 790 · low60 660 · low52mg 660 · net asing sejak 16 Okt Rp0 M · rem: <MA200, <MA50, gerbang

| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |
|---|---:|---:|---|---:|---:|---:|
| B1 | 700 | -1,4% | support | 715 | +1,7% | Rp70.000 |
| B2 | 685 | -3,5% | support | 700 | +1,8% | Rp68.500 |
| B3 | 670 | -5,6% | support+low 60h+low 52mg | 685 | +1,8% | Rp67.000 |
| B4 | 655 | -7,7% | support+low 60h+low 52mg | 670 | +1,9% | Rp65.500 |
| B5 | 640 | -9,9% | langkah σ | 655 | +1,9% | Rp64.000 |

### BFIN · 730 (2026-11-10) · langkah Rp20 = 2,7% (σ 3,3%)
MA50 881 · MA200 793 · low60 675 · low52mg 575 · net asing sejak 16 Okt Rp-8 M · rem: <MA200, <MA50, asing jual

| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |
|---|---:|---:|---|---:|---:|---:|
| B1 | 705 | -3,4% | support | 725 | +2,4% | Rp70.500 |
| B2 | 690 | -5,5% | support | 710 | +2,5% | Rp69.000 |
| B3 | 675 | -7,5% | support+low 60h | 695 | +2,6% | Rp67.500 |
| B4 | 650 | -11,0% | support | 670 | +2,7% | Rp65.000 |
| B5 | 630 | -13,7% | langkah σ | 650 | +2,8% | Rp63.000 |

### BNGA · 1.520 (2026-11-10) · langkah Rp35 = 2,3% (σ 2,5%)
MA50 1.654 · MA200 1.700 · low60 1.435 · low52mg 1.435 · net asing sejak 16 Okt Rp-41 M · rem: <MA200, <MA50, asing jual, gerbang

| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |
|---|---:|---:|---|---:|---:|---:|
| B1 | 1.485 | -2,3% | langkah σ | 1.520 | +2,0% | Rp148.500 |
| B2 | 1.450 | -4,6% | support | 1.485 | +2,0% | Rp145.000 |
| B3 | 1.415 | -6,9% | langkah σ | 1.450 | +2,1% | Rp141.500 |
| B4 | 1.380 | -9,2% | langkah σ | 1.415 | +2,1% | Rp138.000 |
| B5 | 1.345 | -11,5% | langkah σ | 1.380 | +2,2% | Rp134.500 |

### ARNA · 498 (2026-11-10) · langkah Rp6 = 1,2% (σ 1,2%)
MA50 509 · MA200 497 · low60 434 · low52mg 392 · net asing sejak 16 Okt Rp-6 M · rem: <MA50, asing jual, gerbang

| Level | Beli | Jarak | Dasar | Jual | Bersih/putaran | Modal 1 lot |
|---|---:|---:|---|---:|---:|---:|
| B1 | 492 | -1,2% | langkah σ | 498 | +0,8% | Rp49.200 |
| B2 | 486 | -2,4% | support | 492 | +0,8% | Rp48.600 |
| B3 | 480 | -3,6% | support | 486 | +0,8% | Rp48.000 |
| B4 | 474 | -4,8% | langkah σ | 480 | +0,9% | Rp47.400 |
| B5 | 468 | -6,0% | langkah σ | 474 | +0,9% | Rp46.800 |

