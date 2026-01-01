"""
Utility functions: input validators dan formatters.
"""
import os
from src.config import DATA_DIR


def ensure_data_dir() -> None:
    """Pastikan folder data ada."""
    os.makedirs(DATA_DIR, exist_ok=True)


def input_non_empty(prompt: str) -> str:
    """Input yang tidak boleh kosong."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input tidak boleh kosong.")


def input_int(prompt: str, min_val: int | None = None, max_val: int | None = None) -> int:
    """Input integer dengan validasi range."""
    while True:
        try:
            val = int(input(prompt).strip())
            if min_val is not None and val < min_val:
                print(f"Nilai minimal adalah {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Nilai maksimal adalah {max_val}.")
                continue
            return val
        except ValueError:
            print("Harus berupa bilangan bulat.")


def input_float(prompt: str, min_val: float | None = None) -> float:
    """Input float dengan validasi minimum."""
    while True:
        try:
            val = float(input(prompt).strip())
            if min_val is not None and val < min_val:
                print(f"Nilai minimal adalah {min_val}.")
                continue
            return val
        except ValueError:
            print("Harus berupa angka (contoh: 12000 atau 12000.5).")


def format_rupiah(amount: float) -> str:
    """Format angka ke format rupiah (15000 -> 15.000)."""
    return f"{int(round(amount)):,}".replace(",", ".")
