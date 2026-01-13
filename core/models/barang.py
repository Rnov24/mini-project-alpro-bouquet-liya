"""
Model data untuk Barang/Katalog Buket.

Modul ini berisi dataclass untuk merepresentasikan produk buket
yang dijual.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UkuranBarang:
    """Representasi satu varian ukuran dari barang."""
    nama: str
    harga: float
    hpp: float
    stok: int
    
    def to_dict(self) -> dict:
        return {"nama": self.nama, "harga": self.harga, "hpp": self.hpp, "stok": self.stok}
    
    @classmethod
    def from_dict(cls, data: dict) -> "UkuranBarang":
        return cls(
            nama=data["nama"],
            harga=float(data["harga"]),
            hpp=float(data["hpp"]),
            stok=int(data["stok"]),
        )


@dataclass
class Barang:
    """Representasi satu produk buket dalam katalog."""
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
            "ukuran": [u.to_dict() for u in self.ukuran],
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Barang":
        if "ukuran" in data and isinstance(data["ukuran"], list):
            ukuran_list = [UkuranBarang.from_dict(u) for u in data["ukuran"]]
        else:
            ukuran_list = [UkuranBarang(
                nama="Standar",
                harga=float(data.get("harga", 0)),
                hpp=float(data.get("hpp", 0)),
                stok=int(data.get("stok", 0)),
            )]
        return cls(
            kode=data["kode"],
            nama=data["nama"],
            warna_kertas=data.get("warna_kertas", []),
            warna_bunga=data.get("warna_bunga", []),
            ukuran=ukuran_list,
        )
    
    def get_ukuran(self, nama_ukuran: str) -> Optional[UkuranBarang]:
        for u in self.ukuran:
            if u.nama.lower() == nama_ukuran.lower():
                return u
        return None
