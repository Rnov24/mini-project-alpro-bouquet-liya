"""
Fungsi helper untuk output terminal CLI.

Modul ini berisi fungsi-fungsi untuk menampilkan pesan dengan
formatting yang konsisten.
"""
import os
from cli.ui.colors import Colors


def clear_screen() -> None:
    """Membersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str, subtitle: str = "") -> None:
    """Menampilkan header dengan border dekoratif."""
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
    """Menampilkan header untuk section."""
    c = Colors
    padding = 40 - len(title)
    if padding < 0:
        padding = 0
    print(f"\n{c.BOLD_YELLOW}┌─── {title} {'─' * padding}┐{c.RESET}")


def print_section_end() -> None:
    """Menampilkan footer untuk section."""
    c = Colors
    print(f"{c.BOLD_YELLOW}└{'─' * 46}┘{c.RESET}\n")


def print_menu_item(number: str, text: str, icon: str = "•") -> None:
    """Menampilkan item menu dengan format standar."""
    c = Colors
    print(f"  {c.BOLD_CYAN}{icon}{c.RESET} [{c.BOLD_YELLOW}{number}{c.RESET}] {c.WHITE}{text}{c.RESET}")


def print_success(message: str) -> None:
    """Menampilkan pesan sukses (hijau dengan checkmark)."""
    c = Colors
    print(f"\n{c.BOLD_GREEN}✓ {message}{c.RESET}\n")


def print_error(message: str) -> None:
    """Menampilkan pesan error (merah dengan ✗)."""
    c = Colors
    print(f"\n{c.BOLD_RED}✗ {message}{c.RESET}\n")


def print_warning(message: str) -> None:
    """Menampilkan pesan warning (kuning dengan ⚠)."""
    c = Colors
    print(f"\n{c.BOLD_YELLOW}⚠ {message}{c.RESET}\n")


def print_info(message: str) -> None:
    """Menampilkan pesan informasi (cyan dengan ℹ)."""
    c = Colors
    print(f"{c.CYAN}ℹ {message}{c.RESET}")


def print_divider(char: str = "─", length: int = 50) -> None:
    """Menampilkan garis pemisah horizontal."""
    c = Colors
    print(f"{c.DIM}{char * length}{c.RESET}")
