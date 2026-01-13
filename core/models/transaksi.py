"""
Model data untuk Transaksi (dataclass only).

TransaksiItem adalah record final dari penjualan yang sudah selesai.
"""
from dataclasses import dataclass


@dataclass
class TransaksiItem:
    """Representasi satu item dalam transaksi final."""
    kode: str
    nama: str
    ukuran: str
    warna_kertas: str
    warna_bunga: str
    qty: int
    harga: float
    subtotal: float
    hpp: float
    total_hpp: float
    profit: float
    
    def to_dict(self) -> dict:
        return {
            "kode": self.kode,
            "nama": self.nama,
            "ukuran": self.ukuran,
            "warna_kertas": self.warna_kertas,
            "warna_bunga": self.warna_bunga,
            "qty": self.qty,
            "harga": self.harga,
            "subtotal": self.subtotal,
            "hpp": self.hpp,
            "total_hpp": self.total_hpp,
            "profit": self.profit,
        }
    
    @classmethod
    def from_cart_item(cls, kode: str, nama: str, ukuran: str, warna_kertas: str,
                       warna_bunga: str, qty: int, harga: float, hpp: float) -> "TransaksiItem":
        subtotal = harga * qty
        total_hpp = hpp * qty
        profit = subtotal - total_hpp
        return cls(
            kode=kode, nama=nama, ukuran=ukuran, warna_kertas=warna_kertas,
            warna_bunga=warna_bunga, qty=qty, harga=harga, subtotal=subtotal,
            hpp=hpp, total_hpp=total_hpp, profit=profit,
        )
