"""
Handlers untuk Admin Bot.
"""
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
import json
import os

from bot.shared.sessions import admin_sessions, init_admin_session
from .keyboards import (
    menu_utama, menu_katalog, keyboard_produk_list, keyboard_ukuran_stok,
    keyboard_konfirmasi_hapus, keyboard_rekap_periode, keyboard_kembali,
    keyboard_export, keyboard_pending_orders, keyboard_order_action,
    keyboard_order_status_filter
)
from .states import *
from core.services.barang_service import load_barang_dict, save_barang_dict
from core.services.transaksi_service import get_transaction_summary, save_order_to_csv
from core.config import BARANG_FILE, TRANSAKSI_FILE, BUYER_BOT_TOKEN
from core.services.order_service import (
    get_orders_by_status, get_order_by_id, load_orders_raw, get_active_orders,
    process_order, ready_order, cancel_order, delete_order,
    STATUS_PENDING, STATUS_PROCESSING, STATUS_READY, STATUS_CANCELLED,
)
from core.services.invoice_service import generate_invoice_text, generate_invoice_image, format_order_receipt
from bot.shared.admin_registry import (
    register_admin, unregister_admin, is_admin, get_all_admin_ids, ADMIN_REGISTER_PASSWORD
)

# Payment info constant for formatting
PAYMENT_INFO = """💳 *REKENING PEMBAYARAN*
━━━━━━━━━━━━━━━━━━━━
🟢 *DANA*: 081234567890 (a.n. Buqeuet Liya)
🔵 *SeaBank*: 901234567890 (a.n. Buqeuet Liya)
🏦 *BRI*: 0123456789012345 (a.n. Buqeuet Liya)
━━━━━━━━━━━━━━━━━━━━
Setelah transfer, konfirmasi ke admin via WhatsApp."""



def format_payment_request(order):
    """Format pesan permintaan pembayaran."""
    items_str = ""
    for item in order.get("items", []):
        nama = item.get("nama")
        ukuran = item.get("ukuran")
        qty = item.get("qty")
        subtotal = item.get("subtotal")
        items_str += f"  • {nama} ({ukuran}) x{qty} = Rp {subtotal:,.0f}\n"
    
    ongkir = order.get("ongkir", 0)
    diskon = order.get("diskon", 0)
    total = order.get("total", 0)
    
    return f"""📦 *PESANAN SIAP!*
━━━━━━━━━━━━━━━━━━━━
Order ID: `{order.get("order_id")}`

Barang pesanan kamu sudah ready:
{items_str}
Ongkir: Rp {ongkir:,.0f}
Diskon: -Rp {diskon:,.0f}
━━━━━━━━━━━━━━━━━━━━
💰 *TOTAL BAYAR: Rp {total:,.0f}*

Silakan transfer ke salah satu rekening di bawah:
{PAYMENT_INFO}

📸 Jangan lupa kirim bukti transfer ke Admin ya!"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler /start command."""
    chat_id = update.effective_chat.id
    init_admin_session(chat_id)
    admin_sessions[chat_id]["state"] = STATE_MENU

    welcome_msg = """🔐 *Admin Panel - Buqeuet Liya*
━━━━━━━━━━━━━━━━━━━━
Selamat datang, Admin!

Pilih menu untuk mengelola toko:"""

    await update.message.reply_text(
        welcome_msg,
        reply_markup=menu_utama(),
        parse_mode="Markdown"
    )


