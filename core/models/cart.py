"""
Unified Cart Item Model.
Digunakan oleh CLI dan Bot untuk konsistensi data.
"""
from dataclasses import dataclass, asdict, field
from typing import Optional


@dataclass
class CartItem:
    """
    Unified item model untuk keranjang/order.
    Menggantikan TransaksiItem (CLI) dan OrderItem (Bot).
    """
    kode: str
    nama: str
    ukuran: str
    warna_kertas: str
    warna_bunga: str
    qty: int
    harga: float
    hpp: float = 0.0  # HPP opsional, hanya untuk internal/admin
    
    @property
    def subtotal(self) -> float:
        """Harga * qty."""
        return self.harga * self.qty
    
    @property
    def total_hpp(self) -> float:
        """HPP * qty (internal)."""
        return self.hpp * self.qty
    
    @property
    def profit(self) -> float:
        """Subtotal - total_hpp (internal)."""
        return self.subtotal - self.total_hpp
    
    def to_dict(self) -> dict:
        """Convert to dict, include computed properties."""
        return {
            "kode": self.kode,
            "nama": self.nama,
            "ukuran": self.ukuran,
            "warna_kertas": self.warna_kertas,
            "warna_bunga": self.warna_bunga,
            "qty": self.qty,
            "harga": self.harga,
            "hpp": self.hpp,
            "subtotal": self.subtotal,
            "total_hpp": self.total_hpp,
            "profit": self.profit,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "CartItem":
        """Create CartItem from dict."""
        return cls(
            kode=data.get("kode", ""),
            nama=data.get("nama", ""),
            ukuran=data.get("ukuran", ""),
            warna_kertas=data.get("warna_kertas", "-"),
            warna_bunga=data.get("warna_bunga", "-"),
            qty=int(data.get("qty", 1)),
            harga=float(data.get("harga", 0)),
            hpp=float(data.get("hpp", 0)),
        )


@dataclass 
class Cart:
    """
    Shopping cart container.
    Holds multiple CartItems and calculates totals.
    """
    items: list[CartItem] = field(default_factory=list)
    diskon_persen: float = 0.0
    diskon_nominal: float = 0.0
    ongkir: float = 0.0
    delivery_type: str = "ambil"  # "ambil" atau "delivery"
    
    # Buyer info (optional, for orders)
    nama_pembeli: str = ""
    wa_pembeli: str = ""
    alamat: str = ""
    tanggal_pengambilan: str = ""
    
    @property
    def subtotal(self) -> float:
        """Sum of all item subtotals."""
        return sum(item.subtotal for item in self.items)
    
    @property
    def total_hpp(self) -> float:
        """Sum of all item HPP (internal)."""
        return sum(item.total_hpp for item in self.items)
    
    @property
    def diskon(self) -> float:
        """Calculated discount amount (nominal takes precedence if set)."""
        if self.diskon_nominal > 0:
            return self.diskon_nominal
        return self.subtotal * (self.diskon_persen / 100)
    
    @property
    def total(self) -> float:
        """Final total: subtotal - diskon + ongkir."""
        return self.subtotal - self.diskon + self.ongkir
    
    @property
    def total_profit(self) -> float:
        """Total profit after discount (internal)."""
        return self.subtotal - self.diskon - self.total_hpp
    
    def add_item(self, item: CartItem) -> None:
        """Add item to cart."""
        self.items.append(item)
    
    def remove_item(self, index: int) -> CartItem | None:
        """Remove item by index."""
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None
    
    def clear(self) -> None:
        """Clear all items."""
        self.items.clear()
    
    def is_empty(self) -> bool:
        """Check if cart is empty."""
        return len(self.items) == 0
    
    def to_dict(self) -> dict:
        """Convert cart to dict."""
        return {
            "items": [item.to_dict() for item in self.items],
            "subtotal": self.subtotal,
            "diskon_persen": self.diskon_persen,
            "diskon": self.diskon,
            "ongkir": self.ongkir,
            "delivery_type": self.delivery_type,
            "total": self.total,
            "nama_pembeli": self.nama_pembeli,
            "wa_pembeli": self.wa_pembeli,
            "alamat": self.alamat,
            "tanggal_pengambilan": self.tanggal_pengambilan,
        }
