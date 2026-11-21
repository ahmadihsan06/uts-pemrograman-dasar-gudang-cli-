def validate_item(item: dict) -> tuple[bool, str]:
    """
    Memvalidasi satu record barang agar sesuai tipe data dan aturan bisnis.

    Parameter:
        item (dict): Dictionary yang merepresentasikan satu barang.

    Return:
        tuple[bool, str]: (True, "Valid") jika lolos validasi,
                          atau (False, pesan_error) jika tidak valid.
    """
    required_keys = {"kode_barang", "nama_barang", "kategori", "stok", "min_stok", "harga_satuan"}

    if not isinstance(item, dict):
        return False, "Format record bukan dictionary."

    if not required_keys.issubset(item.keys()):
        missing = required_keys - set(item.keys())
        return False, f"Field wajib tidak lengkap: {missing}"

    if not str(item["kode_barang"]).strip() or not str(item["nama_barang"]).strip():
        return False, "Kode barang atau nama barang tidak boleh kosong."

    try:
        stok = int(item["stok"])
        min_stok = int(item["min_stok"])
        harga = float(item["harga_satuan"])
    except (ValueError, TypeError):
        return False, f"Stok atau harga bukan angka valid pada {item.get('kode_barang')}."

    if stok < 0 or min_stok < 0 or harga < 0:
        return False, f"Nilai stok/harga negatif pada {item.get('kode_barang')}."

    return True, "Valid"