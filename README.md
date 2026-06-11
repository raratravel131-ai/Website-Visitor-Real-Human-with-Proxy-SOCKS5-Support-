# Website Visitor with Proxy (SOCKS5 Support)

**Powerful multi-threaded website visitor** dengan dukungan penuh untuk **SOCKS5 & HTTP/HTTPS proxy**, dilengkapi lebih dari **110+ User-Agent** dan **50+ Referer** untuk meniru lalu lintas manusia secara acak.

> ⚠️ **Peringatan Etis**: Gunakan script ini hanya untuk keperluan yang sah seperti testing beban website milik sendiri, meningkatkan traffic organic (white-hat SEO), atau riset. Jangan gunakan untuk DDoS, click fraud, atau aktivitas ilegal lainnya.

## 🚀 Fitur Unggulan

- ✅ **Dukungan SOCKS5 & HTTP/HTTPS** – Otomatis mengenali format `socks5://`, `http://`, atau tanpa skema.
- ✅ **Multi-threading** – Kunjungi banyak proxy secara simultan (default 50 thread).
- ✅ **110+ User-Agent** – Rotasi acak dari berbagai browser (Chrome, Firefox, Edge, Opera, Safari), OS (Windows, macOS, Linux, Android, iOS), dan bahkan bot crawler.
- ✅ **50+ Referer** – Berasal dari domain populer (Google, Facebook, Twitter, YouTube, Wikipedia, dll).
- ✅ **Validasi Proxy Opsional** – Cek hidup/matinya proxy sebelum digunakan.
- ✅ **Retry Mechanism** – Otomatis mencoba ulang hingga 2 kali jika gagal.
- ✅ **Random Delay** – Jeda acak antar request (0.5–2 detik) untuk menghindari deteksi.
- ✅ **Timeout Handling** – Tidak akan hang meskipun proxy lambat (10 detik timeout).
- ✅ **Logging Lengkap** – Semua aktivitas dicatat ke file `visitor_log.txt` dan terminal.
- ✅ **Statistik Real-time** – Total, sukses, gagal, proxy mati, success rate.

## 📦 Persyaratan

- Python 3.6 atau lebih baru
- Library `requests` dan `pysocks`

## 🔧 Instalasi

1. **Clone atau download** script ini ke direktori lokal.

2. **Install dependencies**:

```
pip install requests[socks]
```
Atau jika ingin manual:
```
pip install requests PySocks
```

3. **Siapkan file daftar proxy (contoh: proxylist.txt) dengan format satu baris satu proxy. Lihat bagian Format Proxy.**



## ⚙️ Konfigurasi
Buka file script dan sesuaikan bagian KONFIGURASI di bagian atas:
```
PROXY_FILE = "proxylist.txt"               # File daftar proxy
TARGET_URL = "https://raratravel.id"       # Target website (example)
THREADS = 50                               # Jumlah thread paralel**
TIMEOUT = 10                               # Timeout request (detik)
RETRY_COUNT = 2                            # Jumlah retry jika gagal
DELAY_BETWEEN_REQUESTS = (0.5, 2)          # Delay acak (min, max) detik
CHECK_PROXY_BEFORE_USE = True              # Cek proxy hidup sebelum dipakai
LOG_FILE = "visitor_log.txt"               # File log hasil
```

## 📝 Format Proxy
Script mendukung tiga format berikut (satu per baris):

**#Komentar bisa dengan tanda pagar**
```
http://123.45.67.89:8080
https://111.222.333.444:443
socks5://98.76.54.32:1080
192.168.1.100:3128          #otomatis ditambahi http://
```

**Catatan:** Untuk SOCKS5, pastikan menuliskan socks5:// di awal.

# 🖥️ Cara Menjalankan


```
python3 visitor_powerful.py
```

Output akan terlihat seperti:

```
   ██████╗  █████╗ ██████╗  █████╗ 
   ██╔══██╗██╔══██╗██╔══██╗██╔══██╗
   ...
   ===== Website Visitor v3.0 (SOCKS5 + 110+ User-Agent) =====

[2026-06-10 10:00:01] [INFO] Loaded 150 proxies from proxylist.txt
[2026-06-10 10:00:01] [INFO] Starting with 50 threads, 150 proxies
[2026-06-10 10:00:05] [SUCCESS] http://1.2.3.4:8080 -> Status 200
...
```

# 📊 Statistik
Setelah selesai, script menampilkan ringkasan:
```
============================================================
[2026-06-10 10:05:30] [INFO] VISITING COMPLETED
Total proxies processed : 150
Successful visits       : 120
Failed visits           : 30
Dead proxies detected   : 45
Time elapsed            : 45.23 seconds
Success rate            : 80.00%
============================================================
```

# 🧠 Penjelasan Teknis
- **SOCKS5 Support:** Menggunakan library `requests` dengan skema `socks5://` pada parameter `proxies`. Tidak perlu konfigurasi tambahan.

- **User-Agent & Referer:** Dipilih secara acak menggunakan `random.choice()` setiap request.

- **Multi-threading:** Menggunakan `concurrent.futures.ThreadPoolExecutor` untuk efisiensi.

- **Logging:** Semua pesan dicetak ke console dan disimpan ke file log.

- **Error Handling:** Membedakan `ProxyError`, `Timeout`, `ConnectionError` untuk penanganan yang tepat.

# 📄 Lisensi
Kode ini dilisensikan di bawah MIT License – bebas digunakan, dimodifikasi, dan didistribusikan untuk keperluan apa pun (termasuk komersial) selama menyertakan atribusi kepada penulis asli.

# 👤 Author
Dikembangkan oleh **Rara Travel** (**https://raratravel.id**).
Kode asli dimodifikasi dengan penambahan SOCKS5, multi-threading, dan koleksi user-agent/referer.

# 🤝 Kontribusi
Silakan buat pull request untuk menambah lebih banyak User-Agent atau Referer. Semakin banyak variasi, semakin natural traffic yang dihasilkan.

# ⚠️ Disclaimer
**Penulis** tidak bertanggung jawab atas penyalahgunaan script ini. Gunakan sesuai hukum yang berlaku dan hormati kebijakan website target.

# Selamat menggunakan! 🚀
