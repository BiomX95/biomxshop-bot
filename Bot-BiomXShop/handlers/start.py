from telebot import types
from config import IMG_PATH
from handlers import wheel  # Импорт твоего wheel.py
import os

def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        if message.chat.type != "private":
            return  # Блокировка групп

        # --- Клавиатура ---
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("⏰Аренда аккаунтов")
        btn2 = types.KeyboardButton("Переходник")
        btn3 = types.KeyboardButton("💎Алмазы")
        btn4 = types.KeyboardButton("🎮Наш сайт")
        btn5 = types.KeyboardButton("🎁Особая посылка")
        btn6 = types.KeyboardButton("⭐️Telegram stars")
        btn7 = types.KeyboardButton("🚀🎮VPN для FF")
        btn8 = types.KeyboardButton("🎡 Рулетка")  # Новая кнопка

        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)

        # --- Фото приветствия ---
        with open(IMG_PATH + "logo.jpg", "rb") as logo:
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

    # --- Регистрируем рулетку ---
    wheel.register_handlers(bot)  # <-- Здесь подключаем все хендлеры рулетки


