"""
Inline keyboards untuk Admin Bot.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def menu_utama():
    """Keyboard menu utama admin."""
    keyboard = [
        [InlineKeyboardButton("📦 Kelola Katalog", callback_data="katalog")],
        [InlineKeyboardButton("📊 Rekap Pendapatan", callback_data="rekap")],
        [InlineKeyboardButton("📝 Pesanan Masuk", callback_data="pesanan")],
        [InlineKeyboardButton("📜 Riwayat Transaksi", callback_data="riwayat")],
        [InlineKeyboardButton("📤 Export Data", callback_data="export")],
    ]
    return InlineKeyboardMarkup(keyboard)


def menu_katalog():
    """Keyboard menu kelola katalog."""
    keyboard = [
        [InlineKeyboardButton("👁️ Lihat Semua", callback_data="kat_lihat")],
        [InlineKeyboardButton("➕ Tambah Baru", callback_data="kat_tambah")],
        [InlineKeyboardButton("✏️ Edit Produk", callback_data="kat_edit")],
        [InlineKeyboardButton("🗑️ Hapus Produk", callback_data="kat_hapus")],
        [InlineKeyboardButton("📈 Update Stok", callback_data="kat_stok")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_produk_list(barang_list, action="lihat", page=0, per_page=8):
    """Keyboard list produk untuk aksi tertentu."""
    start = page * per_page
    end = start + per_page
    page_items = barang_list[start:end]
    total_pages = (len(barang_list) + per_page - 1) // per_page
    
    keyboard = []
    for barang in page_items:
        label = f"{barang['kode']} - {barang['nama']}"
        keyboard.append([InlineKeyboardButton(label, callback_data=f"{action}_{barang['kode']}")])
    
    # Pagination
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("◀️", callback_data=f"paging_{action}_{page-1}"))
    if total_pages > 1:
        nav_row.append(InlineKeyboardButton(f"{page+1}/{total_pages}", callback_data="noop"))
    if end < len(barang_list):
        nav_row.append(InlineKeyboardButton("▶️", callback_data=f"paging_{action}_{page+1}"))
    
    if nav_row:
        keyboard.append(nav_row)
    
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data="katalog")])
    return InlineKeyboardMarkup(keyboard)


def keyboard_ukuran_stok(barang):
    """Keyboard pilih ukuran untuk update stok."""
    keyboard = []
    for ukuran in barang["ukuran"]:
        label = f"{ukuran['nama']} (Stok: {ukuran['stok']})"
        keyboard.append([InlineKeyboardButton(label, callback_data=f"stok_ukuran_{ukuran['nama']}")])
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data="kat_stok")])
    return InlineKeyboardMarkup(keyboard)


def keyboard_konfirmasi_hapus(kode):
    """Keyboard konfirmasi hapus produk."""
    keyboard = [
        [
            InlineKeyboardButton("✅ Ya, Hapus", callback_data=f"hapus_konfirm_{kode}"),
            InlineKeyboardButton("❌ Batal", callback_data="katalog"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_rekap_periode():
    """Keyboard pilih periode rekap."""
    keyboard = [
        [
            InlineKeyboardButton("📅 Hari Ini", callback_data="rekap_hari"),
            InlineKeyboardButton("📆 Minggu Ini", callback_data="rekap_minggu"),
        ],
        [
            InlineKeyboardButton("📅 Bulan Ini", callback_data="rekap_bulan"),
            InlineKeyboardButton("📊 Semua", callback_data="rekap_semua"),
        ],
        [InlineKeyboardButton("🔙 Kembali", callback_data="menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_kembali(to="menu"):
    """Keyboard kembali."""
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data=to)],
    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_export():
    """Keyboard export options."""
    keyboard = [
        [InlineKeyboardButton("📊 Export Transaksi (CSV)", callback_data="export_transaksi")],
        [InlineKeyboardButton("📦 Export Katalog (JSON)", callback_data="export_katalog")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_pending_orders(orders):
    """Keyboard list pending orders."""
    keyboard = []
    for order in orders[:10]:  # Max 10
        label = f"⏳ {order.get('order_id', '')[:18]} - Rp {order.get('total', 0):,.0f}"
        keyboard.append([InlineKeyboardButton(label, callback_data=f"ord_{order.get('order_id', '')}")])
    
    if not orders:
        keyboard.append([InlineKeyboardButton("📭 Tidak ada pesanan aktif", callback_data="noop")])
    
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data="menu")])
    return InlineKeyboardMarkup(keyboard)


def keyboard_order_action(order):
    """Keyboard aksi order berdasarkan status."""
    keyboard = []
    
    status = order.get("status", "")
    order_id = order.get("order_id", "")
    
    if status == "pending":
        # Order baru: bisa mulai proses atau batalkan
        keyboard.append([InlineKeyboardButton("🔨 Mulai Proses", callback_data=f"process_{order_id}")])
        keyboard.append([InlineKeyboardButton("🚫 Batalkan", callback_data=f"admincancel_{order_id}")])
    elif status == "processing":
        # Sedang produksi: tandai siap (minta bayar)
        keyboard.append([InlineKeyboardButton("📦 Siap - Minta Bayar", callback_data=f"ready_{order_id}")])
        keyboard.append([InlineKeyboardButton("🚫 Batalkan", callback_data=f"admincancel_{order_id}")])
    elif status == "ready":
        # Siap, menunggu bayar: close order (bayar dikonfirmasi)
        keyboard.append([InlineKeyboardButton("✅ Konfirmasi Bayar & Close", callback_data=f"close_{order_id}")])
        keyboard.append([InlineKeyboardButton("🚫 Batalkan", callback_data=f"admincancel_{order_id}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data="pesanan")])
    return InlineKeyboardMarkup(keyboard)


def keyboard_order_status_filter():
    """Keyboard filter status order untuk riwayat."""
    keyboard = [
        [
            InlineKeyboardButton("⏳ Pending", callback_data="hist_pending"),
            InlineKeyboardButton("🔨 Processing", callback_data="hist_processing"),
        ],
        [
            InlineKeyboardButton("📦 Ready", callback_data="hist_ready"),
            InlineKeyboardButton("✅ Selesai", callback_data="hist_completed"),
        ],
        [
            InlineKeyboardButton("🚫 Cancelled", callback_data="hist_cancelled"),
            InlineKeyboardButton("📋 Semua (Aktif)", callback_data="hist_all"),
        ],
        [InlineKeyboardButton("🔙 Kembali", callback_data="menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


