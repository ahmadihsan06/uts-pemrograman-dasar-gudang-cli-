from warehouse_pkg.validator import validate_item


def clean_and_deduplicate(raw_items: list[dict]) -> tuple[list[dict], list[str]]:
    """
    Membersihkan data tidak valid dan menghapus record dengan kode_barang duplikat.

    Parameter:
        raw_items (list[dict]): Data mentah hasil pembacaan JSON.

    Return:
        tuple[list[dict], list[str]]:
            - List berisi dictionary barang yang valid dan unik.
            - List berisi catatan peringatan data yang diabaikan.
    """
    valid_items: list[dict] = []
    seen_codes: set[str] = set()
    warnings: list[str] = []

    for index, item in enumerate(raw_items, start=1):
        is_valid, message = validate_item(item)
        if not is_valid:
            warnings.append(f"Baris #{index} diabaikan -> {message}")
            continue

        kode = str(item["kode_barang"]).strip().upper()
        if kode in seen_codes:
            warnings.append(f"Baris #{index} ({kode}) diabaikan -> Kode barang duplikat.")
            continue

        seen_codes.add(kode)
        normalized_item = {
            "kode_barang": kode,
            "nama_barang": str(item["nama_barang"]).strip(),
            "kategori": str(item["kategori"]).strip(),
            "stok": int(item["stok"]),
            "min_stok": int(item["min_stok"]),
            "harga_satuan": float(item["harga_satuan"]),
        }
        valid_items.append(normalized_item)

    return valid_items, warnings


def add_new_item(items: list[dict], raw_new_item: dict) -> tuple[bool, str]:
    """
    Memvalidasi dan menambahkan barang baru ke inventaris jika kode belum terdaftar.

    Parameter:
        items (list[dict]): Daftar barang valid yang sudah ada.
        raw_new_item (dict): Data barang baru dari input pengguna.

    Return:
        tuple[bool, str]: (True, pesan_sukses) jika berhasil ditambahkan,
                          atau (False, pesan_error) jika gagal/duplikat.
    """
    is_valid, message = validate_item(raw_new_item)
    if not is_valid:
        return False, message

    kode = str(raw_new_item["kode_barang"]).strip().upper()
    existing_codes: set[str] = {item["kode_barang"] for item in items}

    if kode in existing_codes:
        return False, f"Kode barang '{kode}' sudah terdaftar di gudang."

    normalized_item = {
        "kode_barang": kode,
        "nama_barang": str(raw_new_item["nama_barang"]).strip(),
        "kategori": str(raw_new_item["kategori"]).strip(),
        "stok": int(raw_new_item["stok"]),
        "min_stok": int(raw_new_item["min_stok"]),
        "harga_satuan": float(raw_new_item["harga_satuan"]),
    }
    items.append(normalized_item)
    return True, f"Barang '{normalized_item['nama_barang']}' ({kode}) berhasil ditambahkan."


def get_restock_alerts(items: list[dict]) -> list[dict]:
    """
    Menyaring barang yang jumlah stoknya kurang dari atau sama dengan batas minimum.

    Parameter:
        items (list[dict]): Daftar barang valid.

    Return:
        list[dict]: Daftar barang yang membutuhkan restock.
    """
    return [item for item in items if item["stok"] <= item["min_stok"]]


def search_items(items: list[dict], keyword: str) -> list[dict]:
    """
    Mencari barang berdasarkan potongan kata pada kode atau nama barang.

    Parameter:
        items (list[dict]): Daftar barang valid.
        keyword (str): Kata kunci pencarian.

    Return:
        list[dict]: Daftar barang yang cocok dengan kata kunci.
    """
    key_lower = keyword.strip().lower()
    if not key_lower:
        return []

    return [
        item
        for item in items
        if key_lower in item["kode_barang"].lower() or key_lower in item["nama_barang"].lower()
    ]


def summarize_by_category(items: list[dict]) -> dict[str, dict]:
    """
    Menghitung rekapitulasi total jenis barang, total unit stok, dan valuasi aset per kategori.

    Parameter:
        items (list[dict]): Daftar barang valid.

    Return:
        dict[str, dict]: Dictionary dengan key nama kategori dan value statistiknya.
    """
    unique_categories: set[str] = {item["kategori"] for item in items}
    asset_per_item: dict[str, float] = {
        item["kode_barang"]: item["stok"] * item["harga_satuan"] for item in items
    }

    summary: dict[str, dict] = {}
    for category in sorted(unique_categories):
        cat_items = [item for item in items if item["kategori"] == category]
        total_unit = sum(item["stok"] for item in cat_items)
        total_valuasi = sum(asset_per_item[item["kode_barang"]] for item in cat_items)

        summary[category] = {
            "jumlah_sku": len(cat_items),
            "total_unit": total_unit,
            "total_valuasi": total_valuasi,
        }

    return summary