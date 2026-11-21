# Sistem Pemantau Stok Gudang & Peringatan Restock (CLI)
Aplikasi command line (CLI) berbasis Python untuk mengelola data inventaris gudang, memvalidasi input, menentukan status stok otomatis, menghitung valuasi aset per kategori, serta mengekspor laporan restock ke format CSV.

## Struktur program
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

## 
