# handlers/menu.py (ИЗМЕНЕННЫЙ КОД)

from telebot import types
from config import DONATE_IMG, IMG_PATH
from handlers import wheel 
# --- НОВЫЙ ИМПОРТ ---
# Нам нужна функция, которая показывает меню аренды,
# вероятно, она в handlers/rent.py
from handlers.rent import show_rent_menu 
# --------------------

def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.chat.type == "private")
    def menu(message):

        if message.text == "⏰Аренда аккаунтов":
            # --- ВЫЗЫВАЕМ ФУНКЦИЮ ПОКАЗА МЕНЮ АРЕНДЫ ---
            
            # 1. Отправляем первое сообщение (его нужно будет отредактировать)
            first_msg = bot.send_message(message.chat.id, "Загрузка меню аренды...")
            
            # 2. Создаем фиктивный объект Call для show_rent_menu,
            #    т.к. эта функция написана для обработки колбэка (edit_message_caption)
            class MockCall:
                def __init__(self, message_obj):
                    self.message = message_obj
                    self.id = 0 # Фейковый ID колбэка
            
            # 3. Редактируем сообщение, вызывая функцию показа меню аренды
            show_rent_menu(
                call=MockCall(first_msg), 
                bot=bot
            )
            # -------------------------------------------------------------

        elif message.text == "💎Алмазы":
            # ... (код для Алмазы остается без изменений) ...
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

        elif message.text == "Переходник":
            bot.send_message(
                message.chat.id,
                "Основной канал — @BiomXShops\n"
                "Отзывы — @BiomXShop_Otziv\n"
                "Официальный Чат — @BiomXShop_Chat\n"
                "Чат по Free Fire — @Freec_Fire\n"
                "Сотрудничество — @BiomXShop_Sotryd"
            )

        elif message.text == "🎮Наш сайт":
            with open(IMG_PATH + "logo2.jpg", "rb") as photo:
                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption="Скоро выйдет наш сайт маркетплейс:\nhttps://biomx.shop\nСледите за обновлениями! - @BiomXShops"
                )

        elif message.text == "🎁Особая посылка":
            with open(DONATE_IMG + "posilka.jpg", "rb") as photo:
                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption="Покупаем особые посылки и любые другие внутреигровые донаты🎁🤩\nПисать: @BiomXShop_Support"
                )

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

        elif message.text == "🚀🎮VPN для FF":
            with open(IMG_PATH + "vpn.jpg", "rb") as photo:keyboard = types.InlineKeyboardMarkup()
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

        elif message.text == "🎡 Рулетка":
            wheel.start_wheel(bot, message)  # вызов рулетки

        else:
            bot.send_message(message.chat.id, "Я не знаю эту команду.")










