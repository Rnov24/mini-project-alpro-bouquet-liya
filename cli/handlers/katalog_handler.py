"""
Handler untuk Menu Katalog (CLI).

Menangani otorisasi, visualisasi, dan manajemen data barang.
"""
from cli.ui.helpers import (
    print_header, print_menu_item, print_success, print_error,
    print_warning, print_info, print_divider, clear_screen
)
from cli.ui.inputs import input_styled, input_non_empty, input_int, input_float, input_yes_no
from cli.ui.colors import Colors
from core.services.barang_service import (
    load_barang, save_barang, find_by_kode, search_barang
)
from core.models.barang import Barang, UkuranBarang
from core.utils import format_rupiah


def show_katalog_menu():
    """Menampilkan menu manajemen katalog."""
    while True:
        clear_screen()
        print_header("MANAJEMEN KATALOG")
        print_menu_item("1", "Lihat Semua Barang")
        print_menu_item("2", "Cari Barang")
        print_menu_item("3", "Tambah Barang Baru")
        print_menu_item("4", "Update Stok/Harga")
        print_menu_item("5", "Hapus Barang")
        print_menu_item("0", "Kembali ke Menu Utama")
        
        choice = input_styled("\nPilihan [0-5]: ")
        
        if choice == "0":
            break
        elif choice == "1":
            list_all_barang()
        elif choice == "2":
            find_barang()
        elif choice == "3":
            create_new_barang()
        elif choice == "4":
            update_barang()
        elif choice == "5":
            delete_barang()
        else:
            print_error("Pilihan tidak valid.")
            input("Tekan Enter untuk lanjut...")


def list_all_barang():
    """Menampilkan semua barang di database."""
    clear_screen()
    print_header("DAFTAR KATALOG BUKET")
    
    barang_list = load_barang()
    if not barang_list:
        print_info("Belum ada data barang.")
        input("\nTekan Enter untuk kembali...")
        return

    for i, b in enumerate(barang_list, 1):
        print(f"{Colors.BOLD_CYAN}{i}. {b.nama} {Colors.DIM}({b.kode}){Colors.RESET}")
        
        # Format colors
        kertas = ", ".join(b.warna_kertas) if b.warna_kertas else "-"
        bunga = ", ".join(b.warna_bunga) if b.warna_bunga else "-"
        print(f"   🎨 Kertas: {kertas} | 🌸 Bunga: {bunga}")
        
        # Show variants
        print(f"   📏 Varian Ukuran:")
        for u in b.ukuran:
            stok_color = Colors.GREEN if u.stok > 0 else Colors.RED
            print(f"      - {u.nama:<10} : Rp {format_rupiah(u.harga):<12} "
                  f"[Stok: {stok_color}{u.stok}{Colors.RESET}]")
        print_divider("-", 40)
    
    print(f"\nTotal: {len(barang_list)} barang")
    input("\nTekan Enter untuk kembali...")


def find_barang():
    """Mencari barang berdasarkan keyword."""
    clear_screen()
    print_header("CARI BARANG")
    
    keyword = input_non_empty("Masukkan kata kunci (kode/nama): ")
    barang_list = load_barang()
    results = search_barang(barang_list, keyword)
    
    if not results:
        print_warning(f"Tidak ditemukan barang dengan kata kunci '{keyword}'")
    else:
        print(f"\nDitemukan {len(results)} barang:")
        for b in results:
            print(f"- {b.nama} ({b.kode})")
            
    input("\nTekan Enter untuk kembali...")


