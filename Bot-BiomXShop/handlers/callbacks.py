from telebot import types
from config import ADMIN_IDS
from texts.rent_texts import descriptions

def register_handlers(bot):

    @bot.callback_query_handler(func=lambda call: call.message and call.message.chat.type == "private")
    def callback(call):
        
        # Оставляем только те действия, которых НЕТ в rent.py
        
        # Сдавать свой (Аккаунт 12)
        if call.data == "rent12":
            bot.send_message(call.message.chat.id, descriptions[12])

        # VPN keys
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