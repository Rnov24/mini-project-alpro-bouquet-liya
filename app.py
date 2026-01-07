"""
Sistem Kasir UMKM IKMI Cirebon
Entry point aplikasi.
"""

from src.ui.menu import main_menu
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.handlers import start, callback_router, text_handler

TOKEN = "7824418675:AAGhUBTARI09lTm9VybRhx-XWju-YOso5Cc"
def run_bot():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_router))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))  
    print("🤖 Bot berjalan...")
    app.run_polling()

def main():
    print("1. CLI Kasir")
    print("2. Telegram Bot")
    mode = input("Pilih mode (1/2): ").strip()

    if mode == "1":
        main_menu()
    elif mode == "2":
        run_bot()
    else:
        print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
