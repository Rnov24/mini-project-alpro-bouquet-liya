"""
Unified Order Service - Modul Manajemen Pesanan.

Modul ini berisi business logic inti untuk manajemen order/pesanan.
Digunakan bersama oleh aplikasi CLI dan Telegram Bot.

Alur status order:
    1. PENDING → Order baru masuk, menunggu diproses admin
    2. PROCESSING → Admin sedang memproduksi buket
    3. READY → Buket siap, admin sudah set ongkir/diskon
    4. COMPLETED → Pembayaran diterima, order selesai
    5. CANCELLED → Order dibatalkan

Functions:
    create_order: Buat order baru dari data mentah
    create_order_from_cart: Buat order dari objek Cart
    get_order_by_id: Ambil order berdasarkan ID
    get_orders_by_status: Filter orders berdasarkan status
    update_order_status: Update status order
    delete_order: Hapus order dari storage
"""
import json
import os
import random
import string
from datetime import datetime
from typing import Optional, Any, Callable

from core.config import DATA_DIR
from core.models.cart import Cart, CartItem

ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")

# Order statuses
STATUS_PENDING = "pending"        # ⏳ Order baru, belum diproses
STATUS_PROCESSING = "processing"  # 🔨 Sedang diproduksi
STATUS_READY = "ready"            # 📦 Siap, menunggu pembayaran
STATUS_COMPLETED = "completed"    # ✅ Selesai
STATUS_CANCELLED = "cancelled"    # 🚫 Dibatalkan


def generate_order_id() -> str:
    """Menghasilkan ID order unik dengan format standar.
    
    Format: ORD-YYYYMMDD-XXXX dimana XXXX adalah 4 karakter acak.
    ID ini digunakan sebagai primary key untuk identifikasi pesanan.
    
    Returns:
        String berisi order ID, contoh: "ORD-20260113-AB12"
    """
    now = datetime.now()
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"ORD-{now.strftime('%Y%m%d')}-{random_suffix}"


def generate_transaction_id() -> str:
    """Generate unique transaction ID: LIY-YYYYMMDDHHMMSS."""
    return datetime.now().strftime("LIY%Y%m%d%H%M%S")


# ═══════════════════════════════════════════════════════════════
# ORDER DATA PERSISTENCE
# ═══════════════════════════════════════════════════════════════

def load_orders_raw() -> list[dict]:
    """Memuat semua orders dari file JSON sebagai list dictionary.
    
    Returns:
        List dictionary order dari orders.json.
    """
    if not os.path.exists(ORDERS_FILE):
        return []
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_orders_raw(orders: list[dict]) -> None:
    """Menyimpan list dictionary order ke file JSON.
    
    Args:
        orders: List dictionary order yang akan disimpan.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════
# ORDER CRUD OPERATIONS
# ═══════════════════════════════════════════════════════════════

def create_order_from_cart(
    cart: Cart,
    source: str = "cli",  # "cli" or "telegram"
    telegram_id: Optional[int] = None,
    notes: str = ""
) -> dict:
    """
    Create new order from Cart object.
    
    Args:
        cart: Cart object with items and buyer info
        source: "cli" or "telegram"
        telegram_id: Telegram user ID (for telegram orders)
        notes: Additional notes
    
    Returns:
        Order dict with generated ID and status
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    order_id = generate_order_id()
    
    # Convert cart items to dicts
    items = [item.to_dict() for item in cart.items]
    
    order = {
        "order_id": order_id,
        "source": source,
        "telegram_id": telegram_id,
        "nama_pembeli": cart.nama_pembeli,
        "wa_pembeli": cart.wa_pembeli,
        "alamat": cart.alamat,
        "delivery": cart.delivery_type,
        "ongkir": cart.ongkir,
        "items": items,
        "subtotal": cart.subtotal,
        "diskon_persen": cart.diskon_persen,
        "diskon": cart.diskon,
        "total": cart.total,
        "status": STATUS_PENDING,
        "created_at": now,
        "updated_at": now,
        "tanggal_pengambilan": cart.tanggal_pengambilan,
        "notes": notes,
    }
    
    # Save to file
    orders = load_orders_raw()
    orders.append(order)
    save_orders_raw(orders)
    
    return order


