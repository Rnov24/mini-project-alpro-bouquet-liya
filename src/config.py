"""
Configuration constants untuk Sistem Kasir UMKM.
"""
import os

# Data directory paths
DATA_DIR = "data"
BARANG_FILE = os.path.join(DATA_DIR, "katalog buqet.json")
TRANSAKSI_FILE = os.path.join(DATA_DIR, "transaksi.csv")

# CSV headers untuk transaksi
TRANSAKSI_HEADERS = [
    "waktu",
    "id_transaksi",
    "kode",
    "nama",
    "ukuran",
    "warna_kertas",
    "warna_bunga",
    "qty",
    "harga",
    "subtotal",
    "hpp",
    "total_hpp",
    "profit",
    "diskon",
    "ongkir",
    "delivery",
    "total_transaksi",
]


# App info
APP_NAME = "SISTEM KASIR BUQEUET LIYA"
