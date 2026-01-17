# SISTEM KASIR DAN MANAJEMEN TOKO BUQEUET LIYA

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

Aplikasi manajemen toko buket bunga yang terintegrasi antara **Point of Sales (Kasir CLI)** dan **Telegram Bot (Online Store)**. Sistem ini memungkinkan pengelolaan pesanan terpusat, manajemen stok real-time, dan laporan keuangan otomatis.

## 🌟 Fitur Utama

### 🤖 Telegram Bot (Online Store)
- **Katalog Interaktif**: Pembeli dapat melihat foto, harga, dan varian produk.
- **Order System**: Flow pemesanan langkah-demi-langkah (Pilih Produk -> Ukuran -> Warna -> Qty).
- **Notifikasi Admin**: Notifikasi realtime ke admin saat ada pesanan baru.
- **Tracking**: Pembeli bisa melihat status pesanan mereka.
- **Invoice Otomatis**: Generate invoice digital instan.

### 💻 CLI Kasir (Offline/Admin)
- **Point of Sales**: Mode kasir cepat untuk transaksi di toko.
- **Manajemen Order**: Proses pesanan bot (Update Status: Pending -> Processing -> Ready -> Complete).
- **Manajemen Katalog**: Tambah, edit, hapus produk dan stok.
- **Laporan Keuangan**: Rekap omzet, HPP, dan profit harian/bulanan.

## 📂 Struktur Project

Project ini menggunakan arsitektur modular:

```
.
├── core/               # 🔵 LOGIKA UTAMA (Shared)
│   ├── models/         # Struktur data (Barang, Order, Cart)
│   ├── services/       # Business logic (Order, Transaksi, Invoice)
│   ├── config.py       # Konfigurasi terpusat
│   └── utils.py        # Fungsi bantuan
│
├── cli/                # 🟢 INTERFACE KASIR
│   ├── handlers/       # Logika menu (Katalog, Transaksi, Order)
│   ├── ui/             # Helper tampilan terminal
│   └── main.py         # Entry point CLI
│
├── bot/                # 🟡 TELEGRAM BOT
│   ├── admin/          # Bot untuk Admin (Manage Order)
│   ├── buyer/          # Bot untuk Pembeli (Belanja)
│   └── shared/         # Logic notifikasi & session
│
├── app.py              # Launcher CLI
├── bot.py              # Launcher Bot
└── data/               # Penyimpanan data (JSON/CSV)
```

## 🚀 Cara Menjalankan

### Persiapan
1. Pastikan Python 3.10+ terinstall.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Setup file `.env`:
   ```env
   TELEGRAM_BUYER_BOT_TOKEN=your_token
   TELEGRAM_ADMIN_BOT_TOKEN=your_token
   ADMIN_CHAT_IDS=123456789
   ```

### Menjalankan Bot
```bash
python bot.py
```

### Menjalankan Kasir (CLI)
```bash
python app.py
```

## 👥 Kontributor
- **Rijal** - System Lead
- **Nihlah Auliya** - Programmer
- **Raffi Erlangga Dwi Tama** - Programmer

---
*Dibuat dengan ❤️ untuk UMKM Indonesia.*
