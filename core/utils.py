"""
Utility functions bersama untuk aplikasi Buqeuet Liya.

Modul ini berisi fungsi-fungsi helper yang digunakan bersama oleh
CLI dan Bot. Fungsi-fungsi di sini harus platform-agnostic.

Functions:
    format_rupiah: Format angka ke format mata uang Indonesia
    ensure_data_dir: Pastikan direktori data ada
    generate_random_id: Generate ID acak untuk order/transaksi
"""
import os
from core.config import DATA_DIR


def format_rupiah(amount: float) -> str:
    """Mengubah angka menjadi format mata uang Rupiah.
    
    Fungsi ini memformat angka menjadi string dengan pemisah ribuan
    menggunakan titik (.) sesuai standar penulisan Rupiah Indonesia.
    
    Args:
        amount: Nilai angka yang akan diformat.
    
    Returns:
        String angka terformat, contoh: "15.000" untuk input 15000.
    
    Example:
        >>> format_rupiah(1500000)
        "1.500.000"
    """
    return f"{int(round(amount)):,}".replace(",", ".")


def ensure_data_dir() -> None:
    """Memastikan direktori data ada, buat jika belum ada.
    
    Fungsi ini dipanggil sebelum operasi file untuk memastikan
    folder 'data/' sudah tersedia.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
