"""
Business logic untuk operasi Barang.
"""
from src.models.barang import (
    Barang, UkuranBarang, load_barang, save_barang, find_by_kode, search_barang
)
from src.utils import input_non_empty, input_int, input_float, format_rupiah


UKURAN_OPTIONS = ["Mini", "Standar", "Besar"]


def tampil_semua_barang(barang_list: list[Barang]) -> None:
    """Tampilkan semua barang dalam format tabel."""
    if not barang_list:
        print("\n[!] Data barang masih kosong.\n")
        return
    
    print("\n=== DAFTAR KATALOG BUQET ===")
    for i, b in enumerate(barang_list, start=1):
        print(f"\n{i}. [{b.kode}] {b.nama}")
        if b.warna_kertas:
            print(f"   Warna Kertas: {', '.join(b.warna_kertas)}")
        if b.warna_bunga:
            print(f"   Warna Bunga: {', '.join(b.warna_bunga)}")
        
        # Tampil tabel ukuran
        print(f"   {'Ukuran':<10} {'Harga':>12} {'HPP':>10} {'Stok':>6}")
        print(f"   {'-'*40}")
        for u in b.ukuran:
            print(f"   {u.nama:<10} {format_rupiah(u.harga):>12} {format_rupiah(u.hpp):>10} {u.stok:>6}")
    print()


def tambah_barang(barang_list: list[Barang]) -> bool:
    """Tambah barang baru. Return True jika berhasil."""
    print("\n=== TAMBAH KATALOG BUQET ===")
    kode = input_non_empty("Kode barang: ").upper()
    
    if find_by_kode(barang_list, kode) is not None:
        print("[!] Kode sudah ada. Gunakan menu update.")
        return False
    
    nama = input_non_empty("Nama Katalog Buqet: ")
    
    # Input warna
    warna_kertas_str = input_non_empty("Warna Kertas (pisahkan dengan koma): ")
    warna_kertas = [w.strip() for w in warna_kertas_str.split(",") if w.strip()]
    
    warna_bunga_str = input_non_empty("Warna Bunga (pisahkan dengan koma): ")
    warna_bunga = [w.strip() for w in warna_bunga_str.split(",") if w.strip()]
    
    # Input ukuran
    ukuran_list = []
    for ukuran_nama in UKURAN_OPTIONS:
        print(f"\n== Input Ukuran {ukuran_nama} ==")
        harga = input_float(f"Harga {ukuran_nama}: ", min_val=0)
        hpp = input_float(f"HPP {ukuran_nama}: ", min_val=0)
        stok = input_int(f"Stok {ukuran_nama}: ", min_val=0)
        ukuran_list.append(UkuranBarang(nama=ukuran_nama, harga=harga, hpp=hpp, stok=stok))
    
    barang_baru = Barang(
        kode=kode, 
        nama=nama,
        warna_kertas=warna_kertas,
        warna_bunga=warna_bunga,
        ukuran=ukuran_list
    )
    barang_list.append(barang_baru)
    save_barang(barang_list)
    
    print("[✓] Katalog Buqet berhasil ditambahkan.")
    return True


def update_barang(barang_list: list[Barang]) -> bool:
    """Update harga/stok per ukuran. Return True jika berhasil."""
    print("\n=== UPDATE KATALOG BUQET ===")
    kode = input_non_empty("Masukkan kode barang: ").upper()
    
    barang = find_by_kode(barang_list, kode)
    if barang is None:
        print("[!] Barang tidak ditemukan.")
        return False
    
    print(f"\nBarang ditemukan: [{barang.kode}] {barang.nama}")
    print("Ukuran tersedia:")
    for i, u in enumerate(barang.ukuran, start=1):
        print(f"  {i}) {u.nama} - Harga: {format_rupiah(u.harga)}, HPP: {format_rupiah(u.hpp)}, Stok: {u.stok}")
    
    pilih_ukuran = input_int("Pilih ukuran (nomor): ", min_val=1, max_val=len(barang.ukuran))
    ukuran = barang.ukuran[pilih_ukuran - 1]
    
    print(f"\nUpdate {ukuran.nama}:")
    print("1) Update harga")
    print("2) Update HPP")
    print("3) Update stok (tambah/kurang)")
    pilih = input_int("Pilih (1/2/3): ", min_val=1, max_val=3)
    
    if pilih == 1:
        harga_baru = input_float("Harga baru: ", min_val=0)
        ukuran.harga = harga_baru
        print("[✓] Harga berhasil diupdate.")
    elif pilih == 2:
        hpp_baru = input_float("HPP baru: ", min_val=0)
        ukuran.hpp = hpp_baru
        print("[✓] HPP berhasil diupdate.")
    else:
        delta = input_int("Masukkan perubahan stok (contoh: 5 atau -3): ")
        stok_baru = ukuran.stok + delta
        if stok_baru < 0:
            print("[!] Stok tidak boleh negatif.")
            return False
        ukuran.stok = stok_baru
        print("[✓] Stok berhasil diupdate.")
    
    save_barang(barang_list)
    return True


def cari_barang(barang_list: list[Barang]) -> None:
    """Cari dan tampilkan barang berdasarkan keyword."""
    print("\n=== CARI KATALOG ===")
    keyword = input_non_empty("Masukkan kode/nama (keyword): ")
    
    hasil = search_barang(barang_list, keyword)
    if not hasil:
        print("[!] Tidak ada hasil pencarian.")
        return
    
    tampil_semua_barang(hasil)
