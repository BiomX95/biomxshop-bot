import os
from utils.send_media import send_two_photos
from config import RENT_IMG
from texts.rent_texts import descriptions

def register_handlers(bot, is_private=False):

    @bot.callback_query_handler(func=lambda call: call.message and call.message.chat.type == "private")
    def callback(call):

        # Вспомогательная функция для корректного формирования пути
        def rent_path(filename):
            return os.path.join(RENT_IMG, filename)

        # RENTS
        if call.data == "rent1":
            send_two_photos(
                bot, call.message,
                rent_path("Abakaev.jpg"),
                rent_path("Abakaev.jpg"),
                descriptions[1]
            )

        elif call.data == "rent2":
            send_two_photos(
                bot, call.message,
                rent_path("KARINA.jpg"),
                rent_path("KARINAevo.jpg"),
                descriptions[2]
            )

        elif call.data == "rent3":
            send_two_photos(
                bot, call.message,
                rent_path("BiomXShop.jpg"),
                rent_path("BiomXShop2.jpg"),
                descriptions[3]
            )

        elif call.data == "rent4":
            send_two_photos(
                bot, call.message,
                rent_path("malish.jpg"),
                rent_path("malish2.jpg"),
                descriptions[4]
            )
            
        elif call.data == "rent5":
            send_two_photos(
                bot, call.message,
                rent_path("DAGPropysk.jpg"),
                rent_path("DAGPropysk2.jpg"),
                descriptions[5]
            )
            
        elif call.data == "rent6":
            send_two_photos(
                bot, call.message,
                rent_path("yasmi.jpg"),
                rent_path("yasmi.jpg"),
                descriptions[6]
            )
            
        elif call.data == "rent7":
            send_two_photos(
                bot, call.message,
                rent_path("tyrpalpropusk.jpg"),
                rent_path("tyrpalpropusk.jpg"),
                descriptions[7]
            )
            
        elif call.data == "rent8":
            bot.send_message(call.message.chat.id, descriptions[8])

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






