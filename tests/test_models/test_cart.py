"""
Unit Tests untuk Model Cart dan CartItem.

Menguji shopping cart functionality.
"""
import pytest
from core.models.cart import Cart, CartItem


class TestCartItem:
    """Test cases untuk CartItem dataclass."""

    def test_create_cart_item(self):
        """Test pembuatan CartItem basic."""
        item = CartItem(
            kode="BQT001",
            nama="Buket Mawar",
            ukuran="M",
            warna_kertas="Merah",
            warna_bunga="Putih",
            qty=2,
            harga=50000,
            hpp=25000
        )
        
        assert item.kode == "BQT001"
        assert item.qty == 2
        assert item.harga == 50000

    def test_cart_item_subtotal(self, sample_cart_item):
        """Test perhitungan subtotal (harga * qty)."""
        # sample_cart_item: qty=2, harga=50000
        assert sample_cart_item.subtotal == 100000

    def test_cart_item_subtotal_single_qty(self):
        """Test subtotal dengan qty=1."""
        item = CartItem(
            kode="X", nama="Test", ukuran="M",
            warna_kertas="-", warna_bunga="-",
            qty=1, harga=75000, hpp=0
        )
        assert item.subtotal == 75000

    def test_cart_item_total_hpp(self, sample_cart_item):
        """Test perhitungan total HPP (hpp * qty)."""
        # sample_cart_item: qty=2, hpp=25000
        assert sample_cart_item.total_hpp == 50000

    def test_cart_item_profit(self, sample_cart_item):
        """Test perhitungan profit (subtotal - total_hpp)."""
        # subtotal=100000, total_hpp=50000
        assert sample_cart_item.profit == 50000

    def test_cart_item_profit_zero_hpp(self):
        """Test profit ketika HPP = 0."""
        item = CartItem(
            kode="X", nama="Test", ukuran="M",
            warna_kertas="-", warna_bunga="-",
            qty=2, harga=50000, hpp=0
        )
        assert item.profit == item.subtotal

    def test_cart_item_to_dict(self, sample_cart_item):
        """Test konversi CartItem ke dictionary."""
        result = sample_cart_item.to_dict()
        
        assert isinstance(result, dict)
        assert result["kode"] == "BQT001"
        assert result["qty"] == 2
        assert result["subtotal"] == 100000  # computed property included
        assert result["profit"] == 50000

    def test_cart_item_from_dict(self):
        """Test pembuatan CartItem dari dictionary."""
        data = {
            "kode": "BQT002",
            "nama": "Buket Simple",
            "ukuran": "L",
            "warna_kertas": "Pink",
            "warna_bunga": "Kuning",
            "qty": 3,
            "harga": 75000,
            "hpp": 35000
        }
        item = CartItem.from_dict(data)
        
        assert item.kode == "BQT002"
        assert item.ukuran == "L"
        assert item.qty == 3

    def test_cart_item_from_dict_defaults(self):
        """Test from_dict dengan nilai default."""
        data = {}  # Empty dict
        item = CartItem.from_dict(data)
        
        assert item.kode == ""
        assert item.warna_kertas == "-"
        assert item.qty == 1
        assert item.harga == 0

    def test_cart_item_roundtrip(self, sample_cart_item):
        """Test to_dict -> from_dict."""
        dict_data = sample_cart_item.to_dict()
        restored = CartItem.from_dict(dict_data)
        
        assert restored.kode == sample_cart_item.kode
        assert restored.qty == sample_cart_item.qty
        assert restored.harga == sample_cart_item.harga


