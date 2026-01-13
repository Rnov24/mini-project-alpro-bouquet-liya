"""
Unified Invoice Service.
Generates invoice text and images for both CLI and Bot.
"""
import os
from datetime import datetime
from typing import Optional, Union, Any

from core.config import DATA_DIR

INVOICE_DIR = os.path.join(DATA_DIR, "invoice")

# Try to import Pillow for image generation
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def format_rupiah(value: float) -> str:
    """Format angka ke format rupiah."""
    return f"{value:,.0f}".replace(",", ".")


def generate_invoice_text(
    order_data: dict,
    format_type: str = "telegram"
) -> str:
    """
    Generate invoice text.
    
    Args:
        order_data: Dict containing order info (items, total, buyer info, etc.)
        format_type: "telegram" untuk Markdown, "cli" untuk plain text
    
    Returns:
        Formatted invoice string
    """
    items = order_data.get("items", [])
    subtotal = order_data.get("subtotal", 0)
    diskon = order_data.get("diskon", 0)
    ongkir = order_data.get("ongkir", 0)
    total = order_data.get("total", 0)
    nama_pembeli = order_data.get("nama_pembeli", "-")
    wa_pembeli = order_data.get("wa_pembeli", "-")
    delivery = order_data.get("delivery", "ambil")
    alamat = order_data.get("alamat", "")
    order_id = order_data.get("order_id", "-")
    tanggal = order_data.get("tanggal", datetime.now().strftime("%d/%m/%Y %H:%M"))
    
    # Format items
    items_str = ""
    for item in items:
        if isinstance(item, dict):
            nama = item.get("nama", "")
            ukuran = item.get("ukuran", "")
            qty = item.get("qty", 0)
            item_subtotal = item.get("subtotal", 0)
            warna_kertas = item.get("warna_kertas", "-")
            warna_bunga = item.get("warna_bunga", "-")
        else:
            # Object with attributes
            nama = getattr(item, "nama", "")
            ukuran = getattr(item, "ukuran", "")
            qty = getattr(item, "qty", 0)
            item_subtotal = getattr(item, "subtotal", 0)
            warna_kertas = getattr(item, "warna_kertas", "-")
            warna_bunga = getattr(item, "warna_bunga", "-")
        
        if format_type == "telegram":
            items_str += f"• {nama[:12]} ({ukuran}) ×{qty}\n"
            items_str += f"  Rp {format_rupiah(item_subtotal)}\n"
        else:
            items_str += f"  {nama} ({ukuran}) x{qty} = Rp {format_rupiah(item_subtotal)}\n"
    
    delivery_str = "🏠 Ambil" if delivery == "ambil" else "🛵 Delivery"
    alamat_str = f"\n📍 {alamat[:30]}" if alamat else ""
    
    if format_type == "telegram":
        # Mobile-optimized format
        invoice = f"""🧾 *INVOICE*
`{order_id}`
📅 {tanggal}
─────────────
📦 *ITEM:*
{items_str}─────────────
💰 Subtotal: Rp {format_rupiah(subtotal)}"""
        
        if diskon > 0:
            invoice += f"\n💸 Diskon: -Rp {format_rupiah(diskon)}"
        if ongkir > 0:
            invoice += f"\n🚚 Ongkir: Rp {format_rupiah(ongkir)}"
        
        invoice += f"""
━━━━━━━━━━━━━
✅ *Rp {format_rupiah(total)}*
─────────────
👤 {nama_pembeli[:20]}
{delivery_str}{alamat_str}
🌸 Buqeuet Liya"""
    else:
        # CLI format
        invoice = f"""
╔═══════════════════════════════════════════════════════╗
║                    INVOICE - BUQEUET LIYA            ║
╠═══════════════════════════════════════════════════════╣
║  No: {order_id:<47} ║
║  Tanggal: {tanggal:<42} ║
╟───────────────────────────────────────────────────────╢
║  ITEMS:                                               ║
{items_str}╟───────────────────────────────────────────────────────╢
║  Subtotal: Rp {format_rupiah(subtotal):<40} ║"""
        
        if diskon > 0:
            invoice += f"\n║  Diskon:   -Rp {format_rupiah(diskon):<39} ║"
        if ongkir > 0:
            invoice += f"\n║  Ongkir:   Rp {format_rupiah(ongkir):<40} ║"
        
        invoice += f"""
╟───────────────────────────────────────────────────────╢
║  TOTAL: Rp {format_rupiah(total):<43} ║
╠═══════════════════════════════════════════════════════╣
║  Pembeli: {nama_pembeli:<44} ║
║  WA: {wa_pembeli:<49} ║
╚═══════════════════════════════════════════════════════╝
"""
    
    return invoice


