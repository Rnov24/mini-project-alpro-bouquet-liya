"""
Main Menu CLI - Sistem Kasir Buqeuet Liya.

Menghubungkan semua module CLI (ui dan handlers) menjadi
aplikasi yang utuh.
"""
import sys
from cli.ui.helpers import (
    print_header, print_menu_item, print_error, print_success, 
    clear_screen, print_info
)
from cli.ui.inputs import input_styled
from cli.handlers.katalog_handler import show_katalog_menu
from cli.handlers.transaksi_handler import show_transaksi_menu, show_riwayat_menu
from cli.handlers.order_handler import show_order_menu
from core.config import APP_NAME, APP_VERSION


def show_main_menu():
    """Menampilkan menu utama."""
    clear_screen()
    print_header(APP_NAME, f"v{APP_VERSION}")
    
    print_menu_item("1", "Katalog Barang")
    print_menu_item("2", "Transaksi Baru (Kasir)")
    print_menu_item("3", "Kelola Pesanan (Online)")
    print_menu_item("4", "Riwayat & Laporan")
    print_menu_item("0", "Keluar")


def main():
    """Main application loop."""
    try:
        while True:
            show_main_menu()
            choice = input_styled("\nPilihan [0-4]: ")
            
            if choice == "0":
                print_success("Terima kasih telah menggunakan aplikasi ini!")
                sys.exit(0)
            elif choice == "1":
                show_katalog_menu()
            elif choice == "2":
                show_transaksi_menu()
            elif choice == "3":
                show_order_menu()
            elif choice == "4":
                show_riwayat_menu()
            else:
                print_error("Pilihan tidak valid.")
                input("Tekan Enter untuk lanjut...")
                
    except KeyboardInterrupt:
        print("\n\n")
        print_success("Aplikasi dihentikan. Sampai jumpa!")
        sys.exit(0)
    except Exception as e:
        print_error(f"Terjadi kesalahan fatal: {e}")
        input("Tekan Enter untuk keluar...")
        sys.exit(1)


if __name__ == "__main__":
    main()
