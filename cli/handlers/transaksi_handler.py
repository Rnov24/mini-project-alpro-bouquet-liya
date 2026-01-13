"""
Handler untuk Menu Transaksi (Kasir).

Menangani proses transaksi penjualan langsung (Kasir Mode).
"""
import datetime
from cli.ui.helpers import (
    print_header, print_menu_item, print_success, print_error,
    print_info, print_divider, clear_screen, print_warning
)
from cli.ui.inputs import input_styled, input_non_empty, input_int, input_yes_no, input_float
from cli.ui.colors import Colors
from core.services.barang_service import load_barang, find_by_kode, search_barang
from core.models.cart import Cart, CartItem
from core.services.order_service import create_order_from_cart
from core.services.transaksi_service import finalize_order, load_recent_transactions, get_transaction_summary
from core.services.invoice_service import generate_invoice_text
from core.utils import format_rupiah


def show_transaksi_menu():
    """Menampilkan menu transaksi kasir."""
    # Kasir mode usually goes straight to new transaction
    new_transaction()


def show_riwayat_menu():
    """Menampilkan menu riwayat & rekap."""
    while True:
        clear_screen()
        print_header("RIWAYAT & LAPORAN")
        print_menu_item("1", "Lihat Riwayat Transaksi")
        print_menu_item("2", "Rekap Pendapatan")
        print_menu_item("0", "Kembali")
        
        choice = input_styled("\nPilihan: ")
        if choice == "0":
            break
        elif choice == "1":
            show_recent_transactions()
        elif choice == "2":
            show_rekap_summary()
        else:
            print_error("Pilihan tidak valid.")

def show_recent_transactions():
    """Menampilkan riwayat transaksi terakhir."""
    clear_screen()
    print_header("RIWAYAT TRANSAKSI TERAKHIR")
    
    rows = load_recent_transactions(limit=15)
    if not rows:
        print_info("Belum ada data transaksi.")
        input("Tekan Enter...")
        return
        
    print(f"{'WAKTU':<20} | {'ID TRX':<20} | {'ITEM':<30} | {'TOTAL':>15}")
    print_divider()
    
    for r in rows:
        # Simple display
        item_desc = f"{r.get('nama')} x{r.get('qty')}"
        print(f"{r.get('waktu')[:19]:<20} | {r.get('id_transaksi'):<20} | {item_desc[:30]:<30} | {format_rupiah(float(r.get('subtotal', 0))):>15}")
        
    print_divider()
    input("\nTekan Enter untuk kembali...")

def show_rekap_summary():
    """Menampilkan ringkasan pendapatan."""
    clear_screen()
    print_header("REKAP PENDAPATAN")
    
    summary = get_transaction_summary()
    
    print(f"Total Transaksi : {summary.get('count')}")
    print(f"Total Omzet     : {Colors.BOLD_GREEN}Rp {format_rupiah(summary.get('total_revenue'))}{Colors.RESET}")
    print(f"Total HPP       : Rp {format_rupiah(summary.get('total_hpp'))}")
    print(f"Total Profit    : {Colors.BOLD_CYAN}Rp {format_rupiah(summary.get('total_profit'))}{Colors.RESET}")
    
    input("\nTekan Enter untuk kembali...")


def new_transaction():
    """Memulai transaksi baru."""
    cart = Cart()
    barang_list = load_barang()
    
    while True:
        clear_screen()
        print_header("KASIR - TRANSAKSI BARU")
        
        # Show Cart
        if not cart.items:
            print_info("Keranjang kosong.")
        else:
            print(f"Isi Keranjang ({len(cart.items)} items):")
            for i, item in enumerate(cart.items, 1):
                print(f"{i}. {item.nama:<20} {item.ukuran:<8} x{item.qty:<3} = Rp {format_rupiah(item.subtotal)}")
            print_divider()
            print(f"Subtotal: {Colors.BOLD_GREEN}Rp {format_rupiah(cart.subtotal)}{Colors.RESET}")
            
        print("\nMenu:")
        print("1. Tambah Item")
        print("2. Hapus Item")
        print("3. Checkout / Pembayaran")
        print("0. Batal / Keluar")
        
        choice = input_styled("Pilihan: ")
        
        if choice == "1":
            add_item_to_cart(cart, barang_list)
        elif choice == "2":
            remove_item_from_cart(cart)
        elif choice == "3":
            if not cart.items:
                print_error("Keranjang masih kosong!")
                input("Tekan Enter...")
                continue
            checkout_process(cart)
            return # Exit after checkout
        elif choice == "0":
            if cart.items:
                if input_yes_no("Batalkan transaksi berjalan?"):
                    break
            else:
                break
        else:
            print_error("Pilihan tidak valid.")


