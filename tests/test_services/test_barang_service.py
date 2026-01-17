"""
Unit Tests untuk Barang Service.

Menguji operasi CRUD katalog barang.
"""
import pytest
import json
import os
from unittest.mock import patch, mock_open

from core.models.barang import Barang, UkuranBarang
from core.services.barang_service import (
    load_barang, save_barang, find_by_kode, search_barang,
    load_barang_dict, save_barang_dict, get_barang_by_kode_dict
)


class TestLoadBarang:
    """Test cases untuk load_barang function."""

    def test_load_barang_empty_file(self, temp_barang_file):
        """Test load dari file kosong / tidak ada."""
        with patch('core.services.barang_service.BARANG_FILE', str(temp_barang_file)):
            result = load_barang()
        
        assert result == []

    def test_load_barang_with_data(self, populated_barang_file):
        """Test load dari file dengan data."""
        with patch('core.services.barang_service.BARANG_FILE', str(populated_barang_file)):
            result = load_barang()
        
        assert len(result) == 2
        assert isinstance(result[0], Barang)
        assert result[0].kode == "BQT001"

    def test_load_barang_returns_barang_objects(self, populated_barang_file):
        """Test bahwa load_barang mengembalikan list of Barang."""
        with patch('core.services.barang_service.BARANG_FILE', str(populated_barang_file)):
            result = load_barang()
        
        for item in result:
            assert isinstance(item, Barang)


class TestLoadBarangDict:
    """Test cases untuk load_barang_dict function."""

    def test_load_barang_dict_empty(self, temp_barang_file):
        """Test load dict dari file tidak ada."""
        with patch('core.services.barang_service.BARANG_FILE', str(temp_barang_file)):
            result = load_barang_dict()
        
        assert result == []

    def test_load_barang_dict_with_data(self, populated_barang_file):
        """Test load dict dari file dengan data."""
        with patch('core.services.barang_service.BARANG_FILE', str(populated_barang_file)):
            result = load_barang_dict()
        
        assert len(result) == 2
        assert isinstance(result[0], dict)
        assert result[0]["kode"] == "BQT001"


