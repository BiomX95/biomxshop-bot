from utils.send_media import send_two_photos
from config import RENT_IMG
from texts.rent_texts import descriptions

def register_handlers(bot, is_private=False):

    @bot.callback_query_handler(func=lambda call: call.message and call.message.chat.type == "private")
    def callback(call):

        # RENTS
        if call.data == "rent1":
            send_two_photos(
                bot, call.message,
                RENT_IMG + "Abakaev.jpg",
                RENT_IMG + "Abakaev.jpg",
                descriptions[1]
            )

        elif call.data == "rent2":
            send_two_photos(
                bot, call.message,
                RENT_IMG + "KARINA.jpg",
                RENT_IMG + "KARINAevo.jpg",
                descriptions[2]
            )

        elif call.data == "rent3":
            send_two_photos(
                bot, call.message,
                RENT_IMG + "BiomXShop.jpg",
                RENT_IMG + "BiomXShop2.jpg",
                descriptions[3]
            )

        elif call.data == "rent4":
            send_two_photos(
                bot, call.message,
                RENT_IMG + "malish.jpg",
                RENT_IMG + "malish2.jpg",
                descriptions[4]
            )

        elif call.data == "rent5":
            send_two_photos(
                bot, call.message,
                RENT_IMG + "DAGPropysk.jpg",
                RENT_IMG + "DAGPropysk2.jpg",
                descriptions[5]
            )
             elif call.data == "rent6":
            send_two_photos(
                bot, call.message,
                RENT_IMG + "yasmi.jpg",
                RENT_IMG + "yasmi.jpg",
                descriptions[6]
           )
             elif call.data == "rent7":
            send_two_photos(
                bot, call.message,
                RENT_IMG + "tyrpalpropusk.jpg",
                RENT_IMG + "tyrpalpropusk.jpg",
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




