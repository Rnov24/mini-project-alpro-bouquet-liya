"""
Business logic untuk operasi Transaksi.
"""
from src.models.barang import Barang, save_barang, find_by_kode
from src.models.transaksi import (
    TransaksiItem, save_transaksi, load_transaksi, get_rekap_pendapatan
)
from src.utils import input_int, input_float, format_rupiah


def tampil_struk(
    keranjang: list[TransaksiItem],
    total: float,
    diskon: float,
    total_bayar: float
) -> None:
    """Tampilkan struk transaksi."""
    print("\n===== STRUK =====")
    print(f"{'Kode':<8} {'Nama':<20} {'Qty':>3} {'Harga':>10} {'Sub':>12}")
    print("-" * 60)
    for item in keranjang:
        print(
            f"{item.kode:<8} {item.nama:<20} {item.qty:>3} "
            f"{format_rupiah(item.harga):>10} {format_rupiah(item.subtotal):>12}"
        )
    print("-" * 60)
    print(f"{'Total':<35} Rp{format_rupiah(total):>12}")
    print(f"{'Diskon':<35} Rp{format_rupiah(diskon):>12}")
    print(f"{'Total Bayar':<35} Rp{format_rupiah(total_bayar):>12}")
    print("=================\n")


def rollback_stok(barang_list: list[Barang], keranjang: list[TransaksiItem]) -> None:
    """Kembalikan stok jika transaksi dibatalkan."""
    for item in keranjang:
        barang = find_by_kode(barang_list, item.kode)
        if barang is not None:
            barang.stok += item.qty
    save_barang(barang_list)


def hitung_diskon(total: float) -> float:
    """Tanya dan hitung diskon. Return nilai diskon."""
    pakai_diskon = input("Pakai diskon? (y/n): ").strip().lower()
    if pakai_diskon != "y":
        return 0.0
    
    persen = input_float("Diskon persen (0-100): ", min_val=0)
    if persen > 100:
        persen = 100
    
    return total * (persen / 100)


def proses_transaksi(barang_list: list[Barang]) -> bool:
    """Proses transaksi penjualan. Return True jika berhasil."""
    if not barang_list:
        print("\n[!] Data barang kosong. Tambahkan barang dulu.\n")
        return False
    
    print("\n=== TRANSAKSI PENJUALAN ===")
    print("Ketik 'SELESAI' untuk mengakhiri input barang.\n")
    
    keranjang: list[TransaksiItem] = []
    
    while True:
        kode = input("Kode barang: ").strip()
        if not kode:
            print("Kode tidak boleh kosong.")
            continue
        if kode.upper() == "SELESAI":
            break
        
        barang = find_by_kode(barang_list, kode.upper())
        if barang is None:
            print("[!] Kode tidak ditemukan.")
            continue
        
        print(f"-> {barang.nama} | Harga: {format_rupiah(barang.harga)} | Stok: {barang.stok}")
        
        if barang.stok == 0:
            print("[!] Stok habis.")
            continue
        
        qty = input_int("Qty: ", min_val=1)
        if qty > barang.stok:
            print("[!] Qty melebihi stok.")
            continue
        
        # Buat item dan kurangi stok
        item = TransaksiItem.from_cart(barang.kode, barang.nama, qty, barang.harga)
        keranjang.append(item)
        barang.stok -= qty
        print("[✓] Ditambahkan ke keranjang.\n")
    
    if not keranjang:
        print("[!] Tidak ada item. Transaksi dibatalkan.")
        return False
    
    # Hitung total dan diskon
    total = sum(item.subtotal for item in keranjang)
    diskon = hitung_diskon(total)
    total_bayar = total - diskon
    
    # Tampilkan ringkasan
    print("\n=== RINGKASAN ===")
    tampil_struk(keranjang, total, diskon, total_bayar)
    
    # Proses pembayaran
    bayar = input_float("Uang bayar: ", min_val=0)
    if bayar < total_bayar:
        print("[!] Uang kurang. Transaksi dibatalkan dan stok dikembalikan.")
        rollback_stok(barang_list, keranjang)
        return False
    
    kembalian = bayar - total_bayar
    print(f"Kembalian: Rp{format_rupiah(kembalian)}")
    
    # Simpan transaksi
    save_transaksi(keranjang, total_bayar)
    save_barang(barang_list)
    
    print("[✓] Transaksi berhasil disimpan.")
    return True


def tampil_riwayat(limit: int = 20) -> None:
    """Tampilkan riwayat transaksi terakhir."""
    rows = load_transaksi(limit)
    
    if not rows:
        print("\n[!] Belum ada transaksi.\n")
        return
    
    print("\n=== RIWAYAT TRANSAKSI (TERAKHIR) ===")
    print(f"{'Waktu':<19} {'ID':<16} {'Kode':<8} {'Qty':>3} {'Subtotal':>12} {'TotalTrx':>12}")
    print("-" * 80)
    
    for r in rows:
        print(
            f"{r['waktu']:<19} {r['id_transaksi']:<16} {r['kode']:<8} "
            f"{int(float(r['qty'])):>3} {format_rupiah(float(r['subtotal'])):>12} "
            f"{format_rupiah(float(r['total_transaksi'])):>12}"
        )
    print("-" * 80)


def tampil_rekap() -> None:
    """Tampilkan rekap total pendapatan."""
    jumlah_trx, total_pendapatan = get_rekap_pendapatan()
    
    if jumlah_trx == 0:
        print("\n[!] Belum ada transaksi.\n")
        return
    
    print("\n=== REKAP ===")
    print(f"Jumlah transaksi : {jumlah_trx}")
    print(f"Total pendapatan : Rp{format_rupiah(total_pendapatan)}\n")
