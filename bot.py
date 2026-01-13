"""
Telegram Bot Entry Point.
Menjalankan Buyer Bot dan Admin Bot secara simultan dengan threading.
"""

import threading
import signal
import sys
import asyncio
import io

# Fix Windows terminal encoding for emoji
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from core.config import BUYER_BOT_TOKEN, ADMIN_BOT_TOKEN
from bot.buyer import handlers as buyer_handlers
from bot.admin import handlers as admin_handlers


# Flag untuk graceful shutdown
shutdown_event = threading.Event()


def run_buyer_bot():
    """Jalankan Buyer Bot di thread terpisah."""
    if not BUYER_BOT_TOKEN or BUYER_BOT_TOKEN == "your_buyer_bot_token_here":
        print("❌ BUYER BOT: Token tidak valid. Cek file .env")
        return
    
    try:
        app = Application.builder().token(BUYER_BOT_TOKEN).build()
        
        app.add_handler(CommandHandler("start", buyer_handlers.start))
        app.add_handler(CallbackQueryHandler(buyer_handlers.callback_router))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buyer_handlers.text_handler))
        app.add_handler(MessageHandler(filters.LOCATION, buyer_handlers.location_handler))
        
        print("🛒 Buyer Bot berjalan...")
        app.run_polling(stop_signals=None)
    except Exception as e:
        print(f"❌ Buyer Bot error: {e}")


def run_admin_bot():
    """Jalankan Admin Bot di thread terpisah."""
    if not ADMIN_BOT_TOKEN or ADMIN_BOT_TOKEN == "your_admin_bot_token_here":
        print("❌ ADMIN BOT: Token tidak valid. Cek file .env")
        return
    
    try:
        app = Application.builder().token(ADMIN_BOT_TOKEN).build()
        
        app.add_handler(CommandHandler("start", admin_handlers.start))
        app.add_handler(CommandHandler("daftar", admin_handlers.daftar_admin))
        app.add_handler(CommandHandler("listadmin", admin_handlers.list_admins))
        app.add_handler(CallbackQueryHandler(admin_handlers.callback_router))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, admin_handlers.text_handler))
        
        print("🔐 Admin Bot berjalan...")
        app.run_polling(stop_signals=None)
    except Exception as e:
        print(f"❌ Admin Bot error: {e}")


def signal_handler(sig, frame):
    """Handle Ctrl+C untuk graceful shutdown."""
    print("\n\n⏹️  Menghentikan bot...")
    shutdown_event.set()
    sys.exit(0)


def main():
    """Entry point utama untuk menjalankan kedua bot."""
    print("=" * 50)
    print("  🌸 BUQEUET LIYA - TELEGRAM BOTS")
    print("=" * 50)
    print()
    
    # Validasi tokens
    if not BUYER_BOT_TOKEN or BUYER_BOT_TOKEN == "your_buyer_bot_token_here":
        print("⚠️  Warning: TELEGRAM_BUYER_BOT_TOKEN belum diset di .env")
    
    if not ADMIN_BOT_TOKEN or ADMIN_BOT_TOKEN == "your_admin_bot_token_here":
        print("⚠️  Warning: TELEGRAM_ADMIN_BOT_TOKEN belum diset di .env")
    
    print()
    print("🚀 Memulai bot...")
    print("   Tekan Ctrl+C untuk menghentikan")
    print()
    
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Jalankan kedua bot di thread terpisah
    buyer_thread = threading.Thread(target=run_buyer_bot, name="BuyerBot", daemon=True)
    admin_thread = threading.Thread(target=run_admin_bot, name="AdminBot", daemon=True)
    
    buyer_thread.start()
    admin_thread.start()
    
    # Wait for shutdown signal
    try:
        while not shutdown_event.is_set():
            shutdown_event.wait(timeout=1)
    except KeyboardInterrupt:
        signal_handler(None, None)
    
    print("✅ Bot dihentikan.")


if __name__ == "__main__":
    main()
