# Warehouse Stock & Restock Monitor CLI

Aplikasi command line (CLI) berbasis Python untuk mengelola data inventaris gudang, memvalidasi input, menentukan status stok otomatis, menghitung valuasi aset per kategori, serta mengekspor laporan restock ke format CSV.

Dibuat untuk memenuhi Ujian Tengah Semester (UTS) Mata Kuliah **TK091 - Pemrograman Dasar** (Universitas Amikom Yogyakarta).

## Struktur Program

```text
gudang-cli/
├── main.py                      # Antarmuka CLI (menu, input/output)
├── warehouse_pkg/               # Package buatan sendiri
│   ├── __init__.py              # Ekspor fungsi utama package
│   ├── validator.py             # Validasi input, penanganan error, deduplikasi SKU
│   ├── inventory_ops.py         # Penentuan status, filter kritis, update stok & valuasi
│   └── file_handler.py          # Baca/tulis JSON dan ekspor laporan CSV
├── data/
│   ├── inventaris_gudang.json   # Data utama inventaris gudang (JSON)
│   └── laporan_restock.csv      # Hasil ekspor laporan peringatan restock (CSV)
└── README.md                    # Dokumentasi proyek
```

## Package & Dependency

- **Python:** versi 3.10 atau lebih baru.
- **Dependency:** Hanya menggunakan **Python Standard Library** (`json`, `csv`, `os`). Tidak memerlukan instalasi library eksternal.

## Cara Menjalankan Aplikasi

1. Pastikan Python 3.10+ sudah terpasang:

   ```bash
   python --version
   ```

   *(atau `python3 --version` di Linux/macOS)*

2. *(Opsional)* Buat dan aktifkan virtual environment:

   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. Jalankan program utama:

   ```bash
   python main.py
   ```

## Fitur Utama

1. **Tampilkan Semua Inventaris:** Menampilkan daftar bernomor berisi SKU, nama barang, kategori, stok, batas minimum, harga, dan status stok.
2. **Tambah Barang Baru:** Menambah data barang dengan validasi teks tak kosong, stok & harga bilangan bulat non-negatif (nilai `0` diterima untuk stok awal, `True`/teks ditolak), serta penolakan SKU duplikat.
3. **Update Stok (Masuk / Keluar):** Pembaruan jumlah stok berdasarkan kode `SKU` dengan proteksi agar pengurangan stok tidak melebihi jumlah tersedia.
4. **Peringatan Stok Kritis & Kategori Unik:** Menyaring barang yang perlu segera di-restock serta menampilkan daftar kategori unik menggunakan `set`.
5. **Ringkasan Valuasi Aset Gudang:** Mengurutkan dan menghitung total unit maupun nilai aset per kategori tanpa mengubah urutan list asli (`sorted()`).
6. **Ekspor Laporan (CSV):** Menyimpan daftar barang berstatus kritis ke `data/laporan_restock.csv`.

## Aturan Penentuan Status

Evaluasi dilakukan secara berurutan (prioritas dari atas ke bawah):

1. `stok <= 0` → **Stok Habis (Kritis)**
2. `stok <= min_stok` → **Perlu Restock**
3. `stok <= min_stok * 1.5` → **Menipis (Waspada)**
4. Selain itu → **Aman**

## Exception Handling & Debugging

- **Validasi File & Format JSON:** Menangani `FileNotFoundError` dan `json.JSONDecodeError` saat membaca `data/inventaris_gudang.json` agar program tidak berhenti mendadak (*crash*) jika file hilang atau rusak.
- **Defensive Input Validation:** Menahan input non-angka (`ValueError`), string kosong, harga/stok negatif, serta duplikasi kode `SKU` sebelum data diproses.
- **Skenario Debugging:** Memperbaiki `ValueError` saat pengguna memasukkan huruf pada input jumlah stok masuk/keluar dengan membungkus konversi `int()` ke dalam blok `try-except` di `validator.py`.
