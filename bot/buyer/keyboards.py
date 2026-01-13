"""
Inline keyboards untuk Buyer Bot.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Emoji mapping untuk warna
WARNA_EMOJI = {
    "hitam": "⬛",
    "ungu": "🟣",
    "pink": "💗",
    "biru": "💙",
    "coklat": "🟤",
    "merah": "❤️",
    "putih": "🤍",
    "kuning": "💛",
    "tanpa bunga": "🚫",
}

# Kategori buket
KATEGORI_BUKET = {
    "boneka": {"emoji": "🎀", "nama": "Buket Boneka & Bunga", "kode": ["A1", "A2", "A3"]},
    "foto": {"emoji": "📸", "nama": "Buket Foto", "kode": ["B1", "B2"]},
    "uang": {"emoji": "💵", "nama": "Buket Uang", "kode": ["C1", "C2"]},
    "snack": {"emoji": "🍫", "nama": "Buket Snack", "kode": ["D1"]},
    "spesial": {"emoji": "🦋", "nama": "Buket Spesial", "kode": ["E1", "E2", "F1", "F2", "G1"]},
    "wisuda": {"emoji": "🎓", "nama": "Buket Wisuda & Seasonal", "kode": ["H1", "H2"]},
}


def menu_utama():
    """Keyboard menu utama buyer."""
    keyboard = [
        [InlineKeyboardButton("📖 Lihat Katalog", callback_data="katalog")],
        [InlineKeyboardButton("🛒 Pesan Sekarang", callback_data="pesan")],
        [InlineKeyboardButton("📦 Cek Status Pesanan", callback_data="cek_pesanan")],
        [InlineKeyboardButton("📍 Lokasi Toko", callback_data="lokasi")],
        [InlineKeyboardButton("📞 Hubungi Admin", callback_data="kontak")],
    ]
    return InlineKeyboardMarkup(keyboard)


def menu_kategori():
    """Keyboard pilih kategori buket."""
    keyboard = []
    for key, val in KATEGORI_BUKET.items():
        keyboard.append([
            InlineKeyboardButton(f"{val['emoji']} {val['nama']}", callback_data=f"kat_{key}")
        ])
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data="menu")])
    return InlineKeyboardMarkup(keyboard)


def keyboard_produk(barang_list, kategori=None, page=0, per_page=5):
    """Keyboard list produk dengan pagination."""
    # Filter by kategori if specified
    if kategori and kategori in KATEGORI_BUKET:
        kode_list = KATEGORI_BUKET[kategori]["kode"]
        barang_list = [b for b in barang_list if b["kode"] in kode_list]
    
    # Pagination
    start = page * per_page
    end = start + per_page
    page_items = barang_list[start:end]
    total_pages = (len(barang_list) + per_page - 1) // per_page
    
    keyboard = []
    for barang in page_items:
        harga_min = min(u["harga"] for u in barang["ukuran"])
        harga_max = max(u["harga"] for u in barang["ukuran"])
        label = f"{barang['kode']} - {barang['nama']} (Rp {harga_min:,} - {harga_max:,})"
        keyboard.append([InlineKeyboardButton(label, callback_data=f"lihat_{barang['kode']}")])
    
    # Pagination buttons
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("◀️ Prev", callback_data=f"page_{kategori}_{page-1}"))
    nav_row.append(InlineKeyboardButton(f"{page+1}/{total_pages}", callback_data="noop"))
    if end < len(barang_list):
        nav_row.append(InlineKeyboardButton("Next ▶️", callback_data=f"page_{kategori}_{page+1}"))
    
    if nav_row:
        keyboard.append(nav_row)
    
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data="katalog")])
    return InlineKeyboardMarkup(keyboard)


def keyboard_detail_produk(kode):
    """Keyboard untuk detail produk."""
    keyboard = [
        [InlineKeyboardButton("🛒 Pesan Ini", callback_data=f"order_{kode}")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="back_katalog")],
    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_ukuran(barang):
    """Keyboard pilih ukuran."""
    keyboard = []
    for ukuran in barang["ukuran"]:
        stok_status = "✅" if ukuran["stok"] > 0 else "❌"
        label = f"{ukuran['nama']} - Rp {ukuran['harga']:,} {stok_status} Stok: {ukuran['stok']}"
        keyboard.append([InlineKeyboardButton(label, callback_data=f"ukuran_{ukuran['nama']}")])
    keyboard.append([InlineKeyboardButton("❌ Batalkan", callback_data="batal_order")])
    return InlineKeyboardMarkup(keyboard)


def keyboard_warna(warna_list, tipe="kertas"):
    """Keyboard pilih warna (kertas/bunga)."""
    keyboard = []
    row = []
    for warna in warna_list:
        emoji = WARNA_EMOJI.get(warna.lower(), "🎨")
        row.append(InlineKeyboardButton(f"{emoji} {warna.title()}", callback_data=f"{tipe}_{warna}"))
        if len(row) >= 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("❌ Batalkan", callback_data="batal_order")])
    return InlineKeyboardMarkup(keyboard)


def keyboard_konfirmasi_item():
    """Keyboard konfirmasi item."""
    keyboard = [
        [
            InlineKeyboardButton("➕ Tambah Lagi", callback_data="tambah_lagi"),
            InlineKeyboardButton("✅ Checkout", callback_data="checkout"),
        ],
        [InlineKeyboardButton("❌ Batalkan", callback_data="batal_order")],
    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_pengiriman():
    """Keyboard pilih metode pengiriman."""
    keyboard = [
        [InlineKeyboardButton("🏠 Ambil di Toko (Gratis)", callback_data="kirim_ambil")],
        [InlineKeyboardButton("🛵 Delivery COD (+Rp 10.000)", callback_data="kirim_delivery")],
        [InlineKeyboardButton("❌ Batalkan", callback_data="batal_order")],
    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_kembali_menu():
    """Keyboard kembali ke menu utama."""
    keyboard = [
        [InlineKeyboardButton("🏠 Kembali ke Menu", callback_data="menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_pesanan_list(orders):
    """Keyboard list pesanan user."""
    keyboard = []
    for order in orders[:10]:  # Max 10 orders
        status_emoji = {
            "pending": "⏳",
            "confirmed": "✅",
            "completed": "🎉",
            "rejected": "❌",
            "cancelled": "🚫",
        }.get(order.status, "📦")
        label = f"{status_emoji} {order.order_id[:20]} - Rp {order.total:,.0f}"
        keyboard.append([InlineKeyboardButton(label, callback_data=f"pesanan_{order.order_id}")])
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data="menu")])
    return InlineKeyboardMarkup(keyboard)


def keyboard_pesanan_detail(order):
    """Keyboard untuk detail pesanan."""
    keyboard = []
    if order.status == "pending":
        keyboard.append([InlineKeyboardButton("🚫 Batalkan Pesanan", callback_data=f"cancel_{order.order_id}")])
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data="pesanan_saya")])
    return InlineKeyboardMarkup(keyboard)

