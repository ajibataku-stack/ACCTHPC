Pantau Hotspot (otomatis)
Halaman peta hotspot NASA FIRMS untuk Indonesia. Data diperbarui tiap 3 jam oleh GitHub Actions.
Pasang (sekali saja, sekitar 5 menit)
Buat repositori baru di GitHub (boleh publik), lalu unggah seluruh isi folder ini.
Minta MAP_KEY gratis: https://firms.modaps.eosdis.nasa.gov/api/map_key/
Di repositori: Settings > Secrets and variables > Actions > New repository secret.
Nama `FIRMS_MAP_KEY`, isi dengan kunci Anda. Kunci tidak ikut terlihat di kode.
Settings > Pages > Build and deployment: Source "Deploy from a branch", branch `main`, folder `/ (root)`.
Tab Actions > "Perbarui data hotspot" > Run workflow, untuk mengisi data pertama.
Buka alamat `https://NAMA.github.io/NAMA-REPO/`.
Halaman memeriksa data baru tiap 15 menit selama tab terbuka. Bila `data/hotspot_idn.csv` belum ada, halaman menampilkan data contoh.
Catatan
Rentang data: 5 hari terakhir, satelit VIIRS S-NPP, NOAA-20, NOAA-21. Ubah `--hari` di `.github/workflows/update.yml` (maks 10).
Jadwal GitHub bisa terlambat beberapa menit, dan akan dinonaktifkan bila repositori tidak ada aktivitas 60 hari. Perbarui data otomatis ikut menghitung sebagai aktivitas.
Jika ingin repositori privat, GitHub Pages butuh paket berbayar.
