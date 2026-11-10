# Disclaimer: edukasi, bukan ajakan investasi

**Baca ini sebelum membaca bagian lain dari repo.**

## Apa repo ini
- Repo **edukasi** yang mempertemukan dua bidang: **pasar saham** (ekonomi) dan **AI berbasis LLM** (teknologi).
- Isinya adalah **pembedahan konsep**: bagaimana bot *grid* dinamis bekerja, mengapa bot itu tidak bisa dipindahkan begitu saja dari kripto ke saham Indonesia, dan bagaimana LLM (Claude, Gemini, Codex, dan lainnya) bisa dipakai sebagai **lapisan penalaran** (*pivot*), bukan sebagai mesin yang menekan tombol beli atau jual.
- Repo ini juga menjadi **uji kemampuan** Claude Code dengan model Claude Opus 5.5 dalam riset bersumber.

## Apa repo ini BUKAN
- **Bukan ajakan, rekomendasi, atau saran untuk membeli, menjual, atau menahan saham apa pun.**
- **Bukan nasihat investasi berlisensi.** Pembuat repo dan AI yang membantu bukan penasihat investasi, manajer investasi, atau pihak yang berizin dari OJK.
- **Bukan bot siap pakai.** Tidak ada kode yang terhubung ke broker atau mengirim order. Kalau nanti ada simulasi, sifatnya *paper trading*.
- **Bukan janji hasil.** Angka "imbal tertinggi" seperti 253% di aplikasi bot adalah nilai maksimum dari ratusan ribu bot. Angka itu bukan perkiraan hasil (lihat [docs/01](docs/01-anatomi-grid.md#5-membaca-klaim-highest-yield-253)).

## Tentang daftar emiten
Daftar emiten di repo ini, termasuk **16 emiten "elite"**, adalah **contoh pilihan pembuat repo untuk bahan belajar**. Daftar itu dipakai untuk menunjukkan cara menilai kecocokan sebuah saham dengan strategi *grid*. Daftar itu bukan daftar saham yang disarankan untuk dibeli.

## Risiko yang perlu dipahami
- Harga saham bisa turun dalam dan lama. IHSG turun sekitar 46% dari puncaknya pada 2026. Bot *grid* justru **menumpuk barang** saat harga turun (lihat [docs/01](docs/01-anatomi-grid.md#4-jebakan-inventaris-saat-tren-turun)).
- LLM bisa berhalusinasi, membaca data yang sudah basi, atau terlalu yakin. Karena itu, di repo ini LLM tidak pernah menjadi pengambil keputusan terakhir.
- Aturan bursa berubah cepat. Contohnya ARB 7% yang berlaku sampai 31 Desember 2026. Selalu cek aturan terbaru di [idx.co.id](https://www.idx.co.id).

Segala keputusan investasi dan risikonya ada pada pembaca. **Do your own research.**
