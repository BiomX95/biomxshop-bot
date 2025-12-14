# handlers/callbacks.py

from telebot import types
from utils.send_media import send_two_photos
from config import RENT_IMG, ADMIN_ID # Убедитесь, что ADMIN_ID импортирован
from texts.rent_texts import descriptions

# --- НОВЫЙ ИМПОРТ: КЛАВИАТУРА ДЛЯ ПОСТА ---
from keyboards.rent_menu import get_post_status_markup 
# ------------------------------------------

# Функция get_status_markup УДАЛЕНА, так как заменена на get_post_status_markup

def register_handlers(bot, is_private=False):

    @bot.callback_query_handler(func=lambda call: call.message and call.message.chat.type == "private")
    def callback(call):
        
        # Определяем, является ли пользователь админом
        # Используем try/except, так как в config может быть не целое число
        try:
            is_admin_user = call.from_user.id == int(ADMIN_ID)
        except:
            is_admin_user = False
        
        # RENTS
        if call.data == "rent1":
            markup = get_post_status_markup(account_id=1, is_admin=is_admin_user)
            send_two_photos(
                bot, call.message,
                RENT_IMG + "Abakaev.jpg",
                RENT_IMG + "Abakaev2.jpg", 
                descriptions[1],
                reply_markup=markup
            )

        elif call.data == "rent2":
            markup = get_post_status_markup(account_id=2, is_admin=is_admin_user)
            send_two_photos(
                bot, call.message,
                RENT_IMG + "KARINA.jpg",
                RENT_IMG + "KARINAevo.jpg",
                descriptions[2],
                reply_markup=markup
            )

        elif call.data == "rent3":
            markup = get_post_status_markup(account_id=3, is_admin=is_admin_user)
            send_two_photos(
                bot, call.message,
                RENT_IMG + "BiomXShop.jpg",
                RENT_IMG + "BiomXShop2.jpg",
                descriptions[3],
                reply_markup=markup
            )

        elif call.data == "rent4":
            markup = get_post_status_markup(account_id=4, is_admin=is_admin_user)
            send_two_photos(
                bot, call.message,
                RENT_IMG + "malish.jpg",
                RENT_IMG + "malish2.jpg",
                descriptions[4],
                reply_markup=markup
            )

        elif call.data == "rent5":
            markup = get_post_status_markup(account_id=5, is_admin=is_admin_user)
            send_two_photos(
                bot, call.message,
                RENT_IMG + "DAGPropysk.jpg",
                RENT_IMG + "DAGPropysk22.jpg",
                descriptions[5],
                reply_markup=markup
            )

        elif call.data == "rent6":
            markup = get_post_status_markup(account_id=6, is_admin=is_admin_user)
            send_two_photos(
                bot, call.message,
                RENT_IMG + "Malikak.jpg",
                RENT_IMG + "Malikak2.jpg",
                descriptions[6],
                reply_markup=markup
            )

        elif call.data == "rent7":
            markup = get_post_status_markup(account_id=7, is_admin=is_admin_user)
            send_two_photos(
                bot, call.message,
                RENT_IMG + "yasmi.jpg",
                RENT_IMG + "yasmi.jpg",
                descriptions[7],
                reply_markup=markup
            )
            
        elif call.data == "rent8":
            markup = get_post_status_markup(account_id=8, is_admin=is_admin_user)
            send_two_photos(
                bot, call.message,
                RENT_IMG + "Dashaak.jpg",
                RENT_IMG + "Dashaak2.jpg",
                descriptions[8],
                reply_markup=markup
            )
            
        elif call.data == "rent8":
            markup = get_post_status_markup(account_id=8, is_admin=is_admin_user)
            send_two_photos(
                bot, call.message,
                RENT_IMG + "Dashaakk.jpg",
                RENT_IMG + "Dashaakk2.jpg",
                descriptions[9],
                reply_markup=markup
            )

        elif call.data == "rent10":
            # Аккаунт 9 не имеет ID в базе, поэтому не прикрепляем клавиатуру
            bot.send_message(call.message.chat.id, descriptions[6])

        # VPN keys
        # ... (Остальной код без изменений) ...
        elif call.data == "vpn_ios":
            key = ("vless://cb55c987-9e1e-4a2b-8cea-e429c6bb530b@94.198.100.173:443"
                     "?security=reality&sni=aws.com&alpn=h2&fp=chrome&pbk="
                     "ckRcueERkPqqjZABwxqni_J_Nbb70Q6k5fEEUAjoImw&type=tcp&flow="
                     "xtls-rprx-vision&encryption=none#avovpn.com")
            bot.answer_callback_query(call.id, "Ключ отправлен")
            bot.send_message(call.message.chat.id, key) 
        elif call.data == "vpn_android":
            key = ("vless://cb55c987-9e1e-4a2b-8cea-e429c6bb530b@94.198.100.173:443"
                     "?security=reality&sni=aws.com&alpn=h2&fp=chrome&pbk="
                     "ckRcueERkPqqjZABwxqni_J_Nbb70Q6k5fEEUAjoImw&type=tcp&flow="
                     "xtls-rprx-vision&encryption=none#avovpn.com")
            bot.answer_callback_query(call.id, "Ключ отправлен")
            bot.send_message(call.message.chat.id, key)










