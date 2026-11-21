import json
import os
from warehouse_pkg.file_handler import (
    export_restock_csv,
    load_inventory_json,
    save_inventory_json,
)
from warehouse_pkg.inventory_ops import (
    add_new_item,
    clean_and_deduplicate,
    get_restock_alerts,
    search_items,
    summarize_by_category,
)


def display_items(items: list[dict], title: str) -> None:
    """Menampilkan daftar barang dalam format tabel rapi di terminal."""
    print(f"\n=== {title} ({len(items)} item) ===")
    if not items:
        print("Tidak ada data untuk ditampilkan.")
        return

    print(f"{'KODE':<10} | {'NAMA BARANG':<28} | {'KATEGORI':<13} | {'STOK':<5} | {'MIN':<4} | {'STATUS'}")
    print("-" * 82)
    for item in items:
        status = "PERLU RESTOCK" if item["stok"] <= item["min_stok"] else "AMAN"
        print(
            f"{item['kode_barang']:<10} | {item['nama_barang'][:28]:<28} | "
            f"{item['kategori'][:13]:<13} | {item['stok']:<5} | {item['min_stok']:<4} | {status}"
        )


def handle_add_item(inventory: list[dict], json_path: str) -> None:
    """Meminta input barang baru dari pengguna, memvalidasi, dan menyimpannya ke JSON."""
    print("\n=== TAMBAH BARANG BARU ===")
    kode_barang = input("Masukkan Kode Barang (cth: BRG-005) : ").strip()
    nama_barang = input("Masukkan Nama Barang                 : ").strip()
    kategori = input("Masukkan Kategori                    : ").strip()

    try:
        stok = int(input("Masukkan Jumlah Stok Awal            : ").strip())
        min_stok = int(input("Masukkan Batas Minimum Stok          : ").strip())
        harga_satuan = float(input("Masukkan Harga Satuan (Rp)           : ").strip())
    except ValueError:
        print("[ERROR] Stok, batas minimum, dan harga satuan harus berupa angka!")
        return

    raw_new_item = {
        "kode_barang": kode_barang,
        "nama_barang": nama_barang,
        "kategori": kategori,
        "stok": stok,
        "min_stok": min_stok,
        "harga_satuan": harga_satuan,
    }

    success, message = add_new_item(inventory, raw_new_item)
    if not success:
        print(f"[GAGAL] {message}")
        return

    try:
        save_inventory_json(json_path, inventory)
        print(f"[SUKSES] {message}")
        print(f"[INFO] Perubahan telah disimpan ke {json_path}")
    except OSError as err:
        print(f"[ERROR] Barang masuk ke memori, namun gagal menyimpan ke file JSON: {err}")


def run_cli() -> None:
    """Menjalankan loop utama aplikasi Command Line Interface."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_input = os.path.join(base_dir, "data", "inventaris_gudang.json")
    default_output = os.path.join(base_dir, "data", "laporan_restock.csv")

    print("==========================================================")
    print("   SISTEM PEMANTAU STOK GUDANG & PERINGATAN RESTOCK CLI   ")
    print("==========================================================")

    custom_path = input("Masukkan path file JSON [Enter untuk default: data/inventaris_gudang.json]: ").strip()
    input_path = custom_path if custom_path else default_input

    try:
        raw_data = load_inventory_json(input_path)
    except FileNotFoundError as err:
        print(f"[ERROR] {err}")
        return
    except json.JSONDecodeError as err:
        print(f"[ERROR] Format file JSON rusak/tidak valid: {err}")
        return
    except ValueError as err:
        print(f"[ERROR] {err}")
        return

    inventory, warnings = clean_and_deduplicate(raw_data)

    if warnings:
        print("\n[PERINGATAN DATA INPUT]")
        for warn in warnings:
            print(f" - {warn}")

    while True:
        print("\n================================================")
        print("1. Tampilkan Semua Stok Gudang")
        print("2. Tambah Barang Baru")
        print("3. Cari Barang (Kode / Nama)")
        print("4. Cek Peringatan Barang Perlu Restock")
        print("5. Rekapitulasi Valuasi per Kategori")
        print("6. Ekspor Laporan Restock (CSV)")
        print("7. Keluar")
        print("================================================")

        choice = input("Pilih menu (1-7): ").strip()

        if choice == "1":
            display_items(inventory, "DAFTAR INVENTARIS GUDANG VALID")
        elif choice == "2":
            handle_add_item(inventory, input_path)
        elif choice == "3":
            keyword = input("Masukkan kode atau nama barang yang dicari: ")
            results = search_items(inventory, keyword)
            display_items(results, f"HASIL PENCARIAN '{keyword}'")
        elif choice == "4":
            restock_list = get_restock_alerts(inventory)
            display_items(restock_list, "PERINGATAN STOK MENIPIS (RESTOCK)")
        elif choice == "5":
            summary = summarize_by_category(inventory)
            print("\n=== REKAPITULASI ASET PER KATEGORI ===")
            for kategori, info in summary.items():
                print(
                    f"- {kategori:<15}: {info['jumlah_sku']} jenis | "
                    f"{info['total_unit']} unit | Total Nilai: Rp {info['total_valuasi']:,.0f}"
                )
        elif choice == "6":
            restock_list = get_restock_alerts(inventory)
            if not restock_list:
                print("\n[INFO] Semua stok aman. Tidak ada data yang perlu diekspor.")
            else:
                try:
                    saved_count = export_restock_csv(default_output, restock_list)
                    print(f"\n[SUKSES] {saved_count} item restock berhasil diekspor ke: {default_output}")
                except OSError as err:
                    print(f"[ERROR] Gagal menyimpan file CSV: {err}")
        elif choice == "7":
            print("Terima kasih telah menggunakan Sistem Pemantau Stok Gudang.")
            break
        else:
            print("[PERINGATAN] Pilihan tidak valid. Silakan masukkan angka 1 sampai 7.")


if __name__ == "__main__":
    run_cli()