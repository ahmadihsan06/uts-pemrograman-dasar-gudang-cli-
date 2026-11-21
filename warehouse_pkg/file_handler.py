import csv
import json
import os


def load_inventory_json(filepath: str) -> list[dict]:
    """
    Membaca data inventaris mentah dari file JSON.

    Parameter:
        filepath (str): Lokasi path file JSON input.

    Return:
        list[dict]: Daftar dictionary barang dari file JSON.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File tidak ditemukan di: {filepath}")

    with open(filepath, mode="r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Format root JSON harus berupa list/array objek barang.")

    return data


def save_inventory_json(filepath: str, items: list[dict]) -> None:
    """
    Menyimpan seluruh daftar inventaris barang ke dalam file JSON.

    Parameter:
        filepath (str): Lokasi path file JSON tujuan.
        items (list[dict]): Daftar dictionary barang yang akan disimpan.

    Return:
        None
    """
    dir_name = os.path.dirname(filepath)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with open(filepath, mode="w", encoding="utf-8") as file:
        json.dump(items, file, indent=2, ensure_ascii=False)


def export_restock_csv(filepath: str, restock_items: list[dict]) -> int:
    """
    Menyimpan daftar barang yang perlu restock ke dalam file CSV.

    Parameter:
        filepath (str): Lokasi path file CSV output.
        restock_items (list[dict]): Daftar barang yang stoknya menipis.

    Return:
        int: Jumlah baris data yang berhasil disimpan ke file CSV.
    """
    dir_name = os.path.dirname(filepath)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    fieldnames = [
        "kode_barang",
        "nama_barang",
        "kategori",
        "stok",
        "min_stok",
        "kekurangan_unit",
        "estimasi_biaya_restock",
    ]

    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for item in restock_items:
            kekurangan = max(1, (item["min_stok"] - item["stok"]) + 5)
            estimasi_biaya = kekurangan * item["harga_satuan"]
            writer.writerow(
                {
                    "kode_barang": item["kode_barang"],
                    "nama_barang": item["nama_barang"],
                    "kategori": item["kategori"],
                    "stok": item["stok"],
                    "min_stok": item["min_stok"],
                    "kekurangan_unit": kekurangan,
                    "estimasi_biaya_restock": estimasi_biaya,
                }
            )

    return len(restock_items)