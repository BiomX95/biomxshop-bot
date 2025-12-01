import os
from telebot import types
from config import RENT_IMG

def send_two_photos(bot, message, photo1, photo2, caption):
    # photo1 и photo2 — просто имена файлов
    path1 = os.path.join(RENT_IMG, photo1)
    path2 = os.path.join(RENT_IMG, photo2)

    media = [
        types.InputMediaPhoto(open(path1, "rb")),
        types.InputMediaPhoto(open(path2, "rb"), caption=caption, parse_mode="HTML")
    ]

    bot.send_media_group(message.chat.id, media)
