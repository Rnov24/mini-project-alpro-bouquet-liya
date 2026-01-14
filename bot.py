"""
Telegram Bot Entry Point.
Menjalankan Buyer Bot dan Admin Bot secara simultan dengan threading.
"""

import threading
import signal
import sys
import asyncio
import io
import logging
import traceback
from datetime import datetime

# Fix Windows terminal encoding for emoji
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)


# ==================== LOGGING SETUP ====================
class RealTimeFormatter(logging.Formatter):
    """Custom formatter dengan timestamp dan warna."""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'
    }
    
    def format(self, record):
        timestamp = datetime.now().strftime('%H:%M:%S')
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Format: [HH:MM:SS] [LEVEL] message
        formatted = f"[{timestamp}] {color}[{record.levelname}]{reset} {record.getMessage()}"
        
        # Tambahkan exception info jika ada
        if record.exc_info:
            formatted += f"\n{color}{self._formatException(record.exc_info)}{reset}"
        
        return formatted
    
    def _formatException(self, exc_info):
        """Format exception dengan traceback yang readable."""
        return ''.join(traceback.format_exception(*exc_info))


def setup_logging():
    """Setup logging dengan output real-time."""
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Console handler dengan real-time output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(RealTimeFormatter())
    
    # Clear existing handlers
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    
    # Reduce noise dari library telegram
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.WARNING)
    
    return logging.getLogger('BuqeuetLiya')


# Initialize logger
logger = setup_logging()


# ==================== HELPER FUNCTIONS ====================
def log(message, level='info', flush=True):
    """Helper untuk logging dengan flush otomatis."""
    getattr(logger, level)(message)
    if flush:
        sys.stdout.flush()


def log_error(message, exc_info=None):
    """Log error dengan traceback lengkap."""
    logger.error(message, exc_info=exc_info)
    sys.stdout.flush()


# ==================== TELEGRAM ERROR HANDLER ====================
async def error_handler(update, context):
    """Global error handler untuk telegram bot."""
    from bot.shared.errors import classify_error, get_error_message, log_error
    
    error = context.error
    
    # Classify and get message
    error_key = classify_error(error)
    error_message = get_error_message(error_key)
    
    # Log error dengan context
    context_info = "Global"
    if update:
        if update.callback_query:
            context_info = f"Callback: {update.callback_query.data}"
        elif update.message:
            context_info = f"Message: {update.message.text[:30] if update.message.text else 'N/A'}"
    
    log_error(error, context_info)
    
    # Skip silent errors (like message_not_modified)
    if error_message is None:
        return
    
    # Try to send error message to user
    try:
        if update:
            if update.callback_query:
                try:
                    await update.callback_query.answer(
                        error_message[:200] if len(error_message) > 200 else error_message,
                        show_alert=True
                    )
                except:
                    pass
            elif update.message:
                await update.message.reply_text(error_message)
    except Exception as send_error:
        log_error(send_error, "Sending error to user")


# ==================== BOT RUNNERS ====================
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from core.config import BUYER_BOT_TOKEN, ADMIN_BOT_TOKEN
from bot.buyer import handlers as buyer_handlers
from bot.admin import handlers as admin_handlers


# Flag untuk graceful shutdown
shutdown_event = threading.Event()


def run_buyer_bot():
    """Jalankan Buyer Bot di thread terpisah."""
    if not BUYER_BOT_TOKEN or BUYER_BOT_TOKEN == "your_buyer_bot_token_here":
        log("❌ BUYER BOT: Token tidak valid. Cek file .env", level='error')
        return
    
    try:
        app = Application.builder().token(BUYER_BOT_TOKEN).build()
        
        # Add error handler
        app.add_error_handler(error_handler)
        
        app.add_handler(CommandHandler("start", buyer_handlers.start))
        app.add_handler(CallbackQueryHandler(buyer_handlers.callback_router))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buyer_handlers.text_handler))
        app.add_handler(MessageHandler(filters.LOCATION, buyer_handlers.location_handler))
        
        log("🛒 Buyer Bot berjalan...")
        app.run_polling(stop_signals=None)
    except Exception as e:
        log_error(f"❌ Buyer Bot crash: {e}", exc_info=True)


def run_admin_bot():
    """Jalankan Admin Bot di thread terpisah."""
    if not ADMIN_BOT_TOKEN or ADMIN_BOT_TOKEN == "your_admin_bot_token_here":
        log("❌ ADMIN BOT: Token tidak valid. Cek file .env", level='error')
        return
    
    try:
        app = Application.builder().token(ADMIN_BOT_TOKEN).build()
        
        # Add error handler
        app.add_error_handler(error_handler)
        
        app.add_handler(CommandHandler("start", admin_handlers.start))
        app.add_handler(CommandHandler("daftar", admin_handlers.daftar_admin))
        app.add_handler(CommandHandler("listadmin", admin_handlers.list_admins))
        app.add_handler(CallbackQueryHandler(admin_handlers.callback_router))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, admin_handlers.text_handler))
        
        log("🔐 Admin Bot berjalan...")
        app.run_polling(stop_signals=None)
    except Exception as e:
        log_error(f"❌ Admin Bot crash: {e}", exc_info=True)


def signal_handler(sig, frame):
    """Handle Ctrl+C untuk graceful shutdown."""
    log("\n⏹️  Menghentikan bot...", level='warning')
    shutdown_event.set()
    sys.exit(0)


def main():
    """Entry point utama untuk menjalankan kedua bot."""
    print("=" * 50, flush=True)
    print("  🌸 BUQEUET LIYA - TELEGRAM BOTS", flush=True)
    print("=" * 50, flush=True)
    print(flush=True)
    
    # Validasi tokens
    if not BUYER_BOT_TOKEN or BUYER_BOT_TOKEN == "your_buyer_bot_token_here":
        log("⚠️  Warning: TELEGRAM_BUYER_BOT_TOKEN belum diset di .env", level='warning')
    
    if not ADMIN_BOT_TOKEN or ADMIN_BOT_TOKEN == "your_admin_bot_token_here":
        log("⚠️  Warning: TELEGRAM_ADMIN_BOT_TOKEN belum diset di .env", level='warning')
    
    print(flush=True)
    log("🚀 Memulai bot...")
    log("   Tekan Ctrl+C untuk menghentikan")
    print(flush=True)
    
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Jalankan kedua bot di thread terpisah
    buyer_thread = threading.Thread(target=run_buyer_bot, name="BuyerBot", daemon=True)
    admin_thread = threading.Thread(target=run_admin_bot, name="AdminBot", daemon=True)
    
    buyer_thread.start()
    admin_thread.start()
    
    log("✅ Semua thread bot dimulai")
    
    # Wait for shutdown signal
    try:
        while not shutdown_event.is_set():
            shutdown_event.wait(timeout=1)
    except KeyboardInterrupt:
        signal_handler(None, None)
    
    log("✅ Bot dihentikan.")


if __name__ == "__main__":
    main()
