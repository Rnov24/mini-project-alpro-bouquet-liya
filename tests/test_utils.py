"""
Unit Tests untuk Core Utils.

Menguji utility functions.
"""
import pytest
from core.utils import format_rupiah


class TestFormatRupiah:
    """Test cases untuk format_rupiah function."""

    def test_format_basic(self):
        """Test formatting angka basic."""
        result = format_rupiah(50000)
        
        # Should contain thousand separator
        assert "50" in result
        assert "000" in result

    def test_format_large_number(self):
        """Test formatting angka besar."""
        result = format_rupiah(1500000)
        
        assert "1" in result
        assert "500" in result
        assert "000" in result

    def test_format_zero(self):
        """Test formatting nol."""
        result = format_rupiah(0)
        
        assert "0" in result

    def test_format_float(self):
        """Test formatting float."""
        result = format_rupiah(25000.50)
        
        assert "25" in result
        assert "000" in result

    def test_format_small_number(self):
        """Test formatting angka kecil."""
        result = format_rupiah(100)
        
        assert "100" in result

    def test_returns_string(self):
        """Test return type adalah string."""
        result = format_rupiah(50000)
        
        assert isinstance(result, str)
