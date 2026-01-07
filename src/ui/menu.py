"""
Main menu dan UI untuk Sistem Kasir.
"""
from src.config import APP_NAME
from src.models.barang import load_barang
from src.utils import (
    input_non_empty, Colors, clear_screen, print_header,
    print_menu_item, print_success, print_error, print_divider
)
from src.services.barang_service import (
    tampil_semua_barang, tambah_barang, update_barang, cari_barang
)
from src.services.transaksi_service import (
    proses_transaksi, tampil_riwayat, tampil_rekap
)


# Menu icons untuk setiap pilihan
MENU_ICONS = {
    "1": "📋",  # Katalog
    "2": "➕",  # Tambah
    "3": "✏️",  # Update
    "4": "🔍",  # Cari
    "5": "🛒",  # Transaksi
    "6": "📜",  # Riwayat
    "7": "💰",  # Rekap
    "0": "🚪",  # Keluar
}


def display_logo() -> None:
    """Tampilkan logo ASCII art."""
    c = Colors
    logo = f"""
{c.BOLD_MAGENTA}    ╔╗ ╦ ╦╔═╗ ╦ ╦╔═╗╦ ╦╔═╗╔╦╗
    ╠╩╗║ ║║═╬╗║ ║║╣ ║ ║║╣  ║ 
    ╚═╝╚═╝╚═╝╚╚═╝╚═╝╚═╝╚═╝ ╩ {c.RESET}
{c.DIM}          ✿ L I Y A ✿{c.RESET}
"""
    print(logo)


def display_menu() -> None:
    """Tampilkan menu utama dengan style menarik."""
    c = Colors
    
    # Header box
    print(f"\n{c.BOLD_CYAN}╔══════════════════════════════════════════════════╗{c.RESET}")
    print(f"{c.BOLD_CYAN}║{c.RESET}     {c.BOLD_MAGENTA}🌸 SISTEM KASIR BUQEUET LIYA 🌸{c.RESET}              {c.BOLD_CYAN}║{c.RESET}")
    print(f"{c.BOLD_CYAN}║{c.RESET}  {c.DIM}Bouquet Management & Point of Sale System{c.RESET}       {c.BOLD_CYAN}║{c.RESET}")
    print(f"{c.BOLD_CYAN}╠══════════════════════════════════════════════════╣{c.RESET}")
    
    # Menu items - Katalog
    print(f"{c.BOLD_CYAN}║{c.RESET}                                                  {c.BOLD_CYAN}║{c.RESET}")
    print(f"{c.BOLD_CYAN}║{c.RESET}  {c.BOLD_YELLOW}▸ KATALOG{c.RESET}                                       {c.BOLD_CYAN}║{c.RESET}")
    print(f"{c.BOLD_CYAN}║{c.RESET}    {MENU_ICONS['1']} [{c.BOLD_WHITE}1{c.RESET}] Tampilkan Katalog Buqet                {c.BOLD_CYAN}║{c.RESET}")
    print(f"{c.BOLD_CYAN}║{c.RESET}    {MENU_ICONS['2']} [{c.BOLD_WHITE}2{c.RESET}] Tambah Katalog Buqet                   {c.BOLD_CYAN}║{c.RESET}")
    print(f"{c.BOLD_CYAN}║{c.RESET}    {MENU_ICONS['3']} [{c.BOLD_WHITE}3{c.RESET}] Update Katalog                          {c.BOLD_CYAN}║{c.RESET}")
    print(f"{c.BOLD_CYAN}║{c.RESET}    {MENU_ICONS['4']} [{c.BOLD_WHITE}4{c.RESET}] Cari Buqet                             {c.BOLD_CYAN}║{c.RESET}")
    
    print(f"{c.BOLD_CYAN}║{c.RESET}                                                  {c.BOLD_CYAN}║{c.RESET}")
    print(f"{c.BOLD_CYAN}║{c.RESET}  {c.BOLD_GREEN}▸ TRANSAKSI{c.RESET}                                     {c.BOLD_CYAN}║{c.RESET}")
    print(f"{c.BOLD_CYAN}║{c.RESET}    {MENU_ICONS['5']} [{c.BOLD_WHITE}5{c.RESET}] Transaksi Penjualan                    {c.BOLD_CYAN}║{c.RESET}")
    print(f"{c.BOLD_CYAN}║{c.RESET}    {MENU_ICONS['6']} [{c.BOLD_WHITE}6{c.RESET}] Riwayat Transaksi                      {c.BOLD_CYAN}║{c.RESET}")
    print(f"{c.BOLD_CYAN}║{c.RESET}    {MENU_ICONS['7']} [{c.BOLD_WHITE}7{c.RESET}] Rekap Pendapatan                       {c.BOLD_CYAN}║{c.RESET}")
    
    print(f"{c.BOLD_CYAN}║{c.RESET}                                                  {c.BOLD_CYAN}║{c.RESET}")
    print(f"{c.BOLD_CYAN}╠══════════════════════════════════════════════════╣{c.RESET}")
    print(f"{c.BOLD_CYAN}║{c.RESET}    {MENU_ICONS['0']} [{c.BOLD_RED}0{c.RESET}] Keluar                                 {c.BOLD_CYAN}║{c.RESET}")
    print(f"{c.BOLD_CYAN}╚══════════════════════════════════════════════════╝{c.RESET}")
    print()


