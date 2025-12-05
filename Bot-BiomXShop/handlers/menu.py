from telebot import types
from config import DONATE_IMG, IMG_PATH
from handlers import wheel  # Импорт для рулетки

def register_handlers(bot):

    # Даем возможность работать везде (и в группе, и в личке)
    @bot.message_handler(content_types=['text'])
    def menu(message):

        # Аренда
        if message.text == "⏰Аренда аккаунтов":
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("АККАУНТ №1🚹", callback_data="rent1"),
                types.InlineKeyboardButton("АККАУНТ №2🚺", callback_data="rent2")
            )
            markup.add(
                types.InlineKeyboardButton("АККАУНТ №3🚹", callback_data="rent3"),
                types.InlineKeyboardButton("АККАУНТ №4🚹", callback_data="rent4")
            )
            markup.add(
                types.InlineKeyboardButton("АККАУНТ №5🚹", callback_data="rent5"),
                types.InlineKeyboardButton("АККАУНТ №6🚹", callback_data="rent6")
            )
            markup.add(
                types.InlineKeyboardButton("АККАУНТ №7🚹", callback_data="rent7"),
                types.InlineKeyboardButton("СДАВАТЬ СВОЙ", callback_data="rent8")
            )
            bot.send_message(message.chat.id, "Выберите аккаунт для аренды:", reply_markup=markup)

        # Алмазы
        elif message.text == "💎Алмазы":
            bot.send_message(
                message.chat.id,
                """У нас цены ниже рыночных 🏷
У нас цены ниже
Рыночных 🏷
Скидки на донаты💎🛍

100+5💎 - 70₽
310+16💎 - 230₽
520+26💎 - 375₽
1060+53💎 - 750₽
2180+218💎 - 1500₽
5600+560💎 - 3620₽

Ваучер Лайт - 44₽
Ваучер на неделю - 120₽
Ваучер на месяц - 620₽ 

Прайс на Эво - Пропуск 
3 дня - 49₽   
7 дней - 95₽
30 дней - 249₽ 

Пропуск прокачки💎
Пропуск прокачки - 15LVL — 50₽
Пропуск прокачки - 25LVL — 50₽
Пропуск прокачки - 30LVL — 73₽
Пропуск прокачки - 6LVL — 28₽
Пропуск прокачки - 20LVL — 50₽

🎁Так же могу купить внутреигровые донаты: Особая посылка, Пропуск прокачки.

✍️По вопросам: @BiomXShop_Support"""
            )

        # Переходник
        elif message.text == "Переходник":
            bot.send_message(
                message.chat.id,
                "Основной канал — @BiomXShops\n"
                "Отзывы — @BiomXShop_Otziv\n"
                "Официальный Чат — @BiomXShop_Chat\n"
                "Чат по Free Fire — @Freec_Fire\n"
                "Сотрудничество — @BiomXShop_Sotryd"
            )

        # Наш сайт
        elif message.text == "🎮Наш сайт":
            with open(IMG_PATH + "logo2.jpg", "rb") as photo:
                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption="Скоро выйдет наш сайт маркетплейс:\nhttps://biomx.shop\nСледите за обновлениями! - @BiomXShops"
                )

        # Особая посылка
        elif message.text == "🎁Особая посылка":
            with open(DONATE_IMG + "posilka.jpg", "rb") as photo:
                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption="Покупаем особые посылки и любые другие внутреигровые донаты🎁🤩\nПисать: @BiomXShop_Support"
                )

        # Stars
        elif message.text == "⭐️Telegram stars":
            with open(DONATE_IMG + "stars.jpg", "rb") as photo:
                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption="""
🌟 50 Stars — 72₽
🌟 75 Stars — 105₽
🌟 100 Stars — 138₽
🌟 150 Stars — 208₽
🌟 250 Stars — 345₽
🌟 350 Stars — 485₽
🌟 500 Stars — 695₽
🌟 750 Stars — 1045₽
🌟 1000 Stars — 1395₽
🌟 1500 Stars — 2090₽
🌟 2500 Stars — 3475₽
🌟 5000 Stars — 6948₽
🌟 10000 Stars — 13895₽
Писать: @BiomXShop_Support"""
                )

        # VPN
        elif message.text == "🚀🎮VPN для FF":
            with open(IMG_PATH + "vpn.jpg", "rb") as photo:

                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(
                    types.InlineKeyboardButton("Ключ для iPhone", callback_data="vpn_ios"),
                    types.InlineKeyboardButton("Ключ для Android", callback_data="vpn_android")
                )

                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption="Выберите необходимый ключ для avoVPN ниже:",
                    reply_markup=keyboard
                )

        # Рулетка
        elif message.text == "🎡 Рулетка":
            wheel.start_wheel(bot, message)

        else:
            bot.send_message(message.chat.id, "Я не знаю эту команду.")


    # ОБРАБОТЧИК CALLBACK-КНОПОК (ОБЯЗАТЕЛЬНО!)
    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        bot.answer_callback_query(call.id, "Обрабатываю...")
        # Тут твоя логика callback'ов
        # Можно оставить пустым если у тебя они в других файлах
