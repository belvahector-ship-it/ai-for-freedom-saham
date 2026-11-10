# AI for Freedom (SAHAM)

**Membedah bot "AI Dynamic Grid" dari kripto, lalu menguji apakah konsepnya bisa dibawa ke saham Indonesia (IDX), dengan LLM sebagai lapisan penalaran berbasis RAG.**

> ⚠️ **Edukasi AI + pasar saham, BUKAN ajakan atau saran investasi.** Baca [DISCLAIMER.md](DISCLAIMER.md) dulu.

## Kenapa repo ini ada
Aplikasi kripto mempromosikan bot *grid* "AI Dynamic" yang **otomatis menyesuaikan jarak grid** dan klaim "imbal tertinggi 253%". Pertanyaan repo ini:
1. Apa sebenarnya "AI" di bot itu?
2. Apa yang rusak saat bot itu dibawa ke bursa saham, dengan jam sesi, ARA/ARB, lot 100, fraksi harga, T+2, *short* terbatas, dividen, dan papan FCA?
3. Bisakah LLM (Claude, Gemini, Codex) dipakai sebagai **pivot**, yaitu lapisan yang memutuskan *kapan* grid boleh hidup berdasarkan fundamental, arus dana, dan kejadian, tanpa melatih model AI sendiri?

