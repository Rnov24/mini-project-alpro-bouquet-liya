from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def keyboard_barang(barang_list):
    keyboard = []
    for b in barang_list:
        keyboard.append([
            InlineKeyboardButton(
                f"{b.nama}",
                callback_data=f"barang_{b.kode}"
            )
        ])
    keyboard.append([InlineKeyboardButton("✅ Selesai", callback_data="selesai")])
    return InlineKeyboardMarkup(keyboard)
