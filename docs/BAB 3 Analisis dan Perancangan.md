# BAB 3 Analisis dan Perancangan

## 3.1 Analisis Kebutuhan

### 3.1.1 Deskripsi Sistem

Sistem Kasir dan Manajemen Toko Buqeuet Liya adalah aplikasi Point of Sales (POS) terintegrasi yang menggabungkan **sistem kasir offline (CLI)** dan **toko online (Telegram Bot)**. Sistem ini dirancang untuk membantu UMKM toko buket dalam mengelola operasional harian, mulai dari katalog produk, transaksi penjualan, hingga rekapitulasi keuangan.

### 3.1.2 Kebutuhan Fungsional

| No | Fitur | Deskripsi |
|----|-------|-----------|
| 1 | **Manajemen Katalog** | Sistem dapat menampilkan, menambah, mengubah, dan menghapus data produk buket (CRUD). |
| 2 | **Transaksi Kasir (CLI)** | Kasir dapat melakukan transaksi penjualan langsung di toko dengan fitur keranjang belanja, diskon, dan pilihan delivery. |
| 3 | **Toko Online (Bot Telegram)** | Pembeli dapat melihat katalog, memilih produk, dan melakukan pemesanan melalui Telegram Bot. |
| 4 | **Manajemen Pesanan** | Admin dapat mengelola status pesanan dari bot (Pending → Processing → Ready → Completed). |
| 5 | **Notifikasi Realtime** | Sistem mengirim notifikasi ke admin saat ada pesanan baru dan ke pembeli saat status berubah. |
| 6 | **Generate Invoice** | Sistem dapat menghasilkan invoice/struk dalam format gambar secara otomatis. |
| 7 | **Rekapitulasi Keuangan** | Sistem dapat menampilkan laporan omzet, modal (HPP), dan profit berdasarkan periode (harian/mingguan/bulanan). |
| 8 | **Tracking Sumber Transaksi** | Sistem mencatat sumber transaksi (online/offline) untuk analisis performa channel penjualan. |

### 3.1.3 Kebutuhan Non-Fungsional

| No | Kebutuhan | Deskripsi |
|----|-----------|-----------|
| 1 | **Usability** | Antarmuka CLI yang intuitif dan Bot Telegram dengan flow yang mudah dipahami. |
| 2 | **Portability** | Aplikasi dapat berjalan di berbagai sistem operasi (Windows, Linux, MacOS). |
| 3 | **Reliability** | Data transaksi tersimpan dengan aman dalam format CSV dan JSON. |
| 4 | **Maintainability** | Arsitektur modular memudahkan pengembangan dan perbaikan. |

### 3.1.4 Analisis Data

#### A. Struktur Data Barang (Katalog)

Setiap produk buket memiliki atribut berikut:

| Atribut | Tipe Data | Keterangan |
|---------|-----------|------------|
| `kode` | String | Kode unik produk (contoh: A1, B2) |
| `nama` | String | Nama produk (contoh: Buqet Boneka) |
| `warna_kertas` | Array[String] | Pilihan warna kertas pembungkus |
| `warna_bunga` | Array[String] | Pilihan warna bunga |
| `ukuran` | Array[Ukuran] | Varian ukuran dengan harga berbeda |

**Struktur Ukuran:**
| Atribut | Tipe Data | Keterangan |
|---------|-----------|------------|
| `nama` | String | Nama ukuran (Mini/Standar/Besar) |
| `harga` | Float | Harga jual |
| `hpp` | Float | Harga Pokok Penjualan |
| `stok` | Integer | Jumlah stok tersedia |

#### B. Struktur Data Transaksi

| Atribut | Tipe Data | Keterangan |
|---------|-----------|------------|
| `waktu` | DateTime | Timestamp transaksi |
| `id_transaksi` | String | ID unik (format: INV-YYYYMMDD-XXXX) |
| `kode`, `nama` | String | Identitas barang |
| `ukuran`, `warna_kertas`, `warna_bunga` | String | Varian yang dipilih |
| `qty`, `harga`, `subtotal` | Numeric | Detail kuantitas dan harga |
| `hpp`, `total_hpp`, `profit` | Numeric | Perhitungan keuntungan |
| `diskon`, `ongkir`, `delivery` | Numeric/String | Info pengiriman |
| `source` | String | Sumber transaksi (online/offline) |

