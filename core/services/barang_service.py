"""
Service untuk operasi CRUD Barang/Katalog.

Modul ini menyediakan fungsi untuk membaca dan menyimpan data katalog.
"""
import json
import os
from typing import Optional

from core.config import BARANG_FILE, DATA_DIR
from core.models.barang import Barang, UkuranBarang


def ensure_data_dir() -> None:
    """Memastikan direktori data ada."""
    os.makedirs(DATA_DIR, exist_ok=True)


def load_barang() -> list[Barang]:
    """Memuat semua barang dari katalog sebagai objek Barang."""
    ensure_data_dir()
    try:
        with open(BARANG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Barang.from_dict(item) for item in data]
    except FileNotFoundError:
        return []


def load_barang_dict() -> list[dict]:
    """Memuat katalog barang sebagai list dictionary."""
    ensure_data_dir()
    try:
        with open(BARANG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_barang(barang_list: list[Barang]) -> None:
    """Menyimpan list objek Barang ke file JSON."""
    ensure_data_dir()
    data = [b.to_dict() for b in barang_list]
    with open(BARANG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_barang_dict(barang_list: list[dict]) -> None:
    """Menyimpan list dictionary barang ke file JSON."""
    ensure_data_dir()
    with open(BARANG_FILE, "w", encoding="utf-8") as f:
        json.dump(barang_list, f, ensure_ascii=False, indent=2)


def find_by_kode(barang_list: list[Barang], kode: str) -> Optional[Barang]:
    """Mencari barang berdasarkan kode."""
    kode = kode.strip().lower()
    for b in barang_list:
        if b.kode.lower() == kode:
            return b
    return None


def search_barang(barang_list: list[Barang], keyword: str) -> list[Barang]:
    """Mencari barang berdasarkan keyword di kode atau nama."""
    keyword = keyword.lower()
    return [b for b in barang_list if keyword in b.kode.lower() or keyword in b.nama.lower()]


def get_barang_by_kode_dict(barang_list: list[dict], kode: str) -> Optional[dict]:
    """Mencari barang dari list dict berdasarkan kode."""
    kode = kode.strip().lower()
    for b in barang_list:
        if b.get("kode", "").lower() == kode:
            return b
    return None
