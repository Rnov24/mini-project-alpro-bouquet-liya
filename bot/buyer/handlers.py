"""
Handlers untuk Buyer Bot.
"""
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

from bot.shared.sessions import buyer_sessions, init_buyer_session
from bot.shared.errors import safe_handler, safe_callback, validate_quantity, validate_phone, log_error
from .keyboards import (
    menu_utama, menu_kategori, keyboard_produk, keyboard_detail_produk,
    keyboard_ukuran, keyboard_warna, keyboard_konfirmasi_item,
    keyboard_pengiriman, keyboard_kembali_menu, KATEGORI_BUKET,
    keyboard_pesanan_list, keyboard_pesanan_detail
)
from .states import *
from core.services.barang_service import load_barang_dict
from core.services.order_service import (
    create_order, get_orders_by_telegram_id, get_order_by_id,
    cancel_order, delete_order, STATUS_PENDING
)
from core.models.order import OrderItem
from core.services.invoice_service import generate_invoice_text, format_order_receipt
from bot.shared.notifications import notify_admins_new_order


@safe_handler("buyer_start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler /start command."""
    chat_id = update.effective_chat.id
    init_buyer_session(chat_id)
    buyer_sessions[chat_id]["state"] = STATE_MENU

    welcome_msg = """🌸 *Selamat Datang di Buqeuet Liya!*

Hadiah buket cantik untuk orang tersayang ✨

Pilih menu di bawah ini:"""

    await update.message.reply_text(
        welcome_msg,
        reply_markup=menu_utama(),
        parse_mode="Markdown"
    )


@safe_callback("buyer_callback_router")
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Router untuk semua callback query."""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat.id
    data = query.data
    
    # Init session if not exists
    if chat_id not in buyer_sessions:
        init_buyer_session(chat_id)
    
    session = buyer_sessions[chat_id]

    # ===== MENU UTAMA =====
    if data == "menu":
        session["state"] = STATE_MENU
        await query.edit_message_text(
            "🌸 *Selamat Datang di Buqeuet Liya!*\n\nHadiah buket cantik untuk orang tersayang ✨\n\nPilih menu di bawah ini:",
            reply_markup=menu_utama(),
            parse_mode="Markdown"
        )

    # ===== KATALOG =====
    elif data == "katalog":
        session["state"] = STATE_KATEGORI
        await query.edit_message_text(
            "📂 *Pilih Kategori Buket*\n\nKami menyediakan berbagai jenis buket cantik untuk setiap momen spesial Anda!",
            reply_markup=menu_kategori(),
            parse_mode="Markdown"
        )

    # ===== PILIH KATEGORI =====
    elif data.startswith("kat_"):
        kategori = data.replace("kat_", "")
        session["state"] = STATE_BROWSE_KATALOG
        session["kategori_aktif"] = kategori
        
        barang_list = load_barang_dict()
        kat_info = KATEGORI_BUKET.get(kategori, {})
        
        await query.edit_message_text(
            f"{kat_info.get('emoji', '📦')} *{kat_info.get('nama', 'Katalog')}*\n\nPilih produk untuk melihat detail:",
            reply_markup=keyboard_produk(barang_list, kategori, page=0),
            parse_mode="Markdown"
        )

    # ===== PAGINATION =====
    elif data.startswith("page_"):
        parts = data.split("_")
        kategori = parts[1] if parts[1] != "None" else None
        page = int(parts[2])
        
        barang_list = load_barang_dict()
        await query.edit_message_text(
            "📦 *Katalog Produk*\n\nPilih produk untuk melihat detail:",
            reply_markup=keyboard_produk(barang_list, kategori, page=page),
            parse_mode="Markdown"
        )

    # ===== LIHAT DETAIL PRODUK =====
    elif data.startswith("lihat_"):
        kode = data.replace("lihat_", "")
        barang_list = load_barang_dict()
        barang = next((b for b in barang_list if b["kode"] == kode), None)
        
        if barang:
            session["barang_dilihat"] = kode
            
            # Format harga
            harga_min = min(u["harga"] for u in barang["ukuran"])
            harga_max = max(u["harga"] for u in barang["ukuran"])
            
            # Format ukuran
            ukuran_str = " | ".join(u["nama"] for u in barang["ukuran"])
            
            # Format warna
            kertas_str = ", ".join(barang["warna_kertas"][:3]) + ("..." if len(barang["warna_kertas"]) > 3 else "")
            bunga_str = ", ".join(barang["warna_bunga"][:3]) + ("..." if len(barang["warna_bunga"]) > 3 else "")
            
            detail_msg = f"""🎀 *{barang['nama']}* (`{barang['kode']}`)
━━━━━━━━━━━━━━━━━━━━
💰 *Harga:* Rp {harga_min:,} - Rp {harga_max:,}
📏 *Ukuran:* {ukuran_str}
🎨 *Kertas:* {kertas_str}
🌸 *Bunga:* {bunga_str}
━━━━━━━━━━━━━━━━━━━━"""
            
            await query.edit_message_text(
                detail_msg,
                reply_markup=keyboard_detail_produk(kode),
                parse_mode="Markdown"
            )

    elif data == "back_katalog":
        kategori = session.get("kategori_aktif")
        barang_list = load_barang_dict()
        await query.edit_message_text(
            "📦 *Katalog Produk*\n\nPilih produk untuk melihat detail:",
            reply_markup=keyboard_produk(barang_list, kategori, page=0),
            parse_mode="Markdown"
        )

    # ===== MULAI ORDER =====
    elif data == "pesan" or data.startswith("order_"):
        session["state"] = STATE_PILIH_BARANG
        session["keranjang"] = []
        
        if data.startswith("order_"):
            # Order dari detail produk
            kode = data.replace("order_", "")
            session["barang_aktif"] = kode
            session["state"] = STATE_PILIH_UKURAN
            
            barang_list = load_barang_dict()
            barang = next((b for b in barang_list if b["kode"] == kode), None)
            
            if barang:
                await query.edit_message_text(
                    f"📏 *Pilih Ukuran untuk {barang['nama']}*",
                    reply_markup=keyboard_ukuran(barang),
                    parse_mode="Markdown"
                )
        else:
            # Order dari menu utama
            barang_list = load_barang_dict()
            await query.edit_message_text(
                "📦 *Pilih Produk untuk Dipesan*",
                reply_markup=keyboard_produk(barang_list, page=0),
                parse_mode="Markdown"
            )

    # ===== PILIH UKURAN =====
    elif data.startswith("ukuran_"):
        ukuran = data.replace("ukuran_", "")
        session["ukuran_aktif"] = ukuran
        session["state"] = STATE_PILIH_WARNA_KERTAS
        
        kode = session.get("barang_aktif")
        barang_list = load_barang_dict()
        barang = next((b for b in barang_list if b["kode"] == kode), None)
        
        if barang:
            await query.edit_message_text(
                "🎨 *Pilih Warna Kertas*",
                reply_markup=keyboard_warna(barang["warna_kertas"], "kertas"),
                parse_mode="Markdown"
            )

    # ===== PILIH WARNA KERTAS =====
    elif data.startswith("kertas_"):
        warna = data.replace("kertas_", "")
        session["warna_kertas_aktif"] = warna
        session["state"] = STATE_PILIH_WARNA_BUNGA
        
        kode = session.get("barang_aktif")
        barang_list = load_barang_dict()
        barang = next((b for b in barang_list if b["kode"] == kode), None)
        
        if barang:
            await query.edit_message_text(
                "🌸 *Pilih Warna Bunga*",
                reply_markup=keyboard_warna(barang["warna_bunga"], "bunga"),
                parse_mode="Markdown"
            )

    # ===== PILIH WARNA BUNGA =====
    elif data.startswith("bunga_"):
        warna = data.replace("bunga_", "")
        session["warna_bunga_aktif"] = warna
        session["state"] = STATE_INPUT_QTY
        
        kode = session.get("barang_aktif")
        barang_list = load_barang_dict()
        barang = next((b for b in barang_list if b["kode"] == kode), None)
        ukuran_data = next((u for u in barang["ukuran"] if u["nama"] == session["ukuran_aktif"]), None)
        
        stok = ukuran_data["stok"] if ukuran_data else 0
        
        await query.edit_message_text(
            f"🔢 *Masukkan Jumlah Pesanan*\n\nKetik angka (contoh: 2)\nStok tersedia: {stok}",
            parse_mode="Markdown"
        )

    # ===== KONFIRMASI ITEM =====
    elif data == "tambah_lagi":
        session["state"] = STATE_PILIH_BARANG
        barang_list = load_barang_dict()
        await query.edit_message_text(
            "📦 *Pilih Produk untuk Dipesan*",
            reply_markup=keyboard_produk(barang_list, page=0),
            parse_mode="Markdown"
        )

    elif data == "checkout":
        session["state"] = STATE_INPUT_NAMA
        await query.edit_message_text(
            "📋 *Data Pemesan*\n\nKetik nama lengkap Anda:",
            parse_mode="Markdown"
        )

    # ===== PENGIRIMAN =====
    elif data == "kirim_ambil":
        session["delivery"] = "ambil"
        session["ongkir"] = 0
        await finalize_order(query, session, query.from_user.id)

    elif data == "kirim_delivery":
        session["delivery"] = "delivery"
        session["ongkir"] = 0  # Ongkir akan ditentukan admin saat finalisasi
        session["state"] = STATE_INPUT_LOKASI
        await query.edit_message_text(
            "📍 *Lokasi Pengiriman*\n\n👇 Kirim lokasi Anda menggunakan fitur *Share Location* Telegram:\n\n1. Klik ikon 📎 (lampiran)\n2. Pilih *Location*\n3. Pilih *Send My Current Location* atau pilih lokasi di peta",
            parse_mode="Markdown"
        )

    # ===== BATAL =====
    elif data == "batal_order":
        session["keranjang"] = []
        session["state"] = STATE_MENU
        await query.edit_message_text(
            "❌ *Pesanan dibatalkan*\n\nKembali ke menu utama.",
            reply_markup=menu_utama(),
            parse_mode="Markdown"
        )

    # ===== PESANAN SAYA =====
    elif data == "pesanan_saya":
        telegram_id = query.from_user.id
        orders = get_orders_by_telegram_id(telegram_id)
        
        if not orders:
            await query.edit_message_text(
                "📦 *Pesanan Saya*\n\nAnda belum memiliki pesanan.",
                reply_markup=keyboard_kembali_menu(),
                parse_mode="Markdown"
            )
        else:
            # Sort by created_at desc
            orders.sort(key=lambda x: x.created_at, reverse=True)
            await query.edit_message_text(
                "📦 *Pesanan Saya*\n\nKlik pesanan untuk lihat detail:",
                reply_markup=keyboard_pesanan_list(orders),
                parse_mode="Markdown"
            )

    # ===== DETAIL PESANAN =====
    elif data.startswith("pesanan_"):
        order_id = data.replace("pesanan_", "")
        order = get_order_by_id(order_id)
        
        if order:
            receipt = format_order_receipt(order)
            await query.edit_message_text(
                receipt,
                reply_markup=keyboard_pesanan_detail(order),
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text(
                "❌ Pesanan tidak ditemukan.",
                reply_markup=keyboard_kembali_menu(),
                parse_mode="Markdown"
            )

    # ===== CANCEL PESANAN =====
    elif data.startswith("cancel_"):
        order_id = data.replace("cancel_", "")
        order = get_order_by_id(order_id)
        
        if order and order.status == STATUS_PENDING:
            # Hanya bisa cancel jika masih pending
            cancel_order(order_id)
            delete_order(order_id)
            await query.edit_message_text(
                f"🚫 *Pesanan Dibatalkan*\n\nPesanan `{order_id}` berhasil dibatalkan.",
                reply_markup=keyboard_kembali_menu(),
                parse_mode="Markdown"
            )
        elif order:
            await query.edit_message_text(
                f"❌ Pesanan `{order_id}` tidak dapat dibatalkan karena sudah diproses.",
                reply_markup=keyboard_kembali_menu(),
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text(
                "❌ Pesanan tidak ditemukan.",
                reply_markup=keyboard_kembali_menu(),
                parse_mode="Markdown"
            )

    # ===== LOKASI =====
    elif data == "lokasi":
        lokasi_msg = """📍 *Lokasi Toko Buqeuet Liya*
━━━━━━━━━━━━━━━━━━━━
🏠 Alamat: Jl. Contoh No. 123, Cirebon
⏰ Jam Buka: 09.00 - 21.00 WIB
📱 WhatsApp: 081234567890
━━━━━━━━━━━━━━━━━━━━"""
        await query.edit_message_text(
            lokasi_msg,
            reply_markup=keyboard_kembali_menu(),
            parse_mode="Markdown"
        )

    # ===== KONTAK =====
    elif data == "kontak":
        kontak_msg = """📞 *Hubungi Admin*
━━━━━━━━━━━━━━━━━━━━
📱 WhatsApp: 081234567890
📧 Email: buqeuetliya@email.com
📸 Instagram: @buqeuetliya
━━━━━━━━━━━━━━━━━━━━
Klik link di bawah untuk chat langsung:
https://wa.me/6281234567890"""
        await query.edit_message_text(
            kontak_msg,
            reply_markup=keyboard_kembali_menu(),
            parse_mode="Markdown"
        )


@safe_handler("buyer_text_handler")
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk input text dari user."""
    chat_id = update.effective_chat.id
    
    if chat_id not in buyer_sessions:
        init_buyer_session(chat_id)
        await update.message.reply_text("⏰ Sesi berakhir. Ketik /start untuk memulai lagi.")
        return
    
    session = buyer_sessions[chat_id]
    text = update.message.text.strip()

    # ===== INPUT QTY =====
    if session["state"] == STATE_INPUT_QTY:
        # Validate quantity using helper
        kode = session.get("barang_aktif")
        barang_list = load_barang_dict()
        barang = next((b for b in barang_list if b["kode"] == kode), None)
        
        if not barang:
            await update.message.reply_text("❌ Produk tidak ditemukan. Ketik /start untuk mulai lagi.")
            return
        
        ukuran_data = next((u for u in barang["ukuran"] if u["nama"] == session.get("ukuran_aktif")), None)
        
        if not ukuran_data:
            await update.message.reply_text("❌ Ukuran tidak ditemukan. Ketik /start untuk mulai lagi.")
            return
        
        is_valid, qty, error_msg = validate_quantity(text, ukuran_data["stok"])
        if not is_valid:
            await update.message.reply_text(error_msg)
            return
        
        # Simpan ke keranjang
        item = {
            "kode": kode,
            "nama": barang["nama"],
            "ukuran": session["ukuran_aktif"],
            "warna_kertas": session["warna_kertas_aktif"],
            "warna_bunga": session["warna_bunga_aktif"],
            "harga": ukuran_data["harga"],
            "hpp": ukuran_data["hpp"],
            "qty": qty,
            "subtotal": ukuran_data["harga"] * qty
        }
        session["keranjang"].append(item)
        session["state"] = STATE_KONFIRMASI_ITEM
        
        # Hitung total
        total = sum(i["subtotal"] for i in session["keranjang"])
        
        konfirmasi_msg = f"""✨ *Konfirmasi Pesanan*
━━━━━━━━━━━━━━━━━━━━
📦 {barang['nama']} ({kode})
📏 Ukuran: {session['ukuran_aktif']}
🎨 Kertas: {session['warna_kertas_aktif']}
🌸 Bunga: {session['warna_bunga_aktif']}
🔢 Qty: {qty}
━━━━━━━━━━━━━━━━━━━━
💰 Subtotal: Rp {item['subtotal']:,}
🛒 Total Keranjang: Rp {total:,}
━━━━━━━━━━━━━━━━━━━━"""
        
        await update.message.reply_text(
            konfirmasi_msg,
            reply_markup=keyboard_konfirmasi_item(),
            parse_mode="Markdown"
        )

    # ===== INPUT NAMA =====
    elif session["state"] == STATE_INPUT_NAMA:
        session["nama_pembeli"] = text
        session["state"] = STATE_INPUT_WA
        await update.message.reply_text(
            "📱 *Nomor WhatsApp*\n\nKetik nomor WA (contoh: 081234567890):",
            parse_mode="Markdown"
        )

    # ===== INPUT WA =====
    elif session["state"] == STATE_INPUT_WA:
        # Validate phone number
        is_valid, error_msg = validate_phone(text)
        if not is_valid:
            await update.message.reply_text(error_msg)
            return
        
        session["wa_pembeli"] = text
        session["state"] = STATE_PILIH_PENGIRIMAN
        await update.message.reply_text(
            "🚚 *Pilih Metode Pengiriman*",
            reply_markup=keyboard_pengiriman(),
            parse_mode="Markdown"
        )

    # ===== INPUT ALAMAT (fallback teks) =====
    elif session["state"] == STATE_INPUT_ALAMAT:
        session["alamat"] = text
        await finalize_order_text(update, session, update.effective_user.id)

    # ===== INPUT ORDER ID =====
    elif session["state"] == STATE_INPUT_ORDER_ID:
        # TODO: Implementasi cek status order
        await update.message.reply_text(
            f"📦 *Status Pesanan {text}*\n\n⏳ Fitur ini sedang dalam pengembangan.\n\nSilakan hubungi admin untuk info lebih lanjut.",
            reply_markup=keyboard_kembali_menu(),
            parse_mode="Markdown"
        )
        session["state"] = STATE_MENU


@safe_handler("buyer_location_handler")
async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk location share dari user."""
    chat_id = update.effective_chat.id
    
    if chat_id not in buyer_sessions:
        init_buyer_session(chat_id)
    
    session = buyer_sessions[chat_id]
    location = update.message.location
    
    if session["state"] == STATE_INPUT_LOKASI and location:
        # Simpan koordinat sebagai alamat
        lat = location.latitude
        lon = location.longitude
        maps_link = f"https://maps.google.com/maps?q={lat},{lon}"
        session["alamat"] = f"📍 Lokasi: {maps_link}"
        session["lokasi"] = {"lat": lat, "lon": lon}
        
        await finalize_order_text(update, session, update.effective_user.id)


async def finalize_order(query, session, telegram_id):
    """Finalisasi order dari callback - simpan ke orders.json."""
    
    # Convert keranjang items to OrderItem objects
    order_items = []
    for item in session["keranjang"]:
        # Create dict for item
        order_items.append({
            "kode": item["kode"],
            "nama": item["nama"],
            "ukuran": item["ukuran"],
            "warna_kertas": item["warna_kertas"],
            "warna_bunga": item["warna_bunga"],
            "qty": item["qty"],
            "harga": item["harga"],
            "hpp": item["hpp"],
            "subtotal": item["subtotal"]
        })
    
    # Create order
    order = create_order(
        telegram_id=telegram_id,
        nama_pembeli=session.get("nama_pembeli", "-"),
        wa_pembeli=session.get("wa_pembeli", "-"),
        alamat=session.get("alamat", ""),
        delivery=session.get("delivery", "ambil"),
        ongkir=session.get("ongkir", 0),
        items=order_items,
        source="bot"
    )
    
    # Kirim notifikasi ke semua admin
    try:
        await notify_admins_new_order(order)
    except Exception as e:
        print(f"Notifikasi admin gagal: {e}")
    
    # Format receipt
    receipt = format_order_receipt(order)
    
    await query.edit_message_text(
        receipt,
        reply_markup=keyboard_kembali_menu(),
        parse_mode="Markdown"
    )
    
    # Reset session
    session["keranjang"] = []
    session["state"] = STATE_MENU


async def finalize_order_text(update, session, telegram_id):
    """Finalisasi order dari text handler - simpan ke orders.json."""
    
    # Convert keranjang items to OrderItem objects
    order_items = []
    for item in session["keranjang"]:
        # Create dict for item
        order_items.append({
            "kode": item["kode"],
            "nama": item["nama"],
            "ukuran": item["ukuran"],
            "warna_kertas": item["warna_kertas"],
            "warna_bunga": item["warna_bunga"],
            "qty": item["qty"],
            "harga": item["harga"],
            "hpp": item["hpp"],
            "subtotal": item["subtotal"]
        })
    
    # Create order
    order = create_order(
        telegram_id=telegram_id,
        nama_pembeli=session.get("nama_pembeli", "-"),
        wa_pembeli=session.get("wa_pembeli", "-"),
        alamat=session.get("alamat", ""),
        delivery=session.get("delivery", "ambil"),
        ongkir=session.get("ongkir", 0),
        items=order_items,
        source="bot"
    )
    
    # Kirim notifikasi ke semua admin
    try:
        await notify_admins_new_order(order)
    except Exception as e:
        print(f"Notifikasi admin gagal: {e}")
    
    # Format receipt
    receipt = format_order_receipt(order)
    
    await update.message.reply_text(
        receipt,
        reply_markup=keyboard_kembali_menu(),
        parse_mode="Markdown"
    )
    
    # Reset session
    session["keranjang"] = []
    session["state"] = STATE_MENU

