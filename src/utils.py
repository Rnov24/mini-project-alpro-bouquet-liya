"""
Utility functions: input validators dan formatters.
"""
import os
from src.config import DATA_DIR


# ============== TERMINAL COLORS ==============
class Colors:
    """ANSI color codes untuk terminal."""
    # Reset
    RESET = "\033[0m"
    
    # Regular Colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bold
    BOLD = "\033[1m"
    BOLD_RED = "\033[1;31m"
    BOLD_GREEN = "\033[1;32m"
    BOLD_YELLOW = "\033[1;33m"
    BOLD_BLUE = "\033[1;34m"
    BOLD_MAGENTA = "\033[1;35m"
    BOLD_CYAN = "\033[1;36m"
    BOLD_WHITE = "\033[1;37m"
    
    # Background
    BG_GREEN = "\033[42m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    
    # Dim
    DIM = "\033[2m"


# ============== UI HELPERS ==============
def clear_screen() -> None:
    """Bersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str, subtitle: str = "") -> None:
    """Tampilkan header dengan border cantik."""
    c = Colors
    width = 50
    
    print()
    print(f"{c.BOLD_CYAN}╔{'═' * width}╗{c.RESET}")
    print(f"{c.BOLD_CYAN}║{c.RESET}{c.BOLD_MAGENTA}{title:^{width}}{c.RESET}{c.BOLD_CYAN}║{c.RESET}")
    if subtitle:
        print(f"{c.BOLD_CYAN}║{c.RESET}{c.DIM}{subtitle:^{width}}{c.RESET}{c.BOLD_CYAN}║{c.RESET}")
    print(f"{c.BOLD_CYAN}╚{'═' * width}╝{c.RESET}")
    print()


def print_section(title: str) -> None:
    """Tampilkan section header."""
    c = Colors
    print(f"\n{c.BOLD_YELLOW}┌─── {title} {'─' * (40 - len(title))}┐{c.RESET}")


def print_section_end() -> None:
    """Tampilkan section footer."""
    c = Colors
    print(f"{c.BOLD_YELLOW}└{'─' * 46}┘{c.RESET}\n")


def print_menu_item(number: str, text: str, icon: str = "•") -> None:
    """Tampilkan item menu dengan format cantik."""
    c = Colors
    print(f"  {c.BOLD_CYAN}{icon}{c.RESET} [{c.BOLD_YELLOW}{number}{c.RESET}] {c.WHITE}{text}{c.RESET}")


def print_success(message: str) -> None:
    """Tampilkan pesan sukses."""
    c = Colors
    print(f"\n{c.BOLD_GREEN}✓ {message}{c.RESET}\n")


def print_error(message: str) -> None:
    """Tampilkan pesan error."""
    c = Colors
    print(f"\n{c.BOLD_RED}✗ {message}{c.RESET}\n")


def print_warning(message: str) -> None:
    """Tampilkan pesan warning."""
    c = Colors
    print(f"\n{c.BOLD_YELLOW}⚠ {message}{c.RESET}\n")


def print_info(message: str) -> None:
    """Tampilkan pesan info."""
    c = Colors
    print(f"{c.CYAN}ℹ {message}{c.RESET}")


def print_divider(char: str = "─", length: int = 50) -> None:
    """Tampilkan garis pemisah."""
    c = Colors
    print(f"{c.DIM}{char * length}{c.RESET}")


def input_styled(prompt: str) -> str:
    """Input dengan style."""
    c = Colors
    return input(f"{c.BOLD_GREEN}▸ {c.WHITE}{prompt}{c.RESET}")


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
