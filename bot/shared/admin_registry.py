"""
Admin Registry - Menyimpan dan mengelola daftar admin.
"""
import json
import os

DATA_DIR = "data"
ADMIN_REGISTRY_FILE = os.path.join(DATA_DIR, "admins.json")

# Password untuk daftar sebagai admin (ganti sesuai kebutuhan)
ADMIN_REGISTER_PASSWORD = "buqeuetliya2024"


def load_admin_ids() -> list[int]:
    """Load daftar admin ID dari file JSON."""
    if not os.path.exists(ADMIN_REGISTRY_FILE):
        return []
    
    try:
        with open(ADMIN_REGISTRY_FILE, "r") as f:
            data = json.load(f)
            return data.get("admin_ids", [])
    except Exception:
        return []


def save_admin_ids(admin_ids: list[int]) -> None:
    """Simpan daftar admin ID ke file JSON."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(ADMIN_REGISTRY_FILE, "w") as f:
        json.dump({"admin_ids": admin_ids}, f, indent=2)


def register_admin(chat_id: int) -> bool:
    """
    Daftarkan chat_id sebagai admin.
    Return True jika berhasil, False jika sudah terdaftar.
    """
    admin_ids = load_admin_ids()
    
    if chat_id in admin_ids:
        return False  # Sudah terdaftar
    
    admin_ids.append(chat_id)
    save_admin_ids(admin_ids)
    return True


def unregister_admin(chat_id: int) -> bool:
    """
    Hapus chat_id dari daftar admin.
    Return True jika berhasil, False jika tidak ditemukan.
    """
    admin_ids = load_admin_ids()
    
    if chat_id not in admin_ids:
        return False
    
    admin_ids.remove(chat_id)
    save_admin_ids(admin_ids)
    return True


def is_admin(chat_id: int) -> bool:
    """Cek apakah chat_id adalah admin terdaftar."""
    return chat_id in load_admin_ids()


def get_all_admin_ids() -> list[int]:
    """Dapatkan semua admin ID (dari file + env)."""
    from core.config import ADMIN_CHAT_IDS
    
    file_ids = load_admin_ids()
    env_ids = ADMIN_CHAT_IDS if ADMIN_CHAT_IDS else []
    
    # Gabungkan dan hapus duplikat
    all_ids = list(set(file_ids + env_ids))
    return all_ids
