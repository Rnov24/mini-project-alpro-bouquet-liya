"""
Centralized Error Handling untuk Telegram Bots.
Berisi error messages, decorator, dan utility functions.
"""

import sys
import traceback
import functools
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import (
    TelegramError, BadRequest, TimedOut, NetworkError, 
    ChatMigrated, RetryAfter, Forbidden
)


# ==================== ERROR MESSAGES ====================
# Semua pesan error dalam Bahasa Indonesia

ERROR_MESSAGES = {
    # General
    "unknown": "❌ Terjadi kesalahan. Silakan coba lagi nanti.",
    "session_expired": "⏰ Sesi Anda telah berakhir.\n\nKetik /start untuk memulai lagi.",
    "invalid_input": "⚠️ Input tidak valid. Silakan coba lagi.",
    "permission_denied": "🚫 Akses ditolak. Anda tidak memiliki izin.",
    
    # Product/Catalog
    "product_not_found": "❌ Produk tidak ditemukan.\n\nSilakan pilih dari katalog.",
    "category_empty": "📦 Kategori ini masih kosong.",
    "stock_empty": "⚠️ Maaf, stok habis.\n\nSilakan pilih produk atau ukuran lain.",
    "stock_insufficient": "⚠️ Stok tidak mencukupi.\n\nTersedia: {available} pcs",
    
    # Order
    "order_not_found": "❌ Pesanan tidak ditemukan.\n\nSilakan cek kembali ID pesanan Anda.",
    "order_expired": "⏰ Pesanan sudah kedaluwarsa atau tidak aktif.",
    "order_already_processed": "⚠️ Pesanan sudah diproses dan tidak dapat diubah.",
    "order_cannot_cancel": "❌ Pesanan tidak dapat dibatalkan karena sudah diproses.",
    "cart_empty": "🛒 Keranjang kosong.\n\nSilakan pilih produk terlebih dahulu.",
    
    # Input Validation
    "invalid_quantity": "⚠️ Masukkan jumlah yang valid (angka positif).",
    "invalid_phone": "⚠️ Format nomor WhatsApp tidak valid.\n\nContoh: 081234567890",
    "invalid_number": "⚠️ Masukkan angka yang valid.",
    "input_too_long": "⚠️ Input terlalu panjang. Maksimal {max} karakter.",
    
    # Network/Telegram
    "network_error": "🔌 Koneksi bermasalah.\n\nSilakan coba beberapa saat lagi.",
    "timeout_error": "⏳ Request timeout.\n\nSilakan coba lagi.",
    "telegram_error": "⚠️ Telegram error. Silakan coba lagi.",
    "callback_expired": "⏰ Tombol ini sudah kadaluwarsa.\n\nSilakan ketik /start untuk menu baru.",
    "message_not_modified": None,  # Silent, no need to notify user
    
    # Admin specific
    "not_admin": "🚫 Anda bukan admin.\n\nGunakan /daftar untuk mendaftar.",
    "admin_action_failed": "❌ Aksi admin gagal. Silakan coba lagi.",
    "export_failed": "❌ Gagal export data: {error}",
    "file_not_found": "📁 File tidak ditemukan.",
    
    # Notification
    "notif_failed": "⚠️ Gagal mengirim notifikasi.",
}


# ==================== ERROR CLASSIFIER ====================

def classify_error(error: Exception) -> str:
    """
    Mengklasifikasikan exception ke kategori error message.
    Returns key dari ERROR_MESSAGES.
    """
    error_str = str(error).lower()
    
    # Telegram specific errors
    if isinstance(error, BadRequest):
        if "query is too old" in error_str or "query id is invalid" in error_str:
            return "callback_expired"
        if "message is not modified" in error_str:
            return "message_not_modified"
        if "chat not found" in error_str:
            return "order_not_found"
        return "telegram_error"
    
    if isinstance(error, TimedOut):
        return "timeout_error"
    
    if isinstance(error, NetworkError):
        return "network_error"
    
    if isinstance(error, Forbidden):
        return "permission_denied"
    
    if isinstance(error, RetryAfter):
        return "timeout_error"
    
    # Python built-in errors
    if isinstance(error, (KeyError, AttributeError)):
        if "session" in error_str:
            return "session_expired"
        return "unknown"
    
    if isinstance(error, ValueError):
        return "invalid_input"
    
    if isinstance(error, FileNotFoundError):
        return "file_not_found"
    
    return "unknown"


def get_error_message(error_key: str, **kwargs) -> str | None:
    """
    Mendapatkan pesan error berdasarkan key.
    Supports placeholder formatting dengan kwargs.
    """
    message = ERROR_MESSAGES.get(error_key, ERROR_MESSAGES["unknown"])
    
    if message is None:
        return None
    
    try:
        return message.format(**kwargs)
    except (KeyError, ValueError):
        return message