class TestCart:
    """Test cases untuk Cart dataclass."""

    def test_create_empty_cart(self, empty_cart):
        """Test pembuatan Cart kosong."""
        assert empty_cart.items == []
        assert empty_cart.diskon_persen == 0.0
        assert empty_cart.diskon_nominal == 0.0
        assert empty_cart.ongkir == 0.0

    def test_cart_is_empty(self, empty_cart):
        """Test is_empty() pada cart kosong."""
        assert empty_cart.is_empty() is True

    def test_cart_is_not_empty(self, cart_with_items):
        """Test is_empty() pada cart berisi."""
        assert cart_with_items.is_empty() is False

    def test_cart_add_item(self, empty_cart, sample_cart_item):
        """Test menambahkan item ke cart."""
        empty_cart.add_item(sample_cart_item)
        
        assert len(empty_cart.items) == 1
        assert empty_cart.items[0].kode == "BQT001"

    def test_cart_add_multiple_items(self, empty_cart, sample_cart_item, sample_cart_item_2):
        """Test menambahkan multiple items."""
        empty_cart.add_item(sample_cart_item)
        empty_cart.add_item(sample_cart_item_2)
        
        assert len(empty_cart.items) == 2

    def test_cart_remove_item_valid_index(self, cart_with_items):
        """Test remove item dengan index valid."""
        removed = cart_with_items.remove_item(0)
        
        assert removed is not None
        assert removed.kode == "BQT001"
        assert len(cart_with_items.items) == 1

    def test_cart_remove_item_invalid_index(self, cart_with_items):
        """Test remove item dengan index invalid."""
        removed = cart_with_items.remove_item(99)
        
        assert removed is None
        assert len(cart_with_items.items) == 2  # No change

    def test_cart_remove_item_negative_index(self, cart_with_items):
        """Test remove item dengan negative index."""
        removed = cart_with_items.remove_item(-1)
        
        assert removed is None

    def test_cart_clear(self, cart_with_items):
        """Test clear() mengosongkan cart."""
        cart_with_items.clear()
        
        assert cart_with_items.items == []
        assert cart_with_items.is_empty() is True

    def test_cart_subtotal(self, cart_with_items):
        """Test perhitungan subtotal (sum of all item subtotals)."""
        # item1: 2*50000=100000, item2: 1*25000=25000
        assert cart_with_items.subtotal == 125000

    def test_cart_subtotal_empty(self, empty_cart):
        """Test subtotal pada cart kosong."""
        assert empty_cart.subtotal == 0

    def test_cart_total_hpp(self, cart_with_items):
        """Test perhitungan total HPP."""
        # item1: 2*25000=50000, item2: 1*10000=10000
        assert cart_with_items.total_hpp == 60000

    def test_cart_diskon_persen(self):
        """Test diskon dengan persentase."""
        cart = Cart(diskon_persen=10)
        item = CartItem(
            kode="X", nama="Test", ukuran="M",
            warna_kertas="-", warna_bunga="-",
            qty=1, harga=100000, hpp=50000
        )
        cart.add_item(item)
        
        assert cart.diskon == 10000  # 10% of 100000

    def test_cart_diskon_nominal(self):
        """Test diskon dengan nominal."""
        cart = Cart(diskon_nominal=15000)
        item = CartItem(
            kode="X", nama="Test", ukuran="M",
            warna_kertas="-", warna_bunga="-",
            qty=1, harga=100000, hpp=50000
        )
        cart.add_item(item)
        
        assert cart.diskon == 15000

    def test_cart_diskon_nominal_takes_precedence(self):
        """Test diskon nominal takes precedence over persen."""
        cart = Cart(diskon_persen=20, diskon_nominal=5000)
        item = CartItem(
            kode="X", nama="Test", ukuran="M",
            warna_kertas="-", warna_bunga="-",
            qty=1, harga=100000, hpp=50000
        )
        cart.add_item(item)
        
        # Nominal (5000) takes precedence over persen (20% = 20000)
        assert cart.diskon == 5000

    def test_cart_total_basic(self, cart_with_items):
        """Test perhitungan total (subtotal - diskon + ongkir)."""
        # subtotal=125000, no diskon, no ongkir
        assert cart_with_items.total == 125000

    def test_cart_total_with_diskon(self):
        """Test total dengan diskon."""
        cart = Cart(diskon_nominal=10000)
        cart.add_item(CartItem(
            kode="X", nama="Test", ukuran="M",
            warna_kertas="-", warna_bunga="-",
            qty=1, harga=100000, hpp=50000
        ))
        
        # 100000 - 10000 = 90000
        assert cart.total == 90000

    def test_cart_total_with_ongkir(self):
        """Test total dengan ongkir."""
        cart = Cart(ongkir=15000)
        cart.add_item(CartItem(
            kode="X", nama="Test", ukuran="M",
            warna_kertas="-", warna_bunga="-",
            qty=1, harga=100000, hpp=50000
        ))
        
        # 100000 + 15000 = 115000
        assert cart.total == 115000

    def test_cart_total_with_all(self):
        """Test total dengan diskon dan ongkir."""
        cart = Cart(diskon_nominal=10000, ongkir=15000)
        cart.add_item(CartItem(
            kode="X", nama="Test", ukuran="M",
            warna_kertas="-", warna_bunga="-",
            qty=1, harga=100000, hpp=50000
        ))
        
        # 100000 - 10000 + 15000 = 105000
        assert cart.total == 105000

    def test_cart_total_profit(self, cart_with_items):
        """Test perhitungan total profit."""
        # subtotal=125000, diskon=0, total_hpp=60000
        # profit = 125000 - 0 - 60000 = 65000
        assert cart_with_items.total_profit == 65000

    def test_cart_total_profit_with_diskon(self):
        """Test profit dengan diskon."""
        cart = Cart(diskon_nominal=10000)
        cart.add_item(CartItem(
            kode="X", nama="Test", ukuran="M",
            warna_kertas="-", warna_bunga="-",
            qty=1, harga=100000, hpp=40000
        ))
        
        # 100000 - 10000 - 40000 = 50000
        assert cart.total_profit == 50000

    def test_cart_to_dict(self, cart_with_items):
        """Test konversi Cart ke dictionary."""
        result = cart_with_items.to_dict()
        
        assert isinstance(result, dict)
        assert "items" in result
        assert len(result["items"]) == 2
        assert result["subtotal"] == 125000
        assert result["total"] == 125000

    def test_cart_to_dict_includes_buyer_info(self):
        """Test to_dict includes buyer info."""
        cart = Cart(
            nama_pembeli="John Doe",
            wa_pembeli="08123456789",
            alamat="Jl. Test 123"
        )
        result = cart.to_dict()
        
        assert result["nama_pembeli"] == "John Doe"
        assert result["wa_pembeli"] == "08123456789"
        assert result["alamat"] == "Jl. Test 123"

    def test_cart_delivery_type_default(self, empty_cart):
        """Test default delivery type."""
        assert empty_cart.delivery_type == "ambil"

    def test_cart_delivery_type_custom(self):
        """Test custom delivery type."""
        cart = Cart(delivery_type="delivery", ongkir=20000)
        assert cart.delivery_type == "delivery"
        assert cart.ongkir == 20000
