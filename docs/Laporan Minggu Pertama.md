# LAPORAN MINGGU PERTAMA
## Sistem Kasir UMKM Buqeuet Liya

---

**Nama Proyek:** Sistem Kasir Buqeuet Liya  
**Deskripsi:** Aplikasi Point of Sale (POS) untuk UMKM penjualan buket bunga  
**Tanggal:** 31 Desember 2025 - 7 Januari 2026

---

## DAFTAR ISI

1. [Pendahuluan](#1-pendahuluan)
2. [Deskripsi Fitur](#2-deskripsi-fitur)
3. [Flowchart](#3-flowchart)
4. [Pseudocode](#4-pseudocode)

---

## 1. PENDAHULUAN

### 1.1 Latar Belakang
Sistem Kasir Buqeuet Liya adalah aplikasi berbasis command line (CLI) yang dikembangkan untuk membantu UMKM dalam mengelola transaksi penjualan buket bunga. Aplikasi ini mencakup fitur manajemen katalog, proses transaksi, dan pelaporan.

### 1.2 Tujuan
- Mempermudah pencatatan transaksi penjualan
- Mengelola stok dan katalog produk buket
- Menghasilkan struk/invoice transaksi
- Menyediakan rekap pendapatan

### 1.3 Teknologi yang Digunakan
- **Bahasa Pemrograman:** Python 3.10+
- **Penyimpanan Data:** JSON (katalog), CSV (transaksi)
- **Library:** Pillow (untuk export struk gambar)

---

## 2. DESKRIPSI FITUR

### 2.1 Menu Utama
Menu utama aplikasi menampilkan 8 pilihan menu:
1. **Tampilkan Katalog Buqet** - Melihat semua produk
2. **Tambah Katalog Buqet** - Menambah produk baru
3. **Update Katalog** - Mengubah harga/stok produk
4. **Cari Buqet** - Mencari produk berdasarkan keyword
5. **Transaksi Penjualan** - Memproses penjualan
6. **Riwayat Transaksi** - Melihat transaksi terakhir
7. **Rekap Pendapatan** - Melihat total pendapatan

### 2.2 Struktur Data

#### Katalog Barang (JSON)
Setiap barang memiliki:
- Kode barang (unik)
- Nama katalog
- Warna kertas (pilihan)
- Warna bunga (pilihan)
- Ukuran dengan harga berbeda (Mini, Standar, Besar)

#### Transaksi (CSV)
Setiap transaksi menyimpan:
- ID transaksi
- Waktu transaksi
- Detail barang (kode, nama, ukuran, warna)
- Quantity dan subtotal
- Diskon, ongkir, dan total

---

## 3. FLOWCHART

### 3.1 Main Menu
![Main Menu](flowchart/01_main_menu.png)

**Penjelasan:**
Main menu merupakan entry point aplikasi yang menampilkan pilihan menu dan mengarahkan user ke fitur yang dipilih. Program berjalan dalam loop hingga user memilih untuk keluar.

---

### 3.2 Tampil Katalog
![Tampil Katalog](flowchart/02_tampil_katalog.png)

**Penjelasan:**
Fitur ini menampilkan seluruh katalog buket yang tersedia. Jika data kosong, akan menampilkan pesan error. Setiap barang ditampilkan beserta pilihan warna dan harga per ukuran.

---

### 3.3 Tambah Katalog
![Tambah Katalog](flowchart/03_tambah_katalog.png)

**Penjelasan:**
Proses penambahan katalog baru meliputi:
1. Input kode barang (validasi unik)
2. Input nama katalog
3. Input warna kertas dan bunga
4. Input harga, HPP, dan stok untuk setiap ukuran (Mini/Standar/Besar)

---

### 3.4 Update Katalog
![Update Katalog](flowchart/04_update_katalog.png)

**Penjelasan:**
Fitur update memungkinkan perubahan:
- Harga jual
- HPP (Harga Pokok Penjualan)
- Stok (bisa tambah atau kurang)

User memilih barang berdasarkan kode, kemudian memilih ukuran dan jenis update yang diinginkan.

---

### 3.5 Cari Katalog
![Cari Katalog](flowchart/05_cari_katalog.png)

**Penjelasan:**
Pencarian dilakukan berdasarkan keyword yang bisa berupa kode atau nama barang. Pencarian bersifat case-insensitive dan menggunakan substring matching.

---

### 3.6 Proses Transaksi
![Proses Transaksi](flowchart/06_proses_transaksi.png)

**Penjelasan:**
Ini adalah flowchart utama proses transaksi yang terdiri dari beberapa sub-proses:
1. Input barang ke keranjang
2. Hitung diskon
3. Input info pembeli
4. Pilih pengantaran
5. Proses pembayaran
6. Simpan transaksi

---

### 3.7 Proses Pemilihan Barang
![Proses Pemilihan Barang](flowchart/07_proses_pemilihan_barang.png)

**Penjelasan:**
Sub-proses untuk memilih barang dalam transaksi:
1. Input kode barang
2. Pilih warna kertas
3. Pilih warna bunga
4. Pilih ukuran
5. Input quantity
6. Validasi stok

---

### 3.8 Hitung Diskon
![Hitung Diskon](flowchart/08_hitung_diskon.png)

**Penjelasan:**
Sub-proses untuk menghitung diskon:
1. Tanya apakah pakai diskon
2. Jika ya, input persentase (0-100)
3. Hitung nilai diskon dari total

---

### 3.9 Pilih Pengantaran
![Pilih Pengantaran](flowchart/09_pilih_pengantaran.png)

**Penjelasan:**
Pilihan pengantaran:
1. **Full Delivery** - dengan input ongkir
2. **Ambil Sendiri** - gratis ongkir

---

### 3.10 Finalisasi Transaksi
![Finalisasi Transaksi](flowchart/10_finalisasi_transaksi.png)

**Penjelasan:**
Proses akhir transaksi:
1. Tampilkan struk
2. Proses pembayaran
3. Hitung kembalian
4. Simpan ke file

---

### 3.11 Kembalikan Stok
![Kembalikan Stok](flowchart/11_kembalikan_stok.png)

**Penjelasan:**
Proses rollback stok jika transaksi dibatalkan (misal: uang kurang). Stok yang sudah dikurangi akan dikembalikan.

---

### 3.12 Riwayat Transaksi
![Riwayat Transaksi](flowchart/12_riwayat_transaksi.png)

**Penjelasan:**
Menampilkan daftar transaksi terakhir dari file CSV. Data ditampilkan per item dengan detail lengkap.

---

### 3.13 Rekap Pendapatan
![Rekap Pendapatan](flowchart/13_rekap_pendapatan.png)

**Penjelasan:**
Menghitung dan menampilkan:
- Jumlah transaksi unik
- Total pendapatan keseluruhan

---

## 4. PSEUDOCODE

### 4.1 Tampil Katalog

```
FUNCTION tampil_semua_barang(daftar_barang)
    
    IF daftar_barang IS EMPTY THEN
        PRINT "Data barang masih kosong"
        RETURN
    END IF
    
    PRINT "DAFTAR KATALOG BUQET"
    
    SET nomor = 1
    FOR EACH barang IN daftar_barang DO
        
        PRINT nomor, barang.kode, barang.nama
        
        IF barang.warna_kertas NOT EMPTY THEN
            PRINT "Warna Kertas:", barang.warna_kertas
        END IF
        
        IF barang.warna_bunga NOT EMPTY THEN
            PRINT "Warna Bunga:", barang.warna_bunga
        END IF
        
        PRINT "Ukuran    Harga       HPP      Stok"
        PRINT "------------------------------------"
        
        FOR EACH ukuran IN barang.daftar_ukuran DO
            PRINT ukuran.nama, ukuran.harga, ukuran.hpp, ukuran.stok
        END FOR
        
        SET nomor = nomor + 1
    END FOR

END FUNCTION
```

**Penjelasan:**
- Fungsi menerima parameter `daftar_barang` berupa array/list
- Melakukan pengecekan apakah data kosong
- Menggunakan loop `FOR EACH` untuk iterasi setiap barang
- Menampilkan detail ukuran dengan nested loop

---

### 4.2 Tambah Katalog

```
CONSTANT PILIHAN_UKURAN = ["Mini", "Standar", "Besar"]

FUNCTION tambah_barang(daftar_barang)
    
    PRINT "TAMBAH KATALOG BUQET"
    
    INPUT kode FROM user
    SET kode = UPPERCASE(kode)
    
    // Cek apakah kode sudah ada
    IF cari_by_kode(daftar_barang, kode) IS NOT NULL THEN
        PRINT "Kode sudah ada"
        RETURN FALSE
    END IF
    
    INPUT nama FROM user
    INPUT warna_kertas FROM user     // pisahkan dengan koma
    INPUT warna_bunga FROM user      // pisahkan dengan koma
    
    // Pecah warna menjadi array
    SET list_warna_kertas = SPLIT(warna_kertas, ",")
    SET list_warna_bunga = SPLIT(warna_bunga, ",")
    
    // Input harga per ukuran
    SET list_ukuran = []
    
    FOR EACH nama_ukuran IN PILIHAN_UKURAN DO
        PRINT "Input untuk ukuran:", nama_ukuran
        
        INPUT harga FROM user
        INPUT hpp FROM user
        INPUT stok FROM user
        
        SET ukuran_baru = CREATE UkuranBarang(nama_ukuran, harga, hpp, stok)
        APPEND ukuran_baru TO list_ukuran
    END FOR
    
    // Buat barang baru
    SET barang_baru = CREATE Barang(kode, nama, list_warna_kertas, 
                                     list_warna_bunga, list_ukuran)
    
    APPEND barang_baru TO daftar_barang
    CALL simpan_barang(daftar_barang)
    
    PRINT "Katalog berhasil ditambahkan"
    RETURN TRUE

END FUNCTION
```

**Penjelasan:**
- Validasi kode unik sebelum menambah
- Warna diinput sebagai string dengan koma, lalu di-split menjadi array
- Loop untuk input data setiap ukuran (Mini, Standar, Besar)
- Setelah berhasil, data disimpan ke file JSON

---

### 4.3 Update Katalog

```
FUNCTION update_barang(daftar_barang)
    
    PRINT "UPDATE KATALOG BUQET"
    
    INPUT kode FROM user
    SET kode = UPPERCASE(kode)
    
    SET barang = cari_by_kode(daftar_barang, kode)
    
    IF barang IS NULL THEN
        PRINT "Barang tidak ditemukan"
        RETURN FALSE
    END IF
    
    PRINT "Barang ditemukan:", barang.kode, barang.nama
    
    // Tampilkan ukuran yang tersedia
    PRINT "Pilih ukuran:"
    SET nomor = 1
    FOR EACH ukuran IN barang.daftar_ukuran DO
        PRINT nomor, ukuran.nama, ukuran.harga, ukuran.hpp, ukuran.stok
        SET nomor = nomor + 1
    END FOR
    
    INPUT pilih_ukuran FROM user
    SET ukuran = barang.daftar_ukuran[pilih_ukuran - 1]
    
    // Pilih jenis update
    PRINT "Pilih update:"
    PRINT "1. Update harga"
    PRINT "2. Update HPP"
    PRINT "3. Update stok"
    
    INPUT pilihan FROM user
    
    IF pilihan == 1 THEN
        INPUT harga_baru FROM user
        SET ukuran.harga = harga_baru
        PRINT "Harga berhasil diupdate"
        
    ELSE IF pilihan == 2 THEN
        INPUT hpp_baru FROM user
        SET ukuran.hpp = hpp_baru
        PRINT "HPP berhasil diupdate"
        
    ELSE IF pilihan == 3 THEN
        INPUT perubahan_stok FROM user  // bisa positif atau negatif
        SET stok_baru = ukuran.stok + perubahan_stok
        
        IF stok_baru < 0 THEN
            PRINT "Stok tidak boleh negatif"
            RETURN FALSE
        END IF
        
        SET ukuran.stok = stok_baru
        PRINT "Stok berhasil diupdate"
    END IF
    
    CALL simpan_barang(daftar_barang)
    RETURN TRUE

END FUNCTION
```

**Penjelasan:**
- Cari barang berdasarkan kode
- User memilih ukuran yang ingin diupdate
- Ada 3 pilihan: update harga, HPP, atau stok
- Untuk stok, bisa input positif (tambah) atau negatif (kurang)
- Validasi stok tidak boleh negatif

---

### 4.4 Cari Katalog

```
FUNCTION cari_barang(daftar_barang)
    
    PRINT "CARI KATALOG"
    
    INPUT keyword FROM user
    
    SET hasil = pencarian_barang(daftar_barang, keyword)
    
    IF hasil IS EMPTY THEN
        PRINT "Tidak ada hasil pencarian"
        RETURN
    END IF
    
    PRINT "Ditemukan", LENGTH(hasil), "hasil"
    CALL tampil_semua_barang(hasil)

END FUNCTION


FUNCTION pencarian_barang(daftar_barang, keyword)
    
    SET keyword = LOWERCASE(keyword)
    SET hasil = []
    
    FOR EACH barang IN daftar_barang DO
        SET kode_lower = LOWERCASE(barang.kode)
        SET nama_lower = LOWERCASE(barang.nama)
        
        IF keyword IN kode_lower OR keyword IN nama_lower THEN
            APPEND barang TO hasil
        END IF
    END FOR
    
    RETURN hasil

END FUNCTION
```

**Penjelasan:**
- Pencarian bersifat case-insensitive (menggunakan LOWERCASE)
- Mencari di kode DAN nama barang
- Menggunakan substring matching (keyword bisa ada di mana saja)
- Hasil ditampilkan menggunakan fungsi `tampil_semua_barang`

---

### 4.5 Proses Transaksi

```
FUNCTION proses_transaksi(daftar_barang)
    
    IF daftar_barang IS EMPTY THEN
        PRINT "Data barang kosong"
        RETURN FALSE
    END IF
    
    PRINT "TRANSAKSI PENJUALAN BUQET"
    PRINT "Ketik SELESAI untuk mengakhiri"
    
    SET keranjang = []
    
    // LOOP INPUT BARANG
    WHILE TRUE DO
        INPUT kode FROM user
        
        IF kode IS EMPTY THEN
            PRINT "Kode tidak boleh kosong"
            CONTINUE
        END IF
        
        IF UPPERCASE(kode) == "SELESAI" THEN
            BREAK
        END IF
        
        SET barang = cari_by_kode(daftar_barang, UPPERCASE(kode))
        
        IF barang IS NULL THEN
            PRINT "Kode tidak ditemukan"
            CONTINUE
        END IF
        
        PRINT "Barang:", barang.nama
        
        // Pilih warna kertas
        SET warna_kertas_dipilih = "-"
        IF barang.warna_kertas NOT EMPTY THEN
            PRINT "Pilih warna kertas:"
            SET nomor = 1
            FOR EACH warna IN barang.warna_kertas DO
                PRINT nomor, warna
                SET nomor = nomor + 1
            END FOR
            INPUT pilih_wk FROM user
            SET warna_kertas_dipilih = barang.warna_kertas[pilih_wk - 1]
        END IF
        
        // Pilih warna bunga
        SET warna_bunga_dipilih = "-"
        IF barang.warna_bunga NOT EMPTY THEN
            PRINT "Pilih warna bunga:"
            SET nomor = 1
            FOR EACH warna IN barang.warna_bunga DO
                PRINT nomor, warna
                SET nomor = nomor + 1
            END FOR
            INPUT pilih_wb FROM user
            SET warna_bunga_dipilih = barang.warna_bunga[pilih_wb - 1]
        END IF
        
        // Pilih ukuran
        PRINT "Pilih ukuran:"
        FOR EACH ukuran IN barang.daftar_ukuran DO
            PRINT ukuran.nama, ukuran.harga, "Stok:", ukuran.stok
        END FOR
        
        INPUT pilih_ukuran FROM user
        SET ukuran = barang.daftar_ukuran[pilih_ukuran - 1]
        
        IF ukuran.stok == 0 THEN
            PRINT "Stok habis"
            CONTINUE
        END IF
        
        // Input jumlah
        INPUT qty FROM user
        
        IF qty > ukuran.stok THEN
            PRINT "Qty melebihi stok"
            CONTINUE
        END IF
        
        // Buat item transaksi
        SET subtotal = qty * ukuran.harga
        SET item = CREATE TransaksiItem(barang.kode, barang.nama, ukuran.nama,
                                         warna_kertas_dipilih, warna_bunga_dipilih,
                                         qty, ukuran.harga, subtotal)
        
        APPEND item TO keranjang
        SET ukuran.stok = ukuran.stok - qty
        PRINT "Ditambahkan ke keranjang"
    END WHILE
    
    // Cek keranjang kosong
    IF keranjang IS EMPTY THEN
        PRINT "Tidak ada item, transaksi dibatalkan"
        RETURN FALSE
    END IF
    
    // Hitung total
    SET total = 0
    FOR EACH item IN keranjang DO
        SET total = total + item.subtotal
    END FOR
    
    // Hitung diskon
    SET diskon = hitung_diskon(total)
    
    // Info pembeli
    INPUT nama_pembeli FROM user
    INPUT tanggal_pengambilan FROM user
    
    // Pilih pengantaran
    SET (ongkir, tipe_delivery) = pilih_pengantaran()
    
    // Hitung total bayar
    SET total_bayar = total - diskon + ongkir
    
    // Tampilkan struk
    CALL tampil_struk(keranjang, total, diskon, ongkir, total_bayar)
    
    // Proses pembayaran
    INPUT uang_bayar FROM user
    
    IF uang_bayar < total_bayar THEN
        PRINT "Uang kurang, transaksi dibatalkan"
        CALL kembalikan_stok(daftar_barang, keranjang)
        RETURN FALSE
    END IF
    
    SET kembalian = uang_bayar - total_bayar
    PRINT "Kembalian:", kembalian
    
    // Simpan transaksi
    CALL simpan_transaksi(keranjang, diskon, ongkir, tipe_delivery, total_bayar)
    CALL simpan_barang(daftar_barang)
    
    PRINT "Transaksi berhasil disimpan"
    RETURN TRUE

END FUNCTION
```

**Penjelasan:**
- Ini adalah fungsi paling kompleks dalam sistem
- Menggunakan `WHILE TRUE` loop untuk input multiple items
- User bisa keluar dari loop dengan mengetik "SELESAI"
- Stok langsung dikurangi saat item ditambahkan ke keranjang
- Jika pembayaran gagal (uang kurang), stok dikembalikan (rollback)
- Transaksi disimpan ke file CSV

---

### 4.6 Riwayat Transaksi

```
FUNCTION tampil_riwayat(limit)
    
    SET daftar_transaksi = muat_transaksi(limit)
    
    IF daftar_transaksi IS EMPTY THEN
        PRINT "Belum ada transaksi"
        RETURN
    END IF
    
    PRINT "RIWAYAT TRANSAKSI TERAKHIR"
    
    FOR EACH transaksi IN daftar_transaksi DO
        PRINT "ID:", transaksi.id_transaksi
        PRINT "Waktu:", transaksi.waktu
        PRINT "Kode:", transaksi.kode, "-", transaksi.nama
        PRINT "Ukuran:", transaksi.ukuran
        PRINT "Warna Kertas:", transaksi.warna_kertas
        PRINT "Warna Bunga:", transaksi.warna_bunga
        PRINT "Qty:", transaksi.qty
        PRINT "Subtotal:", transaksi.subtotal
        PRINT "Delivery:", transaksi.delivery
        PRINT "Ongkir:", transaksi.ongkir
        PRINT "Total Transaksi:", transaksi.total_transaksi
        PRINT "------------------------"
    END FOR

END FUNCTION
```

**Penjelasan:**
- Membaca data transaksi dari file CSV
- Parameter `limit` membatasi jumlah transaksi yang ditampilkan
- Menampilkan detail lengkap per item transaksi

---

### 4.7 Rekap Pendapatan

```
FUNCTION tampil_rekap()
    
    SET (jumlah_transaksi, total_pendapatan) = hitung_rekap()
    
    IF jumlah_transaksi == 0 THEN
        PRINT "Belum ada transaksi"
        RETURN
    END IF
    
    PRINT "REKAP PENDAPATAN"
    PRINT "Jumlah transaksi:", jumlah_transaksi
    PRINT "Total pendapatan: Rp", total_pendapatan

END FUNCTION


FUNCTION hitung_rekap()
    
    // Dictionary untuk menyimpan total per transaksi unik
    SET total_per_transaksi = {}
    
    OPEN file transaksi.csv
    FOR EACH baris IN file DO
        SET id_trx = baris.id_transaksi
        SET total = baris.total_transaksi
        
        // Simpan total (akan overwrite jika ID sama)
        SET total_per_transaksi[id_trx] = total
    END FOR
    CLOSE file
    
    IF total_per_transaksi IS EMPTY THEN
        RETURN (0, 0)
    END IF
    
    SET jumlah_transaksi = LENGTH(total_per_transaksi)
    SET total_pendapatan = SUM(ALL VALUES IN total_per_transaksi)
    
    RETURN (jumlah_transaksi, total_pendapatan)

END FUNCTION
```

**Penjelasan:**
- Menggunakan dictionary untuk menghitung transaksi unik
- Karena satu transaksi bisa memiliki banyak item (baris), dictionary memastikan setiap transaksi hanya dihitung sekali
- Mengembalikan tuple (jumlah_transaksi, total_pendapatan)

---

### 4.8 Main Menu

```
FUNCTION main_menu()
    
    SET daftar_barang = muat_barang()
    
    WHILE TRUE DO
        
        PRINT "SISTEM KASIR BUQEUET LIYA"
        PRINT "1. Tampilkan Katalog Buqet"
        PRINT "2. Tambah Katalog Buqet"
        PRINT "3. Update Katalog"
        PRINT "4. Cari Buqet"
        PRINT "5. Transaksi Penjualan"
        PRINT "6. Riwayat Transaksi"
        PRINT "7. Rekap Pendapatan"
        PRINT "0. Keluar"
        
        INPUT pilihan FROM user
        
        IF pilihan == "1" THEN
            CALL tampil_semua_barang(daftar_barang)
            
        ELSE IF pilihan == "2" THEN
            CALL tambah_barang(daftar_barang)
            
        ELSE IF pilihan == "3" THEN
            CALL update_barang(daftar_barang)
            
        ELSE IF pilihan == "4" THEN
            CALL cari_barang(daftar_barang)
            
        ELSE IF pilihan == "5" THEN
            CALL proses_transaksi(daftar_barang)
            // Reload data setelah transaksi
            SET daftar_barang = muat_barang()
            
        ELSE IF pilihan == "6" THEN
            CALL tampil_riwayat(20)
            
        ELSE IF pilihan == "7" THEN
            CALL tampil_rekap()
            
        ELSE IF pilihan == "0" THEN
            PRINT "Sampai jumpa!"
            BREAK
            
        ELSE
            PRINT "Menu tidak valid"
        END IF
        
    END WHILE

END FUNCTION


// Entry point program
CALL main_menu()
```

**Penjelasan:**
- Menggunakan `WHILE TRUE` loop untuk menampilkan menu berulang
- Setelah transaksi, data barang di-reload untuk sinkronisasi stok
- Loop berakhir ketika user memilih opsi "0" (Keluar)
- Menggunakan struktur `IF-ELSE IF` untuk menangani pilihan menu

---

## KESIMPULAN

Pada minggu pertama ini, telah diselesaikan:

1. **Perancangan Flowchart** - 13 diagram flowchart yang mencakup seluruh alur program
2. **Penulisan Pseudocode** - 8 modul pseudocode untuk setiap fitur utama
3. **Dokumentasi** - Penjelasan detail untuk setiap flowchart dan pseudocode

Sistem ini dirancang dengan arsitektur modular yang memisahkan:
- **Models** - Struktur data (Barang, Transaksi)
- **Services** - Business logic (manajemen katalog, transaksi)
- **UI** - User interface (menu, input/output)

---

*Dokumen ini dibuat sebagai bagian dari Laporan Mingguan Proyek Sistem Kasir Buqeuet Liya*
