"""
Core Transaction Service - Modul Finalisasi Transaksi.

Modul ini menangani finalisasi order menjadi transaksi yang disimpan
ke file CSV. Transaksi adalah record final yang tidak bisa diubah,
berbeda dengan order yang masih bisa berubah statusnya.

Alur finalisasi:
    1. Order dengan status READY dibayar customer
    2. Admin klik "Close Order"
    3. finalize_order() dipanggil:
       - Simpan ke transaksi.csv
       - Generate invoice image
       - Hapus order dari orders.json

Functions:
    init_transaksi_file: Inisialisasi file CSV
    save_order_to_csv: Simpan order ke CSV
    finalize_order: Proses lengkap finalisasi order
    get_transaction_summary: Hitung rekap pendapatan
    load_recent_transactions: Load riwayat transaksi
"""
import csv
import os
from datetime import datetime
from typing import Optional

from core.config import TRANSAKSI_FILE, TRANSAKSI_HEADERS, DATA_DIR
from core.services.order_service import (
    get_order_by_id, delete_order, complete_order,
    STATUS_COMPLETED
)
from core.services.invoice_service import generate_invoice_image


def init_transaksi_file() -> None:
    """Menginisialisasi file transaksi CSV jika belum ada.
    
    Membuat file transaksi.csv dengan header jika belum exists.
    Dipanggil otomatis sebelum operasi read/write CSV.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(TRANSAKSI_FILE, "x", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(TRANSAKSI_HEADERS)
    except FileExistsError:
        pass


def generate_transaction_id() -> str:
    """Menghasilkan ID transaksi/invoice unik.
    
    Format: INV-YYYYMMDD-XXXX dimana XXXX adalah 4 karakter acak.
    
    Returns:
        String berisi transaction ID, contoh: "INV-20260113-AB12"
    """
    import random
    import string
    now = datetime.now()
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"INV-{now.strftime('%Y%m%d')}-{random_suffix}"


def save_order_to_csv(order: dict) -> str:
    """Menyimpan order ke file transaksi CSV.
    
    Setiap item dalam order disimpan sebagai baris terpisah.
    ID transaksi sama untuk semua item dalam satu order.
    
    Args:
        order: Dictionary order dari orders.json.
    
    Returns:
        Transaction ID yang di-generate.
    """
    init_transaksi_file()
    trx_id = generate_transaction_id()
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    items = order.get("items", [])
    subtotal = order.get("subtotal", 0)
    diskon = order.get("diskon", 0)
    ongkir = order.get("ongkir", 0)
    delivery = order.get("delivery", "ambil")
    total = order.get("total", 0)
    
    source_raw = order.get("source", "offline")
    # Map raw source to 'online'/'offline' just in case
    source = "online" if source_raw in ["telegram", "bot"] else "offline"
    
    with open(TRANSAKSI_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for item in items:
            item_subtotal = item.get("subtotal", 0)
            hpp = item.get("hpp", 0)
            qty = item.get("qty", 1)
            total_hpp = hpp * qty
            profit = item_subtotal - total_hpp
            
            writer.writerow([
                waktu,
                trx_id,
                item.get("kode", ""),
                item.get("nama", ""),
                item.get("ukuran", ""),
                item.get("warna_kertas", "-"),
                item.get("warna_bunga", "-"),
                qty,
                item.get("harga", 0),
                item_subtotal,
                hpp,
                total_hpp,
                profit,
                diskon,
                ongkir,
                delivery,
                total,
                source
            ])
    
    return trx_id


def finalize_order(
    order_id: str,
    generate_invoice: bool = True
) -> tuple[Optional[str], Optional[str]]:
    """Memfinalisasi order: simpan ke CSV, generate invoice, hapus order.
    
    Proses lengkap finalisasi setelah pembayaran diterima:
    1. Ambil data order
    2. Simpan ke transaksi.csv
    3. Generate invoice image (opsional)
    4. Update status ke COMPLETED
    5. Hapus dari orders.json
    
    Args:
        order_id: ID order yang akan difinalisasi.
        generate_invoice: Apakah perlu generate invoice image.
    
    Returns:
        Tuple (transaction_id, invoice_path). Keduanya None jika gagal.
    """
    # Get order
    order = get_order_by_id(order_id)
    if not order:
        return None, None
    
    # Save to CSV
    trx_id = save_order_to_csv(order)
    
    # Generate invoice image
    invoice_path = None
    if generate_invoice:
        order_data = {
            "order_id": order_id,
            "items": order.get("items", []),
            "subtotal": order.get("subtotal", 0),
            "diskon": order.get("diskon", 0),
            "ongkir": order.get("ongkir", 0),
            "total": order.get("total", 0),
            "nama_pembeli": order.get("nama_pembeli", "-"),
            "wa_pembeli": order.get("wa_pembeli", "-"),
            "tanggal_pengambilan": order.get("tanggal_pengambilan", ""),
            "tanggal": datetime.now().strftime("%d %b %Y, %H:%M"),
        }
        # Use trx_id for filename if available, else order_id
        filename_id = trx_id if trx_id else order_id
        invoice_path = generate_invoice_image(order_data, f"{filename_id}.png")
    
    # Mark as complete and delete from orders.json
    complete_order(order_id)
    delete_order(order_id)
    
    return trx_id, invoice_path


def get_transaction_summary() -> dict:
    """Menghitung rekap pendapatan dari semua transaksi.
    
    Menganalisis file transaksi.csv dan menghitung total pendapatan,
    modal (HPP), dan profit. Juga breakdown per source (online/offline).
    
    Returns:
        Dictionary dengan keys: 
        count, pendapatan, modal, profit, by_source, top_products.
    """
    init_transaksi_file()
    
    transaksi_set = set()
    total_revenue = 0.0
    total_hpp = 0.0
    total_profit = 0.0
    
    # Source breakdown
    by_source = {
        "offline": {"trx": 0, "pendapatan": 0},
        "online": {"trx": 0, "pendapatan": 0}
    }
    
    product_counter = {}
    
    with open(TRANSAKSI_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            trx_id = row.get("id_transaksi")
            source = row.get("source", "offline")
            revenue = float(row.get("total_transaksi", 0))
            
            # Map source if needed (e.g. cli -> offline, telegram -> online)
            # But we assume 'source' col is already normalized or we normalize here
            if source in ["telegram", "bot", "online"]:
                source_key = "online"
            else:
                source_key = "offline"
            
            # Count unique transactions
            if trx_id and trx_id not in transaksi_set:
                transaksi_set.add(trx_id)
                total_revenue += revenue
                
                # Update source stats
                by_source[source_key]["trx"] += 1
                by_source[source_key]["pendapatan"] += revenue
            
            total_hpp += float(row.get("total_hpp", 0))
            total_profit += float(row.get("profit", 0))
            
            # Top Products
            nama_produk = row.get("nama", "")
            qty = int(row.get("qty", 0))
            if nama_produk:
                if nama_produk in product_counter:
                    product_counter[nama_produk] += qty
                else:
                    product_counter[nama_produk] = qty
    
    # Sort top products
    top_products_list = [
        {"nama": k, "qty": v} 
        for k, v in sorted(product_counter.items(), key=lambda item: item[1], reverse=True)
    ]
    
    return {
        "count": len(transaksi_set),
        "pendapatan": total_revenue, # Alias for handler
        "modal": total_hpp,          # Alias for handler
        "profit": total_profit,      # Alias for handler
        "total_revenue": total_revenue,
        "total_hpp": total_hpp,
        "total_profit": total_profit,
        "by_source": by_source,
        "top_products": top_products_list
    }


def load_recent_transactions(limit: int = 20) -> list[dict]:
    """Memuat riwayat transaksi terakhir dari CSV.
    
    Args:
        limit: Jumlah maksimal transaksi yang diambil.
    
    Returns:
        List dictionary transaksi, terbaru di akhir.
    """
    init_transaksi_file()
    with open(TRANSAKSI_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows[-limit:]