async def daftar_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler /daftar command untuk registrasi admin."""
    chat_id = update.effective_chat.id
    init_admin_session(chat_id)
    
    # Cek apakah sudah terdaftar
    if is_admin(chat_id):
        await update.message.reply_text(
            "✅ Anda sudah terdaftar sebagai admin!\n\nKetik /start untuk masuk ke menu.",
            parse_mode="Markdown"
        )
        return
    
    admin_sessions[chat_id]["state"] = STATE_REGISTER_ADMIN
    
    await update.message.reply_text(
        "🔐 *Pendaftaran Admin*\n\n"
        "Masukkan password admin untuk mendaftar:\n\n"
        "_Hubungi owner untuk mendapatkan password_",
        parse_mode="Markdown"
    )


async def list_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler /listadmin command untuk melihat daftar admin."""
    chat_id = update.effective_chat.id
    
    if not is_admin(chat_id):
        await update.message.reply_text("❌ Anda bukan admin.")
        return
    
    admin_ids = get_all_admin_ids()
    
    if not admin_ids:
        await update.message.reply_text("📋 Belum ada admin terdaftar.")
        return
    
    admin_list = "\n".join([f"• `{aid}`" for aid in admin_ids])
    await update.message.reply_text(
        f"👥 *Daftar Admin Terdaftar*\n\n{admin_list}\n\nTotal: {len(admin_ids)} admin",
        parse_mode="Markdown"
    )

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Router untuk semua callback query."""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat.id
    data = query.data
    
    if chat_id not in admin_sessions:
        init_admin_session(chat_id)
    
    session = admin_sessions[chat_id]

    # ===== MENU UTAMA =====
    if data == "menu":
        session["state"] = STATE_MENU
        await query.edit_message_text(
            "🔐 *Admin Panel - Buqeuet Liya*\n━━━━━━━━━━━━━━━━━━━━\nSelamat datang, Admin!\n\nPilih menu untuk mengelola toko:",
            reply_markup=menu_utama(),
            parse_mode="Markdown"
        )

    # ===== KATALOG MENU =====
    elif data == "katalog":
        session["state"] = STATE_MENU
        await query.edit_message_text(
            "📦 *Manajemen Katalog*\n\nPilih aksi yang ingin dilakukan:",
            reply_markup=menu_katalog(),
            parse_mode="Markdown"
        )

    # ===== LIHAT SEMUA =====
    elif data == "kat_lihat":
        session["state"] = STATE_LIHAT_KATALOG
        barang_list = load_barang_dict()
        
        if not barang_list:
            await query.edit_message_text(
                "📦 Katalog kosong.",
                reply_markup=keyboard_kembali("katalog"),
                parse_mode="Markdown"
            )
            return
        
        await query.edit_message_text(
            "📦 *Daftar Produk*\n\nKlik produk untuk lihat detail:",
            reply_markup=keyboard_produk_list(barang_list, "detail"),
            parse_mode="Markdown"
        )

    # ===== DETAIL PRODUK =====
    elif data.startswith("detail_"):
        kode = data.replace("detail_", "")
        barang_list = load_barang_dict()
        barang = next((b for b in barang_list if b["kode"] == kode), None)
        
        if barang:
            ukuran_str = "\n".join([
                f"  • {u['nama']}: Rp {u['harga']:,} | HPP: Rp {u['hpp']:,} | Stok: {u['stok']}"
                for u in barang["ukuran"]
            ])
            kertas_str = ", ".join(barang["warna_kertas"])
            bunga_str = ", ".join(barang["warna_bunga"])
            
            detail = f"""📦 *{barang['nama']}* (`{kode}`)
━━━━━━━━━━━━━━━━━━━━
📏 *Ukuran & Harga:*
{ukuran_str}

