"""
Model dan operasi data untuk Barang.
"""
import json
from dataclasses import dataclass, asdict
from src.config import BARANG_FILE
from src.utils import ensure_data_dir


@dataclass
class Barang:
    """Data model untuk barang."""
    kode: str
    nama: str
    harga: float
    stok: int

    def to_dict(self) -> dict:
        """Convert ke dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Barang":
        """Create Barang dari dictionary."""
        return cls(
            kode=data["kode"],
            nama=data["nama"],
            harga=data["harga"],
            stok=data["stok"]
        )


def load_barang() -> list[Barang]:
    """Load semua barang dari file JSON."""
    ensure_data_dir()
    try:
        with open(BARANG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Barang.from_dict(item) for item in data]
    except FileNotFoundError:
        save_barang([])
        return []


def save_barang(barang_list: list[Barang]) -> None:
    """Simpan semua barang ke file JSON."""
    ensure_data_dir()
    data = [b.to_dict() for b in barang_list]
    with open(BARANG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_by_kode(barang_list: list[Barang], kode: str) -> Barang | None:
    """Cari barang berdasarkan kode."""
    kode = kode.strip().lower()
    for b in barang_list:
        if b.kode.lower() == kode:
            return b
    return None


def search_barang(barang_list: list[Barang], keyword: str) -> list[Barang]:
    """Cari barang berdasarkan keyword (kode atau nama)."""
    keyword = keyword.lower()
    return [
        b for b in barang_list
        if keyword in b.kode.lower() or keyword in b.nama.lower()
    ]