#### C. Struktur Data Order (Pesanan Bot)

| Atribut | Tipe Data | Keterangan |
|---------|-----------|------------|
| `order_id` | String | ID pesanan unik |
| `telegram_id` | Integer | ID Telegram pembeli |
| `nama_pembeli`, `wa_pembeli`, `alamat` | String | Data pembeli |
| `status` | Enum | pending/processing/ready/completed/cancelled |
| `items` | Array[OrderItem] | Daftar barang yang dipesan |
| `subtotal`, `diskon`, `ongkir`, `total` | Float | Perhitungan harga |

---

## 3.2 Perancangan Algoritma

### 3.2.1 Algoritma Menu Utama CLI

```
ALGORITMA: Menu_Utama_CLI

MULAI
    LOOP
        TAMPILKAN Header "SISTEM KASIR BUQEUET LIYA"
        TAMPILKAN Menu:
            [1] Katalog Barang
            [2] Transaksi Baru (Kasir)
            [3] Kelola Pesanan (Online)
            [4] Riwayat & Laporan
            [0] Keluar
        
        INPUT pilihan
        
        CASE pilihan:
            1: CALL Submenu_Katalog()
            2: CALL Flow_Transaksi_CLI()
            3: CALL Submenu_Order()
            4: CALL Submenu_Rekap()
            0: EXIT
            DEFAULT: TAMPILKAN "Pilihan tidak valid"
        END CASE
    END LOOP
SELESAI
```

### 3.2.2 Algoritma CRUD Katalog

```
ALGORITMA: CRUD_Katalog

MULAI
    LOAD data dari file "katalog buqet.json"
    
    LOOP
        TAMPILKAN Menu Katalog:
            [1] Tampilkan Semua
            [2] Cari Barang
            [3] Tambah Baru
            [4] Update Harga/Stok
            [5] Hapus Barang
            [0] Kembali
        
        INPUT pilihan
        
        IF pilihan == 1 THEN
            FOR EACH barang IN daftar_barang
                TAMPILKAN kode, nama, ukuran, stok
            END FOR
            
        ELSE IF pilihan == 3 THEN
            INPUT kode_baru
            IF kode_baru EXISTS THEN
                TAMPILKAN "Kode sudah ada"
                CONTINUE
            END IF
            
            INPUT nama_barang
            INPUT daftar_warna_kertas
            INPUT daftar_warna_bunga
            
            // Input varian ukuran
            LOOP
                INPUT nama_ukuran, harga, hpp, stok
                TAMBAHKAN ke list_ukuran
            UNTIL selesai
            
            BUAT objek Barang baru
            SIMPAN ke file JSON
            
        ELSE IF pilihan == 4 THEN
            CARI barang berdasarkan kode
            PILIH ukuran yang akan diupdate
            INPUT nilai baru (harga/stok)
            UPDATE objek
            SIMPAN ke file JSON
            
        ELSE IF pilihan == 5 THEN
            CARI barang
            KONFIRMASI "Yakin hapus?"
            IF ya THEN
                HAPUS dari daftar
                SIMPAN ke file JSON
            END IF
        END IF
        
        IF pilihan == 0 THEN BREAK
    END LOOP
SELESAI
```

### 3.2.3 Algoritma Transaksi Kasir (CLI)

