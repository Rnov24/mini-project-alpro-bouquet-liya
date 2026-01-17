"""
Handler untuk Manajemen Order (CLI).

Menangani pesanan yang masuk (baik dari Bot maupun CLI),
update status, dan finalisasi.
"""
from cli.ui.helpers import (
    print_header, print_info, print_error, print_success, 
    print_warning, print_divider, clear_screen
)
from cli.ui.colors import Colors
from cli.ui.inputs import input_styled, input_int, input_yes_no, input_float
from cli.errors import ErrorMsg, SuccessMsg, InfoMsg
from core.services.order_service import (
    get_active_orders, get_order_by_id, update_order_status,
    process_order, ready_order, cancel_order,
    STATUS_PENDING, STATUS_PROCESSING, STATUS_READY, STATUS_COMPLETED
)
from core.services.transaksi_service import finalize_order
from core.services.invoice_service import generate_invoice_text
from core.utils import format_rupiah


def show_order_menu():
    """Menampilkan menu pesanan."""
    while True:
        clear_screen()
        print_header("MANAJEMEN PESANAN")
        
        # Show summary of active orders
        active_orders = get_active_orders()
        pending = len([o for o in active_orders if o.get("status") == STATUS_PENDING])
        processing = len([o for o in active_orders if o.get("status") == STATUS_PROCESSING])
        ready = len([o for o in active_orders if o.get("status") == STATUS_READY])
        
        print(f"Status: {Colors.RED}{pending} Pending{Colors.RESET} | "
              f"{Colors.YELLOW}{processing} Processing{Colors.RESET} | "
              f"{Colors.GREEN}{ready} Ready{Colors.RESET}")
        print_divider()
        
        print("1. Lihat Pesanan Aktif")
        print("2. Cari Pesanan (ID)")
        print("0. Kembali")
        
        choice = input_styled("\nPilihan: ")
        
        if choice == "0":
            break
        elif choice == "1":
            list_active_orders()
        elif choice == "2":
            find_order()
        else:
            print_error(ErrorMsg.INVALID_CHOICE)


def list_active_orders():
    """Menampilkan list order aktif."""
    clear_screen()
    print_header("DAFTAR PESANAN AKTIF")
    
    orders = get_active_orders()
    if not orders:
        print_info(ErrorMsg.ORDER_EMPTY)
        input("Tekan Enter...")
        return
        
    # Sort by time desc
    orders.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    for i, o in enumerate(orders, 1):
        status = o.get("status").upper()
        color = Colors.WHITE
        if status == "PENDING": color = Colors.RED
        elif status == "PROCESSING": color = Colors.YELLOW
        elif status == "READY": color = Colors.GREEN
            
        print(f"{i}. {o.get('order_id')} [{color}{status}{Colors.RESET}]")
        print(f"   Pembeli: {o.get('nama_pembeli')} ({o.get('wa_pembeli')})")
        print(f"   Total  : Rp {format_rupiah(o.get('total', 0))} | Source: {o.get('source')}")
        print_divider("-", 40)
        
    try:
        choice = input_int("\nPilih nomor untuk detail (0 kembali): ", min_val=0, max_val=len(orders))
        if choice > 0:
            detail_order(orders[choice-1].get("order_id"))
    except:
        pass


def find_order():
    """Mencari order by ID."""
    order_id = input_styled("Masukkan ID Order: ")
    order = get_order_by_id(order_id)
    if order:
        detail_order(order_id)
    else:
        print_error(ErrorMsg.ORDER_NOT_FOUND.format(order_id=order_id))
        input("Tekan Enter...")


def detail_order(order_id: str):
    """Menampilkan detail order dan menu aksi."""
    while True:
        clear_screen()
        order = get_order_by_id(order_id)
        if not order:
            print_error(ErrorMsg.ORDER_CORRUPTED)
            break
            
        print_header(f"DETAIL ORDER: {order_id}")
        
        # Print Invoice View
        print(generate_invoice_text(order, format_type="cli"))
        
        status = order.get("status")
        print(f"\nStatus Saat Ini: {Colors.BOLD}{status.upper()}{Colors.RESET}")
        print_divider()
        
        # Actions based on status
        valid_actions = ["0"]
        print("Aksi:")
        
        if status == STATUS_PENDING:
            print("1. PROSES Pesanan (Set Processing)")
            print("2. BATALKAN Pesanan")
            valid_actions.extend(["1", "2"])
            
        elif status == STATUS_PROCESSING:
            print("1. SIAP DIHUBUNGI/DIAMBIL (Set Ready)")
            print("2. BATALKAN Pesanan")
            valid_actions.extend(["1", "2"])
            
        elif status == STATUS_READY:
            print("1. SELESAIKAN ORDER (Finalize & Save)")
            print("2. Kembalikan ke Processing")
            valid_actions.extend(["1", "2"])
            
        print("0. Kembali")
        
        choice = input_styled("\nPilihan: ")
        
        if choice == "0":
            break
            
        if choice not in valid_actions:
            print_error(ErrorMsg.INVALID_CHOICE)
            continue
            
        # Execute Action
        if status == STATUS_PENDING:
            if choice == "1":
                process_order(order_id)
                print_success("Status diubah ke PROCESSING.")
            elif choice == "2":
                if input_yes_no("Yakin batalkan order?"):
                    cancel_order(order_id)
                    print_success(SuccessMsg.ORDER_CANCELLED)
                    break
                    
        elif status == STATUS_PROCESSING:
            if choice == "1":
                ready_order(order_id)
                print_success("Status diubah ke READY.")
            elif choice == "2":
                cancel_order(order_id)
                print_success(SuccessMsg.ORDER_CANCELLED)
                break
                
        elif status == STATUS_READY:
            if choice == "1":
                # Finalize
                print("\nMenyelesaikan pesanan...")
                trx_id, _ = finalize_order(order_id, generate_invoice=False)
                if trx_id:
                    print_success(SuccessMsg.TRANSACTION_SUCCESS.format(trx_id=trx_id))
                    break
                else:
                    print_error(ErrorMsg.ORDER_FINALIZE_FAILED.format(error="Unknown error"))
            elif choice == "2":
                process_order(order_id) # back to processing
                print_success("Status kembali ke PROCESSING.")
                
        input("Tekan Enter untuk lanjut...")
