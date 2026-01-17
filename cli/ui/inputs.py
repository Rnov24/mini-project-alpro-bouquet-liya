"""
Fungsi input dengan validasi untuk CLI.

Modul ini berisi fungsi-fungsi untuk mengambil input dari user
dengan validasi built-in dan error messages yang konsisten.
"""
from cli.ui.colors import Colors
from cli.errors import ErrorMsg


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
        print(f"{Colors.BOLD_RED}✗ {ErrorMsg.INPUT_EMPTY}{Colors.RESET}")


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
                print(f"{Colors.BOLD_RED}✗ {ErrorMsg.INPUT_BELOW_MIN.format(min_val=min_val)}{Colors.RESET}")
                continue
            if max_val is not None and val > max_val:
                print(f"{Colors.BOLD_RED}✗ {ErrorMsg.INPUT_ABOVE_MAX.format(max_val=max_val)}{Colors.RESET}")
                continue
            return val
        except ValueError:
            print(f"{Colors.BOLD_RED}✗ {ErrorMsg.INPUT_NOT_INT}{Colors.RESET}")


def input_float(prompt: str, min_val: float | None = None) -> float:
    """Mengambil input angka desimal dengan validasi minimum."""
    while True:
        try:
            raw = input(prompt).strip().replace(",", ".")
            val = float(raw)
            if min_val is not None and val < min_val:
                print(f"{Colors.BOLD_RED}✗ {ErrorMsg.INPUT_BELOW_MIN.format(min_val=min_val)}{Colors.RESET}")
                continue
            return val
        except ValueError:
            print(f"{Colors.BOLD_RED}✗ {ErrorMsg.INPUT_NOT_FLOAT}{Colors.RESET}")


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
        print(f"{Colors.BOLD_RED}✗ {ErrorMsg.INPUT_INVALID_CHOICE.format(choices=choices_display)}{Colors.RESET}")


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
        print(f"{Colors.BOLD_RED}✗ {ErrorMsg.INPUT_YES_NO}{Colors.RESET}")
