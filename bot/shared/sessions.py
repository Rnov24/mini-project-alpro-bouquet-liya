"""
Shared sessions untuk Buyer dan Admin bot.
"""

# Session storage untuk buyer bot
buyer_sessions = {}

# Session storage untuk admin bot  
admin_sessions = {}


def init_buyer_session(chat_id):
    """Initialize session untuk buyer."""
    buyer_sessions[chat_id] = {
        "state": "menu",
        "keranjang": [],
        "barang_aktif": None,
        "ukuran_aktif": None,
        "warna_kertas_aktif": None,
        "warna_bunga_aktif": None,
        "kategori_aktif": None,
        "nama_pembeli": None,
        "wa_pembeli": None,
        "alamat": None,
        "delivery": None,
        "ongkir": 0,
        "order_id": None,
    }


def init_admin_session(chat_id):
    """Initialize session untuk admin."""
    admin_sessions[chat_id] = {
        "state": "menu",
        "barang_edit": None,
        "ukuran_edit": None,
        "new_product": None,
    }
