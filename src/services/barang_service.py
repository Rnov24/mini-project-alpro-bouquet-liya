"""
Business logic untuk operasi Barang.
"""
from src.models.barang import (
    Barang, UkuranBarang, load_barang, save_barang, find_by_kode, search_barang
)
from src.utils import (
    input_non_empty, input_int, input_float, format_rupiah,
    Colors, print_success, print_error, print_warning, print_divider
)


UKURAN_OPTIONS = ["Mini", "Standar", "Besar"]


def tampil_semua_barang(barang_list: list[Barang]) -> None:
    """Tampilkan semua barang dalam format tabel."""
    c = Colors
    
    if not barang_list:
        print_warning("Data barang masih kosong.")
        return
    
    print(f"\n{c.BOLD_CYAN}┌──────────────────────────────────────────────────┐{c.RESET}")
    print(f"{c.BOLD_CYAN}│{c.RESET}           {c.BOLD_MAGENTA}🌸 DAFTAR KATALOG BUQET 🌸{c.RESET}            {c.BOLD_CYAN}│{c.RESET}")
    print(f"{c.BOLD_CYAN}└──────────────────────────────────────────────────┘{c.RESET}")
    
    for i, b in enumerate(barang_list, start=1):
        print(f"\n{c.BOLD_YELLOW}╔═══ [{i}] ════════════════════════════════════════╗{c.RESET}")
        print(f"{c.BOLD_YELLOW}║{c.RESET} {c.BOLD_WHITE}📦 [{b.kode}]{c.RESET} {c.BOLD_CYAN}{b.nama}{c.RESET}")
        print(f"{c.BOLD_YELLOW}╟────────────────────────────────────────────────╢{c.RESET}")
        
        if b.warna_kertas:
            print(f"{c.BOLD_YELLOW}║{c.RESET} {c.GREEN}🎨 Warna Kertas:{c.RESET} {', '.join(b.warna_kertas)}")
        if b.warna_bunga:
            print(f"{c.BOLD_YELLOW}║{c.RESET} {c.MAGENTA}🌺 Warna Bunga:{c.RESET}  {', '.join(b.warna_bunga)}")
        
        print(f"{c.BOLD_YELLOW}╟────────────────────────────────────────────────╢{c.RESET}")
        print(f"{c.BOLD_YELLOW}║{c.RESET} {c.BOLD_WHITE}{'Ukuran':<10} {'Harga':>12} {'HPP':>10} {'Stok':>6}{c.RESET}")
        print(f"{c.BOLD_YELLOW}║{c.RESET} {c.DIM}{'─'*42}{c.RESET}")
        
        for u in b.ukuran:
            stok_color = c.BOLD_GREEN if u.stok > 5 else (c.BOLD_YELLOW if u.stok > 0 else c.BOLD_RED)
            print(f"{c.BOLD_YELLOW}║{c.RESET} {c.CYAN}{u.nama:<10}{c.RESET} {c.WHITE}Rp{format_rupiah(u.harga):>10}{c.RESET} {c.DIM}Rp{format_rupiah(u.hpp):>8}{c.RESET} {stok_color}{u.stok:>6}{c.RESET}")
        
        print(f"{c.BOLD_YELLOW}╚════════════════════════════════════════════════╝{c.RESET}")
    print()


def tambah_barang(barang_list: list[Barang]) -> bool:
    """Tambah barang baru. Return True jika berhasil."""
    c = Colors
    
    print(f"\n{c.BOLD_GREEN}▸ Masukkan data katalog baru:{c.RESET}\n")
    
    kode = input(f"{c.CYAN}  Kode barang: {c.RESET}").strip().upper()
    if not kode:
        print_error("Kode tidak boleh kosong.")
        return False
    
    if find_by_kode(barang_list, kode) is not None:
        print_error("Kode sudah ada. Gunakan menu update.")
        return False
    
    nama = input(f"{c.CYAN}  Nama Katalog Buqet: {c.RESET}").strip()
    if not nama:
        print_error("Nama tidak boleh kosong.")
        return False
    
    # Input warna
    print(f"\n{c.BOLD_YELLOW}  ┌─ Input Warna ─────────────────────────────────┐{c.RESET}")
    warna_kertas_str = input(f"{c.CYAN}  │ Warna Kertas (pisah koma): {c.RESET}").strip()
    warna_kertas = [w.strip() for w in warna_kertas_str.split(",") if w.strip()]
    
    warna_bunga_str = input(f"{c.CYAN}  │ Warna Bunga (pisah koma): {c.RESET}").strip()
    warna_bunga = [w.strip() for w in warna_bunga_str.split(",") if w.strip()]
    print(f"{c.BOLD_YELLOW}  └────────────────────────────────────────────────┘{c.RESET}")
    
    # Input ukuran
    ukuran_list = []
    for ukuran_nama in UKURAN_OPTIONS:
        print(f"\n{c.BOLD_CYAN}  ┌─ Ukuran: {ukuran_nama} ─────────────────────────────┐{c.RESET}")
        harga = input_float(f"{c.CYAN}  │ Harga: {c.RESET}", min_val=0)
        hpp = input_float(f"{c.CYAN}  │ HPP: {c.RESET}", min_val=0)
        stok = input_int(f"{c.CYAN}  │ Stok: {c.RESET}", min_val=0)
        print(f"{c.BOLD_CYAN}  └────────────────────────────────────────────────┘{c.RESET}")
        ukuran_list.append(UkuranBarang(nama=ukuran_nama, harga=harga, hpp=hpp, stok=stok))
    
    barang_baru = Barang(
        kode=kode, 
        nama=nama,
        warna_kertas=warna_kertas,
        warna_bunga=warna_bunga,
        ukuran=ukuran_list
    )
    barang_list.append(barang_baru)
    save_barang(barang_list)
    
    print_success(f"Katalog Buqet '{nama}' berhasil ditambahkan!")
    return True