🎨 *Warna Kertas:* {kertas_str}
🌸 *Warna Bunga:* {bunga_str}
━━━━━━━━━━━━━━━━━━━━"""
            
            await query.edit_message_text(
                detail,
                reply_markup=keyboard_kembali("kat_lihat"),
                parse_mode="Markdown"
            )

    # ===== UPDATE STOK =====
    elif data == "kat_stok":
        barang_list = load_barang_dict()
        session["state"] = STATE_UPDATE_STOK_PILIH
        await query.edit_message_text(
            "📈 *Update Stok*\n\nPilih produk:",
            reply_markup=keyboard_produk_list(barang_list, "stok"),
            parse_mode="Markdown"
        )

    elif data.startswith("stok_"):
        if data.startswith("stok_ukuran_"):
            ukuran = data.replace("stok_ukuran_", "")
            session["ukuran_edit"] = ukuran
            session["state"] = STATE_UPDATE_STOK_VALUE
            await query.edit_message_text(
                f"📈 *Update Stok - {ukuran}*\n\nMasukkan stok baru (angka):",
                parse_mode="Markdown"
            )
        else:
            kode = data.replace("stok_", "")
            session["barang_edit"] = kode
            session["state"] = STATE_UPDATE_STOK_UKURAN
            
            barang_list = load_barang_dict()
            barang = next((b for b in barang_list if b["kode"] == kode), None)
            
            if barang:
                await query.edit_message_text(
                    f"📈 *Update Stok - {barang['nama']}*\n\nPilih ukuran:",
                    reply_markup=keyboard_ukuran_stok(barang),
                    parse_mode="Markdown"
                )

    # ===== HAPUS PRODUK =====
    elif data == "kat_hapus":
        barang_list = load_barang_dict()
        session["state"] = STATE_HAPUS_PILIH
        await query.edit_message_text(
            "🗑️ *Hapus Produk*\n\nPilih produk yang akan dihapus:",
            reply_markup=keyboard_produk_list(barang_list, "hapus"),
            parse_mode="Markdown"
        )

    elif data.startswith("hapus_"):
        if data.startswith("hapus_konfirm_"):
            kode = data.replace("hapus_konfirm_", "")
            barang_list = load_barang_dict()
            barang_list = [b for b in barang_list if b["kode"] != kode]
            save_barang_dict(barang_list)
            
            await query.edit_message_text(
                f"✅ Produk `{kode}` berhasil dihapus!",
                reply_markup=keyboard_kembali("katalog"),
                parse_mode="Markdown"
            )
        else:
            kode = data.replace("hapus_", "")
            barang_list = load_barang_dict()
            barang = next((b for b in barang_list if b["kode"] == kode), None)
            
            if barang:
                session["state"] = STATE_HAPUS_KONFIRM
                await query.edit_message_text(
                    f"⚠️ *Konfirmasi Hapus*\n\nYakin ingin menghapus:\n`{kode}` - {barang['nama']}?",
                    reply_markup=keyboard_konfirmasi_hapus(kode),
                    parse_mode="Markdown"
                )

    # ===== REKAP =====
    elif data == "rekap":
        session["state"] = STATE_REKAP
        await query.edit_message_text(
            "📊 *Rekap Pendapatan*\n\nPilih periode:",
            reply_markup=keyboard_rekap_periode(),
            parse_mode="Markdown"
        )

    elif data.startswith("rekap_"):
        periode = data.replace("rekap_", "")
        from core.services.transaksi_service import get_transaction_summary
        
        stats = get_transaction_summary()
        
        periode_label = {
            "hari": "Hari Ini",
            "minggu": "Minggu Ini",
            "bulan": "Bulan Ini",
            "semua": "Semua Waktu"
        }.get(periode, "Semua Waktu")
        
        # Format Top Products
        top_produk_str = ""
        if stats["top_products"]:
            for i, p in enumerate(stats["top_products"][:3], 1):
                top_produk_str += f"{i}. {p['nama'][:20]} ({p['qty']}x)\n"
        else:
            top_produk_str = "- Belum ada data -"
            
        rekap_msg = f"""📊 *REKAP PENDAPATAN DETAILED*
════════════════════
📅 Periode: {periode_label}
────────────────────
💰 *Omset: Rp {stats['pendapatan']:,.0f}*
📉 Modal: Rp {stats['modal']:,.0f}
📈 Profit: Rp {stats['profit']:,.0f}
────────────────────
🏘️ *Sales Channels:*
🏠 *Toko/Offline:*
• {stats['by_source']['offline']['trx']} Trx - Rp {stats['by_source']['offline']['pendapatan']:,.0f}

