"""
Unit Tests untuk CLI Input Functions.

Menguji validasi input dari user.

Note: Karena input functions interaktif (menggunakan input()),
kita menggunakan mock untuk simulate user input.
"""
import pytest
from unittest.mock import patch

from cli.ui.inputs import (
    input_styled,
    input_non_empty,
    input_int,
    input_float,
    input_choice,
    input_yes_no
)


class TestInputNonEmpty:
    """Test cases untuk input_non_empty function."""

    def test_valid_input(self):
        """Test input yang valid langsung diterima."""
        with patch('builtins.input', return_value="Hello World"):
            result = input_non_empty("Enter: ")
        
        assert result == "Hello World"

    def test_whitespace_stripped(self):
        """Test whitespace di-strip."""
        with patch('builtins.input', return_value="  Test  "):
            result = input_non_empty("Enter: ")
        
        assert result == "Test"

    def test_empty_then_valid(self):
        """Test input kosong kemudian valid."""
        with patch('builtins.input', side_effect=["", "   ", "Valid"]):
            with patch('builtins.print'):  # Suppress error messages
                result = input_non_empty("Enter: ")
        
        assert result == "Valid"


class TestInputInt:
    """Test cases untuk input_int function."""

    def test_valid_integer(self):
        """Test input integer valid."""
        with patch('builtins.input', return_value="42"):
            result = input_int("Enter number: ")
        
        assert result == 42

    def test_negative_integer(self):
        """Test input integer negatif."""
        with patch('builtins.input', return_value="-10"):
            result = input_int("Enter: ")
        
        assert result == -10

    def test_min_value_validation(self):
        """Test validasi nilai minimum."""
        # First input below min, second valid
        with patch('builtins.input', side_effect=["3", "10"]):
            with patch('builtins.print'):
                result = input_int("Enter: ", min_val=5)
        
        assert result == 10

    def test_max_value_validation(self):
        """Test validasi nilai maksimum."""
        # First input above max, second valid
        with patch('builtins.input', side_effect=["100", "50"]):
            with patch('builtins.print'):
                result = input_int("Enter: ", max_val=75)
        
        assert result == 50

    def test_range_validation(self):
        """Test validasi range min-max."""
        with patch('builtins.input', side_effect=["1", "15", "10"]):
            with patch('builtins.print'):
                result = input_int("Enter: ", min_val=5, max_val=12)
        
        assert result == 10

    def test_invalid_then_valid(self):
        """Test input non-integer kemudian valid."""
        with patch('builtins.input', side_effect=["abc", "12.5", "25"]):
            with patch('builtins.print'):
                result = input_int("Enter: ")
        
        assert result == 25

    def test_whitespace_stripped(self):
        """Test whitespace di-strip sebelum parsing."""
        with patch('builtins.input', return_value="  99  "):
            result = input_int("Enter: ")
        
        assert result == 99


class TestInputFloat:
    """Test cases untuk input_float function."""

    def test_valid_float(self):
        """Test input float valid."""
        with patch('builtins.input', return_value="3.14"):
            result = input_float("Enter: ")
        
        assert result == 3.14

    def test_integer_as_float(self):
        """Test integer diterima sebagai float."""
        with patch('builtins.input', return_value="100"):
            result = input_float("Enter: ")
        
        assert result == 100.0

    def test_comma_as_decimal_separator(self):
        """Test koma sebagai pemisah desimal (format Indonesia)."""
        with patch('builtins.input', return_value="50,5"):
            result = input_float("Enter: ")
        
        assert result == 50.5

    def test_min_value_validation(self):
        """Test validasi nilai minimum."""
        with patch('builtins.input', side_effect=["-5", "10"]):
            with patch('builtins.print'):
                result = input_float("Enter: ", min_val=0)
        
        assert result == 10.0

    def test_invalid_then_valid(self):
        """Test input invalid kemudian valid."""
        with patch('builtins.input', side_effect=["abc", "xyz", "25.5"]):
            with patch('builtins.print'):
                result = input_float("Enter: ")
        
        assert result == 25.5


class TestInputChoice:
    """Test cases untuk input_choice function."""

    def test_valid_choice(self):
        """Test memilih opsi yang valid."""
        with patch('builtins.input', return_value="A"):
            result = input_choice("Choose: ", ["A", "B", "C"])
        
        assert result == "A"

    def test_case_insensitive_default(self):
        """Test default case-insensitive."""
        with patch('builtins.input', return_value="a"):
            result = input_choice("Choose: ", ["A", "B", "C"])
        
        assert result == "A"  # Returns original case

    def test_case_sensitive(self):
        """Test mode case-sensitive."""
        with patch('builtins.input', side_effect=["a", "A"]):
            with patch('builtins.print'):
                result = input_choice("Choose: ", ["A", "B"], case_sensitive=True)
        
        assert result == "A"

    def test_invalid_then_valid(self):
        """Test input invalid kemudian valid."""
        with patch('builtins.input', side_effect=["X", "D", "B"]):
            with patch('builtins.print'):
                result = input_choice("Choose: ", ["A", "B", "C"])
        
        assert result == "B"


class TestInputYesNo:
    """Test cases untuk input_yes_no function."""

    def test_yes_variations(self):
        """Test berbagai variasi yes."""
        for yes_input in ["y", "Y", "ya", "YA", "yes", "YES"]:
            with patch('builtins.input', return_value=yes_input):
                result = input_yes_no("Confirm?")
            assert result is True

    def test_no_variations(self):
        """Test berbagai variasi no."""
        for no_input in ["n", "N", "no", "NO", "tidak"]:
            with patch('builtins.input', return_value=no_input):
                result = input_yes_no("Confirm?")
            assert result is False

    def test_default_yes(self):
        """Test default=True dengan input kosong."""
        with patch('builtins.input', return_value=""):
            result = input_yes_no("Confirm?", default=True)
        
        assert result is True

    def test_default_no(self):
        """Test default=False dengan input kosong."""
        with patch('builtins.input', return_value=""):
            result = input_yes_no("Confirm?", default=False)
        
        assert result is False

    def test_invalid_then_valid(self):
        """Test input invalid kemudian valid."""
        with patch('builtins.input', side_effect=["maybe", "xyz", "y"]):
            with patch('builtins.print'):
                result = input_yes_no("Confirm?")
        
        assert result is True
