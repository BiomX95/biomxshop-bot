import time
import datetime
from telebot import types
from config import CHAT_IDS, AUTOPOST_INTERVAL_SECONDS
from database.db import get_rental_accounts
from utils.helpers import format_time_left

# Порядок автопоста
AUTO_SEQUENCE = [
    "💎Алмазы",
    "⭐️Telegram stars",
    "🎁Особая посылка",
    "🎮Наш сайт",
    "RENT_ACCOUNTS" 
]

def make_fake_message(text: str, chat_id: int):
    json_msg = {
        "message_id": int(time.time()),
        "date": int(time.time()),
        "chat": {"id": chat_id, "type": "supergroup"},
        "from": {"id": 999999999, "is_bot": True, "first_name": "AutoPoster"},
        "text": text,
    }
    return types.Message.de_json(json_msg)

def send_accounts_status(bot, chat_id):
    """Отправка всех аккаунтов (как один этап рассылки)"""
    accounts = get_rental_accounts()
    for acc in accounts:
        acc_id, name, rent_until = acc
        time_left = format_time_left(rent_until)
        status_icon = "🔴" if time_left else "🟢"
        status_text = f"СТАТУС: {status_icon} " + ("ЗАНЯТ" if time_left else "СВОБОДЕН")
        
        caption = (f"🔑 <b>{name}</b>\n" f"{status_text}\n")
        if time_left:
            caption += f"⏳ Освободится через: {time_left}\n"
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="🚀 Арендовать", url=f"https://t.me/{(bot.get_me().username)}?start=rent"))

        try:
            bot.send_message(chat_id, caption, parse_mode="HTML", reply_markup=keyboard)
            time.sleep(2) # Небольшая пауза между аккаунтами внутри одного блока
        except Exception as e:
            print(f"Ошибка при отправке аккаунта {name}: {e}")

def auto_posting_sync(bot):
    print(f"[{datetime.datetime.now()}] Autopost запущен. Пауза между постами: {AUTOPOST_INTERVAL_SECONDS}с")

    while True:
        for item in AUTO_SEQUENCE:
            for chat_id in CHAT_IDS:
                try:
                    if item == "RENT_ACCOUNTS":
                        print(f"[{datetime.datetime.now()}] Постим аккаунты в {chat_id}")
                        send_accounts_status(bot, chat_id)
                    else:
                        print(f"[{datetime.datetime.now()}] Постим {item} в {chat_id}")
                        fake_msg = make_fake_message(item, chat_id)
                        bot.process_new_messages([fake_msg])

                except Exception as e:
                    print(f"[AUTOPOST ERROR] {e}")

            # --- ВОТ ТУТ ТЕПЕРЬ ТАЙМЕР ---
            # Бот отправил ОДИН пункт из списка во ВСЕ чаты и засыпает на 370 сек
            print(f"[{datetime.datetime.now()}] Жду {AUTOPOST_INTERVAL_SECONDS} сек перед следующим постом...")
            time.sleep(int(AUTOPOST_INTERVAL_SECONDS))