def add_item_to_cart(cart: Cart, barang_list: list):
    """Menambahkan item ke keranjang."""
    print("\n--- Cari Barang ---")
    query = input_styled("Masukkan kode/nama (kosong untuk batal): ")
    if not query:
        return
        
    results = search_barang(barang_list, query)
    if not results:
        print_error("Barang tidak ditemukan.")
        input("Tekan Enter...")
        return
        
    # Select barang
    selected_barang = None
    if len(results) == 1:
        selected_barang = results[0]
    else:
        print(f"\nDitemukan {len(results)} barang:")
        for i, b in enumerate(results, 1):
            print(f"{i}. {b.nama} ({b.kode})")
        
        try:
            idx = input_int("Pilih nomor: ", min_val=1, max_val=len(results))
            selected_barang = results[idx-1]
        except:
            return

    # Select variant
    print(f"\nBarang: {Colors.BOLD_CYAN}{selected_barang.nama}{Colors.RESET}")
    print("Pilih Ukuran:")
    for i, u in enumerate(selected_barang.ukuran, 1):
        stok_msg = f"{Colors.GREEN}{u.stok}{Colors.RESET}" if u.stok > 0 else f"{Colors.RED}Habis{Colors.RESET}"
        print(f"{i}. {u.nama:<10} (Rp {format_rupiah(u.harga)}) - Stok: {stok_msg}")
        
    try:
        idx = input_int("Pilih ukuran: ", min_val=1, max_val=len(selected_barang.ukuran))
        selected_ukuran = selected_barang.ukuran[idx-1]
    except:
        return
        
    if selected_ukuran.stok <= 0:
        print_error("Stok habis!")
        input("Tekan Enter...")
        return
        
    # Input Qty
    qty = input_int(f"Masukkan jumlah (Max {selected_ukuran.stok}): ", min_val=1, max_val=selected_ukuran.stok)
    
    # Optional colors
    warna_kertas = "-"
    if selected_barang.warna_kertas:
        print(f"\nPilihan Kertas: {', '.join(selected_barang.warna_kertas)}")
        warna_kertas = input_styled("Warna Kertas: ") or "-"
        
    warna_bunga = "-"
    if selected_barang.warna_bunga:
        print(f"\nPilihan Bunga: {', '.join(selected_barang.warna_bunga)}")
        warna_bunga = input_styled("Warna Bunga: ") or "-"
        
    # Add to cart
    cart.add_item(CartItem(
        kode=selected_barang.kode,
        nama=selected_barang.nama,
        ukuran=selected_ukuran.nama,
        warna_kertas=warna_kertas,
        warna_bunga=warna_bunga,
        qty=qty,
        harga=selected_ukuran.harga,
        hpp=selected_ukuran.hpp
    ))
    print_success("Item ditambahkan ke keranjang.")


def remove_item_from_cart(cart: Cart):
    """Menghapus item dari keranjang."""
    if not cart.items:
        return
        
    print("\nHapus Item:")
    for i, item in enumerate(cart.items, 1):
        print(f"{i}. {item.nama} ({item.ukuran}) x{item.qty}")
        
    try:
        idx = input_int("Pilih nomor item (0 batal): ", min_val=0, max_val=len(cart.items))
        if idx > 0:
            cart.remove_item(idx-1)
            print_success("Item dihapus.")
    except:
        pass


def checkout_process(cart: Cart):
    """Proses pembayaran dan finalisasi."""
    clear_screen()
    print_header("CHECKOUT")
    
    print(f"Total Belanja: {Colors.BOLD_GREEN}Rp {format_rupiah(cart.subtotal)}{Colors.RESET}")
    
    # Input Data Pembeli
    cart.nama_pembeli = input_non_empty("Nama Pembeli: ")
    cart.wa_pembeli = input_styled("No WA (Optional): ")
    
    # Diskon
    # Diskon
    # Diskon
    if input_yes_no("Berikan diskon?", default=False):
        diskon_rp = input_float("Nominal Diskon (Rp): ", min_val=0)
        cart.diskon_nominal = diskon_rp
        
    # Delivery Info
    print("\nMetode Pengiriman:")
    print("1. Ambil Sendiri (Pickup)")
    print("2. Delivery")
    choice = input_styled("Pilihan [1/2]: ")
    
    if choice == "2":
        cart.delivery_type = "delivery"
        cart.ongkir = input_float("Biaya Ongkir (Rp): ", min_val=0)
        cart.alamat = input_non_empty("Alamat Pengiriman/Keterangan: ")
    else:
        cart.delivery_type = "ambil"
        cart.ongkir = 0
    
    # Hitung total (auto-calculated property)
    
    print_divider()
    print(f"Subtotal : Rp {format_rupiah(cart.subtotal)}")
    if cart.diskon > 0:
        print(f"Diskon   : -Rp {format_rupiah(cart.diskon)}")
    if cart.ongkir > 0:
        print(f"Ongkir   : Rp {format_rupiah(cart.ongkir)}")
    print(f"TOTAL    : {Colors.BOLD_GREEN}Rp {format_rupiah(cart.total)}{Colors.RESET}")
    print_divider()
    
    # confirm
    if not input_yes_no("Proses transaksi?"):
        print_info("Transaksi dibatalkan (keranjang tidak disimpan).")
        return
        
    # Process
    try:
        # 1. Create Order
        order = create_order_from_cart(cart, source="cli")
        
        # 2. Print Preview Invoice (Text)
        print("\n" + generate_invoice_text(order, format_type="cli"))
        
        # 3. Finalize (Save to CSV & Generate Invoice Image)
        trx_id, inv_path = finalize_order(order["order_id"], generate_invoice=True)
        
        print_success(f"Transaksi Berhasil! ID: {trx_id}")
        if inv_path:
            print_info(f"Invoice saved to: {inv_path}")
        input("Tekan Enter untuk kembali ke menu...")
        
    except Exception as e:
        print_error(f"Gagal memproses transaksi: {e}")
        input("Tekan Enter...")
