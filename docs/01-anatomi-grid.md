# 01 · Anatomi bot *grid*: dari statis ke "AI Dynamic"

Status: **Tahap 1, konsep.** Tanda yang dipakai: `[P]` data primer atau teks asli, `[H]` hitungan sendiri yang bisa diulang, `[N]` angka dari pihak ketiga, `[SARAN AI]` penalaran atau dugaan. Sumber lengkap ada di [sumber.md](../sumber.md).

## 1. Mekanisme dasar
Bot *grid* memasang deretan order beli di bawah harga dan order jual di atas harga, dalam rentang `[L, U]` yang dibagi menjadi `N` tingkat.
- **Grid aritmetika**: jarak antartingkat tetap dalam rupiah (misalnya tiap Rp50).
- **Grid geometrik**: jarak antartingkat tetap dalam persen (misalnya tiap 2%). Jenis ini lebih masuk akal untuk saham karena untung per tingkat sama di harga berapa pun.
- Setiap beli yang terisi di tingkat `i` dipasangkan dengan order jual di tingkat `i+1`. Setiap jual yang terisi diganti order beli di tingkat `i−1`. Satu pasang beli lalu jual disebut satu putaran (*round trip*).

Grid adalah strategi **mean reversion** murni. Bot ini mendapat untung kalau harga bolak-balik dan dirugikan kalau harga bergerak satu arah.