def create_order(
    items: list[dict],
    nama_pembeli: str,
    wa_pembeli: str = "",
    alamat: str = "",
    delivery: str = "ambil",
    ongkir: float = 0,
    diskon: float = 0,
    source: str = "cli",
    telegram_id: Optional[int] = None,
    tanggal_pengambilan: str = "",
    notes: str = ""
) -> dict:
    """
    Create new order from raw data.
    
    Args:
        items: List of item dicts
        nama_pembeli: Buyer name
        ... other params
    
    Returns:
        Order dict with generated ID
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    order_id = generate_order_id()
    
    subtotal = sum(item.get("subtotal", 0) for item in items)
    total = subtotal - diskon + ongkir
    
    order = {
        "order_id": order_id,
        "source": source,
        "telegram_id": telegram_id,
        "nama_pembeli": nama_pembeli,
        "wa_pembeli": wa_pembeli,
        "alamat": alamat,
        "delivery": delivery,
        "ongkir": ongkir,
        "items": items,
        "subtotal": subtotal,
        "diskon": diskon,
        "total": total,
        "status": STATUS_PENDING,
        "created_at": now,
        "updated_at": now,
        "tanggal_pengambilan": tanggal_pengambilan,
        "notes": notes,
    }
    
    orders = load_orders_raw()
    orders.append(order)
    save_orders_raw(orders)
    
    return order


def get_order_by_id(order_id: str) -> Optional[dict]:
    """Mengambil order berdasarkan ID.
    
    Args:
        order_id: ID order yang dicari.
    
    Returns:
        Dictionary order jika ditemukan, None jika tidak.
    """
    orders = load_orders_raw()
    for order in orders:
        if order.get("order_id") == order_id:
            return order
    return None


def get_orders_by_status(status: str) -> list[dict]:
    """Get all orders with specific status."""
    orders = load_orders_raw()
    return [o for o in orders if o.get("status") == status]


def get_orders_by_telegram_id(telegram_id: int) -> list[dict]:
    """Get all orders for a telegram user."""
    orders = load_orders_raw()
    return [o for o in orders if o.get("telegram_id") == telegram_id]


def get_active_orders() -> list[dict]:
    """Get all active orders (not completed/cancelled)."""
    orders = load_orders_raw()
    return [o for o in orders if o.get("status") in [STATUS_PENDING, STATUS_PROCESSING, STATUS_READY]]


def update_order_status(order_id: str, new_status: str) -> Optional[dict]:
    """Mengupdate status order.
    
    Fungsi ini akan mengubah status order dan memperbarui timestamp.
    
    Args:
        order_id: ID order yang akan diupdate.
        new_status: Status baru (pending/processing/ready/completed/cancelled).
    
    Returns:
        Dictionary order yang sudah diupdate, None jika tidak ditemukan.
    """
    orders = load_orders_raw()
    for order in orders:
        if order.get("order_id") == order_id:
            order["status"] = new_status
            order["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_orders_raw(orders)
            return order
    return None


def process_order(order_id: str) -> Optional[dict]:
    """Set order to processing status."""
    return update_order_status(order_id, STATUS_PROCESSING)


def ready_order(order_id: str) -> Optional[dict]:
    """Set order to ready status."""
    return update_order_status(order_id, STATUS_READY)


def complete_order(order_id: str) -> Optional[dict]:
    """Set order to completed status."""
    return update_order_status(order_id, STATUS_COMPLETED)


def cancel_order(order_id: str) -> Optional[dict]:
    """Cancel order."""
    return update_order_status(order_id, STATUS_CANCELLED)


def delete_order(order_id: str) -> bool:
    """Menghapus order dari storage.
    
    Biasanya dipanggil setelah order difinalisasi ke transaksi CSV
    atau setelah order dibatalkan.
    
    Args:
        order_id: ID order yang akan dihapus.
    
    Returns:
        True jika berhasil dihapus, False jika tidak ditemukan.
    """
    orders = load_orders_raw()
    original_len = len(orders)
    orders = [o for o in orders if o.get("order_id") != order_id]
    if len(orders) < original_len:
        save_orders_raw(orders)
        return True
    return False


# ═══════════════════════════════════════════════════════════════
# STOCK MANAGEMENT
# ═══════════════════════════════════════════════════════════════

def reduce_stock_for_order(order: dict, barang_list: list) -> None:
    """
    Reduce stock for items in order.
    barang_list should be list of barang dicts from katalog.
    """
    for item in order.get("items", []):
        kode = item.get("kode")
        ukuran_nama = item.get("ukuran")
        qty = item.get("qty", 0)
        
        for barang in barang_list:
            if barang.get("kode") == kode:
                for ukuran in barang.get("ukuran", []):
                    if ukuran.get("nama") == ukuran_nama:
                        ukuran["stok"] = max(0, ukuran.get("stok", 0) - qty)
                        break
                break


def restore_stock_for_order(order: dict, barang_list: list) -> None:
    """
    Restore stock for cancelled order.
    """
    for item in order.get("items", []):
        kode = item.get("kode")
        ukuran_nama = item.get("ukuran")
        qty = item.get("qty", 0)
        
        for barang in barang_list:
            if barang.get("kode") == kode:
                for ukuran in barang.get("ukuran", []):
                    if ukuran.get("nama") == ukuran_nama:
                        ukuran["stok"] = ukuran.get("stok", 0) + qty
                        break
                break


# ═══════════════════════════════════════════════════════════════
# PRICING UTILITIES
# ═══════════════════════════════════════════════════════════════

def calculate_discount(subtotal: float, persen: float) -> float:
    """Calculate discount from percentage."""
    if persen < 0:
        persen = 0
    if persen > 100:
        persen = 100
    return subtotal * (persen / 100)


def calculate_order_total(
    items: list[dict],
    diskon_persen: float = 0,
    ongkir: float = 0
) -> tuple[float, float, float]:
    """
    Calculate order totals.
    Returns: (subtotal, diskon, total)
    """
    subtotal = sum(item.get("subtotal", 0) for item in items)
    diskon = calculate_discount(subtotal, diskon_persen)
    total = subtotal - diskon + ongkir
    return subtotal, diskon, total
