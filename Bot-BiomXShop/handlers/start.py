from telebot import types
from config import IMG_PATH

def register_handlers(bot):

    @bot.message_handler(commands=['start'])
    def start(message):
        if message.chat.type != "private":
            return  # Блокировка групп

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("⏰Аренда аккаунтов")
        btn2 = types.KeyboardButton("Переходник")
        btn3 = types.KeyboardButton("💎Алмазы")
        btn4 = types.KeyboardButton("🎮Наш сайт")
        btn5 = types.KeyboardButton("🎁Особая посылка")
        btn6 = types.KeyboardButton("⭐️Telegram stars")
        btn7 = types.KeyboardButton("🚀🎮VPN для FF")
btn8 = types.KeyboardButton("🎡 Рулетка")
markup.add(btn1, btn2, btn3, btn4)
markup.add(btn5, btn6, btn7, btn8)


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