🤖 *Bot/Online:*
• {stats['by_source']['online']['trx']} Trx - Rp {stats['by_source']['online']['pendapatan']:,.0f}
────────────────────
🏆 *Produk Terlaris:*
{top_produk_str}
════════════════════"""
        
        try:
            await query.edit_message_text(
                rekap_msg,
                reply_markup=keyboard_rekap_periode(),
                parse_mode="Markdown"
            )
        except Exception:
            pass

    # ===== PESANAN MASUK =====
    elif data == "pesanan":
        active = get_active_orders()
        active.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        count_msg = f"({len(active)} aktif)" if active else "(kosong)"
        await query.edit_message_text(
            f"📝 *Pesanan Aktif* {count_msg}\n\nKlik pesanan untuk lihat detail & kelola:",
            reply_markup=keyboard_pending_orders(active),
            parse_mode="Markdown"
        )

    # ===== DETAIL ORDER =====
    elif data.startswith("ord_"):
        order_id = data.replace("ord_", "")
        order = get_order_by_id(order_id)
        
        if order:
            receipt = format_order_receipt(order)
            await query.edit_message_text(
                receipt,
                reply_markup=keyboard_order_action(order),
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text(
                "❌ Order tidak ditemukan.",
                reply_markup=keyboard_kembali("pesanan"),
                parse_mode="Markdown"
            )

    # ===== MULAI PROSES ORDER =====
    elif data.startswith("process_"):
        order_id = data.replace("process_", "")
        order = process_order(order_id)
        
        if order:
            # Kirim notifikasi ke buyer
            try:
                from telegram import Bot
                if BUYER_BOT_TOKEN and BUYER_BOT_TOKEN != "your_buyer_bot_token_here":
                    buyer_bot = Bot(token=BUYER_BOT_TOKEN)
                    notif_msg = f"🔨 *Pesanan Sedang Diproses!*\n\nPesanan `{order_id}` sedang dalam proses pembuatan.\n\nMohon tunggu sampai buket selesai dibuat!"
                    await buyer_bot.send_message(
                        chat_id=order.get("telegram_id"),
                        text=notif_msg,
                        parse_mode="Markdown"
                    )
            except Exception as e:
                print(f"Gagal kirim notifikasi: {e}")
            
            await query.edit_message_text(
                f"🔨 *Order Diproses*\n\n`{order_id}` sedang diproduksi.\nNotifikasi telah dikirim ke buyer.",
                reply_markup=keyboard_kembali("pesanan"),
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text(
                "❌ Gagal memproses order.",
                reply_markup=keyboard_kembali("pesanan"),
                parse_mode="Markdown"
            )

    # ===== TANDAI SIAP (MINTA ADJUSTMENT) =====
    elif data.startswith("ready_"):
        order_id = data.replace("ready_", "")
        order = get_order_by_id(order_id)
        
        if order:
            # Store order_id in session and ask for ongkir
            session["ready_order_id"] = order_id
            session["state"] = "ready_order_ongkir"
            
            subtotal = order.get("subtotal", 0)
            delivery = order.get("delivery", "ambil")
            
            await query.edit_message_text(
                f"📦 *Siapkan Order*\n\n"
                f"Order: `{order_id}`\n"
                f"Subtotal: Rp {subtotal:,.0f}\n"
                f"Delivery: {delivery}\n\n"
                f"📝 Masukkan *ongkir* (0 jika ambil sendiri):",
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text(
                "❌ Order tidak ditemukan.",
                reply_markup=keyboard_kembali("pesanan"),
                parse_mode="Markdown"
            )

    # ===== CLOSE ORDER (FINALISASI LANGSUNG) =====
    elif data.startswith("close_"):
        order_id = data.replace("close_", "")
        order = get_order_by_id(order_id)
        
        if order:
            # Finalize order directly using existing ongkir/diskon
            from core.services.transaksi_service import finalize_order
            
            subtotal = order.get("subtotal", 0) if isinstance(order, dict) else order.subtotal
            diskon = order.get("diskon", 0) if isinstance(order, dict) else getattr(order, 'diskon', 0)
            ongkir = order.get("ongkir", 0) if isinstance(order, dict) else order.ongkir
            total_final = order.get("total", 0) if isinstance(order, dict) else order.total
            total_final = order.get("total", 0)
            
            # Finalize order via core service
            trx_id, invoice_path = finalize_order(order_id, generate_invoice=True)
            
            # Send invoice to buyer
            try:
                from telegram import Bot
                if BUYER_BOT_TOKEN and BUYER_BOT_TOKEN != "your_buyer_bot_token_here":
                    buyer_bot = Bot(token=BUYER_BOT_TOKEN)
                    
                    # Text invoice
                    invoice_msg = f"""🎉 *INVOICE*
