from utils.send_media import send_two_photos
from texts.rent_texts import descriptions

def register_handlers(bot, is_private):

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):

        # ГЛАВНАЯ защита
        if call.message.chat.type != "private":
            bot.answer_callback_query(call.id)
            return

        if call.data == "rent1":
            send_two_photos(bot, call.message, "Abakaev.jpg", "Abakaev.jpg", descriptions[1])

        elif call.data == "rent2":
            send_two_photos(bot, call.message, "KARINA.jpg", "KARINAevo.jpg", descriptions[2])

        elif call.data == "rent3":
            send_two_photos(bot, call.message, "BiomXShop.jpg", "BiomXShop2.jpg", descriptions[3])

        elif call.data == "rent4":
            send_two_photos(bot, call.message, "malish.jpg", "malish2.jpg", descriptions[4])

        elif call.data == "rent5":
            send_two_photos(bot, call.message, "DAGPropysk.jpg", "DAGPropysk2.jpg", descriptions[5])

        elif call.data == "rent6":
            bot.send_message(call.message.chat.id, descriptions[6])

        elif call.data == "vpn_ios":
            bot.answer_callback_query(call.id, "Ключ отправлен")
            bot.send_message(call.message.chat.id, KEY_STRING)

        elif call.data == "vpn_android":
            bot.answer_callback_query(call.id, "Ключ отправлен")
            bot.send_message(call.message.chat.id, KEY_STRING)



