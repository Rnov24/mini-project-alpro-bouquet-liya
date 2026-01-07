from telegram import Update
from telegram.ext import ContextTypes
from .sessions import user_sessions, init_session
from .menus import menu_utama
from .keyboards import keyboard_barang
from .states import *
from src.services.barang_service import load_barang
from src.services.transaksi_service import get_rekap_pendapatan

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    init_session(chat_id)
    user_sessions[chat_id]["state"] = STATE_MENU

    await update.message.reply_text(
        "🌸 *Sistem Kasir Buqeuet Liya*",
        reply_markup=menu_utama(),
        parse_mode="Markdown"
    )

# Semua tombol masuk ke sini
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    data = query.data
    session = user_sessions[chat_id]

    # ===== MULAI TRANSAKSI =====
    if data == "trx_mulai":
        session["state"] = STATE_PILIH_BARANG
        barang_list = load_barang()

        await query.edit_message_text(
            "🛍️ Pilih barang:",
            reply_markup=keyboard_barang(barang_list)
        )

    # ===== PILIH BARANG =====
    elif data.startswith("barang_"):
        kode = data.replace("barang_", "")
        session["barang_aktif"] = kode
        session["state"] = STATE_QTY

        await query.edit_message_text(
            f"Masukkan jumlah untuk barang `{kode}`:",
            parse_mode="Markdown"
        )

    # ===== SELESAI =====
    elif data == "selesai":
        await query.edit_message_text(
            "✅ Transaksi selesai (next: pembayaran)"
        )

    # ===== REKAP =====
    elif data == "trx_rekap":
        jumlah, pendapatan, modal, profit = get_rekap_pendapatan()

        await query.edit_message_text(
            f"""📊 *Rekap Pendapatan*
Jumlah Transaksi: {jumlah}
Pendapatan: Rp {pendapatan:,.0f}
Modal: Rp {modal:,.0f}
Profit: Rp {profit:,.0f}
""",
            parse_mode="Markdown"
        )

    elif data == "trx_batal":
        user_sessions.pop(chat_id, None)
        await query.edit_message_text("❌ Transaksi dibatalkan")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    session = user_sessions.get(chat_id)

    if not session:
        return

    if session["state"] == STATE_QTY:
        if not update.message.text.isdigit():
            await update.message.reply_text("Masukkan angka!")
            return

        qty = int(update.message.text)
        kode = session["barang_aktif"]

        session["keranjang"].append({
            "kode": kode,
            "qty": qty
        })

        session["state"] = STATE_PILIH_BARANG

        barang_list = load_barang()
        await update.message.reply_text(
            "Barang ditambahkan. Pilih barang lagi:",
            reply_markup=keyboard_barang(barang_list)
        )