```
ALGORITMA: Transaksi_Kasir_CLI

MULAI
    INISIALISASI keranjang = []
    
    // 1. Input Item ke Keranjang
    LOOP
        TAMPILKAN isi keranjang saat ini
        TAMPILKAN Menu: [1] Tambah, [2] Hapus, [3] Bayar
        
        IF pilih tambah THEN
            INPUT kode/nama barang
            CARI barang di katalog
            
            IF ditemukan THEN
                TAMPILKAN pilihan ukuran
                INPUT ukuran yang dipilih
                INPUT warna kertas dan bunga
                INPUT qty
                
                IF stok >= qty THEN
                    HITUNG subtotal = harga × qty
                    TAMBAHKAN item ke keranjang
                ELSE
                    TAMPILKAN "Stok tidak cukup"
                END IF
            END IF
        END IF
        
        IF pilih bayar THEN BREAK
    END LOOP
    
    // 2. Checkout
    INPUT nama pembeli
    INPUT diskon (opsional)
    INPUT metode: [1] Ambil Sendiri, [2] Delivery
    
    IF delivery THEN
        INPUT ongkir
        INPUT alamat
    END IF
    
    // 3. Kalkulasi
    total = subtotal - diskon + ongkir
    
    // 4. Finalisasi
    TAMPILKAN ringkasan pembayaran
    KONFIRMASI "Proses transaksi?"
    
    IF ya THEN
        // Update stok
        FOR EACH item IN keranjang
            KURANGI stok di katalog
        END FOR
        SIMPAN perubahan stok
        
        // Simpan transaksi
        GENERATE ID transaksi (INV-YYYYMMDD-XXXX)
        SIMPAN ke file transaksi.csv
        
        // Generate invoice
        CALL Generate_Invoice_Image()
        
        TAMPILKAN "Transaksi berhasil!"
    END IF
SELESAI
```

### 3.2.4 Algoritma Transaksi Bot (Buyer)

```
ALGORITMA: Transaksi_Bot_Buyer

MULAI
    // 1. User pilih katalog
    TAMPILKAN daftar produk (dengan tombol interaktif)
    TUNGGU user memilih produk
    
    // 2. Pilih varian
    TAMPILKAN pilihan ukuran & harga
    USER pilih ukuran
    
    IF stok tersedia THEN
        TAMPILKAN pilihan warna kertas
        TAMPILKAN pilihan warna bunga
        INPUT qty
        
        HITUNG subtotal
        TAMBAHKAN ke session keranjang
    ELSE
        TAMPILKAN "Maaf, stok habis"
        RETURN
    END IF
    
    // 3. Checkout
    USER klik "Checkout"
    
    IF keranjang kosong THEN RETURN
    
    INPUT nama penerima
    INPUT nomor WA
    INPUT metode: Ambil Sendiri / Delivery
    
    IF delivery THEN
        MINTA share lokasi
    END IF
    
    // 4. Buat Order
    GENERATE order_id
    SET status = PENDING
    SIMPAN order ke orders.json
    
    // 5. Notifikasi
    KIRIM invoice sementara ke buyer
    KIRIM notifikasi ke semua Admin "Ada order baru!"
    RESET session keranjang
SELESAI
```

### 3.2.5 Algoritma Manajemen Order (Admin)

```
ALGORITMA: Manajemen_Order_Admin

MULAI
    LOAD daftar order dari orders.json
    FILTER order yang status != COMPLETED
    SORT berdasarkan tanggal (terbaru dulu)
    
    TAMPILKAN daftar order (ID, Nama, Status)
    INPUT pilih order
    
    TAMPILKAN detail order lengkap
    
    SWITCH status_order:
        CASE PENDING:
            OPSI: [1] Terima/Proses, [2] Tolak
            IF terima THEN
                UPDATE status = PROCESSING
                NOTIFY buyer "Pesanan sedang diproses"
            END IF
            
        CASE PROCESSING:
            OPSI: [1] Set Ready (Selesai Dibuat)
            IF set ready THEN
                INPUT ongkir final (jika ada)
                INPUT diskon (jika ada)
                UPDATE status = READY
                HITUNG total final
                NOTIFY buyer "Pesanan siap! Total: Rp..."
            END IF
            
        CASE READY:
            OPSI: [1] Selesaikan (Lunas), [2] Batal
            IF selesaikan THEN
                UPDATE status = COMPLETED
                
                // Finalisasi
                GENERATE invoice final
                SIMPAN transaksi ke transaksi.csv
                KURANGI stok barang
                HAPUS order dari orders.json
                
                NOTIFY buyer "Pesanan selesai. Terima kasih!"
            END IF
    END SWITCH
    
    SIMPAN perubahan order
SELESAI
```

### 3.2.6 Algoritma Rekapitulasi Keuangan

