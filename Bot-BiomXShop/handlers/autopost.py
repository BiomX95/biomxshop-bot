import time
from telebot import types
from config import CHAT_IDS, AUTOPOST_INTERVAL_SECONDS
from database.db import get_rental_accounts
from handlers.rent import check_account_status # Импортируем функцию показа статуса
from utils.helpers import format_time_left

# Порядок автопоста (убираем лишние "текстовые" аккаунты, будем брать их из БД)
AUTO_SEQUENCE = [
    "💎Алмазы",
    "⭐️Telegram stars",
    "🎁Особая посылка",
    "🎮Наш сайт",
    "RENT_ACCOUNTS" # Метка для вставки всех аккаунтов из базы
]

def make_fake_message(text: str, chat_id: int):
    json_msg = {
        "message_id": int(time.time()),
        "date": int(time.time()),
        "chat": {"id": chat_id, "type": "supergroup"}, # Указываем тип группы
        "from": {"id": 999999999, "is_bot": True, "first_name": "AutoPoster"},
        "text": text,
    }
    return types.Message.de_json(json_msg)

def send_accounts_status(bot, chat_id):
    """
    Получает все аккаунты из базы и отправляет их в чат
    с кнопкой быстрой установки времени для админа.
    """
    accounts = get_rental_accounts()
    for acc in accounts:
        acc_id, name, rent_until = acc
        time_left = format_time_left(rent_until)
        
        status_icon = "🔴" if time_left else "🟢"
        status_text = f"СТАТУС: {status_icon} " + ("ЗАНЯТ" if time_left else "СВОБОДЕН")
        
        caption = (f"🔑 <b>{name}</b>\n"
                   f"{status_text}\n")
        
        if time_left:
            caption += f"⏳ Освободится через: {time_left}\n"
        
        # Создаем кнопку для админа (как вы просили ранее)
        keyboard = types.InlineKeyboardMarkup()
        admin_btn = types.InlineKeyboardButton(
            text="⚙️ Установить время (Админ)", 
            callback_data=f"set_rent_admin_{acc_id}"
        )
        # Кнопка для пользователя (переход в бота)
        user_btn = types.InlineKeyboardButton(
            text="🚀 Арендовать", 
            url=f"https://t.me/{(bot.get_me().username)}?start=rent"
        )
        keyboard.add(admin_btn)
        keyboard.add(user_btn)

        try:
            # Отправляем пост
            bot.send_message(chat_id, caption, parse_mode="HTML", reply_markup=keyboard)
            time.sleep(1) # Небольшая пауза, чтобы не спамить слишком быстро
        except Exception as e:
            print(f"Ошибка при отправке аккаунта {name}: {e}")

def auto_posting_sync(bot):
    print("Autopost запущен...")
    while True:
        for item in AUTO_SEQUENCE:
            for chat_id in CHAT_IDS:
                try:
                    if item == "RENT_ACCOUNTS":
                        # Если дошли до метки аккаунтов — рассылаем все аккаунты из БД
                        send_accounts_status(bot, chat_id)
                    else:
                        # Обычные текстовые команды из меню (Алмазы, Сайт и т.д.)
                        fake_msg = make_fake_message(item, chat_id)
                        bot.process_new_messages([fake_msg])
                    
                    print(f"[AUTOPOST] Выполнено '{item}' в {chat_id}")
                except Exception as e:
                    print(f"[AUTOPOST ERROR] ({chat_id}): {e}")

            # Пауза между разными типами постов (чтобы не все сразу)
            time.sleep(5) 
            
        # Пауза перед следующим циклом рассылки всего списка
        time.sleep(AUTOPOST_INTERVAL_SECONDS)



