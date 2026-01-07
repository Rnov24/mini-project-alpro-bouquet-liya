from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def menu_utama():
    keyboard = [
        [InlineKeyboardButton("🛒 Mulai Transaksi", callback_data="trx_mulai")],
        [InlineKeyboardButton("📊 Rekap Pendapatan", callback_data="trx_rekap")],
        [InlineKeyboardButton("❌ Batal", callback_data="trx_batal")]
    ]
    return InlineKeyboardMarkup(keyboard)
