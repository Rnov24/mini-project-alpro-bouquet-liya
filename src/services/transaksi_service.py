"""
Business logic untuk operasi Transaksi.
"""
import os
from src.config import DATA_DIR

INVOICE_DIR = os.path.join(DATA_DIR, "invoice")
from src.models.barang import Barang, save_barang, find_by_kode
from src.models.transaksi import (
    TransaksiItem, save_transaksi, load_transaksi, get_rekap_pendapatan
)
from src.utils import input_non_empty, input_int, input_float, format_rupiah

# Optional Pillow import for image export
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def tampil_struk(
    keranjang: list[TransaksiItem],
    total: float,
    diskon: float,
    ongkir: float,
    total_bayar: float
) -> None:
    """Tampilkan struk transaksi."""
    print("\n===== STRUK =====")
    print(f"{'Nama':<18} {'Ukuran':<8} {'Warna':<15} {'Qty':>3} {'Sub':>12}")
    print("-" * 65)
    for item in keranjang:
        warna_info = f"{item.warna_kertas}/{item.warna_bunga}" if item.warna_kertas != "-" else "-"
        print(
            f"{item.nama[:17]:<18} {item.ukuran:<8} {warna_info[:14]:<15} {item.qty:>3} "
            f"{format_rupiah(item.subtotal):>12}"
        )
    print("-" * 65)
    print(f"{'Total':<40} Rp{format_rupiah(total):>12}")
    print(f"{'Diskon':<40} Rp{format_rupiah(diskon):>12}")
    print(f"{'Ongkir':<40} Rp{format_rupiah(ongkir):>12}")
    print(f"{'Total Bayar':<40} Rp{format_rupiah(total_bayar):>12}")
    print("=================\n")


def rollback_stok(barang_list: list[Barang], keranjang: list[TransaksiItem]) -> None:
    """Kembalikan stok jika transaksi dibatalkan."""
    for item in keranjang:
        barang = find_by_kode(barang_list, item.kode)
        if barang is not None:
            ukuran = barang.get_ukuran(item.ukuran)
            if ukuran:
                ukuran.stok += item.qty
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


def pilih_pengantaran() -> tuple[float, str]:
    """Pilih metode pengantaran. Return (ongkir, delivery_type)."""
    print("Alur pengantaran:")
    print("1) Full Delivery (Ada ongkir)")
    print("2) Ambil Sendiri (Gratis ongkir)")
    pilihan = input_int("Pilih pengantaran: ", min_val=1, max_val=2)
    
    if pilihan == 1:
        ongkir = input_float("Ongkir (angka): ", min_val=0)
        return (ongkir, "Full Delivery")
    else:
        print("Ongkir gratis untuk pengantaran.")
        return (0.0, "Ambil Sendiri")