def create_new_barang():
    """Menambahkan barang baru ke katalog."""
    clear_screen()
    print_header("TAMBAH BARANG BARU")
    
    barang_list = load_barang()
    
    kode = input_non_empty("Kode Barang (unik): ").upper()
    if find_by_kode(barang_list, kode):
        print_error(f"Barang dengan kode {kode} sudah ada!")
        input("Tekan Enter untuk kembali...")
        return
        
    nama = input_non_empty("Nama Barang: ")
    
    # Input warna (comma separated)
    print("\nMasukkan warna dipisahkan koma (contoh: Merah, Biru, Pink)")
    kertas_raw = input_styled("Warna Kertas: ")
    bunga_raw = input_styled("Warna Bunga: ")
    
    warna_kertas = [w.strip() for w in kertas_raw.split(",")] if kertas_raw else []
    warna_bunga = [w.strip() for w in bunga_raw.split(",")] if bunga_raw else []
    
    # Input ukuran
    ukuran_list = []
    print("\nMasukkan varian ukuran (S/M/L/XL/dll). Ketik 'selesai' jika sudah.")
    
    while True:
        nama_ukuran = input_styled("Nama Ukuran: ")
        if nama_ukuran.lower() == "selesai":
            if not ukuran_list:
                print_error("Minimal harus ada 1 ukuran!")
                continue
            break
            
        harga = input_float(f"Harga Jual untuk {nama_ukuran}: ", min_val=0)
        hpp = input_float(f"HPP (Modal) untuk {nama_ukuran}: ", min_val=0)
        stok = input_int(f"Stok Awal untuk {nama_ukuran}: ", min_val=0)
        
        ukuran_list.append(UkuranBarang(
            nama=nama_ukuran,
            harga=harga,
            hpp=hpp,
            stok=stok
        ))
        print_success(f"Varian {nama_ukuran} ditambahkan.")
        
        if not input_yes_no("Tambah ukuran lain?"):
            break
            
    # Create and save
    new_barang = Barang(
        kode=kode,
        nama=nama,
        warna_kertas=warna_kertas,
        warna_bunga=warna_bunga,
        ukuran=ukuran_list
    )
    
    barang_list.append(new_barang)
    save_barang(barang_list)
    print_success(f"Barang {nama} berhasil disimpan!")
    input("\nTekan Enter untuk kembali...")


def update_barang():
    """Mengupdate data barang (stok/harga)."""
    clear_screen()
    print_header("UPDATE BARANG")
    
    kode = input_non_empty("Masukkan Kode Barang: ")
    barang_list = load_barang()
    target = find_by_kode(barang_list, kode)
    
    if not target:
        print_error("Barang tidak ditemukan.")
        input("Tekan Enter untuk kembali...")
        return
        
    print(f"\nBarang: {Colors.BOLD_CYAN}{target.nama}{Colors.RESET}")
    print("Varian Ukuran:")
    for i, u in enumerate(target.ukuran, 1):
        print(f"{i}. {u.nama} (Stok: {u.stok}, Harga: Rp {format_rupiah(u.harga)})")
        
    pilih_idx = input_int("Pilih nomor varian yang akan diupdate: ", min_val=1, max_val=len(target.ukuran))
    varian = target.ukuran[pilih_idx-1]
    
    print(f"\nUpdate {varian.nama}:")
    print("1. Update Stok")
    print("2. Update Harga")
    print("3. Update Keduanya")
    
    action = input_styled("Pilihan [1-3]: ")
    
    if action in ["1", "3"]:
        varian.stok = input_int(f"Stok baru (saat ini {varian.stok}): ", min_val=0)
        
    if action in ["2", "3"]:
        varian.harga = input_float(f"Harga baru (saat ini {varian.harga}): ", min_val=0)
        
    save_barang(barang_list)
    print_success("Data barang berhasil diupdate.")
    input("\nTekan Enter untuk kembali...")


def delete_barang():
    """Menghapus barang dari katalog."""
    clear_screen()
    print_header("HAPUS BARANG")
    
    kode = input_non_empty("Masukkan Kode Barang yang akan dihapus: ")
    barang_list = load_barang()
    target = find_by_kode(barang_list, kode)
    
    if not target:
        print_error("Barang tidak ditemukan.")
        input("Tekan Enter untuk kembali...")
        return
        
    print(f"\nAkan menghapus: {target.nama} ({target.kode})")
    if input_yes_no("Yakin ingin menghapus?", default=False):
        # Remove from list
        new_list = [b for b in barang_list if b.kode != target.kode]
        save_barang(new_list)
        print_success("Barang berhasil dihapus.")
    else:
        print_info("Penghapusan dibatalkan.")
    
    input("\nTekan Enter untuk kembali...")
