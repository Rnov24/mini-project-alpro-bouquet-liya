"""
Main menu dan UI untuk Sistem Kasir.
"""
from src.config import APP_NAME
from src.models.barang import load_barang
from src.utils import input_non_empty
from src.services.barang_service import (
    tampil_semua_barang, tambah_barang, update_barang, cari_barang
)
from src.services.transaksi_service import (
    proses_transaksi, tampil_riwayat, tampil_rekap
)


MENU_OPTIONS = """
=== {app_name} ===
1) Tampilkan barang
2) Tambah barang
3) Update barang
4) Cari barang
5) Transaksi penjualan
6) Riwayat transaksi
7) Rekap pendapatan
0) Keluar
"""


def main_menu() -> None:
    """Main menu loop aplikasi."""
    barang_list = load_barang()
    
    while True:
        print(MENU_OPTIONS.format(app_name=APP_NAME))
        pilih = input_non_empty("Pilih menu: ")
        
        match pilih:
            case "1":
                tampil_semua_barang(barang_list)
            case "2":
                tambah_barang(barang_list)
            case "3":
                update_barang(barang_list)
            case "4":
                cari_barang(barang_list)
            case "5":
                proses_transaksi(barang_list)
                # Reload untuk sync dengan file
                barang_list = load_barang()
            case "6":
                tampil_riwayat()
            case "7":
                tampil_rekap()
            case "0":
                print("Sampai jumpa!")
                break
            case _:
                print("[!] Menu tidak valid.\n")
