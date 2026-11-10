# 02 · Migrasi bot *grid* dari kripto ke saham IDX

Status: **Tahap 1, konsep.** Aturan bursa diperiksa per **10 Nov 2026**. Aturan ini sering berubah, jadi cek ulang sebelum dipakai. Tanda `[P]`, `[H]`, `[N]`, dan `[SARAN AI]` sama seperti di [01](01-anatomi-grid.md).

## 1. Tabel beda struktural
| Fitur | Kripto (spot) | Saham IDX | Dampak ke grid | Penyesuaian desain `[SARAN AI]` |
|---|---|---|---|---|
| Jam pasar | 24/7 | Pra-pembukaan 08.45–08.59, sesi I 09.00–12.00, sesi II 13.30–15.49, pra-penutupan 15.50–16.00 WIB (Jumat lebih pendek) [N1] | Ada **celah harga** semalam dan di akhir pekan. Order grid bisa terisi di harga pembukaan yang jauh dari tingkatnya | Grid hanya aktif di sesi kontinu. Order dievaluasi ulang setiap pagi. Jangan menumpuk order di pra-pembukaan |
| Batas gerak harian | Tidak ada | ARA 35% (Rp11–200), 25% (Rp200–5.000), 20% (>Rp5.000); **ARB asimetris 7%** untuk saham >Rp10, berlaku 19 Okt–31 Des 2026 (Kep-00157/BEI/10-2026); Rp1–10 = Rp1 [N2]. Rencana **simetris mulai 1 Jan 2027** [N3] | Penurunan besar **terpecah menjadi beberapa hari**. Turun 30% dengan ARB 7% butuh ±5 hari [H]. Grid membeli setiap hari sementara pembeli lawan menghilang | Hentikan grid saat ada saham **menyentuh ARB**. Saat itu antrean jual menumpuk dan pembeli lenyap |
| Pemutus pasar | Tidak ada | *Trading halt* 30 menit bila IHSG turun >8%, lanjutan 30 menit bila >15%, *trading suspend* bila >20% `[BELUM TERVERIFIKASI]` (aturan Apr 2025) [N4] | Order menggantung saat *halt* dan pasar dibuka ulang dengan celah harga | Hari *halt* = grid **mati** dan semua order dibatalkan |
| Satuan transaksi | Pecahan koin | 1 lot = 100 lembar [tanpa sumber — pengetahuan umum] | Modal minimum per tingkat besar (lihat [01 §4](01-anatomi-grid.md#4-jebakan-inventaris-saat-tren-turun)) | Jumlah tingkat dibatasi oleh modal per saham, bukan oleh selera |
| Fraksi harga | Sangat halus | Rp1 sampai Rp25 per tingkat harga [N5] | Jarak minimum 0,2–2% per tick | Jarak grid wajib kelipatan tick dan ≥ 1% |
| Biaya | Maker ±0,02–0,1% | ±0,15% beli, ±0,25% jual termasuk PPh final 0,1% [tanpa sumber primer] | Titik impas per putaran ±0,4% | Jarak bersih minimum lebih dari 0,4% + 1 tick |
| Penyelesaian transaksi | Instan | T+2 [tanpa sumber — pengetahuan umum] | Dana hasil jual baru cair 2 hari bursa kemudian. Daya beli dibatasi aturan broker | Model kas harus memakai saldo T+2, bukan saldo sesaat |
| *Short* | Bebas (*futures*) | *Short selling* baru dibuka **1 Okt 2026**: 5 saham, 2 anggota bursa, rekening reguler minimal 6 bulan [N6] | Grid netral atau grid *short* praktis **tidak tersedia** untuk ritel | Hanya grid *long*. Perlindungan saat pasar turun harus lewat kas, bukan posisi *short* |
| Aksi korporasi | Jarang (*fork*, *airdrop*) | Dividen (harga turun di tanggal *ex*), *split*, *rights issue*, *buyback*, *tender offer* | Penurunan di tanggal *ex* dibaca bot sebagai "harga turun", lalu bot membeli | Kalender aksi korporasi masuk ke lapisan LLM ([06](06-arsitektur-llm-pivot.md)). Geser grid sebesar DPS di tanggal *ex* |
| Papan khusus | Tidak ada | Papan Pemantauan Khusus (*Full Call Auction*, FCA). 92 saham dikeluarkan dari FCA dan batas harga minimum diturunkan dari Rp50 ke **Rp1**, efektif 28 Sep 2026 [N7] | Saham FCA tidak punya *order book* kontinu. Grid tidak berfungsi | **Keluarkan** saham FCA, UMA, dan yang disuspensi dari semesta |
| Transparansi alur | Data di rantai (*on-chain*) dan *order book* publik | Kode broker dan tipe investor (asing atau domestik) **disembunyikan secara *real-time*** sejak 6 Des 2021. Pembukaan kembali masih wacana dan bentuknya tidak *real-time* [N8] | Arus asing hanya tersedia sebagai data **akhir hari** | Sinyal arus asing dipakai harian (EOD), bukan per menit |
| Akses API | API resmi bursa terbuka | Umumnya tanpa API publik untuk order ritel [tanpa sumber — perlu dicek per broker] | Bot penuh otomatis sulit dibuat secara legal dan praktis | Repo ini hanya *paper trading* dan **manusia yang menekan tombol** |

## 2. Struktur pasar yang membuat saham berbeda dari koin
1. **Nilai intrinsik dan siklus emiten.** Saham punya laba, dividen, dan neraca. Harga yang "murah" bisa terus murah selama laba memburuk (*value trap*). Koin tidak punya jangkar seperti ini. Grid saham harus tahu **kenapa** harga turun. Penurunan karena kepanikan pasar masih masuk akal untuk grid. Penurunan karena laba runtuh berarti grid harus mati.
2. **Konsentrasi kepemilikan.** Banyak emiten IDX punya pengendali di atas 50% dan *free float* rendah. *Free float* kecil berarti *order book* tipis dan harga mudah digerakkan pihak tertentu. Saringan proyek pembuat repo memakai syarat *free float* ≥ 15% `[H]`.
3. **Investor asing dan lokal.** Arus asing besar bisa memindahkan harga emiten berkapitalisasi besar selama berminggu-minggu. Ini sumber **tren**, musuh utama grid. Dvořák (2005) meneliti apakah investor domestik punya keunggulan informasi di bursa Indonesia ([doi:10.1111/j.1540-6261.2005.00747.x](https://doi.org/10.1111/j.1540-6261.2005.00747.x)). R8: baca hasilnya per horizon dan per jenis broker sebelum mengutip kesimpulannya.
4. **Batas harga dan efek magnet.** Kim dan Rhee (1997) menemukan bahwa batas harga di Bursa Tokyo cenderung **menunda** penemuan harga dan memindahkan volatilitas ke hari berikutnya ([doi:10.1111/j.1540-6261.1997.tb04827.x](https://doi.org/10.1111/j.1540-6261.1997.tb04827.x)). Untuk grid, ARB 7% berarti kejatuhan datang **bertahap**. Pola itu tampak seperti peluang beli setiap hari, padahal sebenarnya harga masih dicicil turun.
5. **Kejadian struktural 2026.** Konsultasi MSCI soal status pasar (*standalone*), perubahan batas harga Rp1, pembukaan *short selling*, dan ARB 7% yang bersifat sementara semuanya mengubah perilaku harga **di tengah jalan**. Grid yang dikalibrasi pada data 2020–2025 belum tentu cocok dengan rezim baru ini. Bagian ini didalami di [04](04-kondisi-bursa-2026.md) (Tahap 2).

## 3. Kalender risiko yang harus "dibaca" bot
| Kejadian | Kenapa penting | Aksi grid `[SARAN AI]` |
|---|---|---|
| Tanggal *ex* dividen | Harga turun mekanis sebesar DPS | Geser grid ke bawah sebesar DPS, jangan menghitungnya sebagai sinyal beli |
| Rilis laporan keuangan (TW) | Celah harga, perubahan valuasi | Jeda grid 1 hari sebelum dan sesudah rilis |
| RUPS, *rights issue*, *tender offer* | Harga bisa melompat atau terdilusi | Jeda grid dan evaluasi ulang |
| UMA atau suspensi dari BEI | Likuiditas hilang | Grid mati |
| Masuk papan FCA | Tidak ada perdagangan kontinu | Keluarkan dari semesta |
| Rebalancing indeks (MSCI, FTSE, LQ45) | Arus besar satu arah | Lebarkan jarak grid atau jeda |
| *Trading halt* IHSG | Pasar membeku | Grid mati, batalkan semua order |

## 4. Sumber bagian ini
- [N1] Jadwal sesi: [Cermati](https://www.cermati.com/artikel/ketahui-jam-bursa-saham-dan-kapan-membeli-dan-menjual-saham-yang-tepat), [IDX Channel](https://www.idxchannel.com/market-news/mulai-pekan-depan-bei-resmi-perluas-saham-pre-opening-dan-pre-closing/all). Periksa halaman jam perdagangan resmi di idx.co.id.
- [N2] ARB 7% dan tabel ARA: [Investortrust, Okt 2026](https://investortrust.id/market/119705/mulai-hari-ini-bei-tetapkan-batas-arb-saham-7). Ajaib menyebut SK Kep-00158/BEI/10-2026 untuk penyesuaian rentang Rp11–14 [(Ajaib)](https://ajaib.co.id/belajar/berita/bei-ubah-lagi-aturan-arb-saham-harga-rp11-rp14-kini-turun-maksimal-rp1). Periksa nomor SK dan tanggal mulai (19 atau 20 Okt) di pengumuman BEI.
- [N3] Rencana ARB simetris 2027: [Ajaib](https://ajaib.co.id/belajar/berita/aturan-baru-ara-arb-saham-28-september-2026). `[BELUM TERVERIFIKASI ke SK]`
- [N4] *Trading halt* Apr 2025: [CNBC Indonesia](https://www.cnbcindonesia.com/market/20250408084106-17-624101/bei-ubah-kebijakan-arb-ini-aturan-terbarunya), [Bisnis](https://market.bisnis.com/read/20250408/7/1867351/aturan-lama-vs-baru-bei-soal-trading-halt-dan-auto-rejection-bawah-arb). Periksa apakah ambang ini berubah pada 2026.
- [N5] Fraksi harga: [Binus Accounting](https://accounting.binus.ac.id/?p=13586), mengutip aturan BEI 2016. Periksa apakah ada perubahan setelah batas harga Rp1 berlaku.
- [N6] *Short selling*: [Kabar Bursa](https://www.kabarbursa.com/market-hari-ini/bei-umumkan-perdagangan-short-selling-dimulai-pada-1-oktober-2026). Kode 5 sahamnya belum disebut.
- [N7] FCA dan batas harga Rp1: [Katadata](https://katadata.co.id/finansial/bursa/6ab88bb98f54a/bei-keluarkan-92-saham-dari-fca-picu-volatilitas-saat-harga-bawah-rp-1-berlaku), [Bisnis](https://market.bisnis.com/read/20260402/7/1963843/dilema-papan-fca-di-bei-antara-transparansi-dan-risiko-merugikan-investor-publik).
- [N8] Kode broker: [Bisnis, Jan 2024](https://market.bisnis.com/read/20240102/7/1728667/kode-broker-bakal-dibuka-bei-tapi-tidak-real-time-seperti-dulu), [Katadata, 2026](https://katadata.co.id/amp/finansial/bursa/698a5f00eaa65/bei-beri-sinyal-buka-kembali-kode-broker-transparansi-transaksi-saham-berubah/).
- Catatan: *Non-cancellation period* berlaku 6 Des 2024 lalu dicabut 8 Apr 2025 ([FAQ Binaartha](https://www.binaartha.com/uploads/9/7/6/8/97682954/non-cancellation_period_-_faq_id.pdf)). BEI kembali mengusulkannya untuk papan FCA pada 2026 [N7].