def update_barang(barang_list: list[Barang]) -> bool:
    """Update harga/stok per ukuran. Return True jika berhasil."""
    c = Colors
    
    kode = input(f"\n{c.CYAN}  Masukkan kode barang: {c.RESET}").strip().upper()
    if not kode:
        print_error("Kode tidak boleh kosong.")
        return False
    
    barang = find_by_kode(barang_list, kode)
    if barang is None:
        print_error("Barang tidak ditemukan.")
        return False
    
    print(f"\n{c.BOLD_GREEN}✓ Barang ditemukan:{c.RESET}")
    print(f"  {c.BOLD_CYAN}[{barang.kode}]{c.RESET} {c.BOLD_WHITE}{barang.nama}{c.RESET}\n")
    
    print(f"{c.BOLD_YELLOW}  Pilih Ukuran:{c.RESET}")
    for i, u in enumerate(barang.ukuran, start=1):
        print(f"  {c.CYAN}[{i}]{c.RESET} {u.nama} - Rp{format_rupiah(u.harga)} | HPP: Rp{format_rupiah(u.hpp)} | Stok: {u.stok}")
    
    pilih_ukuran = input_int(f"\n{c.GREEN}  ▸ Pilih ukuran (1-{len(barang.ukuran)}): {c.RESET}", min_val=1, max_val=len(barang.ukuran))
    ukuran = barang.ukuran[pilih_ukuran - 1]
    
    print(f"\n{c.BOLD_YELLOW}  Update {ukuran.nama}:{c.RESET}")
    print(f"  {c.CYAN}[1]{c.RESET} 💵 Update harga")
    print(f"  {c.CYAN}[2]{c.RESET} 📊 Update HPP")
    print(f"  {c.CYAN}[3]{c.RESET} 📦 Update stok")
    
    pilih = input_int(f"\n{c.GREEN}  ▸ Pilih (1/2/3): {c.RESET}", min_val=1, max_val=3)
    
    if pilih == 1:
        harga_baru = input_float(f"{c.CYAN}  Harga baru: {c.RESET}", min_val=0)
        ukuran.harga = harga_baru
        print_success("Harga berhasil diupdate!")
    elif pilih == 2:
        hpp_baru = input_float(f"{c.CYAN}  HPP baru: {c.RESET}", min_val=0)
        ukuran.hpp = hpp_baru
        print_success("HPP berhasil diupdate!")
    else:
        delta = input_int(f"{c.CYAN}  Perubahan stok (contoh: 5 atau -3): {c.RESET}")
        stok_baru = ukuran.stok + delta
        if stok_baru < 0:
            print_error("Stok tidak boleh negatif.")
            return False
        ukuran.stok = stok_baru
        print_success(f"Stok berhasil diupdate! Stok sekarang: {stok_baru}")
    
    save_barang(barang_list)
    return True


def cari_barang(barang_list: list[Barang]) -> None:
    """Cari dan tampilkan barang berdasarkan keyword."""
    c = Colors
    
    keyword = input(f"\n{c.CYAN}  🔍 Masukkan kode/nama: {c.RESET}").strip()
    if not keyword:
        print_error("Keyword tidak boleh kosong.")
        return
    
    hasil = search_barang(barang_list, keyword)
    if not hasil:
        print_warning(f"Tidak ada hasil untuk '{keyword}'")
        return
    
    print(f"\n{c.BOLD_GREEN}✓ Ditemukan {len(hasil)} hasil:{c.RESET}")
    tampil_semua_barang(hasil)
