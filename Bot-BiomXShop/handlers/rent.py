# handlers/rent.py

from telebot import types
from database.db import get_rental_account, set_rent_time
from keyboards.rent_menu import get_accounts_keyboard, get_refresh_keyboard
from utils.helpers import format_time_left
from config import ADMIN_ID

# --- ЧАСТЬ ПОЛЬЗОВАТЕЛЯ: Проверка статуса (Всплывающее окно) ---

def quick_status_check(call, bot):
    try:
        # ! ИСПРАВЛЕНО: Принудительное преобразование в int
        acc_id = int(call.data.split('_')[2])
    except:
        bot.answer_callback_query(call.id, "Ошибка ID аккаунта.", show_alert=True)
        return
        
    account = get_rental_account(acc_id)
    
    if not account:
        bot.answer_callback_query(call.id, "Аккаунт не найден!", show_alert=True)
        return

    _, name, rent_until = account
    time_left = format_time_left(rent_until)
    
    if time_left:
        text = (f"🔒 Аккаунт: {name}\n"
                f"Статус: ЗАНЯТ 🔴\n"
                f"Освободится через: {time_left}")
    else:
        text = (f"🔓 Аккаунт: {name}\n"
                f"Статус: СВОБОДЕН 🟢\n"
                f"Можно арендовать прямо сейчас!")

    bot.answer_callback_query(
        callback_query_id=call.id,
        text=text,
        show_alert=True
    )

# --- ЧАСТЬ ПОЛЬЗОВАТЕЛЯ: Страница деталей (Обновление сообщения) ---

def show_rent_menu(call, bot):
    bot.edit_message_caption( 
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption="📂 <b>Доступные аккаунты для аренды:</b>\nВыберите аккаунт или проверьте его статус.",
        parse_mode="HTML",
        reply_markup=get_accounts_keyboard(is_admin=False)
    )

def check_account_status(call, bot):
    # ! ИСПРАВЛЕНО: Принудительное преобразование в int
    acc_id = int(call.data.split("_")[2])
    account = get_rental_account(acc_id)
    
    if not account:
        bot.answer_callback_query(call.id, "Аккаунт не найден!")
        return

    _, name, rent_until = account
    time_left = format_time_left(rent_until)
    
    if time_left:
        text = (f"🔒 <b>Аккаунт: {name}</b>\n\n"
                f"Статус: 🔴 <b>ЗАНЯТ</b>\n"
                f"Освободится через: <code>{time_left}</code>")
    else:
        text = (f"🔓 <b>Аккаунт: {name}</b>\n\n"
                f"Статус: 🟢 <b>СВОБОДЕН</b>\n"
                f"Вы можете арендовать его прямо сейчас!")
    
    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=text,
        parse_mode="HTML",
        reply_markup=get_refresh_keyboard(acc_id)
    )

# --- ЧАСТЬ АДМИНА (/admin_rent) ---

def admin_rent_panel(message, bot):
    bot.send_message(
        message.chat.id, 
        "🔧 <b>Управление арендой</b>\nВыберите аккаунт, чтобы установить время аренды:", 
        parse_mode="HTML",
        reply_markup=get_accounts_keyboard(is_admin=True)
    )
