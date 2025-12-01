from utils.send_media import send_two_photos
from texts.rent_texts import descriptions

def register_handlers(bot, is_private):

    @bot.callback_query_handler(func=lambda call: call.message.chat.type == "private")
    def callback(call):

        if call.data == "rent1":
            send_two_photos(
                bot, call.message,
                "Abakaev.jpg",
                "Abakaev.jpg",
                descriptions[1]
            )

        elif call.data == "rent2":
            send_two_photos(
                bot, call.message,
                "KARINA.jpg",
                "KARINAevo.jpg",
                descriptions[2]
            )

        elif call.data == "rent3":
            send_two_photos(
                bot, call.message,
                "BiomXShop.jpg",
                "BiomXShop2.jpg",
                descriptions[3]
            )

        elif call.data == "rent4":
            send_two_photos(
                bot, call.message,
                "malish.jpg",
                "malish2.jpg",
                descriptions[4]
            )

        elif call.data == "rent5":
            send_two_photos(
                bot, call.message,
                "DAGPropysk.jpg",
                "DAGPropysk2.jpg",
                descriptions[5]
            )

        elif call.data == "rent6":
            bot.send_message(call.message.chat.id, descriptions[6])

        # VPN
        elif call.data == "vpn_ios":
            key = "vless://cb55c987-9e1e-4a2b-8cea-e429c6bb530b@94.198.100.173:443?security=reality&sni=aws.com&alpn=h2&fp=chrome&pbk=ckRcueERkPqqjZABwxqni_J_Nbb70Q6k5fEEUAjoImw&type=tcp&flow=xtls-rprx-vision&encryption=none#avovpn.com-4636825-3414822"
            bot.answer_callback_query(call.id, "Ключ отправлен")
            bot.send_message(call.message.chat.id, key)

        elif call.data == "vpn_android":
            key = "vless://cb55c987-9e1e-4a2b-8cea-e429c6bb530b@94.198.100.173:443?security=reality&sni=aws.com&alpn=h2&fp=chrome&pbk=ckRcueERkPqqjZABwxqni_J_Nbb70Q6k5fEEUAjoImw&type=tcp&flow=xtls-rprx-vision&encryption=none#avovpn.com-4636825-3414822"
            bot.answer_callback_query(call.id, "Ключ отправлен")
            bot.send_message(call.message.chat.id, key)



