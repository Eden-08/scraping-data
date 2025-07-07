# scraping-data

Project scraping data sederhana

# Dokumentasi Instalasi & Menjalankan Project Book Scraper

## Persyaratan

- Python 3.8 atau lebih baru
- pip (Python package manager)
- Git (opsional, jika clone dari GitHub)

## 1. Clone Repository (jika dari GitHub)

```
git clone https://github.com/Eden-08/scraping-data.git
cd scraping-data
```

## 2. Buat & Aktifkan Virtual Environment (opsional tapi disarankan)

```
python -m venv venv
# Aktifkan venv (Windows)
venv\Scripts\activate
# Aktifkan venv (Linux/Mac)
source venv/bin/activate
```

## 3. Install Dependensi

```
pip install -r requirment.txt
```

## 4. Jalankan Aplikasi

```
python app.py
```

Akses aplikasi di browser: [http://localhost:5000](http://localhost:5000)

## 5. Cara Menggunakan

- Masukkan URL target scraping pada form.
- Atur jumlah data dan delay jika perlu.
- Klik "Mulai Scraping".
- Progress scraping akan tampil, bisa dihentikan dengan tombol "Hentikan Scraping".
- Data hasil scraping bisa diunduh dalam format CSV/Excel.
- Data bisa diedit/hapus langsung dari tabel.

## Catatan

- Jika ingin scraping website lain, Anda harus menyesuaikan kode di file `scraper.py` sesuai struktur HTML website target.
- Untuk menghindari error, pastikan semua dependensi sudah terinstall dan gunakan Python versi terbaru.

---

Jika ada pertanyaan, silakan hubungi pengembang repo ini.
