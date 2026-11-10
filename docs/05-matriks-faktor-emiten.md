# 05 · Matriks faktor emiten dan skor kecocokan grid (Tahap 2, belum dikerjakan)

> **Contoh pilihan pembuat repo untuk bahan belajar. Bukan saran atau ajakan membeli saham.** Lihat [DISCLAIMER](../DISCLAIMER.md).

## Semesta contoh
**16 emiten "elite"** (dari riset pribadi pembuat repo): BMRI, BBRI, BBNI, BNGA, BJTM, BJBR, TLKM, ACES, ARNA, BFIN, TAPG, ASII, AKRA, POWR, SMSM, SSMS.

Ditambah dua kelompok (kriteria draf, bisa berubah):
- ***Bluechip***: sekitar 15 emiten dengan kapitalisasi pasar terbesar yang likuid dan belum masuk 16 elite.
- **Calon *bluechip***: anggota IDX80 dengan laba tumbuh, nilai transaksi > Rp5 M/hari, dan *free float* ≥ 15%.

## Kolom yang direncanakan
| Kelompok | Faktor |
|---|---|
| Valuasi | PER, PBV, persentil 5 tahun, *earnings yield* vs SBN |
| Kualitas | Laba dan tren, ROE, arus kas bebas, *payout*, utang |
| Dividen | Yield, konsistensi, tanggal *ex* |
| Kepemilikan | Pengendali, *free float*, rasio pemegang saham, investor asing vs lokal |
| Struktur | Grup usaha, transaksi afiliasi, siklus emiten (komoditas, kredit, konsumsi) |
| Pasar | Nilai transaksi, Amihud, spread, σ, ATR, drawdown, korelasi dengan IHSG, arus asing |
| *Order book* | Snapshot *depth* (lihat [03](03-orderbook-depth.md)) |
| **Skor grid** | Gabungan: likuid, *range-bound*, fundamental stabil, tidak terlalu terpapar arus MSCI |

Sumber yang akan dipakai: IDX (`GetCompanyProfilesDetail`, laporan keuangan xlsx, pengumuman), Yahoo `.JK`, dan stockanalysis. Semua dicocokkan ke IDX.
