"""
Notification services untuk Telegram Bot.
Mengirim notifikasi ke admin saat ada order baru.
"""
import asyncio
from telegram import Bot
from core.config import ADMIN_BOT_TOKEN
from bot.shared.admin_registry import get_all_admin_ids


async def notify_admins_new_order(order) -> None:
    """
    Kirim notifikasi ke semua admin saat ada order baru.
    
    Args:
        order: Order object yang baru dibuat
    """
    if not ADMIN_BOT_TOKEN or ADMIN_BOT_TOKEN == "your_admin_bot_token_here":
        print("⚠️ ADMIN_BOT_TOKEN tidak valid, skip notifikasi")
        return
    
    admin_ids = get_all_admin_ids()
    if not admin_ids:
        print("⚠️ Tidak ada admin terdaftar, skip notifikasi")
        return
    
    # Format items
    items_str = ""
    # Format items
    items_str = ""
    for item in order.get("items", []):
        nama = item.get("nama")
        ukuran = item.get("ukuran")
        qty = item.get("qty")
        subtotal = item.get("subtotal")
        items_str += f"  • {nama} ({ukuran}) x{qty} = Rp {subtotal:,.0f}\n"
    
    # Format delivery
    delivery = order.get("delivery", "ambil")
    ongkir = order.get("ongkir", 0)
    delivery_str = "🏠 Ambil Sendiri" if delivery == "ambil" else f"🚚 Delivery (+Rp {ongkir:,.0f})"
    
    # Notification message
    notif_msg = f"""🔔 *PESANAN BARU MASUK!*
━━━━━━━━━━━━━━━━━━━━
📋 *Order ID:* `{order.get('order_id')}`
👤 *Pembeli:* {order.get('nama_pembeli')}
📱 *WA:* {order.get('wa_pembeli')}

📦 *Items:*
{items_str}
💰 *Total:* Rp {order.get('total'):,.0f}
{delivery_str}
━━━━━━━━━━━━━━━━━━━━
⏰ Segera tindak lanjuti pesanan ini!

Buka Admin Bot untuk proses pesanan."""

    try:
        bot = Bot(token=ADMIN_BOT_TOKEN)
        
        for admin_id in admin_ids:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=notif_msg,
                    parse_mode="Markdown"
                )
                print(f"✅ Notifikasi terkirim ke admin {admin_id}")
            except Exception as e:
                print(f"❌ Gagal kirim notifikasi ke {admin_id}: {e}")
                
    except Exception as e:
        print(f"❌ Error notifikasi: {e}")


def notify_admins_sync(order) -> None:
    """Wrapper sync untuk notify_admins_new_order."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Jika dalam async context, schedule sebagai task
            asyncio.create_task(notify_admins_new_order(order))
        else:
            loop.run_until_complete(notify_admins_new_order(order))
    except RuntimeError:
        # No event loop, create new one
        asyncio.run(notify_admins_new_order(order))
