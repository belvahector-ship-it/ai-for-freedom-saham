# 04 · Kondisi bursa 2026 dan proyeksi kejadian

Status: **Tahap 2.** Data per **10 Nov 2026**. Ini **skenario bersyarat, bukan ramalan dan bukan rekomendasi**. Tanda `[P]` sumber primer (BEI/OJK/MSCI), `[H]` hitungan sendiri, `[N]` media atau data pihak ketiga, `[SARAN AI]` penalaran. Sumber bernomor ada di §7.

## 1. Ringkasan
- IHSG di **5.139** (10 Nov), **−43,7% dari puncak 9.135** (20 Jan 2026) dan −41,3% sejak awal tahun. Titik terendah 4.904 (3 Nov) `[N, Yahoo ^JKSE; H]`.
- Pemicu terbesar: **MSCI membuka konsultasi untuk menurunkan status Indonesia menjadi *Standalone*** (15 Okt). Keputusannya paling lambat akhir Juni 2027 [S1]. IHSG anjlok **−11,57% dalam sehari** (16 Okt) dan memicu *trading halt* [S2].
- BEI merespons dengan **perubahan aturan bertubi-tubi**: ARB 7% sementara, kriteria IHSG baru yang mengeluarkan saham berkepemilikan terkonsentrasi, publikasi pengendali dan afiliasinya, serta pengawasan perdagangan yang lebih tegas [P1–P5].
- Masalah intinya **struktural, bukan valuasi**. Valuasi sudah murah: median PER saham lolos saringan 8,1× (*earnings yield* ±12,4%) dibanding SBN 10 tahun ±7–7,7% `[H]`. Yang dipersoalkan MSCI adalah **transparansi kepemilikan dan konsentrasi**. Data kami menunjukkan gejalanya (§3).
- Implikasi untuk grid: rezim saat ini adalah **tren turun yang digerakkan arus asing**. 42 dari 51 saham lolos saringan berada **di bawah MA200** `[H]`. Grid "beli tiap turun" berbahaya di rezim ini (lihat [01 §4](01-anatomi-grid.md#4-jebakan-inventaris-saat-tren-turun)).

## 2. Peta kejadian 2026
| Tanggal | Kejadian | Sumber |
|---|---|---|
| 20 Jan | IHSG puncak 9.134,7 | `[N]` Yahoo |
| Jan–Nov | Asing jual bersih **±Rp98 T** s.d. 6 Nov (Bisnis), sumber lain Rp127 T (basis hitung berbeda) | [S3] |
| 21 Sep | Batas harga minimum Rp50 → **Rp1** (efektif 28 Sep), Kep-00136/BEI/09-2026. **ARB kembali simetris mulai 1 Jan 2027** (35/25/20%) | [P1] |
| 28 Sep | Papan Pemantauan Khusus (FCA) disempurnakan, 92 saham keluar | [N7 di 02] |
| 1 Okt | *Short selling* terbatas mulai (5 saham, 2 anggota bursa) | [N6 di 02] |
| 15 Okt | **MSCI: konsultasi status *Standalone*** | [S1] |
| 16 Okt | IHSG **−11,57%** ke 5.185; *trading halt*; asing jual bersih Rp3,34 T | [S2] |
| 19–20 Okt | **ARB 7%** (Kep-00157 lalu Kep-00158/BEI/10-2026) berlaku s.d. 31 Des 2026 | [P2] |
| 19–23 Okt | IHSG +4,9% sepekan ke 5.439 | [P4] |
| 22 Okt | Kriteria IHSG baru: **saham *High Shareholding Concentration* (HSC) dikeluarkan dari IHSG**; efektif 2 Nov | [P3] |
| 23 Okt | FTSE Russell **tetap** Secondary Emerging, tanpa *watchlist* | [P4] |
| 26 Okt | Pengawasan diperketat; *buyback* tanpa RUPS diperpanjang s.d. Jun 2027 | [P4] |
| 3 Nov | IHSG terendah tahun ini 4.904 | `[N]` Yahoo |
| 4 Nov | BEI dan KSEI mempublikasikan **pengendali dan afiliasi** untuk pemegang >1% (Kep-00160/BEI/11-2026), bulanan mulai data 30 Okt | [P5] |
| 10 Nov | IHSG 5.139. Rupiah **Rp18.039/US$** (awal 2026: Rp16.668, melemah ±7,6%) | `[N]` Yahoo IDR=X |

## 3. Gejala struktural dalam data `[H, data IDX GetStockSummary & profil, 1 Jul–9 Nov 2026]`
1. **Kapitalisasi besar ≠ bisa diperdagangkan.** Dari 30 emiten berkapitalisasi terbesar, **7 emiten** (DCII, SMMA, DNET, SRAJ, MPRO, CASA, MORA) bernilai transaksi median **< Rp1 M/hari**. Gabungan kapitalisasinya ±Rp1.036 T, atau **21% kapitalisasi 30 besar**. Empat lainnya (BREN, HMSP, UNVR, ADMR) porsi publiknya < 15%. Inilah jenis konsentrasi yang disorot MSCI dan yang kini dikeluarkan dari IHSG lewat aturan HSC [P3].
2. **Arus asing terkonsentrasi di bank besar dan TLKM.** Sejak 16 Okt, asing jual bersih di 108 emiten semesta repo ini ±**Rp16,5 T**. Penjual terbesar: BBRI −Rp4,29 T, BBCA −Rp3,81 T, BMRI −Rp2,82 T, TLKM −Rp1,88 T, ANTM −Rp0,78 T. Beli bersih terbesar: ASII +Rp0,53 T. Nilai dihitung dari volume asing × harga penutupan, sehingga merupakan **perkiraan**.
3. **Volatilitas tinggi.** Median σ harian saham lolos saringan **3,3%** (rentang 1,6–5,9%). Ini mengubah jarak grid yang masuk akal (lihat [05](05-matriks-faktor-emiten.md)).

## 4. MSCI *Standalone*: apa artinya untuk grid
- **Mekanisme** `[SARAN AI]`: dana pasif yang mengikuti indeks MSCI Emerging Markets wajib menjual saat Indonesia keluar. Dana aktif bisa menjual lebih awal. Penjualan ini **terjadwal** di sekitar tanggal efektif, sehingga cenderung menciptakan **tren**, bukan *range*.
- **Perkiraan arus keluar** `[N]`: Goldman Sachs ±Rp101 T (pasif), Mirae US$8–11 miliar, UBS hingga US$19 miliar [S4]. Angka analis sangat bervariasi. R8: periksa asumsi masing-masing.
- **Preseden** `[N]`: studi reklasifikasi pasar melaporkan rata-rata −12,5% dari pengumuman hingga tanggal efektif dan +23,3% setahun sesudahnya, dengan sampel kecil [S5]. Pernyataan ini belum dibaca penuh dari paper aslinya.
- **Yang paling terpapar** adalah saham berkapitalisasi besar dengan partisipasi asing tinggi: BBCA 60%, TLKM 66%, ASII 69%, BMRI 49%, BBRI 45% dari nilai transaksi `[H]`.

## 5. Skenario bersyarat sampai Juni 2027 `[SARAN AI]`
| Skenario | Pemicu yang bisa diamati | Rezim pasar | Perilaku grid yang cocok |
|---|---|---|---|
| **A. Batal atau ditunda** | MSCI mengakui reformasi; asing kembali beli bersih; IHSG menembus MA200 | Tren naik | Grid menjual terlalu cepat. Kalau dipakai, versi *trailing* ke atas dengan barang awal. Opsi lain: matikan grid dan tahan |
| **B. Standalone, pasif saja** | Pengumuman final dan tanggal efektif; jual bersih terkonsentrasi di saham besar | Tren turun bertahap sampai tanggal efektif, lalu bisa berbalik | **Jeda** di saham dengan partisipasi asing tinggi. Grid hanya di saham yang digerakkan investor domestik, dengan jarak lebar |
| **C. Standalone + aktif keluar** | Jual bersih asing di atas Rp1 T/hari berturut-turut; rupiah melemah tajam | Krisis | **Grid mati**, kas. Aturan L6 di [06](06-arsitektur-llm-pivot.md) berlaku |
| **D. Menggantung (konsolidasi)** | Belum ada keputusan, reformasi berjalan, arus asing netral | *Range* lebar | Kondisi paling ideal untuk grid: jarak ≥ σ harian, hanya saham lolos [05](05-matriks-faktor-emiten.md) |

**Kalender yang wajib dibaca lapisan LLM**:
- **1 Jan 2027**: ARB kembali simetris. Batas turun harian melebar dari 7% menjadi 20–35%, sehingga jatuh dalam sehari kembali mungkin.
- Evaluasi IHSG baru: Jan/Apr/Jul/Okt, efektif bulan berikutnya [P3].
- Publikasi bulanan pengendali dan afiliasi [P5].
- Keputusan MSCI paling lambat akhir Jun 2027 [S1].
- *Buyback* tanpa RUPS s.d. Jun 2027 [P4].

## 6. Makro singkat `[N]`
- BI Rate 5,75% (rapat Sep 2026) [S6].
- SBN 10 tahun 7,18% (6 Okt) [S6]. Catatan pribadi pembuat repo mencatat ±7,71% pada 3 Nov (tradingeconomics) `[BELUM TERVERIFIKASI]`, artinya naik setelah guncangan MSCI.
- Rupiah melemah ±7,6% YTD (§2).

Untuk grid, rupiah melemah dan yield naik menambah tekanan pada saham bank dan konsumen yang bergantung impor. Sebaliknya, eksportir komoditas relatif diuntungkan. Ini juga terlihat di matriks [05](05-matriks-faktor-emiten.md): 9 dari 20 calon *bluechip* yang lolos adalah emiten energi atau bahan baku.

## 7. Sumber
**Primer (idx.co.id, diakses 10 Nov 2026):**
- [P1] [Siaran pers BEI 21 Sep 2026: batas harga Rp1 dan ARB 2027](https://www.idx.co.id/id/berita/siaran-pers/2704)
- [P2] [Siaran pers 19 Okt 2026: ARB 7%, Kep-00157](https://www.idx.co.id/id/berita/siaran-pers/2732) · [20 Okt 2026: Kep-00158](https://www.idx.co.id/id/berita/siaran-pers/2734)
- [P3] [22 Okt 2026: kriteria evaluasi IHSG dan HSC](https://www.idx.co.id/id/berita/siaran-pers/2736)
- [P4] [26 Okt 2026: transparansi, FTSE Russell, *buyback*](https://www.idx.co.id/id/berita/siaran-pers/2740)
- [P5] [4 Nov 2026: pengendali dan afiliasi, Kep-00160](https://www.idx.co.id/id/berita/siaran-pers/2752)
- Data: `GetStockSummary` (1 Jul–9 Nov 2026, 92 hari bursa), `GetCompanyProfilesDetail`, *Financial Data & Ratio* IDX.

**Sekunder:**
- [S1] [Siaran pers MSCI, Okt 2026](https://www.msci.com/downloads/documents/press-releases/media-room/Indonesia_PR_Oct_26.pdf). Periksa tanggal keputusan dan syaratnya.
- [S2] [Bisnis, 16 Okt 2026](https://market.bisnis.com/read/20261016/7/2013245/ihsg-ditutup-ambles-1157-ke-5185-usai-peringatan-msci) · [Cermati](https://invest.cermati.com/artikel/amp/usulan-msci-memicu-tekanan-jual-saham-ihsg-terperosok-108percent-dan-alami-trading-halt)
- [S3] [Bisnis, 7 Nov 2026](https://market.bisnis.com/read/20261107/7/2019247/ihsg-turun-013-sepekan-ke-5050-net-sell-asing-capai-rp98-triliun) · [Katadata](https://katadata.co.id/finansial/bursa/6aea875e140bb/net-sell-tembus-rp-127-t-sejak-awal-tahun-mengapa-asing-tinggalkan-pasar-ri). Basis pasar reguler dan seluruh pasar berbeda.
- [S4] [Investortrust](https://investortrust.id/market/119745/jika-indonesia-ke-standalone-dana-asing-keluar-bisa-tembus-us19-miliar) · [Katadata](https://katadata.co.id/finansial/bursa/6aeae176295cb/analis-pasar-saham-ri-dibayangi-arus-keluar-dana-asing-hampir-rp-200-triliun)
- [S5] [CFA Institute: *Effect of market reclassifications on share prices*](https://rpc.cfainstitute.org/research/financial-analysts-journal/2018/ip-v3-n1-4-effect-of-market-reclassifications-on-share-prices). Baru ringkasan yang dibaca.
- [S6] [Bisnis, Agu 2026 (BI Rate)](https://market.bisnis.com/read/20260819/92/1997545/bi-rate-ditahan-yield-mulai-stabil-tapi-pasar-masih-waspada) · [BCA Sekuritas (BI Rate 5,75%)](https://bcasekuritas.co.id/latest-news/news/bi-rate-tetap-575-investor-dapat-manfaatkan-yield-sbn-secara-bertahap). Periksa tanggal rapat terakhir di bi.go.id.
