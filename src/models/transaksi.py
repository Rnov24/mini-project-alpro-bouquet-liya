"""
Model dan operasi data untuk Transaksi.
"""
import csv
from dataclasses import dataclass, asdict
from datetime import datetime
from src.config import TRANSAKSI_FILE, TRANSAKSI_HEADERS
from src.utils import ensure_data_dir


# =========================
# DATA MODEL
# =========================
@dataclass
class TransaksiItem:
    """Data model untuk item dalam transaksi."""
    kode: str
    nama: str
    ukuran: str
    warna_kertas: str
    warna_bunga: str
    qty: int
    harga: float
    subtotal: float
    hpp: float              # modal per item (internal)
    total_hpp: float        # qty * hpp (internal)
    profit: float           # subtotal - total_hpp

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_cart(
        cls,
        kode: str,
        nama: str,
        ukuran: str,
        warna_kertas: str,
        warna_bunga: str,
        qty: int,
        harga: float,
        hpp: float
    ) -> "TransaksiItem":
        subtotal = qty * harga
        total_hpp = qty * hpp
        profit = subtotal - total_hpp

        return cls(
            kode=kode,
            nama=nama,
            ukuran=ukuran,
            warna_kertas=warna_kertas,
            warna_bunga=warna_bunga,
            qty=qty,
            harga=harga,
            subtotal=subtotal,
            hpp=hpp,
            total_hpp=total_hpp,
            profit=profit
        )


# =========================
# FILE HANDLING
# =========================
def init_transaksi_file() -> None:
    """Inisialisasi file transaksi jika belum ada."""
    ensure_data_dir()
    try:
        with open(TRANSAKSI_FILE, "x", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(TRANSAKSI_HEADERS)
    except FileExistsError:
        pass


def generate_transaksi_id() -> str:
    """Generate ID transaksi unik."""
    return datetime.now().strftime("LIY%Y%m%d%H%M%S")


def save_transaksi(
    items: list[TransaksiItem],
    diskon: float,
    ongkir: float,
    delivery: str,
    total_transaksi: float
) -> str:
    """Simpan transaksi ke CSV (HPP & profit hanya untuk internal)."""
    init_transaksi_file()
    trx_id = generate_transaksi_id()
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(TRANSAKSI_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for item in items:
            writer.writerow([
                waktu,
                trx_id,
                item.kode,
                item.nama,
                item.ukuran,
                item.warna_kertas,
                item.warna_bunga,
                item.qty,
                item.harga,
                item.subtotal,
                item.hpp,
                item.total_hpp,
                item.profit,
                diskon,
                ongkir,
                delivery,
                total_transaksi
            ])

    return trx_id


def load_transaksi(limit: int = 20) -> list[dict]:
    """Load transaksi terakhir."""
    init_transaksi_file()
    with open(TRANSAKSI_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows[-limit:]


# =========================
# REKAP & AKUNTANSI
# =========================
def get_rekap_pendapatan():
    """
    Return:
    - jumlah_transaksi
    - total_pendapatan (berdasarkan total_transaksi per invoice)
    - total_modal (HPP)
    - total_profit
    """
    init_transaksi_file()

    transaksi_set = set()
    total_pendapatan = 0.0
    total_modal = 0.0
    total_profit = 0.0

    with open(TRANSAKSI_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            trx_id = row.get("id_transaksi")

            # Hitung pendapatan per transaksi (tidak dobel)
            if trx_id and trx_id not in transaksi_set:
                transaksi_set.add(trx_id)
                total_pendapatan += float(row.get("total_transaksi", 0))

            # Aman untuk CSV lama & baru
            total_modal += float(row.get("total_hpp", 0))
            total_profit += float(row.get("profit", 0))

    return (
        len(transaksi_set),
        total_pendapatan,
        total_modal,
        total_profit
    )