```
ALGORITMA: Rekapitulasi_Keuangan

MULAI
    TAMPILKAN pilihan periode:
        [1] Harian (Hari Ini)
        [2] Mingguan
        [3] Bulanan
        [4] Semua Data
    
    INPUT pilihan
    TENTUKAN start_date dan end_date
    
    // Inisialisasi variabel akumulasi
    total_omzet = 0
    total_hpp = 0
    total_profit = 0
    total_transaksi_online = 0
    total_transaksi_offline = 0
    product_counter = {} // Map untuk produk terlaris
    
    // Proses data
    BACA file transaksi.csv
    
    FOR EACH transaksi IN file_csv
        IF tanggal BETWEEN start_date AND end_date THEN
            total_omzet += transaksi.subtotal
            total_hpp += transaksi.total_hpp
            total_profit += transaksi.profit
            
            IF transaksi.source == "online" THEN
                total_transaksi_online += 1
            ELSE
                total_transaksi_offline += 1
            END IF
            
            product_counter[transaksi.nama] += transaksi.qty
        END IF
    END FOR
    
    // Cari produk terlaris
    top_product = FIND MAX VALUE IN product_counter
    
    // Tampilkan laporan
    TAMPILKAN "═══ LAPORAN KEUANGAN ═══"
    TAMPILKAN "Periode: " + start_date + " s/d " + end_date
    TAMPILKAN "──────────────────────────"
    TAMPILKAN "Total Omzet    : Rp " + total_omzet
    TAMPILKAN "Total Modal    : Rp " + total_hpp
    TAMPILKAN "Gross Profit   : Rp " + total_profit
    TAMPILKAN "──────────────────────────"
    TAMPILKAN "Transaksi Online  : " + total_transaksi_online
    TAMPILKAN "Transaksi Offline : " + total_transaksi_offline
    TAMPILKAN "──────────────────────────"
    TAMPILKAN "Produk Terlaris: " + top_product
SELESAI
```

---

## 3.3 Struktur Menu Program

### 3.3.1 Hierarki Menu CLI (Aplikasi Kasir)

```
SISTEM KASIR BUQEUET LIYA v2.0.0
│
├── [1] Katalog Barang
│   ├── [1] Tampilkan Semua Katalog
│   ├── [2] Cari Barang
│   ├── [3] Tambah Barang Baru
│   ├── [4] Update Harga/Stok
│   ├── [5] Hapus Barang
│   └── [0] Kembali
│
├── [2] Transaksi Baru (Kasir)
│   ├── Keranjang Belanja
│   │   ├── [1] Tambah Item
│   │   ├── [2] Hapus Item
│   │   └── [3] Bayar/Checkout
│   ├── Input Data Pembeli
│   ├── Pilih Metode (Ambil/Delivery)
│   └── Konfirmasi & Cetak Struk
│
├── [3] Kelola Pesanan (Online)
│   ├── Daftar Pesanan Aktif
│   ├── Detail Pesanan
│   │   ├── [PENDING] → Terima/Tolak
│   │   ├── [PROCESSING] → Set Ready
│   │   └── [READY] → Selesaikan/Batal
│   └── [0] Kembali
│
├── [4] Riwayat & Laporan
│   ├── [1] Riwayat Transaksi
│   ├── [2] Rekap Harian
│   ├── [3] Rekap Mingguan
│   ├── [4] Rekap Bulanan
│   └── [0] Kembali
│
└── [0] Keluar
```

### 3.3.2 Flow Menu Telegram Bot (Buyer)

```
BOT: Buqeuet Liya Shop
│
├── /start
│   ├── [📦 Lihat Katalog]
│   │   ├── Tampil Daftar Produk
│   │   │   └── Pilih Produk
│   │   │       ├── Pilih Ukuran
│   │   │       ├── Pilih Warna Kertas
│   │   │       ├── Pilih Warna Bunga
│   │   │       ├── Input Qty
│   │   │       └── Tambah ke Keranjang
│   │   └── [🛒 Keranjang]
│   │       └── [✅ Checkout]
│   │           ├── Input Nama
│   │           ├── Input No. WA
│   │           ├── Pilih: Ambil/Delivery
│   │           └── Konfirmasi Order
│   │
│   ├── [📋 Status Pesanan]
│   │   └── Tampil Daftar Order User
│   │       └── Detail Status Order
│   │
│   └── [📞 Hubungi Admin]
│       └── Link ke WA Admin
│
└── /help → Panduan Penggunaan
```

