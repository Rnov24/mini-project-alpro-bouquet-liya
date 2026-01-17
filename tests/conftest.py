"""
Pytest Configuration dan Fixtures.

Menyediakan fixtures yang digunakan di seluruh test suite.
"""
import pytest
import os
import json
import tempfile
import shutil
from pathlib import Path

# Import models
from core.models.barang import Barang, UkuranBarang
from core.models.cart import Cart, CartItem


# ==================== SAMPLE DATA FIXTURES ====================

@pytest.fixture
def sample_ukuran_small():
    """Fixture: Varian ukuran S."""
    return UkuranBarang(nama="S", harga=30000, hpp=15000, stok=5)


@pytest.fixture
def sample_ukuran_medium():
    """Fixture: Varian ukuran M."""
    return UkuranBarang(nama="M", harga=50000, hpp=25000, stok=10)


@pytest.fixture
def sample_ukuran_large():
    """Fixture: Varian ukuran L."""
    return UkuranBarang(nama="L", harga=75000, hpp=40000, stok=3)


@pytest.fixture
def sample_barang(sample_ukuran_small, sample_ukuran_medium, sample_ukuran_large):
    """Fixture: Contoh barang dengan multiple ukuran."""
    return Barang(
        kode="BQT001",
        nama="Buket Mawar Premium",
        warna_kertas=["Merah", "Pink", "Putih"],
        warna_bunga=["Merah", "Putih"],
        ukuran=[sample_ukuran_small, sample_ukuran_medium, sample_ukuran_large]
    )


@pytest.fixture
def sample_barang_minimal():
    """Fixture: Barang dengan data minimal."""
    return Barang(
        kode="BQT002",
        nama="Buket Simple",
        warna_kertas=[],
        warna_bunga=[],
        ukuran=[UkuranBarang(nama="Standar", harga=25000, hpp=10000, stok=20)]
    )


@pytest.fixture
def sample_cart_item():
    """Fixture: Contoh item di keranjang."""
    return CartItem(
        kode="BQT001",
        nama="Buket Mawar Premium",
        ukuran="M",
        warna_kertas="Merah",
        warna_bunga="Putih",
        qty=2,
        harga=50000,
        hpp=25000
    )


@pytest.fixture
def sample_cart_item_2():
    """Fixture: Item kedua untuk testing multiple items."""
    return CartItem(
        kode="BQT002",
        nama="Buket Simple",
        ukuran="Standar",
        warna_kertas="-",
        warna_bunga="-",
        qty=1,
        harga=25000,
        hpp=10000
    )


@pytest.fixture
def empty_cart():
    """Fixture: Keranjang kosong."""
    return Cart()


@pytest.fixture
def cart_with_items(sample_cart_item, sample_cart_item_2):
    """Fixture: Keranjang dengan beberapa item."""
    cart = Cart()
    cart.add_item(sample_cart_item)
    cart.add_item(sample_cart_item_2)
    return cart


# ==================== FILE I/O FIXTURES ====================

@pytest.fixture
def temp_data_dir(tmp_path):
    """
    Fixture: Temporary data directory untuk testing file I/O.
    
    Menggunakan pytest's tmp_path fixture yang auto-cleanup.
    """
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir


@pytest.fixture
def temp_barang_file(temp_data_dir):
    """Fixture: Temporary barang.json file path."""
    return temp_data_dir / "barang.json"


@pytest.fixture
def temp_transaksi_file(temp_data_dir):
    """Fixture: Temporary transaksi.csv file path."""
    return temp_data_dir / "transaksi.csv"


@pytest.fixture
def sample_barang_json_data():
    """Fixture: Sample JSON data untuk barang."""
    return [
        {
            "kode": "BQT001",
            "nama": "Buket Mawar Premium",
            "warna_kertas": ["Merah", "Pink"],
            "warna_bunga": ["Merah", "Putih"],
            "ukuran": [
                {"nama": "S", "harga": 30000, "hpp": 15000, "stok": 5},
                {"nama": "M", "harga": 50000, "hpp": 25000, "stok": 10}
            ]
        },
        {
            "kode": "BQT002",
            "nama": "Buket Simple",
            "warna_kertas": [],
            "warna_bunga": [],
            "ukuran": [
                {"nama": "Standar", "harga": 25000, "hpp": 10000, "stok": 20}
            ]
        }
    ]


@pytest.fixture
def populated_barang_file(temp_barang_file, sample_barang_json_data):
    """Fixture: Barang file yang sudah terisi data."""
    with open(temp_barang_file, "w", encoding="utf-8") as f:
        json.dump(sample_barang_json_data, f, ensure_ascii=False, indent=2)
    return temp_barang_file


# ==================== LEGACY DATA FIXTURES ====================

@pytest.fixture
def legacy_barang_data():
    """
    Fixture: Data barang format lama (tanpa ukuran array).
    Untuk testing backward compatibility.
    """
    return {
        "kode": "OLD001",
        "nama": "Buket Lama",
        "harga": 40000,
        "hpp": 20000,
        "stok": 8
    }
