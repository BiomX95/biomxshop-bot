# keyboards/rent_menu.py
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import get_rental_accounts
from utils.helpers import format_time_left

def get_accounts_keyboard(is_admin=False):
    """
    Генерирует клавиатуру со списком аккаунтов. 
    Каждая строка содержит кнопку деталей/аренды и кнопку быстрого статуса.
    """
    markup = InlineKeyboardMarkup() 
    accounts = get_rental_accounts()
    
    prefix = "admin_rent_" if is_admin else "user_rent_"
    
    for acc in accounts:
        acc_id, name, rent_until = acc
        time_str = format_time_left(rent_until)
        
        # 1. Кнопка для АРЕНДЫ / ПРОСМОТРА ДЕТАЛЕЙ (левая кнопка)
        rent_details_button = InlineKeyboardButton(
            text=f"🔑 {name}", 
            callback_data=f"{prefix}{acc_id}"
        )
        
        # 2. Кнопка для БЫСТРОЙ ПРОВЕРКИ СТАТУСА (правая кнопка, всплывающее окно)
        status_icon = "🔴 Занят" if time_str else "🟢 Свободен"
        quick_status_button = InlineKeyboardButton(
            text=f"🏠 {status_icon}", 
            callback_data=f"quick_status_{acc_id}" 
        )
        
        # Добавляем обе кнопки в одну строку
        markup.row(rent_details_button, quick_status_button)
    
    markup.add(InlineKeyboardButton("🔙 Назад", callback_data="main_menu"))
    return markup

# Кнопка обновления для пользователя (используется на странице деталей аккаунта)
def get_refresh_keyboard(account_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔄 Обновить статус", callback_data=f"user_rent_{account_id}"))
    markup.add(InlineKeyboardButton("🔙 К списку", callback_data="open_rent_menu"))
    return markup

# --- НОВАЯ ФУНКЦИЯ КЛАВИАТУРЫ ДЛЯ ПОСТА ---
def get_post_status_markup(account_id: int, is_admin: bool = False):
    """
    Клавиатура, которая прикрепляется к посту с описанием аккаунта.
    Включает "Проверить статус" (для всех) и "Установить статус" (для админа).
    """
    markup = InlineKeyboardMarkup()
    
    # Кнопка 1: Проверить статус (для всех пользователей)
    status_button = InlineKeyboardButton(
        "🏠 Проверить статус", 
        callback_data=f"quick_status_{account_id}"
    )
    
    # Кнопка 2: Установить статус (только для админа)
    if is_admin:
        set_rent_button = InlineKeyboardButton(
            "🔧 Установить аренду (ADMIN)", 
            callback_data=f"set_rent_admin_{account_id}"
        )
        # Если админ, ставим обе кнопки в одну строку
        markup.row(status_button, set_rent_button)
    else:
        # Если не админ, только кнопка статуса
        markup.add(status_button)
        
    return markup
