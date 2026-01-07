# 🧾 SISTEM KASIR BUQEUET LIYA

Sistem Kasir **Buqeuet Liya** adalah aplikasi kasir berbasis **Command Line Interface (CLI)** yang dirancang untuk membantu pengelolaan penjualan buqet secara sederhana dan efisien. Aplikasi ini mendukung manajemen produk, transaksi penjualan, penyimpanan riwayat transaksi, serta perhitungan **pendapatan, HPP (Harga Pokok Produksi), dan keuntungan** secara otomatis.

---

## ✨ Fitur Utama

- 📦 Manajemen katalog produk buqet
- 🛒 Transaksi penjualan dengan perhitungan otomatis
- 🧮 Perhitungan HPP dan keuntungan (internal, tidak tampil di struk)
- 🧾 Riwayat transaksi tersimpan dalam file CSV
- 📊 Rekap pendapatan, modal (HPP), dan laba
- 💻 Antarmuka CLI sederhana dan mudah digunakan

---

## 📋 Tampilan Menu Utama

```text
=== SISTEM KASIR BUQEUET LIYA ===
1) Tampilkan Katalog Buqet
2) Tambah Katalog Buqet
3) Update Katalog
4) Cari Buqet
5) Transaksi penjualan
6) Riwayat transaksi
7) Rekap pendapatan
0) Keluar
```

---

## 🗂️ Struktur Folder Proyek

```text
alpro-mini-project/
│
├── app.py                     # Entry point aplikasi
│
├── data/
│   ├── barang.json            # Data katalog produk buqet
│   └── transaksi.csv          # Riwayat transaksi penjualan
│
├── src/
│   ├── models/
│   │   ├── barang.py          # Model data produk
│   │   └── transaksi.py       # Model data transaksi & rekap
│   │
│   ├── services/
│   │   ├── barang_service.py  # Logika pengelolaan produk
│   │   └── transaksi_service.py # Logika transaksi & perhitungan
│   │
│   └── ui/
│       └── menu.py            # Tampilan dan navigasi menu CLI
│
├── README.md                  # Dokumentasi proyek
└── requirements.txt           # (Opsional) dependency Python
```

---

## 🧭 Flow Penggunaan Aplikasi (Step by Step)

### 1️⃣ Menjalankan Aplikasi

Jalankan perintah berikut pada terminal:

```bash
py app.py
```

Sistem akan menampilkan menu utama.

---

### 2️⃣ Menambahkan Produk Buqet

1. Pilih menu **2) Tambah Katalog Buqet**
2. Masukkan data produk:

   - Kode produk
   - Nama buqet
   - Ukuran
   - Warna kertas
   - Warna bunga
   - Harga jual
   - HPP (Harga Pokok Produksi)

3. Data produk akan disimpan ke dalam file `barang.json`

📌 **Catatan:** HPP hanya digunakan untuk perhitungan internal dan tidak ditampilkan pada struk pelanggan.

---

### 3️⃣ Melihat & Mencari Produk

- **Menu 1** → Menampilkan seluruh katalog produk
- **Menu 4** → Mencari produk berdasarkan kode atau nama

---

### 4️⃣ Melakukan Transaksi Penjualan

1. Pilih menu **5) Transaksi penjualan**
2. Pilih produk dari katalog
3. Masukkan jumlah pembelian (qty)
4. Sistem otomatis menghitung:

   - Subtotal
   - Total HPP
   - Profit per item

5. Masukkan:

   - Diskon (jika ada)
   - Ongkir
   - Metode delivery

6. Transaksi disimpan ke file `transaksi.csv`

---

### 5️⃣ Melihat Riwayat Transaksi

1. Pilih menu **6) Riwayat transaksi**
2. Sistem menampilkan data transaksi dari file CSV

---

### 6️⃣ Melihat Rekap Pendapatan

1. Pilih menu **7) Rekap pendapatan**
2. Sistem menampilkan ringkasan:

   - Jumlah transaksi
   - Total pendapatan
   - Total modal (HPP)
   - Total keuntungan

**Contoh Output:**

```text
===== REKAP TRANSAKSI =====
Jumlah Transaksi : 2
Total Pendapatan : Rp 391,300
Total Modal (HPP): Rp 46,000
Keuntungan       : Rp 56,000
===========================
```

---

### 7️⃣ Keluar Aplikasi

Pilih menu **0) Keluar** untuk menghentikan aplikasi.

---

## 📁 Penyimpanan Data

- **barang.json** → Menyimpan data produk buqet
- **transaksi.csv** → Menyimpan histori transaksi penjualan
- Data bersifat persisten dan tidak hilang saat aplikasi ditutup

---

## 🎯 Tujuan Pengembangan

- Membantu pencatatan penjualan buqet secara rapi
- Menghindari kesalahan perhitungan manual
- Mempermudah analisis keuntungan usaha
- Sebagai proyek pembelajaran Algoritma dan Pemrograman

---

## 👩‍💻 Author

**KELOMPOK 1 ALGORITMA DAN PEMROGRAMAN DASAR**

1. Rijal
2. Nihlah Auliya
3. Rafi Erlangga Dwi Tama

Mahasiswa Teknik Informatika
