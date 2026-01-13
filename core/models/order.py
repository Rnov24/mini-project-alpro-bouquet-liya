"""
Model data untuk Order/Pesanan (dataclass only).

Model ini hanya berisi data structure. Operasi CRUD ada di
core/services/order_service.py.
"""
from dataclasses import dataclass

# Status constants
STATUS_PENDING = "pending"
STATUS_PROCESSING = "processing"
STATUS_READY = "ready"
STATUS_COMPLETED = "completed"
STATUS_CANCELLED = "cancelled"


@dataclass
class OrderItem:
    """Representasi satu item dalam order."""
    kode: str
    nama: str
    ukuran: str
    warna_kertas: str
    warna_bunga: str
    qty: int
    harga: float
    hpp: float
    subtotal: float
    
    def to_dict(self) -> dict:
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
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "OrderItem":
        return cls(
            kode=data.get("kode", ""),
            nama=data.get("nama", ""),
            ukuran=data.get("ukuran", ""),
            warna_kertas=data.get("warna_kertas", "-"),
            warna_bunga=data.get("warna_bunga", "-"),
            qty=int(data.get("qty", 1)),
            harga=float(data.get("harga", 0)),
            hpp=float(data.get("hpp", 0)),
            subtotal=float(data.get("subtotal", 0)),
        )


@dataclass
class Order:
    """Representasi lengkap satu pesanan customer."""
    order_id: str
    telegram_id: int
    nama_pembeli: str
    wa_pembeli: str
    alamat: str
    delivery: str
    ongkir: float
    diskon: float
    items: list[OrderItem]
    subtotal: float
    total: float
    status: str
    source: str = "cli"
    notes: str = ""
    created_at: str = ""
    updated_at: str = ""
    
    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "telegram_id": self.telegram_id,
            "nama_pembeli": self.nama_pembeli,
            "wa_pembeli": self.wa_pembeli,
            "alamat": self.alamat,
            "delivery": self.delivery,
            "ongkir": self.ongkir,
            "diskon": self.diskon,
            "items": [item.to_dict() for item in self.items],
            "subtotal": self.subtotal,
            "total": self.total,
            "status": self.status,
            "source": self.source,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        items = [OrderItem.from_dict(item) for item in data.get("items", [])]
        return cls(
            order_id=data.get("order_id", ""),
            telegram_id=int(data.get("telegram_id", 0)),
            nama_pembeli=data.get("nama_pembeli", ""),
            wa_pembeli=data.get("wa_pembeli", ""),
            alamat=data.get("alamat", ""),
            delivery=data.get("delivery", "ambil"),
            ongkir=float(data.get("ongkir", 0)),
            diskon=float(data.get("diskon", 0)),
            items=items,
            subtotal=float(data.get("subtotal", 0)),
            total=float(data.get("total", 0)),
            status=data.get("status", STATUS_PENDING),
            source=data.get("source", "cli"),
            notes=data.get("notes", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
        )
    
    def is_active(self) -> bool:
        return self.status not in [STATUS_COMPLETED, STATUS_CANCELLED]
