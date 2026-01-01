"""
Model dan operasi data untuk Transaksi.
"""
import csv
from dataclasses import dataclass, asdict
from datetime import datetime
from src.config import TRANSAKSI_FILE, TRANSAKSI_HEADERS
from src.utils import ensure_data_dir


@dataclass
class TransaksiItem:
    """Data model untuk item dalam transaksi."""
    kode: str
    nama: str
    ukuran: str  # Mini/Standar/Besar
    warna_kertas: str
    warna_bunga: str
    qty: int
    harga: float
    subtotal: float

    def to_dict(self) -> dict:
        """Convert ke dictionary."""
        return asdict(self)

    @classmethod
    def from_cart(
        cls, kode: str, nama: str, ukuran: str, 
        warna_kertas: str, warna_bunga: str,
        qty: int, harga: float
    ) -> "TransaksiItem":
        """Create TransaksiItem dari data keranjang."""
        return cls(
            kode=kode,
            nama=nama,
            ukuran=ukuran,
            warna_kertas=warna_kertas,
            warna_bunga=warna_bunga,
            qty=qty,
            harga=harga,
            subtotal=qty * harga
        )


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
    """Generate ID transaksi unik berdasarkan waktu."""
    return datetime.now().strftime("LIY%Y%m%d%H%M%S")


def save_transaksi(
    items: list[TransaksiItem], 
    diskon: float,
    ongkir: float,
    delivery: str,
    total_transaksi: float
) -> str:
    """Simpan transaksi ke CSV. Return transaction ID."""
    init_transaksi_file()
    trx_id = generate_transaksi_id()
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(TRANSAKSI_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for item in items:
            writer.writerow([
                waktu, trx_id,
                item.kode, item.nama, item.ukuran,
                item.warna_kertas, item.warna_bunga,
                item.qty, item.harga, item.subtotal,
                diskon, ongkir, delivery, total_transaksi
            ])
    return trx_id


def load_transaksi(limit: int = 20) -> list[dict]:
    """Load transaksi terakhir dari CSV."""
    init_transaksi_file()
    rows = []
    with open(TRANSAKSI_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows[-limit:] if rows else []


def get_rekap_pendapatan() -> tuple[int, float]:
    """Hitung rekap pendapatan. Return (jumlah_transaksi, total_pendapatan)."""
    init_transaksi_file()
    totals_by_trx: dict[str, float] = {}
    
    with open(TRANSAKSI_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            trx_id = row["id_transaksi"]
            totals_by_trx[trx_id] = float(row["total_transaksi"])
    
    if not totals_by_trx:
        return 0, 0.0
    
    return len(totals_by_trx), sum(totals_by_trx.values())
