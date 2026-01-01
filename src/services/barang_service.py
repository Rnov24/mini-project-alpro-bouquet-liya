"""
Business logic untuk operasi Barang.
"""
from src.models.barang import Barang, load_barang, save_barang, find_by_kode, search_barang
from src.utils import input_non_empty, input_int, input_float, format_rupiah


def tampil_semua_barang(barang_list: list[Barang]) -> None:
    """Tampilkan semua barang dalam format tabel."""
    if not barang_list:
        print("\n[!] Data barang masih kosong.\n")
        return
    
    print("\n=== DAFTAR BARANG ===")
    print(f"{'No':<4} {'Kode':<10} {'Nama':<25} {'Harga':>12} {'Stok':>6}")
    print("-" * 65)
    for i, b in enumerate(barang_list, start=1):
        print(f"{i:<4} {b.kode:<10} {b.nama:<25} {format_rupiah(b.harga):>12} {b.stok:>6}")
    print("-" * 65)


def tambah_barang(barang_list: list[Barang]) -> bool:
    """Tambah barang baru. Return True jika berhasil."""
    print("\n=== TAMBAH BARANG ===")
    kode = input_non_empty("Kode barang: ").upper()
    
    if find_by_kode(barang_list, kode) is not None:
        print("[!] Kode sudah ada. Gunakan menu update.")
        return False
    
    nama = input_non_empty("Nama barang: ")
    harga = input_float("Harga (angka): ", min_val=0)
    stok = input_int("Stok awal: ", min_val=0)
    
    barang_baru = Barang(kode=kode, nama=nama, harga=harga, stok=stok)
    barang_list.append(barang_baru)
    save_barang(barang_list)
    
    print("[✓] Barang berhasil ditambahkan.")
    return True


def update_barang(barang_list: list[Barang]) -> bool:
    """Update harga atau stok barang. Return True jika berhasil."""
    print("\n=== UPDATE BARANG ===")
    kode = input_non_empty("Masukkan kode barang: ").upper()
    
    barang = find_by_kode(barang_list, kode)
    if barang is None:
        print("[!] Barang tidak ditemukan.")
        return False
    
    print(f"Barang ditemukan: {barang.kode} - {barang.nama} "
          f"(Harga {format_rupiah(barang.harga)}, Stok {barang.stok})")
    print("1) Update harga")
    print("2) Update stok (tambah/kurang)")
    
    pilih = input_int("Pilih (1/2): ", min_val=1, max_val=2)
    
    if pilih == 1:
        harga_baru = input_float("Harga baru: ", min_val=0)
        barang.harga = harga_baru
        save_barang(barang_list)
        print("[✓] Harga berhasil diupdate.")
    else:
        delta = input_int("Masukkan perubahan stok (contoh: 5 atau -3): ")
        stok_baru = barang.stok + delta
        if stok_baru < 0:
            print("[!] Stok tidak boleh negatif.")
            return False
        barang.stok = stok_baru
        save_barang(barang_list)
        print("[✓] Stok berhasil diupdate.")
    
    return True


def cari_barang(barang_list: list[Barang]) -> None:
    """Cari dan tampilkan barang berdasarkan keyword."""
    print("\n=== CARI BARANG ===")
    keyword = input_non_empty("Masukkan kode/nama (keyword): ")
    
    hasil = search_barang(barang_list, keyword)
    if not hasil:
        print("[!] Tidak ada hasil pencarian.")
        return
    
    tampil_semua_barang(hasil)