Rujukan akademik untuk grid otomatis memang sedikit. Salah satunya GTSbot dari Rundo dkk. (2019), yang mengusulkan algoritma *grid* untuk pasar valas ([doi:10.3390/app9091796](https://doi.org/10.3390/app9091796)). Paper itu tentang FX, bukan saham, jadi hasilnya tidak bisa langsung dipindahkan.

## 2. Untung per grid dan biaya di IDX `[H]`
Untung bersih per putaran kira-kira sama dengan jarak grid dikurangi biaya beli dan biaya jual.

Asumsi biaya yang dipakai di seluruh repo: beli 0,15% dan jual 0,25%. Biaya jual sudah termasuk PPh final 0,1% atas penjualan saham. Biaya sebenarnya berbeda per broker. `[N, tanpa sumber primer — cek tarif broker dan ketentuan PPh final di pajak.go.id]`

| Jarak grid | Biaya per putaran | Bersih per putaran | Porsi yang dimakan biaya |
|---|---|---|---|
| 0,5% | 0,40% | 0,10% | 80% |
| 1,0% | 0,40% | 0,60% | 40% |
| 2,0% | 0,40% | 1,60% | 20% |
| 3,0% | 0,40% | 2,60% | 13% |

Ada batas kedua, yaitu **fraksi harga**. Order hanya bisa dipasang di kelipatan tick. Akibatnya jarak grid minimum sangat bergantung pada harga saham `[H]`. Tabel fraksi: di bawah Rp200 tick-nya Rp1; Rp200 sampai di bawah Rp500 tick-nya Rp2; Rp500 sampai di bawah Rp2.000 tick-nya Rp5; Rp2.000 sampai di bawah Rp5.000 tick-nya Rp10; Rp5.000 ke atas tick-nya Rp25 `[N — periksa ulang ke idx.co.id]`.

| Harga | Tick | 1 tick = |
|---|---|---|
| Rp100 | Rp1 | 1,00% |
| Rp199 | Rp1 | 0,50% |
| Rp200 | Rp2 | 1,00% |
| Rp500 | Rp5 | 1,00% |
| Rp1.995 | Rp5 | 0,25% |
| Rp2.000 | Rp10 | 0,50% |
| Rp4.990 | Rp10 | 0,20% |
| Rp5.000 | Rp25 | 0,50% |
| Rp10.000 | Rp25 | 0,25% |

Bandingkan dengan kripto. Di sana biaya *maker* sering di bawah 0,1% dan tick-nya sangat halus, sehingga grid 0,3% masih bisa untung. Di IDX, jarak grid yang realistis **mulai sekitar 1%**, dan jauh lebih lebar untuk saham murah.

## 3. Dari grid statis ke grid dinamis
Teks di aplikasi (screenshot, diakses 10 Nov 2026) `[P]` menyebut tiga hal:
- bot menyesuaikan **jumlah grid dan jaraknya secara *real-time*** berdasarkan volatilitas dan perubahan harga;
- saat harga keluar dari rentang awal, bot **memasang order baru di atas dan di bawah harga terkini**, sehingga grid ikut pindah bersama harga;
- bot paling cocok untuk **pasar yang sedang naik**. Pernyataan ini juga diakui oleh teks aplikasinya sendiri.

Dugaan cara kerja di balik layar `[SARAN AI]`. Teks aplikasi tidak menyebut adanya LLM. Kemungkinan besar "AI"-nya adalah aturan adaptif, misalnya:
1. **Jarak dari volatilitas**: jarak = k × ATR atau k × σ harian. Saat pasar tenang grid merapat; saat pasar liar grid melebar.
2. **Rentang dari distribusi harga**: batas `L` dan `U` diambil dari persentil harga N hari terakhir atau dari pita Bollinger.
3. **Geser ke tengah (*re-centering*)**: saat harga menembus `U` atau `L`, seluruh grid digeser. Varian yang hanya bergeser ke atas biasa disebut *trailing grid* atau *infinity grid*.
4. **Pemilihan parameter dari *backtest***: kombinasi yang "terbaik" pada data lalu ditawarkan sebagai parameter AI.

Konsekuensinya penting. Grid yang "selalu ikut harga" artinya **saat harga turun terus, bot terus membeli di tingkat baru**. Tidak ada mekanisme berhenti kecuali modal habis.

## 4. Jebakan inventaris saat tren turun
Contoh ini memakai grid geometrik dengan modal sama besar per tingkat, lalu harga turun 46,3%. Angka 46,3% adalah kedalaman penurunan IHSG Jan sampai Nov 2026 menurut hitungan sendiri pembuat repo dari data Yahoo; angka ini diverifikasi ulang di Tahap 2 `[H]`.

| Jarak grid | Tingkat beli yang terisi | Rugi belum terealisasi di dasar | Harga harus naik dari dasar untuk impas |
|---|---|---|---|
| 2% | 30 | −25,4% | +34,1% |
| 3% | 20 | −24,9% | +33,2% |
| 5% | 12 | −23,9% | +31,4% |

Rumus jumlah tingkat: k = ⌊ln(1−d) / ln(1−g)⌋, dengan d = kedalaman turun dan g = jarak grid.

Pelajarannya: **jarak grid hampir tidak mengubah kerugian.** Jarak grid hanya mengatur seberapa cepat modal habis. Selama harga turun, semua "untung grid" kecil dari pantulan tertelan oleh kerugian barang yang menumpuk.

Hitung juga modal minimum per saham. Satu lot berisi 100 lembar. Contoh: kalau harga Rp4.840, 1 lot = Rp484.000, sehingga 20 tingkat × 1 lot = **sekitar Rp9,7 juta untuk satu saham saja** `[H]`. Grid untuk 16 saham dengan 20 tingkat masing-masing butuh modal ratusan juta. Ini jauh berbeda dari kripto yang bisa dibeli dalam pecahan kecil.

## 5. Membaca klaim "Highest Yield 253%"
Aplikasi menampilkan **124.546 bot** dan **imbal tertinggi 253%** `[P]`. Itu adalah **nilai maksimum**, bukan rata-rata atau median.

Ilustrasi `[H]`: misalkan hasil semua bot berdistribusi normal dengan rata-rata 0% dan simpangan 50%. Nilai maksimum dari N sampel kira-kira rata-rata + σ·√(2 ln N). Untuk N = 124.546, nilai √(2 ln N) ≈ 4,84. Artinya angka maksimum sekitar 240% bisa muncul **walaupun rata-rata bot tidak untung sama sekali**. Data rata-rata dan median tidak ditampilkan di layar, jadi klaim 253% tidak bisa dipakai untuk menilai strategi ini. Ini contoh *survivorship* atau *selection bias*.

## 6. Grid sebagai taruhan statistik
- Grid mendapat untung dari **mean reversion jangka pendek**. Poterba dan Summers (1988) menemukan *mean reversion* harga saham **pada horizon panjang** ([doi:10.1016/0304-405X(88)90021-9](https://doi.org/10.1016/0304-405X(88)90021-9)). Itu bukan horizon harian yang dipakai grid.
- Pada horizon 3 sampai 12 bulan, yang lebih sering ditemukan justru **momentum**: pemenang terus menang dan pecundang terus kalah (Jegadeesh dan Titman, 1993, [doi:10.1111/j.1540-6261.1993.tb04702.x](https://doi.org/10.1111/j.1540-6261.1993.tb04702.x)). Grid melawan arah momentum ini karena **membeli pecundang** dan **menjual pemenang terlalu awal**.
- Pengalaman pembuat repo di proyek kripto terpisah: pantulan dari zona *support/resistance* hampir sama dengan pantulan di zona acak setelah biaya `[H, proyek pribadi, belum dipublikasikan]`. Itulah alasan semua uji di repo ini nanti **wajib memakai pembanding acak**.

R8, yang perlu diperiksa pembaca: periksa horizon dan pasar yang diteliti di setiap paper. Temuan dari pasar AS atau FX tidak otomatis berlaku untuk IDX.

## 7. Ringkasan untuk migrasi
1. Jarak minimum di IDX sekitar 1% atau lebih, karena biaya dan tick. Untuk saham murah lebih lebar lagi.
2. Grid harus punya **rem**: batas barang, batas modal, dan saklar untuk kondisi tren turun. Tanpa rem, grid dinamis hanya cara mencicil membeli pisau jatuh.
3. Kecocokan grid adalah sifat **per saham per kondisi pasar**, bukan sifat strateginya. Bagian ini dibahas di [05-matriks-faktor-emiten.md](05-matriks-faktor-emiten.md).
4. Bagian "AI" yang berguna adalah **memutuskan kapan grid boleh hidup**, bukan menebak harga. Ini dibahas di [06-arsitektur-llm-pivot.md](06-arsitektur-llm-pivot.md).
