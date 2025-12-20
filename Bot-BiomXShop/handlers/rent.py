import os
from telebot import types
from database.db import get_rental_account, set_rent_time
from utils.helpers import format_time_left
from texts.rent_texts import descriptions  # Твои описания
from config import RENT_IMG, ADMIN_IDS  # Пути к фото и ID админов

# Словарь соответствия ID аккаунта и его скриншотов
ACCOUNT_IMAGES = {
    1: ["Abakaev.jpg", "Abakaev2.jpg"],
    2: ["KARINA.jpg", "KARINAevo.jpg"],
    3: ["BiomXShop.jpg", "BiomXShop2.jpg"],
    4: ["malish.jpg", "malish2.jpg"],
    5: ["DAGPropysk.jpg", "DAGPropysk22.jpg"],
    6: ["Malikak.jpg", "Malikak2.jpg"],
    7: ["yasmi.jpg", "yasmi2.jpg"],
    8: ["Dashaakk.jpg", "Dashaakk2.jpg"],
    9: ["ivan1.jpg", "ivan2.jpg"],
    10: ["ivan3.jpg", "ivan4.jpg"],
    11: ["ivan5.jpg", "ivan6.jpg"]
}

# --- Всплывающее окно статуса ---
def quick_status_check(call, bot):
    try:
        acc_id = int(call.data.split('_')[2])
    except: return
        
    account = get_rental_account(acc_id)
    if not account:
        bot.answer_callback_query(call.id, "Аккаунт не найден!", show_alert=True)
        return

    _, name, rent_until = account
    time_left = format_time_left(rent_until)
    
    status = f"🔴 ЗАНЯТ (еще {time_left})" if time_left else "🟢 СВОБОДЕН"
    text = f"📊 Аккаунт: {name}\nСтатус: {status}"
    bot.answer_callback_query(call.id, text=text, show_alert=True)

# --- ГЛАВНАЯ ФУНКЦИЯ: ВЫДАЧА СКРИНОВ И ОПИСАНИЯ ---
def check_account_status(call, bot):
    try:
        acc_id = int(call.data.split("_")[2])
    except: return

    account = get_rental_account(acc_id)
    if not account:
        bot.answer_callback_query(call.id, "Аккаунт не найден!")
        return

    _, name, rent_until = account
    time_left = format_time_left(rent_until)
    
    # Берем красивый текст из descriptions.py
    base_text = descriptions.get(acc_id, f"<b>Аккаунт №{acc_id}</b>")
    status_icon = "🔴 ЗАНЯТ" if time_left else "🟢 СВОБОДЕН"
    status_info = f"\n\n📊 <b>СТАТУС: {status_icon}</b>"
    if time_left:
        status_info += f"\n⏳ Освободится через: <code>{time_left}</code>"
    
    full_caption = base_text + status_info

    # Клавиатура (БЕЗ КНОПКИ АРЕНДОВАТЬ)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(text="🔄 Проверить статус", callback_data=f"quick_status_{acc_id}")
    )
    
    # Если нажал админ, добавляем кнопку управления временем
    if call.from_user.id in ADMIN_IDS:
        keyboard.add(types.InlineKeyboardButton(text="⚙️ Установить аренду", callback_data=f"set_rent_admin_{acc_id}"))

    # Получаем список фото для этого ID
    photo_filenames = ACCOUNT_IMAGES.get(acc_id, [])

    try:
        # Удаляем старое сообщение с кнопками (меню выбора)
        bot.delete_message(call.message.chat.id, call.message.message_id)

        if photo_filenames:
            media = []
            for i, filename in enumerate(photo_filenames):
                path = os.path.join(RENT_IMG, filename)
                if os.path.exists(path):
                    with open(path, 'rb') as f:
                        if i == 0:
                            media.append(types.InputMediaPhoto(f.read(), caption=full_caption, parse_mode="HTML"))
                        else:
                            media.append(types.InputMediaPhoto(f.read()))
            
            if media:
                bot.send_media_group(call.message.chat.id, media)
                bot.send_message(call.message.chat.id, "<b>Управление аккаунтом:</b>", reply_markup=keyboard, parse_mode="HTML")
            else:
                bot.send_message(call.message.chat.id, full_caption, parse_mode="HTML", reply_markup=keyboard)
        else:
            bot.send_message(call.message.chat.id, full_caption, parse_mode="HTML", reply_markup=keyboard)
            
    except Exception as e:
        print(f"Ошибка выдачи: {e}")
        bot.send_message(call.message.chat.id, full_caption, parse_mode="HTML", reply_markup=keyboard)

# --- АДМИНСКАЯ ЛОГИКА ---
def admin_set_rent_from_post(call, bot):
    acc_id = int(call.data.split('_')[3]) 
    msg = bot.send_message(call.message.chat.id, f"⏳ Введите время в минутах для аккаунта №{acc_id}:")
    bot.register_next_step_handler(msg, lambda m: process_rent_time_input(m, acc_id, bot))

def process_rent_time_input(message, acc_id, bot):
    try:
        minutes = int(message.text)
        set_rent_time(acc_id, minutes)
        bot.send_message(message.chat.id, f"✅ Для аккаунта №{acc_id} время успешно установлено!")
    except:
        bot.send_message(message.chat.id, "❌ Ошибка! Введите число.")

# --- РЕГИСТРАЦИЯ ---
def register_handlers(bot):
    bot.register_callback_query_handler(lambda call: check_account_status(call, bot), 
                                        func=lambda call: call.data.startswith("user_rent_"))
    
    bot.register_callback_query_handler(lambda call: quick_status_check(call, bot), 
                                        func=lambda call: call.data.startswith("quick_status_"))
    
    bot.register_callback_query_handler(lambda call: admin_set_rent_from_post(call, bot), 
                                        func=lambda call: call.data.startswith("set_rent_admin_"))