def display_goodbye() -> None:
    """Tampilkan pesan perpisahan."""
    c = Colors
    print(f"""
{c.BOLD_CYAN}╔══════════════════════════════════════════════════╗{c.RESET}
{c.BOLD_CYAN}║{c.RESET}                                                  {c.BOLD_CYAN}║{c.RESET}
{c.BOLD_CYAN}║{c.RESET}   {c.BOLD_MAGENTA}✿ Terima kasih telah menggunakan ✿{c.RESET}             {c.BOLD_CYAN}║{c.RESET}
{c.BOLD_CYAN}║{c.RESET}       {c.BOLD_WHITE}SISTEM KASIR BUQEUET LIYA{c.RESET}                  {c.BOLD_CYAN}║{c.RESET}
{c.BOLD_CYAN}║{c.RESET}                                                  {c.BOLD_CYAN}║{c.RESET}
{c.BOLD_CYAN}║{c.RESET}   {c.BOLD_GREEN}Sampai jumpa! Semoga sukses selalu 🌸{c.RESET}          {c.BOLD_CYAN}║{c.RESET}
{c.BOLD_CYAN}║{c.RESET}                                                  {c.BOLD_CYAN}║{c.RESET}
{c.BOLD_CYAN}╚══════════════════════════════════════════════════╝{c.RESET}
""")


def main_menu() -> None:
    """Main menu loop aplikasi."""
    barang_list = load_barang()
    c = Colors
    
    # Welcome screen
    clear_screen()
    display_logo()
    print(f"{c.DIM}Tekan Enter untuk melanjutkan...{c.RESET}")
    input()
    
    while True:
        clear_screen()
        display_logo()
        display_menu()
        
        pilih = input(f"{c.BOLD_GREEN}▸ {c.WHITE}Pilih menu [{c.BOLD_YELLOW}0-7{c.WHITE}]: {c.RESET}").strip()
        
        match pilih:
            case "1":
                print_header("📋 KATALOG BUQET", "Menampilkan semua katalog")
                tampil_semua_barang(barang_list)
                input(f"\n{c.DIM}Tekan Enter untuk kembali ke menu...{c.RESET}")
            case "2":
                print_header("➕ TAMBAH KATALOG", "Menambahkan katalog baru")
                tambah_barang(barang_list)
                input(f"\n{c.DIM}Tekan Enter untuk kembali ke menu...{c.RESET}")
            case "3":
                print_header("✏️ UPDATE KATALOG", "Mengubah data katalog")
                update_barang(barang_list)
                input(f"\n{c.DIM}Tekan Enter untuk kembali ke menu...{c.RESET}")
            case "4":
                print_header("🔍 CARI BUQET", "Pencarian katalog")
                cari_barang(barang_list)
                input(f"\n{c.DIM}Tekan Enter untuk kembali ke menu...{c.RESET}")
            case "5":
                print_header("🛒 TRANSAKSI PENJUALAN", "Proses transaksi baru")
                proses_transaksi(barang_list)
                # Reload untuk sync dengan file
                barang_list = load_barang()
                input(f"\n{c.DIM}Tekan Enter untuk kembali ke menu...{c.RESET}")
            case "6":
                print_header("📜 RIWAYAT TRANSAKSI", "Daftar transaksi terakhir")
                tampil_riwayat()
                input(f"\n{c.DIM}Tekan Enter untuk kembali ke menu...{c.RESET}")
            case "7":
                print_header("💰 REKAP PENDAPATAN", "Ringkasan pendapatan")
                tampil_rekap()
                input(f"\n{c.DIM}Tekan Enter untuk kembali ke menu...{c.RESET}")
            case "0":
                clear_screen()
                display_goodbye()
                break
            case _:
                print_error("Menu tidak valid! Pilih 0-7.")
                input(f"\n{c.DIM}Tekan Enter untuk kembali ke menu...{c.RESET}")
