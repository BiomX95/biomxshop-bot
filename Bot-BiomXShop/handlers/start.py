from telebot import types
from config import IMG_PATH

def register_handlers(bot):

    @bot.message_handler(commands=['start'])
    def start(message):
        # Разрешаем только приватные чаты
        if message.chat.type != "private":
            return

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Меню")
        markup.add(btn1)

        # Отправка логотипа
        try:
            with open(IMG_PATH + "logo.jpg", "rb") as logo:
                bot.send_photo(
                    message.chat.id,
                    logo,
                    caption="Добро пожаловать!",
                    reply_markup=markup
                )
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Логотип не найден, добавьте logo.jpg в папку images")