def export_struk_as_image(
    keranjang: list[TransaksiItem],
    total: float,
    diskon: float,
    ongkir: float,
    total_bayar: float,
    nama_pembeli: str,
    tanggal_pengambilan: str,
    trx_id: str
) -> str | None:
    """Export struk as PNG image. Return path jika berhasil."""
    if not PIL_AVAILABLE:
        return None

    from datetime import datetime

    logo_path = os.path.join(DATA_DIR, "logo.png")
    width = 500
    padding = 30
    line_height = 28

    # Fonts
    try:
        font_small = ImageFont.truetype("arial.ttf", 14)
        font = ImageFont.truetype("arial.ttf", 16)
        font_bold = ImageFont.truetype("arialbd.ttf", 18)
        font_title = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        font_small = ImageFont.load_default()
        font = font_small
        font_bold = font_small
        font_title = font_small

    # Logo size
    logo_w, logo_h = 0, 0
    if os.path.exists(logo_path):
        try:
            tmp = Image.open(logo_path)
            max_logo_w = 140
            wpercent = max_logo_w / float(tmp.size[0])
            logo_h = int(float(tmp.size[1]) * wpercent)
            logo_w = max_logo_w
            tmp.close()
        except Exception:
            pass

    # Create LARGE canvas first (will crop later)
    max_height = 2000
    img = Image.new("RGB", (width, max_height), "#FAFAFA")
    draw = ImageDraw.Draw(img)

    y = padding
    center_x = width // 2

    # === HEADER ===
    if logo_w > 0 and logo_h > 0:
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo = logo.resize((logo_w, logo_h))
            img.paste(logo, (center_x - logo_w // 2, y), logo)
            y += logo_h + 15
        except Exception:
            pass

    title = "BUQEUET LIYA"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    draw.text((center_x - (bbox[2] - bbox[0]) // 2, y), title, font=font_title, fill="#333333")
    y += 30

    subtitle = "Invoice / Struk Pembayaran"
    bbox = draw.textbbox((0, 0), subtitle, font=font_small)
    draw.text((center_x - (bbox[2] - bbox[0]) // 2, y), subtitle, font=font_small, fill="#666666")
    y += 35

    draw.line((padding, y, width - padding, y), fill="#CCCCCC", width=1)
    y += 20

    # === INFO ===
    info_left = padding
    draw.text((info_left, y), "No. Invoice:", font=font_small, fill="#666666")
    draw.text((info_left + 90, y), trx_id, font=font_bold, fill="#333333")
    y += line_height
    draw.text((info_left, y), "Tanggal:", font=font_small, fill="#666666")
    draw.text((info_left + 90, y), datetime.now().strftime("%d/%m/%Y %H:%M"), font=font, fill="#333333")
    y += line_height
    draw.text((info_left, y), "Pembeli:", font=font_small, fill="#666666")
    draw.text((info_left + 90, y), nama_pembeli, font=font, fill="#333333")
    y += line_height
    if tanggal_pengambilan:
        draw.text((info_left, y), "Pengambilan:", font=font_small, fill="#666666")
        draw.text((info_left + 90, y), tanggal_pengambilan, font=font, fill="#333333")
        y += line_height
    y += 10

    # === TABLE HEADER ===
    draw.rectangle([padding, y, width - padding, y + 30], fill="#4A90A4")
    y += 6
    col_nama, col_qty, col_harga, col_sub = padding + 10, 280, 340, 420
    draw.text((col_nama, y), "Item", font=font_bold, fill="white")
    draw.text((col_qty, y), "Qty", font=font_bold, fill="white")
    draw.text((col_harga, y), "Harga", font=font_bold, fill="white")
    draw.text((col_sub, y), "Sub", font=font_bold, fill="white")
    y += 30

    # === ITEMS ===
    for i, item in enumerate(keranjang):
        bg = "#FFFFFF" if i % 2 == 0 else "#F5F5F5"
        draw.rectangle([padding, y, width - padding, y + line_height], fill=bg)
        # Combine nama + ukuran
        nama_dengan_ukuran = f"{item.nama[:15]} ({item.ukuran})"
        draw.text((col_nama, y + 4), nama_dengan_ukuran, font=font, fill="#333333")
        draw.text((col_qty, y + 4), str(item.qty), font=font, fill="#333333")
        draw.text((col_harga, y + 4), format_rupiah(item.harga), font=font, fill="#333333")
        draw.text((col_sub, y + 4), format_rupiah(item.subtotal), font=font, fill="#333333")
        y += line_height

    draw.line((padding, y, width - padding, y), fill="#4A90A4", width=2)
    y += 20

    # === SUMMARY ===
    summary_left, summary_right = 280, width - padding - 10
    draw.text((summary_left, y), "Subtotal", font=font, fill="#666666")
    draw.text((summary_right - 80, y), f"Rp {format_rupiah(total)}", font=font, fill="#333333")
    y += line_height
    if diskon > 0:
        draw.text((summary_left, y), "Diskon", font=font, fill="#666666")
        draw.text((summary_right - 80, y), f"- Rp {format_rupiah(diskon)}", font=font, fill="#E74C3C")
        y += line_height
    if ongkir > 0:
        draw.text((summary_left, y), "Ongkir", font=font, fill="#666666")
        draw.text((summary_right - 80, y), f"Rp {format_rupiah(ongkir)}", font=font, fill="#333333")
        y += line_height
    y += 5
    draw.line((summary_left, y, width - padding, y), fill="#333333", width=1)
    y += 10
    draw.text((summary_left, y), "TOTAL", font=font_bold, fill="#333333")
    draw.text((summary_right - 100, y), f"Rp {format_rupiah(total_bayar)}", font=font_title, fill="#4A90A4")
    y += 50

    # === FOOTER ===
    draw.line((padding, y, width - padding, y), fill="#CCCCCC", width=1)
    y += 20
    footer1 = "✿ Terima kasih telah berbelanja di Buqeuet Liya ✿"
    bbox = draw.textbbox((0, 0), footer1, font=font_bold)
    draw.text((center_x - (bbox[2] - bbox[0]) // 2, y), footer1, font=font_bold, fill="#4A90A4")
    y += line_height
    footer2 = "Semoga buket kami membawa kebahagiaan untuk Anda!"
    bbox = draw.textbbox((0, 0), footer2, font=font_small)
    draw.text((center_x - (bbox[2] - bbox[0]) // 2, y), footer2, font=font_small, fill="#666666")
    y += line_height
    footer3 = "Follow us: @buqeuet.liya"
    bbox = draw.textbbox((0, 0), footer3, font=font_small)
    draw.text((center_x - (bbox[2] - bbox[0]) // 2, y), footer3, font=font_small, fill="#888888")
    y += line_height  # space after last text

    # === CROP to actual content ===
    final_height = y + padding  # add bottom padding
    img = img.crop((0, 0, width, final_height))
    
    # Redraw border on cropped image
    draw = ImageDraw.Draw(img)
    draw.rectangle([5, 5, width - 6, final_height - 6], outline="#E0E0E0", width=2)

    os.makedirs(INVOICE_DIR, exist_ok=True)
    out_path = os.path.join(INVOICE_DIR, f"struk_{trx_id}.png")
    img.save(out_path)
    return out_path



def proses_transaksi(barang_list: list[Barang]) -> bool:
    """Proses transaksi penjualan. Return True jika berhasil."""
    if not barang_list:
        print("\n[!] Data barang kosong. Tambahkan barang dulu.\n")
        return False
    
    print("\n=== TRANSAKSI PENJUALAN BUQET ===")
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
        
        print(f"\n-> {barang.nama}")
        
        # Pilih warna kertas
        warna_kertas_dipilih = "-"
        if barang.warna_kertas:
            print("   Pilih Warna Kertas:")
            for i, w in enumerate(barang.warna_kertas, start=1):
                print(f"   {i}) {w}")
            pilih_wk = input_int("   Pilih warna kertas (nomor): ", min_val=1, max_val=len(barang.warna_kertas))
            warna_kertas_dipilih = barang.warna_kertas[pilih_wk - 1]
        
        # Pilih warna bunga
        warna_bunga_dipilih = "-"
        if barang.warna_bunga:
            print("   Pilih Warna Bunga:")
            for i, w in enumerate(barang.warna_bunga, start=1):
                print(f"   {i}) {w}")
            pilih_wb = input_int("   Pilih warna bunga (nomor): ", min_val=1, max_val=len(barang.warna_bunga))
            warna_bunga_dipilih = barang.warna_bunga[pilih_wb - 1]
        
        # Show ukuran options
        print("   Pilih Ukuran:")
        for i, u in enumerate(barang.ukuran, start=1):
            print(f"   {i}) {u.nama} - Rp{format_rupiah(u.harga)} (Stok: {u.stok})")
        
        pilih_ukuran = input_int("   Pilih ukuran (nomor): ", min_val=1, max_val=len(barang.ukuran))
        ukuran = barang.ukuran[pilih_ukuran - 1]
        
        if ukuran.stok == 0:
            print("[!] Stok ukuran ini habis.")
            continue
        
        qty = input_int("Qty: ", min_val=1)
        if qty > ukuran.stok:
            print("[!] Qty melebihi stok.")
            continue
        
        # Buat item dan kurangi stok
        item = TransaksiItem.from_cart(
            barang.kode, barang.nama, ukuran.nama,
            warna_kertas_dipilih, warna_bunga_dipilih,
            qty, ukuran.harga, ukuran.hpp
        )
        keranjang.append(item)
        ukuran.stok -= qty
        print("[✓] Ditambahkan ke keranjang.\n")
    
    if not keranjang:
        print("[!] Tidak ada item. Transaksi dibatalkan.")
        return False
    
    # Hitung total dan diskon
    total = sum(item.subtotal for item in keranjang)
    diskon = hitung_diskon(total)
    
    # Info pembeli
    print("\n=== RINGKASAN ===")
    nama_pembeli = input_non_empty("Nama pembeli: ")
    tanggal_pengambilan = input("Tanggal pengambilan (YYYY-MM-DD) (boleh kosong): ").strip()
    
    # Pilih pengantaran
    ongkir, delivery = pilih_pengantaran()
    
    total_bayar = total - diskon + ongkir
    
    # Tampilkan struk
    tampil_struk(keranjang, total, diskon, ongkir, total_bayar)
    
    # Proses pembayaran
    bayar = input_float("Uang bayar: ", min_val=0)
    if bayar < total_bayar:
        print("[!] Uang kurang. Transaksi dibatalkan dan stok dikembalikan.")
        rollback_stok(barang_list, keranjang)
        return False
    
    kembalian = bayar - total_bayar
    print(f"Kembalian: Rp{format_rupiah(kembalian)}")
    
    # Simpan transaksi
    trx_id = save_transaksi(keranjang, diskon, ongkir, delivery, total_bayar)
    save_barang(barang_list)
    
    # Export struk ke gambar
    if PIL_AVAILABLE:
        try:
            img_path = export_struk_as_image(
                keranjang, total, diskon, ongkir, total_bayar,
                nama_pembeli, tanggal_pengambilan, trx_id
            )
            if img_path:
                print(f"[✓] Struk diekspor ke gambar: {img_path}")
        except Exception as e:
            print(f"[!] Gagal ekspor struk ke gambar: {e}")
    
    print("[✓] Transaksi berhasil disimpan.")
    return True


def tampil_riwayat(limit: int = 20) -> None:
    """Tampilkan riwayat transaksi terakhir."""
    rows = load_transaksi(limit)
    
    if not rows:
        print("\n[!] Belum ada transaksi.\n")
        return
    
    print("\n=== RIWAYAT TRANSAKSI (TERAKHIR) ===")
    for r in rows:
        print(f"\n[{r.get('id_transaksi', 'N/A')}] {r.get('waktu', 'N/A')}")
        print(f"  Kode: {r.get('kode', 'N/A')} - {r.get('nama', 'N/A')}")
        print(f"  Ukuran: {r.get('ukuran', '-')}")
        print(f"  Warna Kertas: {r.get('warna_kertas', '-')}, Warna Bunga: {r.get('warna_bunga', '-')}")
        print(f"  Qty: {r.get('qty', '0')}, Subtotal: Rp{format_rupiah(float(r.get('subtotal', 0)))}")
        print(f"  Delivery: {r.get('delivery', '-')}, Ongkir: Rp{format_rupiah(float(r.get('ongkir', 0)))}")
        print(f"  Total Transaksi: Rp{format_rupiah(float(r.get('total_transaksi', 0)))}")
    print("-" * 50)


def tampil_rekap() -> None:
    """Tampilkan rekap total pendapatan."""
    jumlah_trx, total_pendapatan, total_modal, total_profit = get_rekap_pendapatan()
    
    if jumlah_trx == 0:
        print("\n[!] Belum ada transaksi.\n")
        return
    
    print("===== REKAP TRANSAKSI =====")
    print(f"Jumlah Transaksi : {jumlah_trx}")
    print(f"Total Pendapatan : Rp {total_pendapatan:,.0f}")
    print(f"Total Modal (HPP): Rp {total_modal:,.0f}")
    print(f"Keuntungan       : Rp {total_profit:,.0f}")
    print("===========================\n")
