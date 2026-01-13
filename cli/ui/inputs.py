"""
Fungsi input dengan validasi untuk CLI.

Modul ini berisi fungsi-fungsi untuk mengambil input dari user
dengan validasi built-in.
"""
from cli.ui.colors import Colors


def input_styled(prompt: str) -> str:
    """Mengambil input dengan prompt yang di-style."""
    c = Colors
    return input(f"{c.BOLD_GREEN}▸ {c.WHITE}{prompt}{c.RESET}").strip()


def input_non_empty(prompt: str) -> str:
    """Mengambil input yang tidak boleh kosong."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input tidak boleh kosong.")


def input_int(
    prompt: str,
    min_val: int | None = None,
    max_val: int | None = None
) -> int:
    """Mengambil input integer dengan validasi range."""
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
    """Mengambil input angka desimal dengan validasi minimum."""
    while True:
        try:
            raw = input(prompt).strip().replace(",", ".")
            val = float(raw)
            if min_val is not None and val < min_val:
                print(f"Nilai minimal adalah {min_val}.")
                continue
            return val
        except ValueError:
            print("Harus berupa angka.")


def input_choice(
    prompt: str,
    choices: list[str],
    case_sensitive: bool = False
) -> str:
    """Mengambil input yang harus salah satu dari pilihan."""
    choices_display = ", ".join(choices)
    while True:
        value = input(prompt).strip()
        if case_sensitive:
            if value in choices:
                return value
        else:
            for c in choices:
                if value.lower() == c.lower():
                    return c
        print(f"Pilihan tidak valid. Pilih: {choices_display}")


def input_yes_no(prompt: str, default: bool = True) -> bool:
    """Mengambil input konfirmasi ya/tidak."""
    hint = "(Y/n)" if default else "(y/N)"
    full_prompt = f"{prompt} {hint}: "
    while True:
        value = input(full_prompt).strip().lower()
        if value == "":
            return default
        if value in ["y", "ya", "yes"]:
            return True
        if value in ["n", "no", "tidak"]:
            return False
        print("Masukkan Y untuk ya atau N untuk tidak.")
