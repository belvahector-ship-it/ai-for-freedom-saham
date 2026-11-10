# 03 · *Order book depth*: grid hidup atau mati di sini

Status: **Tahap 1, konsep.** Tanda `[P]`, `[H]`, `[N]`, dan `[SARAN AI]` sama seperti di [01](01-anatomi-grid.md).

## 1. Anatomi *order book* IDX
- Dua sisi: **bid** (antrean beli) dan **offer** (antrean jual), masing-masing per tingkat harga, dengan volume dalam lot.
- Pencocokan order memakai **prioritas harga lalu waktu**. Order grid yang baru dipasang masuk **di belakang antrean** pada tingkat harganya.
- **Spread** adalah selisih harga offer terbaik dan bid terbaik. Di saham likuid, spread biasanya **1 tick**. Di saham tipis, spread bisa beberapa tick.
- **Depth** adalah total volume di N tingkat teratas tiap sisi. Angka ini menentukan berapa besar order bisa terisi tanpa menggeser harga.

## 2. Teori singkat: kenapa *depth* penting
Cont, Kukanov, dan Stoikov (2014) menunjukkan bahwa perubahan harga jangka pendek dijelaskan oleh ***order flow imbalance*** (OFI), yaitu ketidakseimbangan order masuk dan keluar di bid dan offer terbaik. Kemiringan hubungan itu **berbanding terbalik dengan *depth***. Artinya, *order book* yang dalam membuat harga sulit didorong, sedangkan *order book* tipis membuat harga mudah meloncat ([doi:10.1093/jjfinec/nbt003](https://doi.org/10.1093/jjfinec/nbt003)).

Ukuran kasar likuiditas dari data harian adalah **ilikuiditas Amihud**: rata-rata |return harian| ÷ nilai transaksi ([Amihud 2002, doi:10.1016/S1386-4181(01)00024-6](https://doi.org/10.1016/S1386-4181(01)00024-6)). Ukuran ini bisa dihitung **tanpa** data *order book*, jadi berguna sebagai penyaring awal.

R8, yang perlu diperiksa: kedua paper diuji di pasar AS. Periksa apakah hubungannya masih berlaku di IDX yang punya ARB dan fraksi harga kasar.

## 3. Turunan praktis untuk grid `[SARAN AI]` + `[H]`
| Metrik | Cara hitung | Ambang usulan | Alasan |
|---|---|---|---|
| Spread (tick) | offer₁ − bid₁ dalam tick | ≤ 1–2 tick | Spread lebar = biaya tersembunyi setiap putaran |
| Jarak grid minimum | maks(0,4% biaya + 1 tick, k × σ intrahari) | k ≈ 1 sampai 1,5 | Grid tidak boleh lebih rapat dari "noise" dan biaya |
| Rasio order terhadap antrean | lot per tingkat grid ÷ rata-rata volume di tingkat itu | ≤ 5–10% | Order kecil terhadap antrean tidak menggeser harga dan tidak terlihat sebagai "dinding" |
| Depth 5 tingkat (Rp) | Σ harga × lot × 100 di 5 tingkat bid | ≥ 20 × modal per tingkat | Bot bisa keluar tanpa membanting harga |
| Ketidakseimbangan (*imbalance*) | (bid depth − offer depth) ÷ total | Dipakai sebagai sinyal jeda, bukan sinyal beli | Antrean tebal satu sisi bisa palsu |
| Antrean di ARB | Volume offer di harga ARB | Kalau ada, grid **mati** | Pembeli hilang dan barang tidak bisa dijual besok |
| Nilai transaksi harian | Median 60 hari | ≥ Rp1 M/hari (ambang proyek pembuat repo) | Di bawah itu *order book* biasanya terlalu tipis |

## 4. Jebakan membaca *order book*
1. **Dinding palsu (*spoofing/layering*).** Antrean besar yang dipasang lalu dicabut sebelum terisi. Ada kesan "tertahan", padahal tidak. BEI pernah menerapkan ***non-cancellation period*** (6 Des 2024) lalu mencabutnya (8 Apr 2025) ([FAQ](https://www.binaartha.com/uploads/9/7/6/8/97682954/non-cancellation_period_-_faq_id.pdf)). Pada 2026 aturan itu diusulkan lagi untuk papan FCA.
2. **Tanpa identitas.** Kode broker dan domisili investor tidak tampil *real-time* (lihat [02](02-migrasi-kripto-ke-saham.md)). Tafsiran populer "bandar sedang menampung" dari *order book* tidak bisa dibuktikan dengan data publik `[SARAN AI]`.
3. **Pra-pembukaan dan pra-penutupan** memakai mekanisme lelang. *Depth* di sesi ini tidak bisa dibandingkan dengan sesi kontinu.
4. **Saham FCA** tidak punya *order book* kontinu, sehingga metrik di atas tidak berlaku.

## 5. Ketersediaan data (kendala nyata)
| Data | Sumber | Bisa otomatis? |
|---|---|---|
| Harga dan volume harian | Yahoo Finance (`.JK`), IDX | Ya (EOD) |
| Ringkasan per saham termasuk asing beli/jual | IDX `GetStockSummary` (akhir hari) | Ya, dengan batas laju |
| *Order book* atau *depth* *real-time* | Aplikasi broker, terminal berbayar | **Tidak** untuk publik gratis. Paling realistis berupa **snapshot manual** di jam tetap |
| *Running trade* | Aplikasi broker | Sama dengan di atas |

Implikasi desain: **lapisan LLM bekerja harian (EOD)**. Metrik *depth* masuk sebagai snapshot berkala atau dihampiri dengan Amihud dan spread harian (*high-low*). Bot ini bukan bot frekuensi tinggi, dan memang tidak perlu menjadi bot frekuensi tinggi.

## 6. Contoh ilustrasi `[H]`, angka rekaan untuk latihan dan bukan data nyata
Misalkan saham X berharga Rp4.000 (tick Rp10 = 0,25%):
- Bid₁ 4.000 (1.200 lot), offer₁ 4.010 (900 lot). Spread = 1 tick.
- Rencana grid 1 lot per tingkat = 0,08% dari antrean bid₁. Dampaknya terhadap antrean dapat diabaikan.
- Jarak minimum = maks(0,4% + 0,25%, 1 × σ intrahari 1,1%) → **sekitar 1,1%**, dibulatkan ke 4 atau 5 tick (Rp40–50).
- Kalau besok saham X menyentuh ARB dengan antrean offer 50.000 lot di harga ARB → **grid mati**. Order beli dibatalkan, bukan ditambah.
