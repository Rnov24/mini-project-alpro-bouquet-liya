user_sessions = {}

def init_session(chat_id):
    user_sessions[chat_id] = {
        "state": None,
        "keranjang": [],
        "current_barang": None,
        "current_ukuran": None,
        "total": 0,
        "diskon": 0,
        "ongkir": 0
    }
