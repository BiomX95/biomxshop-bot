import telebot
import threading

from config import TOKEN
from handlers.autopost import auto_posting_sync
from handlers.roulette import register_handlers as roulette_handlers

# после создания bot и определения is_private (если ты используешь)
roulette_handlers(bot, is_private=False)   # вторым аргументом можно передать is_private, но внутри есть своя проверка

# Инициализация бота
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Регистрация всех хендлеров
from handlers.start import register_handlers as start_handlers
from handlers.menu import register_handlers as menu_handlers
from handlers.callbacks import register_handlers as callback_handlers

start_handlers(bot)
menu_handlers(bot)
callback_handlers(bot, is_private=True)

# Запуск автопостинга (важно: только один аргумент — bot!)
threading.Thread(
    target=auto_posting_sync,
    args=(bot,),
    daemon=True
).start()

print("Bot started")
bot.infinity_polling(none_stop=True)