class TestSaveBarang:
    """Test cases untuk save_barang function."""

    def test_save_barang_creates_file(self, temp_barang_file, sample_barang):
        """Test save_barang membuat file baru."""
        with patch('core.services.barang_service.BARANG_FILE', str(temp_barang_file)):
            save_barang([sample_barang])
        
        assert os.path.exists(temp_barang_file)

    def test_save_barang_content(self, temp_barang_file, sample_barang):
        """Test isi file yang disimpan benar."""
        with patch('core.services.barang_service.BARANG_FILE', str(temp_barang_file)):
            save_barang([sample_barang])
        
        with open(temp_barang_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        assert len(data) == 1
        assert data[0]["kode"] == "BQT001"
        assert data[0]["nama"] == "Buket Mawar Premium"

    def test_save_barang_multiple(self, temp_barang_file, sample_barang, sample_barang_minimal):
        """Test save multiple barang."""
        with patch('core.services.barang_service.BARANG_FILE', str(temp_barang_file)):
            save_barang([sample_barang, sample_barang_minimal])
        
        with open(temp_barang_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        assert len(data) == 2

    def test_save_barang_empty_list(self, temp_barang_file):
        """Test save list kosong."""
        with patch('core.services.barang_service.BARANG_FILE', str(temp_barang_file)):
            save_barang([])
        
        with open(temp_barang_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        assert data == []


class TestSaveBarangDict:
    """Test cases untuk save_barang_dict function."""

    def test_save_barang_dict(self, temp_barang_file, sample_barang_json_data):
        """Test save list of dicts."""
        with patch('core.services.barang_service.BARANG_FILE', str(temp_barang_file)):
            save_barang_dict(sample_barang_json_data)
        
        with open(temp_barang_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        assert len(data) == 2


class TestFindByKode:
    """Test cases untuk find_by_kode function."""

    def test_find_by_kode_found(self, sample_barang, sample_barang_minimal):
        """Test mencari kode yang ada."""
        barang_list = [sample_barang, sample_barang_minimal]
        result = find_by_kode(barang_list, "BQT001")
        
        assert result is not None
        assert result.kode == "BQT001"

    def test_find_by_kode_not_found(self, sample_barang):
        """Test mencari kode yang tidak ada."""
        result = find_by_kode([sample_barang], "NOTEXIST")
        
        assert result is None

    def test_find_by_kode_case_insensitive(self, sample_barang):
        """Test pencarian case-insensitive."""
        result_lower = find_by_kode([sample_barang], "bqt001")
        result_upper = find_by_kode([sample_barang], "BQT001")
        result_mixed = find_by_kode([sample_barang], "Bqt001")
        
        assert result_lower is not None
        assert result_upper is not None
        assert result_mixed is not None

    def test_find_by_kode_with_whitespace(self, sample_barang):
        """Test pencarian dengan whitespace."""
        result = find_by_kode([sample_barang], "  BQT001  ")
        
        assert result is not None
        assert result.kode == "BQT001"

    def test_find_by_kode_empty_list(self):
        """Test pencarian di list kosong."""
        result = find_by_kode([], "BQT001")
        
        assert result is None


class TestSearchBarang:
    """Test cases untuk search_barang function."""

    def test_search_by_kode(self, sample_barang, sample_barang_minimal):
        """Test search berdasarkan kode."""
        barang_list = [sample_barang, sample_barang_minimal]
        results = search_barang(barang_list, "BQT001")
        
        assert len(results) == 1
        assert results[0].kode == "BQT001"

    def test_search_by_nama(self, sample_barang, sample_barang_minimal):
        """Test search berdasarkan nama."""
        barang_list = [sample_barang, sample_barang_minimal]
        results = search_barang(barang_list, "Mawar")
        
        assert len(results) == 1
        assert "Mawar" in results[0].nama

    def test_search_partial_match(self, sample_barang, sample_barang_minimal):
        """Test partial match."""
        barang_list = [sample_barang, sample_barang_minimal]
        results = search_barang(barang_list, "Buket")
        
        assert len(results) == 2  # Both contain "Buket"

    def test_search_case_insensitive(self, sample_barang):
        """Test search case-insensitive."""
        results = search_barang([sample_barang], "mawar")
        
        assert len(results) == 1

    def test_search_no_results(self, sample_barang):
        """Test search tanpa hasil."""
        results = search_barang([sample_barang], "Melati")
        
        assert len(results) == 0

    def test_search_empty_list(self):
        """Test search di list kosong."""
        results = search_barang([], "test")
        
        assert len(results) == 0


class TestGetBarangByKodeDict:
    """Test cases untuk get_barang_by_kode_dict function."""

    def test_get_by_kode_dict_found(self, sample_barang_json_data):
        """Test mencari dari list dict."""
        result = get_barang_by_kode_dict(sample_barang_json_data, "BQT001")
        
        assert result is not None
        assert result["kode"] == "BQT001"

    def test_get_by_kode_dict_not_found(self, sample_barang_json_data):
        """Test mencari kode yang tidak ada."""
        result = get_barang_by_kode_dict(sample_barang_json_data, "NOTEXIST")
        
        assert result is None

    def test_get_by_kode_dict_case_insensitive(self, sample_barang_json_data):
        """Test pencarian case-insensitive."""
        result = get_barang_by_kode_dict(sample_barang_json_data, "bqt002")
        
        assert result is not None
        assert result["kode"] == "BQT002"


class TestRoundTrip:
    """Integration tests untuk save -> load roundtrip."""

    def test_save_load_roundtrip(self, temp_barang_file, sample_barang):
        """Test save kemudian load menghasilkan data sama."""
        with patch('core.services.barang_service.BARANG_FILE', str(temp_barang_file)):
            # Save
            save_barang([sample_barang])
            
            # Load
            loaded = load_barang()
        
        assert len(loaded) == 1
        assert loaded[0].kode == sample_barang.kode
        assert loaded[0].nama == sample_barang.nama
        assert len(loaded[0].ukuran) == len(sample_barang.ukuran)

    def test_dict_roundtrip(self, temp_barang_file, sample_barang_json_data):
        """Test save_dict kemudian load_dict."""
        with patch('core.services.barang_service.BARANG_FILE', str(temp_barang_file)):
            save_barang_dict(sample_barang_json_data)
            loaded = load_barang_dict()
        
        assert len(loaded) == len(sample_barang_json_data)
        assert loaded[0]["kode"] == sample_barang_json_data[0]["kode"]
