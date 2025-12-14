# handlers/start.py (Исправленная версия)

from telebot import types
# from config import IMG_PATH  <-- Больше не нужен, если путь определяется здесь
from handlers import wheel
import os
import inspect # Используем для получения пути к текущему файлу

# ----------------------------------------------------
# * ИСПРАВЛЕНИЕ ОШИБКИ FILE NOT FOUND *
# ----------------------------------------------------
# 1. Получаем путь к папке, где находится 'handlers/start.py'
CURRENT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# 2. Строим путь к файлу 'logo.jpg' относительно КОРНЯ ПРОЕКТА
#    (Выходим из handlers/ (..), затем заходим в images/)
LOGO_PATH = os.path.join(CURRENT_DIR, '..', 'images', 'logo.jpg')
# ----------------------------------------------------


def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        if message.chat.type != "private":
            return # Блокировка групп

        # --- Клавиатура ---
        # ... (Код клавиатуры остается без изменений) ...
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("⏰Аренда аккаунтов")
        btn2 = types.KeyboardButton("Переходник")
        btn3 = types.KeyboardButton("💎Алмазы")
        btn4 = types.KeyboardButton("🎮Наш сайт")
        btn5 = types.KeyboardButton("🎁Особая посылка")
        btn6 = types.KeyboardButton("⭐️Telegram stars")
        btn7 = types.KeyboardButton("🚀🎮VPN для FF")
        btn8 = types.KeyboardButton("🎡 Рулетка") # Новая кнопка

        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)


        # --- Фото приветствия ---
        try:
            # Используем исправленный, надежный путь LOGO_PATH
            with open(LOGO_PATH, "rb") as logo:
                bot.send_photo(
                    message.chat.id,
                    logo,
                    caption=(
                        "Добро пожаловать в BiomX Shop!\n\n"
                        "Отзывы — @BiomXShop_Otziv\n"
                        "Официальный Чат — @BiomXShop_Chat\n"
                        "Чат по Free Fire — @Freec_Fire\n"
                        "Основной канал — @BiomXShops\n"
                        "Сотрудничество — @BiomXShop_Sotryd"
                    ),
                    reply_markup=markup
                )
        except FileNotFoundError:
             # Если даже абсолютный путь не сработал, отправим сообщение без фото
             bot.send_message(message.chat.id, "Бот запущен, но не удалось загрузить 'logo.jpg'. Проверьте пути файлов!")

    # --- Регистрируем рулетку ---
    wheel.register_handlers(bot) # <-- Здесь подключаем все хендлеры рулетки