# ==================== LOGGING HELPER ====================

def log_error(error: Exception, context_info: str = ""):
    """Log error dengan timestamp dan traceback."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    error_type = type(error).__name__
    
    print(f"[{timestamp}] ❌ ERROR [{context_info}]: {error_type}: {error}", flush=True)
    
    # Print traceback untuk debugging
    if hasattr(error, '__traceback__') and error.__traceback__:
        tb_lines = traceback.format_exception(type(error), error, error.__traceback__)
        for line in tb_lines[-3:]:  # Last 3 lines of traceback
            print(f"  {line.strip()}", flush=True)


# ==================== SAFE HANDLER DECORATOR ====================

def safe_handler(handler_name: str = ""):
    """
    Decorator untuk wrapping handler dengan error handling otomatis.
    
    Usage:
        @safe_handler("start")
        async def start(update, context):
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            try:
                return await func(update, context)
            
            except Exception as error:
                # Classify error
                error_key = classify_error(error)
                error_message = get_error_message(error_key)
                
                # Log error
                name = handler_name or func.__name__
                log_error(error, f"Handler: {name}")
                
                # Skip silent errors
                if error_message is None:
                    return
                
                # Send error message to user
                try:
                    if update.callback_query:
                        # Callback query - try to answer first
                        try:
                            await update.callback_query.answer(error_message[:200], show_alert=True)
                        except:
                            pass
                        
                        # Try to edit message
                        try:
                            from bot.buyer.keyboards import keyboard_kembali_menu
                            await update.callback_query.edit_message_text(
                                error_message,
                                reply_markup=keyboard_kembali_menu(),
                                parse_mode="Markdown"
                            )
                        except:
                            pass
                    
                    elif update.message:
                        await update.message.reply_text(error_message)
                
                except Exception as send_error:
                    log_error(send_error, "Sending error message")
        
        return wrapper
    return decorator


def safe_callback(handler_name: str = ""):
    """
    Decorator khusus untuk callback query handlers.
    Lebih toleran terhadap expired callback.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            try:
                return await func(update, context)
            
            except BadRequest as error:
                error_str = str(error).lower()
                
                # Silent skip untuk expired callback
                if "query is too old" in error_str or "message is not modified" in error_str:
                    log_error(error, f"Callback: {handler_name or func.__name__} (silent)")
                    return
                
                # Other BadRequest - log and notify
                log_error(error, f"Callback: {handler_name or func.__name__}")
                try:
                    await update.callback_query.answer(
                        "⚠️ Terjadi kesalahan. Ketik /start untuk menu baru.",
                        show_alert=True
                    )
                except:
                    pass
            
            except Exception as error:
                log_error(error, f"Callback: {handler_name or func.__name__}")
                try:
                    await update.callback_query.answer(
                        "❌ Error. Ketik /start untuk mulai lagi.",
                        show_alert=True
                    )
                except:
                    pass
        
        return wrapper
    return decorator


# ==================== VALIDATION HELPERS ====================

def validate_quantity(text: str, max_stock: int = None) -> tuple[bool, int | None, str | None]:
    """
    Validasi input quantity.
    Returns: (is_valid, quantity, error_message)
    """
    if not text.isdigit():
        return False, None, ERROR_MESSAGES["invalid_quantity"]
    
    qty = int(text)
    
    if qty <= 0:
        return False, None, ERROR_MESSAGES["invalid_quantity"]
    
    if max_stock is not None and qty > max_stock:
        return False, None, get_error_message("stock_insufficient", available=max_stock)
    
    return True, qty, None


def validate_phone(text: str) -> tuple[bool, str | None]:
    """
    Validasi format nomor telepon Indonesia.
    Returns: (is_valid, error_message)
    """
    # Remove common separators
    cleaned = text.replace(" ", "").replace("-", "").replace("+", "")
    
    # Check if numeric
    if not cleaned.isdigit():
        return False, ERROR_MESSAGES["invalid_phone"]
    
    # Check length (8-15 digits)
    if len(cleaned) < 8 or len(cleaned) > 15:
        return False, ERROR_MESSAGES["invalid_phone"]
    
    return True, None


def validate_number(text: str, allow_zero: bool = True) -> tuple[bool, int | None, str | None]:
    """
    Validasi input angka.
    Returns: (is_valid, number, error_message)
    """
    if not text.isdigit():
        return False, None, ERROR_MESSAGES["invalid_number"]
    
    num = int(text)
    
    if not allow_zero and num == 0:
        return False, None, ERROR_MESSAGES["invalid_number"]
    
    return True, num, None
