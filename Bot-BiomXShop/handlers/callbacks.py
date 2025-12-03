import os
from utils.send_media import send_two_photos
from config import RENT_IMG
from texts.rent_texts import descriptions

def register_handlers(bot, is_private=False):

    @bot.callback_query_handler(func=lambda call: call.message and call.message.chat.type == "private")
    def callback(call):

        # Вспомогательная функция для корректного формирования пути и проверки файла
        def rent_path(filename):
            path = os.path.join(RENT_IMG, filename)
            if not os.path.exists(path):
                print(f"Файл не найден: {path}")
                return None
            return path

        # RENTS
        if call.data == "rent1":
            file1 = rent_path("Abakaev.jpg")
            file2 = rent_path("Abakaev.jpg")
            if file1 and file2:
                send_two_photos(bot, call.message, file1, file2, descriptions[1])
            else:
                bot.send_message(call.message.chat.id, "Извините, фото временно недоступны.")

        elif call.data == "rent2":
            file1 = rent_path("KARINA.jpg")
            file2 = rent_path("KARINAevo.jpg")
            if file1 and file2:
                send_two_photos(bot, call.message, file1, file2, descriptions[2])
            else:
                bot.send_message(call.message.chat.id, "Извините, фото временно недоступны.")

        elif call.data == "rent3":
            file1 = rent_path("BiomXShop.jpg")
            file2 = rent_path("BiomXShop2.jpg")
            if file1 and file2:
                send_two_photos(bot, call.message, file1, file2, descriptions[3])
            else:
                bot.send_message(call.message.chat.id, "Извините, фото временно недоступны.")

        elif call.data == "rent4":
            file1 = rent_path("malish.jpg")
            file2 = rent_path("malish2.jpg")
            if file1 and file2:
                send_two_photos(bot, call.message, file1, file2, descriptions[4])
            else:
                bot.send_message(call.message.chat.id, "Извините, фото временно недоступны.")

        elif call.data == "rent5":
            file1 = rent_path("DAGPropysk.jpg")
            file2 = rent_path("DAGPropysk2.jpg")
            if file1 and file2:
                send_two_photos(bot, call.message, file1, file2, descriptions[5])
            else:
                bot.send_message(call.message.chat.id, "Извините, фото временно недоступны.")

        elif call.data == "rent6":
            file1 = rent_path("yasmi.jpg")
            file2 = rent_path("yasmi.jpg")
            if file1 and file2:
                send_two_photos(bot, call.message, file1, file2, descriptions[6])
            else:
                bot.send_message(call.message.chat.id, "Извините, фото временно недоступны.")

        elif call.data == "rent7":
            file1 = rent_path("tyrpalpropusk.jpg")
            file2 = rent_path("tyrpalpropusk.jpg")
            if file1 and file2:
                send_two_photos(bot, call.message, file1, file2, descriptions[7])
            else:
                bot.send_message(call.message.chat.id, "Извините, фото временно недоступны.")

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





