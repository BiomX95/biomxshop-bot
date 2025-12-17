import time
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
    "RENT_ACCOUNTS" # Сюда бот сам вставит все аккаунты из базы
]

def make_fake_message(text: str, chat_id: int):
    """Создает имитацию сообщения для вызова старых функций меню"""
    json_msg = {
        "message_id": int(time.time()),
        "date": int(time.time()),
        "chat": {"id": chat_id, "type": "supergroup"},
        "from": {"id": 999999999, "is_bot": True, "first_name": "AutoPoster"},
        "text": text,
    }
    return types.Message.de_json(json_msg)

def send_accounts_status(bot, chat_id):
    """Рассылает актуальные карточки всех аккаунтов с кнопками"""
    accounts = get_rental_accounts()
    for acc in accounts:
        acc_id, name, rent_until = acc
        time_left = format_time_left(rent_until)
        
        status_icon = "🔴" if time_left else "🟢"
        status_text = "ЗАНЯТ" if time_left else "СВОБОДЕН"
        
        caption = (f"🔑 <b>{name}</b>\n"
                   f"Статус: {status_icon} <b>{status_text}</b>\n")
        
        if time_left:
            caption += f"⏳ Освободится через: <code>{time_left}</code>\n"
        
        keyboard = types.InlineKeyboardMarkup()
        # Кнопка для админов
        admin_btn = types.InlineKeyboardButton(
            text="⚙️ Установить время (Админ)", 
            callback_data=f"set_rent_admin_{acc_id}"
        )
        # Кнопка для клиентов (ссылка на личку бота)
        user_btn = types.InlineKeyboardButton(
            text="🚀 Арендовать в боте", 
            url=f"https://t.me/{(bot.get_me().username)}?start=rent"
        )
        keyboard.add(admin_btn)
        keyboard.add(user_btn)

        try:
            bot.send_message(chat_id, caption, parse_mode="HTML", reply_markup=keyboard)
            time.sleep(1.5) 
        except Exception as e:
            print(f"[SPAMMER ERROR] {name}: {e}")

def auto_posting_sync(bot):
    print("Autopost запущен...")
    while True:
        for item in AUTO_SEQUENCE:
            for chat_id in CHAT_IDS:
                try:
                    if item == "RENT_ACCOUNTS":
                        send_accounts_status(bot, chat_id)
                    else:
                        fake_msg = make_fake_message(item, chat_id)
                        bot.process_new_messages([fake_msg])
                    
                    print(f"[AUTOPOST] Отправлено: {item}")
                except Exception as e:
                    print(f"[AUTOPOST ERROR]: {e}")

        time.sleep(AUTOPOST_INTERVAL_SECONDS)
