import telebot
import threading
from config import TOKEN
from handlers.autopost import auto_posting_sync
from database.db import create_tables, setup_initial_accounts

# Импорт хендлеров
from handlers.start import register_handlers as start_handlers
from handlers.menu import register_handlers as menu_handlers
from handlers.callbacks import register_handlers as callback_handlers
from handlers.rent import register_handlers as rent_handlers

# Инициализация
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
create_tables()
setup_initial_accounts()

# Регистрация (Порядок важен!)
start_handlers(bot)
rent_handlers(bot)
menu_handlers(bot)
callback_handlers(bot)

# ЗАПУСК АВТОПОСТИНГА В ОТДЕЛЬНОМ ПОТОКЕ
if __name__ == "__main__":
    threading.Thread(
        target=auto_posting_sync,
        args=(bot,),
        daemon=True
    ).start()

    print("Бот запущен...")
    bot.infinity_polling(none_stop=True)