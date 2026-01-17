"""
Unit Tests untuk Transaksi Service.

Menguji finalisasi transaksi dan rekap pendapatan.
"""
import pytest
import csv
import os
from datetime import datetime
from unittest.mock import patch, MagicMock

from core.services.transaksi_service import (
    generate_transaction_id,
    init_transaksi_file
)


class TestGenerateTransactionId:
    """Test cases untuk generate_transaction_id function."""

    def test_generate_id_format(self):
        """Test format ID transaksi: INV-YYYYMMDD-XXXX."""
        tx_id = generate_transaction_id()
        
        assert tx_id.startswith("INV-")
        parts = tx_id.split("-")
        assert len(parts) == 3
        
        # Check date part (YYYYMMDD)
        date_part = parts[1]
        assert len(date_part) == 8
        assert date_part.isdigit()

    def test_generate_id_date_part(self):
        """Test date part sesuai tanggal hari ini."""
        tx_id = generate_transaction_id()
        today = datetime.now().strftime("%Y%m%d")
        
        assert today in tx_id

    def test_generate_id_random_part(self):
        """Test random part adalah 4 karakter."""
        tx_id = generate_transaction_id()
        random_part = tx_id.split("-")[2]
        
        assert len(random_part) == 4

    def test_generate_id_uniqueness(self):
        """Test generate multiple IDs menghasilkan ID berbeda."""
        ids = set()
        for _ in range(100):
            ids.add(generate_transaction_id())
        
        # Should be mostly unique (allowing small chance of collision)
        assert len(ids) >= 95


class TestInitTransaksiFile:
    """Test cases untuk init_transaksi_file function."""

    def test_init_creates_file(self, temp_transaksi_file, temp_data_dir):
        """Test init membuat file CSV baru."""
        with patch('core.services.transaksi_service.TRANSAKSI_FILE', str(temp_transaksi_file)):
            with patch('core.services.transaksi_service.DATA_DIR', str(temp_data_dir)):
                init_transaksi_file()
        
        assert os.path.exists(temp_transaksi_file)

    def test_init_creates_headers(self, temp_transaksi_file, temp_data_dir):
        """Test init membuat file dengan headers."""
        with patch('core.services.transaksi_service.TRANSAKSI_FILE', str(temp_transaksi_file)):
            with patch('core.services.transaksi_service.DATA_DIR', str(temp_data_dir)):
                init_transaksi_file()
        
        with open(temp_transaksi_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)
        
        # Should have headers (using actual column names from TRANSAKSI_HEADERS)
        assert len(headers) > 0
        assert "id_transaksi" in headers or "waktu" in headers

    def test_init_does_not_overwrite(self, temp_transaksi_file, temp_data_dir):
        """Test init tidak overwrite file existing."""
        # Create file with custom content
        with open(temp_transaksi_file, "w", encoding="utf-8") as f:
            f.write("existing,content\n")
            f.write("row1,data1\n")
        
        with patch('core.services.transaksi_service.TRANSAKSI_FILE', str(temp_transaksi_file)):
            with patch('core.services.transaksi_service.DATA_DIR', str(temp_data_dir)):
                init_transaksi_file()
        
        # Should not overwrite
        with open(temp_transaksi_file, "r") as f:
            content = f.read()
        
        assert "existing" in content or "row1" in content
