"""
States untuk Admin Bot conversation flow.
"""

# Menu states
STATE_MENU = "menu"

# Katalog management
STATE_LIHAT_KATALOG = "lihat_katalog"
STATE_TAMBAH_KODE = "tambah_kode"
STATE_TAMBAH_NAMA = "tambah_nama"
STATE_TAMBAH_UKURAN = "tambah_ukuran"
STATE_EDIT_PILIH = "edit_pilih"
STATE_EDIT_FIELD = "edit_field"
STATE_HAPUS_PILIH = "hapus_pilih"
STATE_HAPUS_KONFIRM = "hapus_konfirm"
STATE_UPDATE_STOK_PILIH = "update_stok_pilih"
STATE_UPDATE_STOK_UKURAN = "update_stok_ukuran"
STATE_UPDATE_STOK_VALUE = "update_stok_value"

# Rekap
STATE_REKAP = "rekap"

# Pesanan
STATE_PESANAN_LIST = "pesanan_list"
STATE_PESANAN_DETAIL = "pesanan_detail"

# Riwayat
STATE_RIWAYAT = "riwayat"

# Admin Registration
STATE_REGISTER_ADMIN = "register_admin"

# Close Order with adjustments
STATE_CLOSE_ORDER_DISKON = "close_order_diskon"
STATE_CLOSE_ORDER_ONGKIR = "close_order_ongkir"
