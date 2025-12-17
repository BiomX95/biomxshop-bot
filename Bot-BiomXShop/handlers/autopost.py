import time
from telebot import types
from config import CHAT_IDS, AUTOPOST_INTERVAL_SECONDS

# Порядок автопоста
AUTO_SEQUENCE = [
    "💎Алмазы",
    "⭐️Telegram stars",
    "🎁Особая посылка",
    "АККАУНТ №2🚺",
    "АККАУНТ №1🚹",
    "АККАУНТ №2🚹",
    "АККАУНТ №3🚹",
    "АККАУНТ №4🚹",
    "АККАУНТ №5🚹",
    "АККАУНТ №6🚹",
    "АККАУНТ №7🚹",
    "АККАУНТ №8🚺",
    "АККАУНТ №9🚹",
    "АККАУНТ №10🚹",
    "АККАУНТ №11🚹",
    "АККАУНТ №12🚹",
    "🎮Наш сайт",
]


def make_fake_message(text: str, chat_id: int):
    """
    Создает корректный Message для конкретного chat_id.
    """
    json_msg = {
        "message_id": int(time.time()),
        "date": int(time.time()),
        "chat": {
            "id": chat_id,
            "type": "private"
        },
        "from": {
            "id": 999999999,
            "is_bot": True,
            "first_name": "AutoPoster"
        },
        "text": text,
    }

    return types.Message.de_json(json_msg)


def auto_posting_sync(bot):
    print("Autopost запущен...")
    while True:
        for text in AUTO_SEQUENCE:
            for chat_id in CHAT_IDS:
                try:
                    fake_msg = make_fake_message(text, chat_id)
                    bot.process_new_messages([fake_msg])
                    print(f"[AUTOPOST] Отправлено '{text}' в {chat_id}")
                except Exception as e:
                    print(f"[AUTOPOST ERROR] ({chat_id}): {e}")

            time.sleep(AUTOPOST_INTERVAL_SECONDS)



