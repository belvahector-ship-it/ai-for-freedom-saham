# 06 · Arsitektur "LLM sebagai *pivot*": AI yang memutuskan *kapan*, bukan *berapa*

Status: **Tahap 1, konsep.** Tanpa kode order, tanpa koneksi broker. Tanda `[P]`, `[H]`, `[N]`, dan `[SARAN AI]` sama seperti di [01](01-anatomi-grid.md).

## 1. Prinsip
1. **Kami tidak melatih model AI sendiri.** LLM yang sudah ada (Claude, Gemini, Codex/GPT, dan lainnya) dipakai sebagai **lapisan penalaran yang bisa ditukar**.
2. **LLM tidak menghitung angka dan tidak mengirim order.** Angka dihitung kode deterministik. LLM hanya membaca, mengklasifikasi, dan memberi alasan bersumber.
3. **LLM hanya boleh membuat bot lebih hati-hati, tidak boleh membuatnya lebih berani.** Aturan risiko keras tidak bisa ditimpa LLM.
4. **Manusia menekan tombol terakhir.**

Kenapa RAG dan bukan sekadar bertanya ke LLM? LLM punya batas pengetahuan (*knowledge cutoff*) dan bisa berhalusinasi, yaitu menghasilkan teks yang meyakinkan tetapi tidak sesuai sumber ([Ji dkk. 2023, ACM Computing Surveys, doi:10.1145/3571730](https://doi.org/10.1145/3571730)). *Retrieval-Augmented Generation* (RAG) mengambil dokumen relevan lebih dulu, lalu meminta model menjawab berdasarkan dokumen itu ([Lewis dkk. 2020, NeurIPS; arXiv:2005.11401](https://arxiv.org/abs/2005.11401)). Untuk saham, ini berarti setiap penilaian LLM **wajib menunjuk** laporan keuangan, pengumuman IDX, atau data harga yang diambil hari itu.

## 2. Diagram lapisan
```
L0 Data mentah ──► L1 Mesin fitur (Python, deterministik)
  harga EOD,           ATR, σ, MA200, drawdown, Amihud, spread,
  ringkasan IDX,       percentil PER/PBV, yield, free float,
  laporan keuangan,    arus asing 5/20 hari
  keterbukaan IDX,           │
  berita, makro              ▼
        │            L2 Penyimpanan RAG (potongan dokumen + metadata:
        └──────────►    emiten, tanggal, URL sumber, jenis dokumen)
                             │
                             ▼
                     L3 LLM pivot (Claude / Gemini / Codex)
                       tugas: klasifikasi rezim, tandai kejadian,
                       cek kewarasan fundamental → JSON + kutipan
                             │
                             ▼
                     L4 Cek silang: ≥2 LLM independen
                       tidak sepakat → ambil opsi paling konservatif
                             │
                             ▼
                     L5 Mesin grid (deterministik)
                       rentang, jarak, jumlah tingkat, lot
                             │
                             ▼
                     L6 Penjaga risiko (aturan keras, LLM tak bisa menimpa)
                             │
                             ▼
                     L7 Manusia: setujui / tolak  ──► L8 Jurnal & audit
```

## 3. Apa yang diputuskan LLM (dan yang tidak)
| Keputusan | Siapa | Catatan |
|---|---|---|
| Rezim pasar: *range*, tren naik, tren turun, krisis, kejadian khusus | **LLM** (dengan fitur L1 sebagai bukti) | Inti "dinamis": grid hanya hidup di *range* dan tren naik yang landai |
| Kalender kejadian: *ex* dividen, RUPS, rilis TW, *rights*, UMA, FCA, rebalancing indeks | **LLM + RAG** dari pengumuman IDX | Kejadian = jeda atau geser grid |
| Kewarasan fundamental: laba runtuh? *payout* > 100%? dilusi? | **LLM** membaca laporan, **angka dari L1** | Penurunan karena fundamental memburuk → grid mati, bukan "diskon" |
| Lebar rentang, jarak, jumlah tingkat | **Mesin grid** (rumus) | LLM hanya memberi faktor pengali dari daftar tetap, misalnya {0, 0,5, 1, 1,5} |
| Batas modal, batas barang, saklar krisis | **Aturan keras** | Tidak bisa diubah LLM |
| Kirim order | **Manusia** | Repo ini tidak punya kode order |

## 4. Kontrak keluaran LLM (contoh skema)
```json
{
  "tanggal": "2026-11-10",
  "emiten": "XXXX",
  "model": "nama-model + versi",
  "rezim": "range | tren_naik | tren_turun | krisis | kejadian",
  "keyakinan": "rendah | sedang | tinggi",
  "pengali_jarak": 0.0,
  "boleh_beli_baru": false,
  "kejadian": [{"jenis": "ex_dividen", "tanggal": "2026-11-20", "sumber": "URL pengumuman IDX"}],
  "alasan": ["kalimat pendek, masing-masing punya sumber"],
  "sumber": ["URL / id dokumen RAG"],
  "data_basi": false
}
```
Aturan validasi `[SARAN AI]`: JSON yang tidak valid, tanpa sumber, atau `data_basi: true` diperlakukan sebagai `krisis`. Bot lalu **berhenti membeli**.

## 5. Aturan keras L6 (contoh awal, belum diuji) `[SARAN AI]`
1. IHSG di bawah MA200 pada dua awal bulan berturut-turut → semua grid berhenti membeli. Aturan ini diambil dari uji "tahan kerontokan" pembuat repo, yang menunjukkan saklar tren dengan konfirmasi bulanan sebagai komponen paling berguna `[H, proyek pribadi]`.
2. Saham menyentuh ARB, masuk FCA, terkena UMA, atau disuspensi → grid saham itu mati.
3. Barang per saham ≤ X% modal dan total barang ≤ Y% modal. Sisanya kas.
4. *Trading halt* IHSG → batalkan semua order hari itu.
5. Tidak ada *averaging down* di luar tingkat grid yang sudah direncanakan.

## 6. Kenapa beberapa LLM sekaligus
- Model berbeda punya titik buta berbeda. Kalau dua model independen **tidak sepakat**, itu sinyal bahwa informasinya ambigu, dan bot memilih opsi paling aman.
- Antarmuka dibuat **netral model**: prompt, skema, dan versi model dicatat di jurnal supaya keputusan bisa diulang dan diaudit.
- Biaya dan latensi: penilaian cukup **sekali sehari** setelah bursa tutup, sesuai data EOD (lihat [03 §5](03-orderbook-depth.md#5-ketersediaan-data-kendala-nyata)).

## 7. Bukti dan batas: apa kata literatur
- Lopez-Lira dan Tang menguji kemampuan ChatGPT menilai **judul berita** untuk memprediksi return saham berikutnya ([Journal of Financial Economics, 2026, doi:10.1016/j.jfineco.2026.104335](https://doi.org/10.1016/j.jfineco.2026.104335)). R8: periksa horizon, pasar (AS), dan apakah efeknya bertahan setelah biaya.
- **Bias melihat ke depan (*look-ahead bias*)**: LLM yang dilatih dengan data setelah periode uji bisa "tahu" masa depan. Glasserman dan Lin (2023) membahas cara menilai bias ini pada prediksi sentimen GPT ([Journal of Financial Data Science, doi:10.3905/jfds.2023.1.143](https://doi.org/10.3905/jfds.2023.1.143)). Akibatnya, **backtest keputusan LLM pada periode sebelum batas pengetahuannya tidak sah**. Uji yang jujur hanya *forward test* atau *paper trading* setelah tanggal batas pengetahuan model.
- Survei LLM di keuangan: [Li dkk. 2023, ACM ICAIF, doi:10.1145/3604237.3626869](https://doi.org/10.1145/3604237.3626869).

## 8. Risiko lapisan LLM
| Risiko | Mitigasi |
|---|---|
| Halusinasi angka | LLM tidak boleh menulis angka yang tidak ada di keluaran L1 |
| Data basi | Setiap dokumen RAG diberi tanggal. Dokumen di atas N hari ditandai basi |
| Injeksi prompt dari berita atau dokumen | Isi dokumen diperlakukan sebagai data, bukan perintah. Keluaran wajib sesuai skema |
| Terlalu yakin | Kolom `keyakinan` + cek silang antarmodel |
| Model berubah versi | Versi dicatat dan diuji ulang setiap ganti model |
| *Look-ahead bias* | Hanya *forward test* |

## 9. Jalan berikutnya
- Tahap 2 (selesai): [04 kondisi bursa 2026](04-kondisi-bursa-2026.md) mengisi kalender kejadian dan skenario untuk L3. [05 matriks faktor emiten](05-matriks-faktor-emiten.md) berisi contoh nyata keluaran L1 (gerbang dan skor) untuk 108 emiten.
- Tahap 3: [07 tangga grid 16 emiten elite](07-tangga-grid-16-elite.md) adalah contoh nyata keluaran L5 yang ditahan oleh L6.
- Tahap berikutnya (bila disetujui): prototipe L1 + L5 + L6 dalam Python, uji *paper trading* dengan pembanding acak. **Backtest sengaja belum dilakukan.**