### 3.3.3 Flow Menu Telegram Bot (Admin)

```
BOT: Buqeuet Liya Admin
│
├── /start
│   ├── [📋 List Pesanan]
│   │   ├── Filter: All / Pending / Processing / Ready
│   │   └── Pilih Order
│   │       ├── Detail Order
│   │       └── Aksi Berdasarkan Status
│   │           ├── PENDING → Proses / Tolak
│   │           ├── PROCESSING → Set Ready
│   │           └── READY → Complete / Cancel
│   │
│   ├── [📊 Rekap Keuangan]
│   │   ├── Harian
│   │   ├── Mingguan
│   │   └── Bulanan
│   │
│   └── [📢 Broadcast]
│       └── Kirim Pesan ke Semua Buyer
│
└── Notifikasi Otomatis
    └── "🔔 Ada order baru! [Order ID]"
```

### 3.3.4 Diagram Arsitektur Sistem

```
┌────────────────────────────────────────────────────────────────┐
│                     BUQEUET LIYA SYSTEM                        │
├─────────────────────────┬──────────────────────────────────────┤
│    CLI (Offline/Admin)  │       Telegram Bot (Online)          │
│                         │                                      │
│  ┌─────────────────┐    │    ┌──────────────┐  ┌────────────┐  │
│  │   cli/main.py   │    │    │  Buyer Bot   │  │ Admin Bot  │  │
│  │    (Entry)      │    │    │              │  │            │  │
│  └────────┬────────┘    │    └──────┬───────┘  └─────┬──────┘  │
│           │             │           │                │         │
│  ┌────────┴────────┐    │           └───────┬────────┘         │
│  │    handlers/    │    │                   │                  │
│  │ katalog,order,  │    │    ┌──────────────┴───────────────┐  │
│  │   transaksi     │    │    │       bot/shared/            │  │
│  └────────┬────────┘    │    │    (session, notifikasi)     │  │
│           │             │    └──────────────┬───────────────┘  │
├───────────┴─────────────┴───────────────────┴──────────────────┤
│                        CORE (Shared Logic)                     │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    core/services/                         │  │
│  │  barang_service  order_service  transaksi_service        │  │
│  │                  invoice_service                          │  │
│  └────────────────────────────┬─────────────────────────────┘  │
│                               │                                │
│  ┌────────────────────────────┴─────────────────────────────┐  │
│  │                     core/models/                          │  │
│  │      Barang    Cart/CartItem    Order/OrderItem           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                               │                                │
│  ┌────────────────────────────┴─────────────────────────────┐  │
│  │                     core/config.py                        │  │
│  │           (Path, Token, Headers, Constants)               │  │
│  └──────────────────────────────────────────────────────────┘  │
├────────────────────────────────────────────────────────────────┤
│                       DATA STORAGE                             │
│                                                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐  │
│  │ katalog buqet   │  │   orders.json   │  │ transaksi.csv  │  │
│  │     .json       │  │  (Order Aktif)  │  │   (History)    │  │
│  └─────────────────┘  └─────────────────┘  └────────────────┘  │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   data/invoice/                          │   │
│  │              (Generated Invoice Images)                  │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

### 3.3.5 Status Flow Pesanan

```
┌──────────┐     Buyer       ┌────────────┐     Admin      ┌───────────┐
│  START   │ ─── Order ───→  │  PENDING   │ ─── Accept ──→ │PROCESSING │
└──────────┘                 └────────────┘                └─────┬─────┘
                                   │                             │
                                   │ Reject                      │ Set Ready
                                   ↓                             ↓
                             ┌──────────┐                  ┌───────────┐
                             │CANCELLED │                  │   READY   │
                             └──────────┘                  └─────┬─────┘
                                                                 │
                                                    ┌────────────┴────────────┐
                                                    │                         │
                                               Complete                    Cancel
                                                    ↓                         ↓
                                             ┌───────────┐             ┌──────────┐
                                             │ COMPLETED │             │CANCELLED │
                                             │ (Archived │             └──────────┘
                                             │  to CSV)  │
                                             └───────────┘
```
