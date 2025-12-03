import telebot
import threading

from config import TOKEN
from handlers.autopost import auto_posting_sync

# 1. Создаем бота
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# 2. Регистрируем хендлеры
from handlers.start import register_handlers as start_handlers
from handlers.menu import register_handlers as menu_handlers
from handlers.callbacks import register_handlers as callback_handlers
from handlers.wheel import register_handlers as wheel_handlers

start_handlers(bot)
menu_handlers(bot)
callback_handlers(bot)
wheel_handlers(bot)   # ← теперь ОК

# 3. Запуск автопостинга
threading.Thread(
    target=auto_posting_sync,
    args=(bot,),
    daemon=True
).start()

print("Bot started")
bot.infinity_polling(none_stop=True)






