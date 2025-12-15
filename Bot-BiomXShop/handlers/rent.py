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
             online = (f"Статус: СВОБОДЕН 🟢)\n"
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

def admin_select_account(call, bot):
    # Проверка на АДМИНА
    if call.from_user.id != int(ADMIN_ID): 
        bot.answer_callback_query(call.id, "Доступ запрещен.")
        return
    
    # ! ИСПРАВЛЕНО: Принудительное преобразование в int
    acc_id = int(call.data.split("_")[2])
    
    bot.answer_callback_query(call.id, f"Ожидаю ввод времени для аккаунта ID {acc_id}.", show_alert=False)
    
    msg = bot.send_message(
        call.message.chat.id, 
        f"⏳ Для аккаунта ID {acc_id}, введите время аренды в <b>минутах</b> (только число).\nНапример: <code>120</code> для 2 часов. \n\n*Для ОСВОБОЖДЕНИЯ введите <code>0</code>*", 
        parse_mode="HTML"
    )
    bot.register_next_step_handler(msg, lambda m: process_rent_time_input(m, acc_id, bot)) 
    
def process_rent_time_input(message, acc_id, bot):
    try:
        minutes = int(message.text)
        
        if minutes <= 0:
            set_rent_time(acc_id, 0)
            bot.send_message(message.chat.id, f"✅ Аккаунт ID {acc_id} успешно ОСВОБОЖДЕН.")
        else:
            set_rent_time(acc_id, minutes)
            bot.send_message(message.chat.id, f"✅ Таймер установлен на {minutes} мин.")
        
        admin_rent_panel(message, bot)
        
    except ValueError:
        bot.send_message(message.chat.id, "❌ Ошибка! Нужно ввести целое число (минуты).")

        
# --- ЛОГИКА ДЛЯ УСТАНОВКИ СТАТУСА С ПОСТА (set_rent_admin_ID) ---

def admin_set_rent_from_post(call, bot):
    bot.answer_callback_query(call.id, text="Начало установки времени...") 
    
    if call.from_user.id != int(ADMIN_ID):
        bot.send_message(call.message.chat.id, "🚫 Доступ запрещен. Вы не администратор.")
        return
        
    try:
        # ! ИСПРАВЛЕНО: Принудительное преобразование в int
        acc_id = int(call.data.split('_')[3]) 
    except Exception as e:
        error_msg = f"❌ Ошибка ID аккаунта. Колбэк: {call.data}. Ошибка: {e}" 
        bot.send_message(call.message.chat.id, error_msg)
        return

    msg = bot.send_message(
        call.message.chat.id, 
        f"⏳ Для аккаунта ID {acc_id}, введите время аренды в <b>минутах</b> (только число).\n\n*Для ОСВОБОЖДЕНИЯ введите <code>0</code>*", 
        parse_mode="HTML"
    )
    
    bot.register_next_step_handler(msg, lambda m: process_rent_time_input_from_post(m, acc_id, bot))

def process_rent_time_input_from_post(message, acc_id, bot):
    try:
        minutes = int(message.text)
        
        if minutes <= 0:
            set_rent_time(acc_id, 0)
            bot.send_message(message.chat.id, f"✅ Аккаунт ID {acc_id} успешно ОСВОБОЖДЕН.")
        else:
            set_rent_time(acc_id, minutes)
            bot.send_message(message.chat.id, f"✅ Таймер для аккаунта ID {acc_id} установлен на {minutes} мин.")
            
    except ValueError:
        bot.send_message(message.chat.id, "❌ Ошибка! Нужно ввести целое число (минуты).")


# ----------------------------------------------
# ФУНКЦИЯ РЕГИСТРАЦИИ
# ---------------------------------------------- 

def register_handlers(bot):
    # Регистрируем хендлеры сообщений (например, /admin_rent)
    bot.register_message_handler(lambda m: admin_rent_panel(m, bot), 
                                 commands=['admin_rent'], 
                                 func=lambda message: message.from_user.id == int(ADMIN_ID), 
                                 pass_bot=False)
    
    # Регистрируем хендлеры колбэков
    bot.register_callback_query_handler(lambda call: show_rent_menu(call, bot), 
                                        func=lambda call: call.data == "open_rent_menu", 
                                        pass_bot=False)
    
    bot.register_callback_query_handler(lambda call: check_account_status(call, bot),
                                        func=lambda call: call.data.startswith("user_rent_"), 
                                        pass_bot=False)
    
    bot.register_callback_query_handler(lambda call: admin_select_account(call, bot), 
                                        func=lambda call: call.data.startswith("admin_rent_"), 
                                        pass_bot=False)
                                        
    bot.register_callback_query_handler(lambda call: quick_status_check(call, bot), 
                                        func=lambda call: call.data.startswith("quick_status_"), 
                                        pass_bot=False)
                                        
    # --- РЕГИСТРАЦИЯ для установки статуса с поста (set_rent_admin_ID) ---
    bot.register_callback_query_handler(lambda call: admin_set_rent_from_post(call, bot), 
                                        func=lambda call: call.data.startswith("set_rent_admin_"), 
                                        pass_bot=False)
    # --------------------------------------------------------------------------
