from telebot import types

def send_two_photos(bot, message, path1, path2, caption):
    media = [
        types.InputMediaPhoto(open(path1, "rb")),
        types.InputMediaPhoto(open(path2, "rb"))
    ]

    bot.send_media_group(message.chat.id, media)
    bot.send_message(message.chat.id, caption)
