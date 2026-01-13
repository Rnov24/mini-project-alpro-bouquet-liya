"""
Konfigurasi aplikasi Buqeuet Liya.

Modul ini berisi semua konstanta konfigurasi yang digunakan oleh aplikasi,
termasuk path file data, token bot Telegram, dan header CSV.

Konfigurasi sensitif seperti token disimpan di file .env dan diload
menggunakan python-dotenv.

Example:
    from core.config import DATA_DIR, BARANG_FILE
    print(f"Data disimpan di: {DATA_DIR}")
"""
import os
from dotenv import load_dotenv

# Load environment variables dari file .env
load_dotenv()


# ═══════════════════════════════════════════════════════════════
# PATH KONFIGURASI
# ═══════════════════════════════════════════════════════════════

DATA_DIR = "data"
"""Direktori utama untuk menyimpan semua file data."""

BARANG_FILE = os.path.join(DATA_DIR, "katalog buqet.json")
"""Path file JSON untuk menyimpan katalog barang."""

TRANSAKSI_FILE = os.path.join(DATA_DIR, "transaksi.csv")
"""Path file CSV untuk menyimpan riwayat transaksi."""


# ═══════════════════════════════════════════════════════════════
# TELEGRAM BOT TOKENS
# ═══════════════════════════════════════════════════════════════

BUYER_BOT_TOKEN = os.getenv("TELEGRAM_BUYER_BOT_TOKEN", "")
"""Token untuk Telegram Bot pembeli (customer-facing)."""

ADMIN_BOT_TOKEN = os.getenv("TELEGRAM_ADMIN_BOT_TOKEN", "")
"""Token untuk Telegram Bot admin (internal)."""

# Admin Chat IDs untuk notifikasi (comma-separated di .env)
# Contoh: ADMIN_CHAT_IDS=123456789,987654321
_admin_ids_str = os.getenv("ADMIN_CHAT_IDS", "")
ADMIN_CHAT_IDS = [int(x.strip()) for x in _admin_ids_str.split(",") if x.strip().isdigit()]
"""List chat ID admin yang akan menerima notifikasi order baru."""


# ═══════════════════════════════════════════════════════════════
# CSV HEADERS
# ═══════════════════════════════════════════════════════════════

TRANSAKSI_HEADERS = [
    "waktu",           # Timestamp transaksi
    "id_transaksi",    # ID unik transaksi (INV-YYYYMMDD-XXXX)
    "kode",            # Kode barang
    "nama",            # Nama barang
    "ukuran",          # Ukuran yang dibeli
    "warna_kertas",    # Warna kertas pembungkus
    "warna_bunga",     # Warna bunga
    "qty",             # Jumlah item
    "harga",           # Harga satuan
    "subtotal",        # Total per item (harga × qty)
    "hpp",             # Harga Pokok Penjualan satuan
    "total_hpp",       # Total HPP (hpp × qty)
    "profit",          # Profit per item (subtotal - total_hpp)
    "diskon",          # Nilai diskon transaksi
    "ongkir",          # Biaya pengiriman
    "delivery",        # Jenis delivery (ambil/delivery)
    "total_transaksi", # Total akhir transaksi
    "source",          # Sumber: online/offline
]
"""Header kolom untuk file transaksi.csv."""


# ═══════════════════════════════════════════════════════════════
# APP INFO
# ═══════════════════════════════════════════════════════════════

APP_NAME = "SISTEM KASIR BUQEUET LIYA"
"""Nama aplikasi yang ditampilkan di header CLI."""

APP_VERSION = "2.0.0"
"""Versi aplikasi saat ini."""
