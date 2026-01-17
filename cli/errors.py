"""
Centralized Error Messages untuk CLI.

Modul ini berisi konstanta pesan error yang digunakan di seluruh
komponen CLI untuk konsistensi dan kemudahan maintenance.
"""


class ErrorMsg:
    """Konstanta pesan error untuk CLI."""
    
    # ==================== MENU ====================
    INVALID_CHOICE = "Pilihan tidak valid."
    INVALID_CHOICE_RANGE = "Pilihan tidak valid. Masukkan angka {min_val}-{max_val}."
    
    # ==================== INPUT VALIDATION ====================
    INPUT_EMPTY = "Input tidak boleh kosong."
    INPUT_NOT_INT = "Harus berupa bilangan bulat."
    INPUT_NOT_FLOAT = "Harus berupa angka."
    INPUT_BELOW_MIN = "Nilai minimal adalah {min_val}."
    INPUT_ABOVE_MAX = "Nilai maksimal adalah {max_val}."
    INPUT_YES_NO = "Masukkan Y untuk ya atau N untuk tidak."
    INPUT_INVALID_CHOICE = "Pilihan tidak valid. Pilih: {choices}"
    
    # ==================== BARANG / KATALOG ====================
    BARANG_NOT_FOUND = "Barang dengan kode '{kode}' tidak ditemukan."
    BARANG_NOT_FOUND_SIMPLE = "Barang tidak ditemukan."
    BARANG_EMPTY = "Belum ada data barang di katalog."
    BARANG_DUPLICATE = "Barang dengan kode '{kode}' sudah ada!"
    BARANG_SEARCH_EMPTY = "Tidak ditemukan barang dengan kata kunci '{keyword}'."
    
    # ==================== UKURAN / VARIAN ====================
    MIN_UKURAN_REQUIRED = "Minimal harus ada 1 varian ukuran!"
    UKURAN_NOT_FOUND = "Ukuran '{ukuran}' tidak tersedia untuk barang ini."
    
    # ==================== STOK ====================
    STOCK_EMPTY = "Stok untuk {nama} ({ukuran}) habis."
    STOCK_EMPTY_SIMPLE = "Stok habis!"
    STOCK_NOT_ENOUGH = "Stok tidak cukup. Tersedia: {stok}, diminta: {qty}."
    
    # ==================== KERANJANG ====================
    CART_EMPTY = "Keranjang belanja kosong!"
    CART_EMPTY_CHECKOUT = "Keranjang masih kosong! Tambahkan item terlebih dahulu."
    CART_ITEM_NOT_FOUND = "Item tidak ditemukan di keranjang."
    
    # ==================== TRANSAKSI ====================
    TRANSACTION_FAILED = "Gagal memproses transaksi: {error}"
    TRANSACTION_EMPTY = "Belum ada data transaksi."
    TRANSACTION_CANCELLED = "Transaksi dibatalkan."
    
    # ==================== ORDER ====================
    ORDER_NOT_FOUND = "Order dengan ID '{order_id}' tidak ditemukan."
    ORDER_NOT_FOUND_SIMPLE = "Order tidak ditemukan."
    ORDER_CORRUPTED = "Data order rusak atau sudah dihapus."
    ORDER_EMPTY = "Belum ada pesanan online."
    ORDER_FINALIZE_FAILED = "Gagal menyelesaikan order: {error}"
    ORDER_ALREADY_COMPLETED = "Order sudah selesai diproses."
    ORDER_ALREADY_CANCELLED = "Order sudah dibatalkan."
    
    # ==================== FILE / SYSTEM ====================
    FILE_NOT_FOUND = "File tidak ditemukan: {path}"
    FILE_READ_ERROR = "Gagal membaca file: {error}"
    FILE_WRITE_ERROR = "Gagal menyimpan file: {error}"
    SYSTEM_ERROR = "Terjadi kesalahan sistem: {error}"
    
    # ==================== PEMBAYARAN ====================
    PAYMENT_INVALID = "Jumlah pembayaran tidak valid."
    PAYMENT_NOT_ENOUGH = "Pembayaran kurang. Kurang: Rp {kurang}"


class SuccessMsg:
    """Konstanta pesan sukses untuk CLI."""
    
    # ==================== BARANG ====================
    BARANG_CREATED = "Barang '{nama}' berhasil disimpan!"
    BARANG_UPDATED = "Data barang berhasil diupdate."
    BARANG_DELETED = "Barang berhasil dihapus."
    UKURAN_ADDED = "Varian {ukuran} ditambahkan."
    
    # ==================== KERANJANG ====================
    CART_ITEM_ADDED = "Item ditambahkan ke keranjang."
    CART_ITEM_REMOVED = "Item dihapus dari keranjang."
    CART_CLEARED = "Keranjang dikosongkan."
    
    # ==================== TRANSAKSI ====================
    TRANSACTION_SUCCESS = "Transaksi Berhasil! ID: {trx_id}"
    
    # ==================== ORDER ====================
    ORDER_FINALIZED = "Order berhasil difinalisasi."
    ORDER_CANCELLED = "Order dibatalkan."
    
    # ==================== APP ====================
    APP_EXIT = "Terima kasih telah menggunakan aplikasi ini!"
    APP_INTERRUPTED = "Aplikasi dihentikan. Sampai jumpa!"


class InfoMsg:
    """Konstanta pesan informasi untuk CLI."""
    
    OPERATION_CANCELLED = "Operasi dibatalkan."
    DELETE_CANCELLED = "Penghapusan dibatalkan."
    NO_CHANGES = "Tidak ada perubahan yang dilakukan."
    INVOICE_SAVED = "Invoice disimpan ke: {path}"


class WarningMsg:
    """Konstanta pesan warning untuk CLI."""
    
    CONFIRM_DELETE = "Yakin ingin menghapus?"
    CONFIRM_CANCEL = "Batalkan transaksi berjalan?"
    LOW_STOCK = "Stok {nama} tinggal {stok}!"
