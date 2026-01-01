"""
Model dan operasi data untuk Barang/Katalog Buqet.
"""
import json
from dataclasses import dataclass, asdict, field
from src.config import BARANG_FILE
from src.utils import ensure_data_dir


@dataclass
class UkuranBarang:
    """Data model untuk ukuran barang (Mini/Standar/Besar)."""
    nama: str  # "Mini", "Standar", "Besar"
    harga: float
    hpp: float
    stok: int

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "UkuranBarang":
        return cls(
            nama=data["nama"],
            harga=data["harga"],
            hpp=data["hpp"],
            stok=data["stok"]
        )


@dataclass
class Barang:
    """Data model untuk katalog buqet."""
    kode: str
    nama: str
    warna_kertas: list[str] = field(default_factory=list)
    warna_bunga: list[str] = field(default_factory=list)
    ukuran: list[UkuranBarang] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "kode": self.kode,
            "nama": self.nama,
            "warna_kertas": self.warna_kertas,
            "warna_bunga": self.warna_bunga,
            "ukuran": [u.to_dict() for u in self.ukuran]
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Barang":
        # Handle legacy format (single harga/hpp/stok)
        if "ukuran" in data and isinstance(data["ukuran"], list):
            ukuran_list = [UkuranBarang.from_dict(u) for u in data["ukuran"]]
        else:
            # Migrate old format to new
            ukuran_list = [
                UkuranBarang(
                    nama="Standar",
                    harga=data.get("harga", 0),
                    hpp=data.get("hpp", 0),
                    stok=data.get("stok", 0)
                )
            ]
        
        return cls(
            kode=data["kode"],
            nama=data["nama"],
            warna_kertas=data.get("warna_kertas", []),
            warna_bunga=data.get("warna_bunga", []),
            ukuran=ukuran_list
        )

    def get_ukuran(self, nama_ukuran: str) -> UkuranBarang | None:
        """Get ukuran by nama."""
        for u in self.ukuran:
            if u.nama.lower() == nama_ukuran.lower():
                return u
        return None

    def total_stok(self) -> int:
        """Get total stok semua ukuran."""
        return sum(u.stok for u in self.ukuran)


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
