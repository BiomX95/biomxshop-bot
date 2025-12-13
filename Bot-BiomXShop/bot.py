# bot.py (ИСПРАВЛЕННЫЙ ПОРЯДОК ВЫЗОВА)

import telebot
import threading

from config import TOKEN
from handlers.autopost import auto_posting_sync

# --- НОВЫЙ ИМПОРТ: БАЗА ДАННЫХ ---
from database.db import create_tables, setup_initial_accounts
# ----------------------------------

# 1. Создаем бота
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# --- ИСПРАВЛЕНИЕ: СОЗДАНИЕ ТАБЛИЦ И АККАУНТОВ ПРИ СТАРТЕ ---
create_tables() 
setup_initial_accounts()
# ------------------------------------------------------------


# 2. Регистрируем хендлеры
# Старые импорты
from handlers.start import register_handlers as start_handlers
from handlers.menu import register_handlers as menu_handlers
from handlers.callbacks import register_handlers as callback_handlers
from handlers.wheel import register_handlers as wheel_handlers

# --- ИМПОРТ ДЛЯ ФУНКЦИОНАЛА АРЕНДЫ (rent.py) ---
from handlers.rent import register_handlers as rent_handlers
# ------------------------------------------------------

# Старые вызовы регистрации
start_handlers(bot)
menu_handlers(bot)

# --- ! КРИТИЧЕСКОЕ ИЗМЕНЕНИЕ: ВЫЗОВ rent_handlers ПЕРЕД callback_handlers ! ---
rent_handlers(bot) # <-- Сначала регистрируем специфические хендлеры аренды
# -----------------------------------------------------------------------------

callback_handlers(bot) # Затем более общие
wheel_handlers(bot) 

# 3. Запуск автопостинга
threading.Thread(
    target=auto_posting_sync,
    args=(bot,),
    daemon=True
).start()

print("Bot started")
bot.infinity_polling(none_stop=True)