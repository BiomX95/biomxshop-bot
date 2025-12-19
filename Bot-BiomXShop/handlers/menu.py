from telebot import types
from config import DONATE_IMG, IMG_PATH
from handlers import wheel 
from database.db import get_rental_accounts

def register_handlers(bot):

    @bot.message_handler(func=lambda m: True)
    def menu(message):
        
        # --- ЛОГИКА ДЛЯ СПАМЕРА (чтобы не было "не знаю команду") ---
        if message.text and message.text.startswith("АККАУНТ"):
            all_accs = get_rental_accounts()
            match = next((a for a in all_accs if a[1] == message.text), None)
            if match:
                from handlers.rent import check_account_status
                class MockCall:
                    def __init__(self):
                        self.message = message
                        self.data = f"user_rent_{match[0]}"
                        self.from_user = message.from_user
                check_account_status(MockCall(), bot)
                return

        # --- ТВОЙ ОСНОВНОЙ ФУНКЦИОНАЛ ---
        if message.text == "⏰Аренда аккаунтов":
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("АККАУНТ №1🚹", callback_data="user_rent_1"),
                types.InlineKeyboardButton("АККАУНТ №2🚺", callback_data="user_rent_2")
            )
            markup.add(
                types.InlineKeyboardButton("АККАУНТ №3🚹", callback_data="user_rent_3"),
                types.InlineKeyboardButton("АККАУНТ №4🚹", callback_data="user_rent_4")
            )
            markup.add(
                types.InlineKeyboardButton("АККАУНТ №5🚹", callback_data="user_rent_5"),
                types.InlineKeyboardButton("АККАУНТ №6🚹", callback_data="user_rent_6")
            )
            markup.add(
                types.InlineKeyboardButton("АККАУНТ №7🚹", callback_data="user_rent_7"),
                types.InlineKeyboardButton("АККАУНТ №8🚺", callback_data="user_rent_8")
            )
            markup.add(
                types.InlineKeyboardButton("АККАУНТ №9🚹", callback_data="user_rent_9"),
                types.InlineKeyboardButton("АККАУНТ №10🚹", callback_data="user_rent_10")
            )
            markup.add(
                types.InlineKeyboardButton("АККАУНТ №11🚹", callback_data="user_rent_11"),
                types.InlineKeyboardButton("СДАВАТЬ СВОЙ", callback_data="rent12")
            )
            bot.send_message(message.chat.id, "Выберите аккаунт для аренды:", reply_markup=markup)

        elif message.text == "💎Алмазы":
            bot.send_message(
                message.chat.id,
                "У нас цены ниже рыночных 🏷\n"
                "Скидки на донаты💎🛍\n\n"
                "100+5💎 - 70₽\n310+16💎 - 230₽\n520+26💎 - 375₽\n"
                "1060+53💎 - 750₽\n2180+218💎 - 1500₽\n5600+560💎 - 3620₽\n\n"
                "Ваучер Лайт - 44₽\nВаучер на неделю - 120₽\nВаучер на месяц - 620₽\n\n"
                "Прайс на Эво - Пропуск\n3 дня - 49₽\n7 дней - 95₽\n30 дней - 249₽\n\n"
                "Пропуск прокачки💎\n15LVL — 50₽\n25LVL — 50₽\n30LVL — 73₽\n6LVL — 28₽\n20LVL — 50₽\n\n"
                "🎁Так же могу купить внутреигровые донаты: Особая посылка, Пропуск прокачки.\n\n"
                "✍️По вопросам: @BiomXShop_Support"
            )

        elif message.text == "Переходник":
            bot.send_message(
                message.chat.id,
                "Основной канал — @BiomXShops\nОтзывы — @BiomXShop_Otziv\n"
                "Официальный Чат — @BiomXShop_Chat\nЧат по Free Fire — @Freec_Fire\n"
                "Сотрудничество — @BiomXShop_Sotryd"
            )

        elif message.text == "🎮Наш сайт":
            try:
                with open(IMG_PATH + "logo2.jpg", "rb") as photo:
                    bot.send_photo(
                        message.chat.id, photo,
                        caption="Скоро выйдет наш сайт маркетплейс:\nhttps://biomx.shop\nСледите за обновлениями! - @BiomXShops"
                    )
            except:
                bot.send_message(message.chat.id, "Наш сайт: https://biomx.shop")

        elif message.text == "🎁Особая посылка":
            try:
                with open(DONATE_IMG + "posilka.jpg", "rb") as photo:
                    bot.send_photo(message.chat.id, photo, caption="Покупаем особые посылки🎁🤩\nПисать: @BiomXShop_Support")
            except:
                bot.send_message(message.chat.id, "Покупаем посылки! Писать: @BiomXShop_Support")

        elif message.text == "⭐️Telegram stars":
            try:
                with open(DONATE_IMG + "stars.jpg", "rb") as photo:
                    bot.send_photo(
                        message.chat.id, photo,
                        caption="🌟 50 Stars — 72₽\n🌟 75 Stars — 105₽\n🌟 100 Stars — 138₽\n🌟 500 Stars — 695₽\n🌟 1000 Stars — 1395₽\nПисать: @BiomXShop_Support"
                    )
            except:
                bot.send_message(message.chat.id, "Цены на Stars уточняйте у @BiomXShop_Support")

        elif message.text == "🚀🎮VPN для FF":
            try:
                with open(IMG_PATH + "vpn.jpg", "rb") as photo:
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(
                        types.InlineKeyboardButton("Ключ для iPhone", callback_data="vpn_ios"),
                        types.InlineKeyboardButton("Ключ для Android", callback_data="vpn_android")
                    )
                    bot.send_photo(message.chat.id, photo, caption="Выберите ключ ниже:", reply_markup=keyboard)
            except:
                bot.send_message(message.chat.id, "VPN ключи доступны в меню.")

        elif message.text == "🎡 Рулетка":
            wheel.start_wheel(bot, message)

        else:
            if message.chat.type == "private":
                bot.send_message(message.chat.id, "Я не знаю эту команду.")