def format_order_receipt(order: Any) -> str:
    """Wrapper alias for generate_invoice_text (Telegram format)."""
    # Ensure it's a dict
    if hasattr(order, "to_dict"):
        data = order.to_dict()
    elif isinstance(order, dict):
        data = order
    else:
        data = order_to_dict(order)
    
    return generate_invoice_text(data, format_type="telegram")


def generate_invoice_image(
    order_data: dict,
    output_filename: Optional[str] = None
) -> Optional[str]:
    """
    Generate premium invoice as PNG image.
    
    Args:
        order_data: Dict containing order info
        output_filename: Optional custom filename, auto-generated if not provided
    
    Returns:
        Path to generated image, or None if PIL not available
    """
    if not PIL_AVAILABLE:
        return None
    
    # Extract data
    items = order_data.get("items", [])
    subtotal = order_data.get("subtotal", 0)
    diskon = order_data.get("diskon", 0)
    ongkir = order_data.get("ongkir", 0)
    total = order_data.get("total", 0)
    nama_pembeli = order_data.get("nama_pembeli", "-")
    wa_pembeli = order_data.get("wa_pembeli", "-")
    order_id = order_data.get("order_id", datetime.now().strftime("INV%Y%m%d%H%M%S"))
    tanggal = order_data.get("tanggal", datetime.now().strftime("%d %b %Y, %H:%M"))
    tanggal_pengambilan = order_data.get("tanggal_pengambilan", "")
    logo_path = os.path.join(DATA_DIR, "logo.png")

    # === PREMIUM DESIGN CONFIGURATION ===
    width = 800
    margin = 40
    inner_padding = 25
    
    # Refined Color Palette
    PRIMARY = "#2C3E50"          # Dark Blue-Grey (More Professional)
    PRIMARY_LIGHT = "#ECF0F1"    # Very Light Grey
    TEXT_PRIMARY = "#2C3E50"     # Dark text
    TEXT_SECONDARY = "#7F8C8D"   # Grey text
    TEXT_MUTED = "#95A5A6"       # Light grey
    BG_MAIN = "#FFFFFF"          
    BG_CARD = "#FDFFE6"          # Slight warm tint for card (Paper-like)
    BG_TABLE_ALT = "#F8F9F9"     
    BORDER_LIGHT = "#BDC3C7"     
    DANGER = "#E74C3C"           

    # Fonts
    try:
        font_xs = ImageFont.truetype("arial.ttf", 14)
        font_sm = ImageFont.truetype("arial.ttf", 16)
        font_base = ImageFont.truetype("arial.ttf", 18)
        font_md = ImageFont.truetype("arialbd.ttf", 18)
        font_lg = ImageFont.truetype("arialbd.ttf", 22)
        font_xl = ImageFont.truetype("arialbd.ttf", 28)
        font_2xl = ImageFont.truetype("arialbd.ttf", 36)
    except Exception:
        font_xs = ImageFont.load_default()
        font_sm = font_xs
        font_base = font_xs
        font_md = font_xs
        font_lg = font_xs
        font_xl = font_xs
        font_2xl = font_xs

    # Load logo
    logo_w, logo_h = 0, 0
    if os.path.exists(logo_path):
        try:
            tmp = Image.open(logo_path)
            max_logo_h = 100
            ratio = max_logo_h / float(tmp.size[1])
            logo_w = int(float(tmp.size[0]) * ratio)
            logo_h = max_logo_h
            tmp.close()
        except Exception:
            pass

    # Create large canvas
    max_height = 3000
    img = Image.new("RGB", (width, max_height), BG_MAIN)
    draw = ImageDraw.Draw(img)
    
    center = width // 2
    left = margin
    right = width - margin
    content_width = right - left
    
    y = margin + 20

    # ═══════════════════════════════════════════════════════════════
    # HEADER SECTION
    # ═══════════════════════════════════════════════════════════════
    
    if logo_w > 0 and logo_h > 0:
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo = logo.resize((logo_w, logo_h))
            img.paste(logo, (center - logo_w // 2, y), logo)
            y += logo_h + 15
        except Exception:
            pass
    
    # Brand name
    brand = "BUQEUET LIYA"
    bbox = draw.textbbox((0, 0), brand, font=font_2xl)
    draw.text((center - (bbox[2] - bbox[0]) // 2, y), brand, font=font_2xl, fill=TEXT_PRIMARY)
    y += 45
    
    # Subtitle
    sub = "official invoice"
    bbox = draw.textbbox((0, 0), sub, font=font_sm)
    # Draw spaced out subtitle
    # simple centering
    draw.text((center - (bbox[2] - bbox[0]) // 2, y), sub.upper(), font=font_sm, fill=TEXT_SECONDARY)
    y += 40
    
    # ═══════════════════════════════════════════════════════════════
    # INFO CARD SECTION
    # ═══════════════════════════════════════════════════════════════
    
    info_card_start = y
    info_lines = 4 if tanggal_pengambilan else 3
    info_card_height = info_lines * 32 + 30
    
    # Background card
    draw.rounded_rectangle(
        [left, y, right, y + info_card_height],
        radius=12, fill=BG_CARD, outline=BORDER_LIGHT, width=1
    )
    y += 20
    
    label_x = left + inner_padding
    value_x = left + 180  # More space for labels
    line_h = 32
    
    draw.text((label_x, y), "No. Invoice", font=font_base, fill=TEXT_SECONDARY)
    draw.text((value_x, y), f": {order_id}", font=font_md, fill=PRIMARY)
    y += line_h
    
    draw.text((label_x, y), "Tanggal", font=font_base, fill=TEXT_SECONDARY)
    draw.text((value_x, y), f": {tanggal}", font=font_base, fill=TEXT_PRIMARY)
    y += line_h
    
    draw.text((label_x, y), "Pembeli", font=font_base, fill=TEXT_SECONDARY)
    draw.text((value_x, y), f": {nama_pembeli[:30]}", font=font_base, fill=TEXT_PRIMARY)
    y += line_h
    
    if tanggal_pengambilan:
        draw.text((label_x, y), "Pengambilan", font=font_base, fill=TEXT_SECONDARY)
        draw.text((value_x, y), f": {tanggal_pengambilan}", font=font_base, fill=TEXT_PRIMARY)
        y += line_h
    
    y = info_card_start + info_card_height + 40

    # ═══════════════════════════════════════════════════════════════
    # ITEMS TABLE SECTION
    # ═══════════════════════════════════════════════════════════════
    
    # Columns Layout for 800px width
    # Margin 40. Content 720.
    # Item: start at left+15. Max width ~350.
    # Size: start right-320
    # Qty: start right-220
    # Price: start right-150
    # Total: start right-20 (align right)
    
    col_item_x = left + 20
    col_size_x = right - 320
    col_qty_x = right - 200
    col_price_x = right - 130
    col_total_x = right - 20
    
    header_h = 50
    
    # Header Background
    draw.rounded_rectangle(
        [left, y, right, y + header_h],
        radius=8, fill=PRIMARY
    )
    
    hy = y + 14
    draw.text((col_item_x, hy), "ITEM DETAIL", font=font_md, fill=BG_MAIN)
    draw.text((col_size_x, hy), "UKURAN", font=font_md, fill=BG_MAIN)
    draw.text((col_qty_x, hy), "QTY", font=font_md, fill=BG_MAIN)
    # Removed single price column to save space if needed, but let's keep it minimal
    # draw.text((col_price_x, hy), "HARGA", font=font_md, fill=BG_MAIN)
    
    total_label = "SUBTOTAL"
    bbox = draw.textbbox((0, 0), total_label, font=font_md)
    draw.text((col_total_x - (bbox[2] - bbox[0]), hy), total_label, font=font_md, fill=BG_MAIN)
    y += header_h
    
    import textwrap
    
    # Table rows
    for idx, item in enumerate(items):
        if isinstance(item, dict):
            nama = item.get("nama", "")
            ukuran = item.get("ukuran", "")
            qty = str(item.get("qty", 0))
            harga = item.get("harga", 0)
            item_subtotal = item.get("subtotal", 0)
            warna_kertas = item.get("warna_kertas", "-")
            warna_bunga = item.get("warna_bunga", "-")
        else:
            nama = getattr(item, "nama", "")
            ukuran = getattr(item, "ukuran", "")
            qty = str(getattr(item, "qty", 0))
            harga = getattr(item, "harga", 0)
            item_subtotal = getattr(item, "subtotal", 0)
            warna_kertas = getattr(item, "warna_kertas", "-")
            warna_bunga = getattr(item, "warna_bunga", "-")
        
        # Wrap text
        wrapped_nama = textwrap.wrap(nama, width=35)
        # Add color info
        detail_info = f"🎨 {warna_kertas} / 🌸 {warna_bunga}"
        wrapped_total_lines = len(wrapped_nama) + 1 # +1 for detail info
        
        # Dynamic row height
        line_height = 24
        padding_y = 20
        row_h = (wrapped_total_lines * line_height) + padding_y
        
        bg = BG_MAIN if idx % 2 == 0 else BG_TABLE_ALT
        if idx == len(items) - 1:
            draw.rounded_rectangle([left, y, right, y + row_h], radius=8, fill=bg)
        else:
            draw.rectangle([left, y, right, y + row_h], fill=bg)
        
        # Item Name
        curr_text_y = y + 15
        for line in wrapped_nama:
            draw.text((col_item_x, curr_text_y), line, font=font_md, fill=TEXT_PRIMARY)
            curr_text_y += line_height
        
        # Detail Info (Colors)
        draw.text((col_item_x, curr_text_y), detail_info, font=font_xs, fill=TEXT_SECONDARY)
        
        # Other Columns (Vertically Centered)
        cy = y + (row_h // 2) - 10
        
        draw.text((col_size_x, cy), ukuran, font=font_base, fill=TEXT_PRIMARY)
        draw.text((col_qty_x + 10, cy), qty, font=font_base, fill=TEXT_PRIMARY)
        
        # Subtotal
        row_total_str = format_rupiah(item_subtotal)
        bbox = draw.textbbox((0, 0), row_total_str, font=font_md)
        draw.text((col_total_x - (bbox[2] - bbox[0]), cy), row_total_str, font=font_md, fill=TEXT_PRIMARY)
        
        y += row_h
    
    y += 10
    draw.line((left, y, right, y), fill=PRIMARY, width=3)
    y += 30

    # ═══════════════════════════════════════════════════════════════
    # SUMMARY SECTION
    # ═══════════════════════════════════════════════════════════════
    
    sum_label_x = right - 350
    sum_value_x = right - 20
    sum_line_h = 35
    
    # Subtotal
    draw.text((sum_label_x, y), "Subtotal", font=font_base, fill=TEXT_SECONDARY)
    sub_val = f"Rp {format_rupiah(subtotal)}"
    bbox = draw.textbbox((0, 0), sub_val, font=font_base)
    draw.text((sum_value_x - (bbox[2] - bbox[0]), y), sub_val, font=font_base, fill=TEXT_PRIMARY)
    y += sum_line_h
    
    if diskon > 0:
        draw.text((sum_label_x, y), "Diskon", font=font_base, fill=TEXT_SECONDARY)
        diskon_val = f"- Rp {format_rupiah(diskon)}"
        bbox = draw.textbbox((0, 0), diskon_val, font=font_base)
        draw.text((sum_value_x - (bbox[2] - bbox[0]), y), diskon_val, font=font_base, fill=DANGER)
        y += sum_line_h
    
    if ongkir > 0:
        draw.text((sum_label_x, y), "Ongkir", font=font_base, fill=TEXT_SECONDARY)
        ongkir_val = f"Rp {format_rupiah(ongkir)}"
        bbox = draw.textbbox((0, 0), ongkir_val, font=font_base)
        draw.text((sum_value_x - (bbox[2] - bbox[0]), y), ongkir_val, font=font_base, fill=TEXT_PRIMARY)
        y += sum_line_h
    
    y += 15
    
    # GRAND TOTAL
    total_box_h = 70
    draw.rounded_rectangle(
        [sum_label_x - 20, y, right, y + total_box_h],
        radius=10, fill=PRIMARY, width=0
    )
    
    draw.text((sum_label_x, y + 22), "TOTAL", font=font_lg, fill=BG_MAIN)
    grand_total = f"Rp {format_rupiah(total)}"
    bbox = draw.textbbox((0, 0), grand_total, font=font_xl)
    draw.text((sum_value_x - (bbox[2] - bbox[0]) - 15, y + 18), grand_total, font=font_xl, fill=BG_MAIN) # Padded right
    
    y += total_box_h + 50

    # ═══════════════════════════════════════════════════════════════
    # FOOTER SECTION
    # ═══════════════════════════════════════════════════════════════
    
    draw.line((left + 50, y, right - 50, y), fill=BORDER_LIGHT, width=1)
    y += 20
    
    thank_msg = "Terima kasih telah berbelanja! 💐"
    bbox = draw.textbbox((0, 0), thank_msg, font=font_lg)
    draw.text((center - (bbox[2] - bbox[0]) // 2, y), thank_msg, font=font_lg, fill=PRIMARY)
    y += 28
    
    tagline = "Semoga buket kami membawa kebahagiaan untuk Anda"
    bbox = draw.textbbox((0, 0), tagline, font=font_sm)
    draw.text((center - (bbox[2] - bbox[0]) // 2, y), tagline, font=font_sm, fill=TEXT_MUTED)
    y += 22
    
    ig = "@buqeuet.liya"
    bbox = draw.textbbox((0, 0), ig, font=font_xs)
    draw.text((center - (bbox[2] - bbox[0]) // 2, y), ig, font=font_xs, fill=TEXT_MUTED)
    y += 15

    # ═══════════════════════════════════════════════════════════════
    # FINAL PROCESSING
    # ═══════════════════════════════════════════════════════════════
    
    final_h = y + margin
    img = img.crop((0, 0, width, final_h))
    
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, 4], fill=PRIMARY)
    draw.line((0, 4, 0, final_h), fill=BORDER_LIGHT, width=1)
    draw.line((width-1, 4, width-1, final_h), fill=BORDER_LIGHT, width=1)
    draw.line((0, final_h-1, width, final_h-1), fill=BORDER_LIGHT, width=1)

    os.makedirs(INVOICE_DIR, exist_ok=True)
    
    if output_filename:
        out_path = os.path.join(INVOICE_DIR, output_filename)
    else:
        out_path = os.path.join(INVOICE_DIR, f"invoice_{order_id}.png")
    
    img.save(out_path, "PNG", optimize=True)
    return out_path


# ═══════════════════════════════════════════════════════════════
# HELPER: Convert Order/Cart to order_data dict
# ═══════════════════════════════════════════════════════════════

def order_to_dict(order: Any) -> dict:
    """Convert Order object to invoice data dict."""
    if hasattr(order, "to_dict"):
        data = order.to_dict()
    elif isinstance(order, dict):
        data = order
    else:
        # Assume it's an Order-like object
        data = {
            "order_id": getattr(order, "order_id", ""),
            "items": [item.to_dict() if hasattr(item, "to_dict") else item for item in getattr(order, "items", [])],
            "subtotal": getattr(order, "subtotal", 0),
            "ongkir": getattr(order, "ongkir", 0),
            "total": getattr(order, "total", 0),
            "nama_pembeli": getattr(order, "nama_pembeli", "-"),
            "wa_pembeli": getattr(order, "wa_pembeli", "-"),
            "delivery": getattr(order, "delivery", "ambil"),
            "alamat": getattr(order, "alamat", ""),
        }
    return data


def cart_to_dict(cart: Any) -> dict:
    """Convert Cart object to invoice data dict."""
    if hasattr(cart, "to_dict"):
        return cart.to_dict()
    elif isinstance(cart, dict):
        return cart
    else:
        # Assume it's a Cart-like object
        return {
            "items": [item.to_dict() if hasattr(item, "to_dict") else item for item in getattr(cart, "items", [])],
            "subtotal": getattr(cart, "subtotal", 0),
            "diskon": getattr(cart, "diskon", 0),
            "ongkir": getattr(cart, "ongkir", 0),
            "total": getattr(cart, "total", 0),
            "nama_pembeli": getattr(cart, "nama_pembeli", "-"),
            "wa_pembeli": getattr(cart, "wa_pembeli", "-"),
            "delivery_type": getattr(cart, "delivery_type", "ambil"),
            "alamat": getattr(cart, "alamat", ""),
            "tanggal_pengambilan": getattr(cart, "tanggal_pengambilan", ""),
        }