## Temuan utama Tahap 1 (konsep)
- **"AI"-nya kemungkinan aturan adaptif berbasis volatilitas**, bukan LLM. Grid yang "selalu ikut harga" terus membeli saat harga turun → [01](docs/01-anatomi-grid.md).
- **Di IDX, jarak grid minimum ±1%** karena biaya ±0,4% per putaran dan tick Rp1–25. Grid 0,3% ala kripto tidak mungkin untung → [01 §2](docs/01-anatomi-grid.md#2-untung-per-grid-dan-biaya-di-idx-h).
- **Jarak grid hampir tidak mengubah kerugian saat pasar runtuh.** Penurunan 46% menghasilkan rugi belum terealisasi ±24–25% di jarak 2%, 3%, maupun 5% → [01 §4](docs/01-anatomi-grid.md#4-jebakan-inventaris-saat-tren-turun).
- **"Highest Yield 253%" adalah nilai maksimum dari 124.546 bot.** Angka sebesar itu bisa muncul walaupun rata-rata bot tidak untung → [01 §5](docs/01-anatomi-grid.md#5-membaca-klaim-highest-yield-253).
- **ARB 7% (Okt–Des 2026) memecah kejatuhan menjadi beberapa hari.** Grid akan membeli setiap hari sementara pembeli lawan lenyap → [02](docs/02-migrasi-kripto-ke-saham.md).
- **Data *order book* real-time tidak tersedia gratis**, dan kode broker serta domisili investor disembunyikan. Lapisan AI realistisnya bekerja **harian** → [03](docs/03-orderbook-depth.md).
- **Arsitektur LLM pivot**: LLM membaca dan mengklasifikasi rezim dengan kutipan sumber; angka dan order tetap deterministik; aturan risiko keras tidak bisa ditimpa; manusia menekan tombol. **Backtest keputusan LLM rawan *look-ahead bias***, jadi yang sah hanya *forward test* → [06](docs/06-arsitektur-llm-pivot.md).

## Temuan utama Tahap 2 (kondisi bursa + 108 emiten, data IDX per 9 Nov 2026)
- **IHSG −43,7% dari puncak** (9.135 pada 20 Jan → 5.139 pada 10 Nov). Pemicunya konsultasi **MSCI *Standalone*** (15 Okt) dan IHSG −11,57% dalam sehari. Masalahnya **struktural** (transparansi dan konsentrasi kepemilikan), bukan valuasi: median PER saham lolos saringan 8,1× → [04](docs/04-kondisi-bursa-2026.md).
- **7 dari 30 emiten berkapitalisasi terbesar bertransaksi < Rp1 M/hari.** Gabungan kapitalisasinya ±Rp1.036 T (21% dari 30 besar). Kapitalisasi besar tidak sama dengan bisa diperdagangkan → [04 §3](docs/04-kondisi-bursa-2026.md#3-gejala-struktural-dalam-data-h-data-idx-getstocksummary--profil-1-jul9-nov-2026).
- **Asing jual bersih ±Rp16,5 T sejak 16 Okt** di 108 emiten, terkonsentrasi di BBRI, BBCA, BMRI, dan TLKM. Ini tren yang terjadwal, musuh utama grid.
- **Jarak grid realistis ≈ σ harian 1,6–5,9% (median 3,3%)**, bukan 1% → [05](docs/05-matriks-faktor-emiten.md).
- **5 dari 16 emiten elite gugur gerbang grid** (likuiditas atau *free float*). Saham dividen bagus belum tentu cocok untuk grid. **42 dari 51 saham lolos berada di bawah MA200.**
- Aturan BEI sudah **diverifikasi ke siaran pers resmi**: ARB 7% (Kep-00157/158) sampai 31 Des 2026, lalu **simetris lagi mulai 1 Jan 2027**.

## Contoh kerja Tahap 3 (tangga grid 16 emiten elite, data 10 Nov 2026)
- **Mesin grid menghitung tangga, rem risiko melarang memasangnya.** IHSG di bawah MA200 dua awal bulan → `boleh_beli_baru = false` untuk semua emiten → [07](docs/07-tangga-grid-16-elite.md).
- **Langkah realistis 6–125 rupiah (±1,2–4,1% harga)**, dibulatkan ke tick harga. Untung bersih per putaran 0,8–3,7% setelah biaya.
- **Hanya 3 dari 16 yang tidak sedang dibuang asing dan dekat MA50** (POWR, ASII, ACES). Bank BUMN dan TLKM kena rem penuh.
- **Saham dividen yang tenang (σ ±1,2%) tidak cocok untuk grid**: untung bersih ±0,8% per putaran.

## Isi
| Dokumen | Status |
|---|---|
| [01 · Anatomi grid](docs/01-anatomi-grid.md) | ✅ Tahap 1 |
| [02 · Migrasi kripto → saham IDX](docs/02-migrasi-kripto-ke-saham.md) | ✅ Tahap 1 (sumber ARB diperbarui di Tahap 2) |
| [03 · *Order book depth*](docs/03-orderbook-depth.md) | ✅ Tahap 1 |
| [04 · Kondisi bursa 2026 & proyeksi](docs/04-kondisi-bursa-2026.md) | ✅ Tahap 2 |
| [05 · Matriks faktor emiten & skor grid](docs/05-matriks-faktor-emiten.md) | ✅ Tahap 2 |
| [06 · Arsitektur LLM sebagai pivot](docs/06-arsitektur-llm-pivot.md) | ✅ Tahap 1 |
| [07 · Tangga grid 16 emiten elite](docs/07-tangga-grid-16-elite.md) | ✅ Tahap 3 (contoh kerja L5 + L6) |
| [alat/](alat/README.md) | Skrip untuk mengulang matriks (tanpa data mentah) |
| [sumber.md](sumber.md) · [keputusan.md](keputusan.md) | Daftar sumber dan keputusan pembuat repo |

**Sengaja belum ada backtest.** Konsep dimatangkan dulu.

## Aturan main isi
- `[P]` data primer atau teks asli · `[H]` hitungan sendiri yang bisa diulang · `[N]` angka pihak ketiga · `[SARAN AI]` penalaran atau dugaan.
- Klaim faktual memakai DOI atau URL. Yang belum pasti ditandai `[BELUM TERVERIFIKASI]` atau `[tanpa sumber]`.
- Jurnal *peer-reviewed* diutamakan. arXiv hanya pelengkap.
- Tidak ada rekomendasi beli atau jual. Daftar emiten = contoh pilihan pembuat repo untuk belajar.

## Metodologi: dikerjakan bersama Claude Code (Claude Opus 5.5)
Repo ini juga menjadi **uji kemampuan Claude Code dengan model Claude Opus 5.5** (Anthropic) sebagai asisten riset. Semua isi dikerjakan di sesi Claude Code: menelusuri aturan BEI terbaru, memverifikasi setiap DOI lewat Crossref API, menghitung ilustrasi, dan menyusun dokumen. Pembuat repo menetapkan arah, kriteria, dan keputusan. Commit memakai atribusi *co-author* Claude.

Batas yang disadari: AI bisa salah. Karena itu setiap angka diberi tanda asal-usul dan daftar hal yang perlu diperiksa ([sumber.md](sumber.md)).

## Lisensi
[MIT](LICENSE) untuk teks dan kode di repo ini. Isi dari pihak ketiga tetap milik pemiliknya dan hanya dirujuk lewat tautan.
