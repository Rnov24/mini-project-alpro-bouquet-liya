"""
States untuk Buyer Bot conversation flow.
"""

# Menu states
STATE_MENU = "menu"

# Katalog states
STATE_KATEGORI = "kategori"
STATE_BROWSE_KATALOG = "browse_katalog"

# Order flow states
STATE_PILIH_BARANG = "pilih_barang"
STATE_PILIH_UKURAN = "pilih_ukuran"
STATE_PILIH_WARNA_KERTAS = "pilih_warna_kertas"
STATE_PILIH_WARNA_BUNGA = "pilih_warna_bunga"
STATE_INPUT_QTY = "input_qty"
STATE_KONFIRMASI_ITEM = "konfirmasi_item"

# Checkout states
STATE_INPUT_NAMA = "input_nama"
STATE_INPUT_WA = "input_wa"
STATE_PILIH_PENGIRIMAN = "pilih_pengiriman"
STATE_INPUT_ALAMAT = "input_alamat"
STATE_INPUT_LOKASI = "input_lokasi"  # Untuk share location
STATE_ORDER_SUMMARY = "order_summary"

# Cek pesanan
STATE_INPUT_ORDER_ID = "input_order_id"