════════════════════
🧶 `{trx_id}`
────────────────────
📦 *ITEM:*
"""
                    for item in order.get("items", []):
                        nama = item.get("nama", "")
                        ukuran = item.get("ukuran", "")
                        qty = item.get("qty", 0)
                        item_subtotal = item.get("subtotal", 0)
                        invoice_msg += f"  • {nama} ({ukuran}) × {qty}\n"
                        invoice_msg += f"    → Rp {item_subtotal:,.0f}\n"
                    
                    invoice_msg += f"""────────────────────
💰 Subtotal: Rp {subtotal:,.0f}
"""
                    if diskon > 0:
                        invoice_msg += f"💸 Diskon: -Rp {diskon:,.0f}\n"
                    if ongkir > 0:
                        invoice_msg += f"🚚 Ongkir: Rp {ongkir:,.0f}\n"
                    
                    invoice_msg += f"""━━━━━━━━━━━━━━━━━━━━
✅ *TOTAL: Rp {total_final:,.0f}*
════════════════════
✨ Terima kasih! 🌸"""
                    
                    await buyer_bot.send_message(
                        chat_id=order.get("telegram_id"),
                        text=invoice_msg,
                        parse_mode="Markdown"
                    )
                    
                    # Image invoice
                    if invoice_path:
                        with open(invoice_path, "rb") as img:
                            await buyer_bot.send_photo(
                                chat_id=order.get("telegram_id"),
                                photo=img,
                                caption="🧶 Invoice Buqeuet Liya"
                            )
            except Exception as e:
                print(f"Gagal kirim invoice: {e}")
            
            await query.edit_message_text(
                f"✅ *Order Selesai!*\n\n"
                f"📋 Order: `{order_id}`\n"
                f"🧶 Invoice: `{trx_id}`\n"
                f"────────────────────\n"
                f"💵 *TOTAL: Rp {total_final:,.0f}*\n\n"
                f"✅ Invoice dikirim ke buyer.",
                reply_markup=keyboard_kembali("pesanan"),
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text(
                "❌ Order tidak ditemukan.",
                reply_markup=keyboard_kembali("pesanan"),
                parse_mode="Markdown"
            )

    # ===== BATALKAN ORDER (ADMIN) =====
    elif data.startswith("admincancel_"):
        order_id = data.replace("admincancel_", "")
        order = cancel_order(order_id)
        
        if order:
            # Kirim notifikasi ke buyer
            try:
                from telegram import Bot
                if BUYER_BOT_TOKEN and BUYER_BOT_TOKEN != "your_buyer_bot_token_here":
                    buyer_bot = Bot(token=BUYER_BOT_TOKEN)
                    notif_msg = f"🚫 *Pesanan Dibatalkan*\n\nMaaf, pesanan `{order_id}` dibatalkan oleh admin.\n\nSilakan hubungi admin untuk info lebih lanjut."
                    await buyer_bot.send_message(
                        chat_id=order.telegram_id,
                        text=notif_msg,
                        parse_mode="Markdown"
                    )
            except Exception as e:
                print(f"Gagal kirim notifikasi: {e}")
            
            # Hapus order yang dibatalkan
            delete_order(order_id)
            
            await query.edit_message_text(
                f"🚫 *Order Dibatalkan*\n\n`{order_id}` telah dibatalkan dan dihapus.",
                reply_markup=keyboard_kembali("pesanan"),
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text(
                "❌ Gagal membatalkan order.",
                reply_markup=keyboard_kembali("pesanan"),
                parse_mode="Markdown"
            )

    # ===== RIWAYAT ORDER =====
    elif data == "riwayat":
        await query.edit_message_text(
            "📜 *Riwayat Order*\n\nFilter berdasarkan status:",
            reply_markup=keyboard_order_status_filter(),
            parse_mode="Markdown"
        )

    # ===== FILTER HISTORY =====
    elif data.startswith("hist_"):
        status_filter = data.replace("hist_", "")
        
        if status_filter == "completed":
            # Load from CSV for completed transactions
            from core.services.transaksi_service import load_recent_transactions
            # Load last 10 transactions
            transaksi_list = load_recent_transactions(limit=10)
            
            if not transaksi_list:
                await query.edit_message_text(
                    "📜 Belum ada transaksi selesai.",
                    reply_markup=keyboard_kembali("riwayat"),
                    parse_mode="Markdown"
                )
            else:
                orders_list = ""
                for t in transaksi_list:
                    # t is a dictionary from load_transaksi
                    trx_id = t.get("id_transaksi", "N/A")
                    total = float(t.get("total_transaksi", 0))
                    waktu = t.get("waktu", "")[:10] # Date only
                    orders_list += f"✅ `{trx_id}` ({waktu}) - Rp {total:,.0f}\n"

                await query.edit_message_text(
                    f"📜 *Riwayat Order Selesai* (Last 10)\n\n{orders_list}",
                    reply_markup=keyboard_kembali("riwayat"),
                    parse_mode="Markdown"
                )
            return

        elif status_filter == "all":
            orders = load_orders_raw()
        else:
            orders = get_orders_by_status(status_filter)
        
        orders.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        if not orders:
            await query.edit_message_text(
                "📜 Tidak ada order dengan status ini.",
                reply_markup=keyboard_kembali("riwayat"),
                parse_mode="Markdown"
            )
        else:
            orders_list = ""
            for o in orders[:10]:
                status = o.get("status", "pending") if isinstance(o, dict) else o.status
                status_emoji = {"pending": "⏳", "processing": "🔨", "ready": "📦", "completed": "✅", "rejected": "❌", "cancelled": "🚫"}.get(status, "📦")
                order_id = o.get("order_id", "-") if isinstance(o, dict) else o.order_id
                total = o.get("total", 0) if isinstance(o, dict) else o.total
                orders_list += f"{status_emoji} `{order_id}` - Rp {total:,.0f}\n"
            
            await query.edit_message_text(
                f"📜 *Riwayat Order* ({len(orders)} total)\n\n{orders_list}",
                reply_markup=keyboard_kembali("riwayat"),
                parse_mode="Markdown"
            )

    # ===== EXPORT =====
    elif data == "export":
        await query.edit_message_text(
            "📤 *Export Data*\n\nPilih data yang ingin di-export:",
            reply_markup=keyboard_export(),
            parse_mode="Markdown"
        )

    elif data == "export_katalog":
        try:
            with open(BARANG_FILE, "rb") as f:
                await context.bot.send_document(
                    chat_id=chat_id,
                    document=f,
                    filename="katalog_buket.json",
                    caption="📦 Data Katalog Produk"
                )
        except Exception as e:
            await query.edit_message_text(
                f"❌ Gagal export: {str(e)}",
                reply_markup=keyboard_kembali("export"),
                parse_mode="Markdown"
            )

    elif data == "export_transaksi":
        if os.path.exists(TRANSAKSI_FILE):
            try:
                with open(TRANSAKSI_FILE, "rb") as f:
                    await context.bot.send_document(
                        chat_id=chat_id,
                        document=f,
                        filename="transaksi.csv",
                        caption="📊 Data Transaksi"
                    )
            except Exception as e:
                await query.edit_message_text(
                    f"❌ Gagal export: {str(e)}",
                    reply_markup=keyboard_kembali("export"),
                    parse_mode="Markdown"
                )
        else:
            await query.edit_message_text(
                "📊 Belum ada data transaksi.",
                reply_markup=keyboard_kembali("export"),
                parse_mode="Markdown"
            )

    # ===== PAGINATION =====
    elif data.startswith("paging_"):
        parts = data.split("_")
        action = parts[1]
        page = int(parts[2])
        barang_list = load_barang_dict()
        
        await query.edit_message_text(
            "📦 *Daftar Produk*",
            reply_markup=keyboard_produk_list(barang_list, action, page),
            parse_mode="Markdown"
        )

    # ===== TAMBAH PRODUK =====
    elif data == "kat_tambah":
        session["state"] = STATE_TAMBAH_KODE
        await query.edit_message_text(
            "➕ *Tambah Produk Baru*\n\nMasukkan kode produk (contoh: A4):",
            parse_mode="Markdown"
        )

    # ===== EDIT PRODUK =====
    elif data == "kat_edit":
        barang_list = load_barang_dict()
        session["state"] = STATE_EDIT_PILIH
        await query.edit_message_text(
            "✏️ *Edit Produk*\n\n⏳ Fitur ini sedang dalam pengembangan.",
            reply_markup=keyboard_kembali("katalog"),
            parse_mode="Markdown"
        )


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk input text dari admin."""
    chat_id = update.effective_chat.id
    
    if chat_id not in admin_sessions:
        init_admin_session(chat_id)
        return
    
    session = admin_sessions[chat_id]
    text = update.message.text.strip()

    # ===== UPDATE STOK =====
    if session["state"] == STATE_UPDATE_STOK_VALUE:
        if not text.isdigit():
            await update.message.reply_text("⚠️ Masukkan angka yang valid!")
            return
        
        stok_baru = int(text)
        kode = session.get("barang_edit")
        ukuran_nama = session.get("ukuran_edit")
        
        barang_list = load_barang_dict()
        for barang in barang_list:
            if barang["kode"] == kode:
                for ukuran in barang["ukuran"]:
                    if ukuran["nama"] == ukuran_nama:
                        ukuran["stok"] = stok_baru
                        break
                break
        
        save_barang_dict(barang_list)
        session["state"] = STATE_MENU
        
        await update.message.reply_text(
            f"✅ Stok `{kode}` ukuran *{ukuran_nama}* diupdate menjadi *{stok_baru}*",
            reply_markup=keyboard_kembali("katalog"),
            parse_mode="Markdown"
        )

    # ===== TAMBAH PRODUK - KODE =====
    elif session["state"] == STATE_TAMBAH_KODE:
        session["new_product"] = {"kode": text.upper()}
        session["state"] = STATE_TAMBAH_NAMA
        await update.message.reply_text(
            "📝 Masukkan nama produk:",
            parse_mode="Markdown"
        )

    # ===== TAMBAH PRODUK - NAMA =====
    elif session["state"] == STATE_TAMBAH_NAMA:
        session["new_product"]["nama"] = text
        session["new_product"]["warna_kertas"] = ["hitam", "pink", "ungu", "biru", "coklat"]
        session["new_product"]["warna_bunga"] = ["merah", "pink", "biru", "ungu", "putih"]
        session["new_product"]["ukuran"] = [
            {"nama": "Mini", "harga": 25000, "hpp": 18000, "stok": 10},
            {"nama": "Standar", "harga": 40000, "hpp": 28000, "stok": 10},
            {"nama": "Besar", "harga": 55000, "hpp": 40000, "stok": 10}
        ]
        
        # Save product
        barang_list = load_barang_dict()
        barang_list.append(session["new_product"])
        save_barang_dict(barang_list)
        
        session["state"] = STATE_MENU
        
        await update.message.reply_text(
            f"✅ Produk *{session['new_product']['nama']}* (`{session['new_product']['kode']}`) berhasil ditambahkan!\n\n_Edit harga/ukuran via menu Edit Produk_",
            reply_markup=keyboard_kembali("katalog"),
            parse_mode="Markdown"
        )

    # ===== REGISTRASI ADMIN =====
    elif session["state"] == STATE_REGISTER_ADMIN:
        if text == ADMIN_REGISTER_PASSWORD:
            # Password benar, daftarkan admin
            success = register_admin(chat_id)
            session["state"] = STATE_MENU
            
            if success:
                await update.message.reply_text(
                    "✅ *Selamat! Anda berhasil terdaftar sebagai Admin!*\n\n"
                    f"Chat ID Anda: `{chat_id}`\n\n"
                    "Ketik /start untuk masuk ke menu admin.",
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    "ℹ️ Anda sudah terdaftar sebagai admin.\n\nKetik /start untuk masuk ke menu.",
                    parse_mode="Markdown"
                )
        else:
            # Password salah
            await update.message.reply_text(
                "❌ *Password salah!*\n\nCoba lagi atau hubungi owner untuk password yang benar.",
                parse_mode="Markdown"
            )

    # ===== READY ORDER - ONGKIR INPUT =====
    elif session["state"] == "ready_order_ongkir":
        try:
            ongkir = float(text.replace(",", ".").replace(".", "").strip())
            if ongkir < 0:
                ongkir = 0
            
            session["ready_ongkir"] = ongkir
            session["state"] = "ready_order_diskon"
            
            await update.message.reply_text(
                f"✅ Ongkir: *Rp {ongkir:,.0f}*\n\n"
                "📝 Masukkan *diskon (%)* (contoh: 10, 0 untuk tanpa diskon):",
                parse_mode="Markdown"
            )
        except ValueError:
            await update.message.reply_text(
                "❌ Format salah. Masukkan angka (contoh: 10000, 15000):",
                parse_mode="Markdown"
            )

    # ===== READY ORDER - DISKON INPUT =====
    elif session["state"] == "ready_order_diskon":
        try:
            diskon_persen = float(text.replace(",", ".").replace("%", "").strip())
            if diskon_persen < 0: diskon_persen = 0
            if diskon_persen > 100: diskon_persen = 100
            
            order_id = session.get("ready_order_id")
            ongkir = session.get("ready_ongkir", 0)
            
            order = get_order_by_id(order_id)
            if not order:
                session["state"] = STATE_MENU
                await update.message.reply_text("❌ Order tidak ditemukan.")
                return

            # Calculate finals
            subtotal = order.get("subtotal", 0)
            diskon = subtotal * (diskon_persen / 100)
            total_final = subtotal - diskon + ongkir
            
            # Update order data
            from core.services.order_service import load_orders_raw, save_orders_raw
            orders = load_orders_raw()
            for o in orders:
                if o.get("order_id") == order_id:
                    o["diskon"] = diskon
                    o["ongkir"] = ongkir
                    o["total"] = total_final
                    break
            save_orders_raw(orders)
            
            # Set status to READY
            updated_order = ready_order(order_id)
            
            # Notify Buyer with payment request
            try:
                from telegram import Bot
                if BUYER_BOT_TOKEN and BUYER_BOT_TOKEN != "your_buyer_bot_token_here":
                    buyer_bot = Bot(token=BUYER_BOT_TOKEN)
                    payment_msg = format_payment_request(updated_order)
                    await buyer_bot.send_message(
                        chat_id=updated_order.get("telegram_id"),
                        text=payment_msg,
                        parse_mode="Markdown"
                    )
            except Exception as e:
                print(f"Gagal kirim notifikasi: {e}")
            
            session["state"] = STATE_MENU
            
            await update.message.reply_text(
                f"📦 *Order Siap (Menunggu Pembayaran)*\n\n"
                f"Order: `{order_id}`\n"
                f"Subtotal: Rp {subtotal:,.0f}\n"
                f"Ongkir: Rp {ongkir:,.0f}\n"
                f"Diskon ({diskon_persen}%): -Rp {diskon:,.0f}\n"
                f"────────────────────\n"
                f"💵 *TAGIHAN: Rp {total_final:,.0f}*\n\n"
                f"✅ Permintaan pembayaran dikirim ke buyer.",
                reply_markup=keyboard_kembali("pesanan"),
                parse_mode="Markdown"
            )
            
        except ValueError:
            await update.message.reply_text(
                "❌ Format salah. Masukkan angka (contoh: 10, 5.5):",
                parse_mode="Markdown"
            )

