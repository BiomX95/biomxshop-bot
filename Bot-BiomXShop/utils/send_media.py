from telebot import types

def send_two_photos(bot, message, photo1, photo2, caption):
    media = [
        types.InputMediaPhoto(open(photo1, "rb")),
        types.InputMediaPhoto(open(photo2, "rb"), caption=caption, parse_mode="HTML")
    ]
    bot.send_media_group(message.chat.id, media)
