"""
Unit Tests untuk Model Barang dan UkuranBarang.

Menguji dataclass models untuk katalog produk.
"""
import pytest
from core.models.barang import Barang, UkuranBarang


class TestUkuranBarang:
    """Test cases untuk UkuranBarang dataclass."""

    def test_create_ukuran(self):
        """Test pembuatan UkuranBarang basic."""
        ukuran = UkuranBarang(nama="M", harga=50000, hpp=25000, stok=10)
        
        assert ukuran.nama == "M"
        assert ukuran.harga == 50000
        assert ukuran.hpp == 25000
        assert ukuran.stok == 10

    def test_ukuran_to_dict(self, sample_ukuran_medium):
        """Test konversi UkuranBarang ke dictionary."""
        result = sample_ukuran_medium.to_dict()
        
        assert isinstance(result, dict)
        assert result["nama"] == "M"
        assert result["harga"] == 50000
        assert result["hpp"] == 25000
        assert result["stok"] == 10

    def test_ukuran_from_dict(self):
        """Test pembuatan UkuranBarang dari dictionary."""
        data = {"nama": "L", "harga": 75000, "hpp": 40000, "stok": 5}
        ukuran = UkuranBarang.from_dict(data)
        
        assert ukuran.nama == "L"
        assert ukuran.harga == 75000.0
        assert ukuran.hpp == 40000.0
        assert ukuran.stok == 5

    def test_ukuran_from_dict_type_conversion(self):
        """Test from_dict mengkonversi string ke numeric."""
        data = {"nama": "XL", "harga": "100000", "hpp": "50000", "stok": "3"}
        ukuran = UkuranBarang.from_dict(data)
        
        assert isinstance(ukuran.harga, float)
        assert isinstance(ukuran.hpp, float)
        assert isinstance(ukuran.stok, int)
        assert ukuran.harga == 100000.0

    def test_ukuran_roundtrip(self, sample_ukuran_medium):
        """Test to_dict -> from_dict menghasilkan data yang sama."""
        dict_data = sample_ukuran_medium.to_dict()
        restored = UkuranBarang.from_dict(dict_data)
        
        assert restored.nama == sample_ukuran_medium.nama
        assert restored.harga == sample_ukuran_medium.harga
        assert restored.hpp == sample_ukuran_medium.hpp
        assert restored.stok == sample_ukuran_medium.stok


class TestBarang:
    """Test cases untuk Barang dataclass."""

    def test_create_barang(self):
        """Test pembuatan Barang basic."""
        ukuran = UkuranBarang(nama="M", harga=50000, hpp=25000, stok=10)
        barang = Barang(
            kode="BQT001",
            nama="Buket Mawar",
            warna_kertas=["Merah"],
            warna_bunga=["Putih"],
            ukuran=[ukuran]
        )
        
        assert barang.kode == "BQT001"
        assert barang.nama == "Buket Mawar"
        assert len(barang.ukuran) == 1

    def test_barang_default_values(self):
        """Test Barang dengan default values."""
        barang = Barang(kode="TEST", nama="Test Barang")
        
        assert barang.warna_kertas == []
        assert barang.warna_bunga == []
        assert barang.ukuran == []

    def test_barang_to_dict(self, sample_barang):
        """Test konversi Barang ke dictionary."""
        result = sample_barang.to_dict()
        
        assert isinstance(result, dict)
        assert result["kode"] == "BQT001"
        assert result["nama"] == "Buket Mawar Premium"
        assert "Merah" in result["warna_kertas"]
        assert isinstance(result["ukuran"], list)
        assert len(result["ukuran"]) == 3

    def test_barang_from_dict(self, sample_barang_json_data):
        """Test pembuatan Barang dari dictionary."""
        data = sample_barang_json_data[0]  # BQT001
        barang = Barang.from_dict(data)
        
        assert barang.kode == "BQT001"
        assert barang.nama == "Buket Mawar Premium"
        assert len(barang.ukuran) == 2
        assert barang.ukuran[0].nama == "S"

    def test_barang_from_dict_legacy_format(self, legacy_barang_data):
        """Test backward compatibility dengan format lama (tanpa ukuran array)."""
        barang = Barang.from_dict(legacy_barang_data)
        
        assert barang.kode == "OLD001"
        assert barang.nama == "Buket Lama"
        # Harus auto-generate ukuran "Standar"
        assert len(barang.ukuran) == 1
        assert barang.ukuran[0].nama == "Standar"
        assert barang.ukuran[0].harga == 40000

    def test_barang_from_dict_missing_colors(self):
        """Test from_dict dengan warna kosong."""
        data = {
            "kode": "TEST",
            "nama": "Test",
            "ukuran": [{"nama": "M", "harga": 50000, "hpp": 25000, "stok": 5}]
        }
        barang = Barang.from_dict(data)
        
        assert barang.warna_kertas == []
        assert barang.warna_bunga == []

    def test_barang_roundtrip(self, sample_barang):
        """Test to_dict -> from_dict menghasilkan data yang sama."""
        dict_data = sample_barang.to_dict()
        restored = Barang.from_dict(dict_data)
        
        assert restored.kode == sample_barang.kode
        assert restored.nama == sample_barang.nama
        assert len(restored.ukuran) == len(sample_barang.ukuran)

    def test_get_ukuran_found(self, sample_barang):
        """Test get_ukuran berhasil menemukan ukuran."""
        ukuran = sample_barang.get_ukuran("M")
        
        assert ukuran is not None
        assert ukuran.nama == "M"
        assert ukuran.harga == 50000

    def test_get_ukuran_case_insensitive(self, sample_barang):
        """Test get_ukuran case-insensitive."""
        ukuran_lower = sample_barang.get_ukuran("m")
        ukuran_upper = sample_barang.get_ukuran("M")
        
        assert ukuran_lower is not None
        assert ukuran_upper is not None
        assert ukuran_lower.nama == ukuran_upper.nama

    def test_get_ukuran_not_found(self, sample_barang):
        """Test get_ukuran return None jika tidak ditemukan."""
        ukuran = sample_barang.get_ukuran("XXL")
        
        assert ukuran is None

    def test_get_ukuran_empty_list(self):
        """Test get_ukuran pada barang tanpa ukuran."""
        barang = Barang(kode="EMPTY", nama="Empty")
        result = barang.get_ukuran("M")
        
        assert result is None
