# handlers/wheel.py
import json
import os
import random
import time
import threading
from telebot import types

# Файл для хранения последних прокрутов пользователей
FILE_PATH = "wheel_data.json"

# Заглушки кодов для призов 1–5
PRIZE_CODES = {
    1: "CODE-CLOWN-XXX",
    2: "CODE-GIRL-XXX",
    3: "CODE-DISC10-XXX",
    4: "CODE-DISC30-XXX",
    5: "CODE-PROPUSK1H-XXX"
}

# Призы рулетки
PRIZES = {
    1: "🎭 Скидка на аренду 5%",
    2: "👩 Скидка на женский аккаунт 50%",
    3: "💸 Скидка на аренду 10%",
    4: "💎 Скидка на аренду 30%",
    5: "🔥 Скидка на аккаунт BiomX.Shop c 2 пропуском 20%",
    6: "❌ Проигрыш! Попробуй в следующий раз."
}

# --- Вспомогательные функции ---
def load_data():
    """Загрузка JSON с последними прокрутами"""
    if not os.path.exists(FILE_PATH):
        return {}
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    """Сохранение JSON"""
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def can_spin(user_id):
    """Проверка, прошли ли 24 часа с последнего прокрута"""
    data = load_data()
    if str(user_id) not in data:
        return True, 0
    last_spin = data[str(user_id)]
    now = time.time()
    diff = now - last_spin
    if diff >= 86400:  # 24 часа
        return True, 0
    else:
        return False, int(86400 - diff)

# --- Основные хендлеры ---
def register_handlers(bot):
    """Регистрирует кнопки рулетки и спины"""

    # Кнопка меню "🎡 Рулетка"
    @bot.message_handler(func=lambda m: m.chat.type == "private" and m.text == "🎡 Рулетка")
    def start_wheel(message):
        user_id = message.from_user.id
        can, wait_time = can_spin(user_id)

        if not can:
            hours = wait_time // 3600
            minutes = (wait_time % 3600) // 60
            bot.send_message(
                message.chat.id,
                f"⏳ Ты уже крутил рулетку! Следующая попытка через {hours} ч {minutes} мин."
            )
            return

        # Создаем кнопку "Крутить рулетку"
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("🎰 Крутить рулетку", callback_data="spin_wheel")
        markup.add(btn)

        bot.send_message(
            message.chat.id,
            "Готов? Жми кнопку и крути рулетку!",
            reply_markup=markup
        )

    # Обработчик нажатия кнопки "Крутить рулетку"
    @bot.callback_query_handler(func=lambda call: call.data == "spin_wheel")
    def spin(call):

        def _spin_thread():
            user_id = call.from_user.id

            # Случайный приз
            prize_num = random.randint(1, 6)
            prize_text = PRIZES[prize_num]

            # Сохраняем время прокрута
            data = load_data()
            data[str(user_id)] = time.time()
            save_data(data)

            # Ответ на нажатие кнопки
            bot.answer_callback_query(call.id, "Крутим рулетку...")
            bot.edit_message_text("🎡 Крутится...", call.message.chat.id, call.message.message_id)

            # Имитация кручения
            time.sleep(2)

            # Сообщение с результатом
            if prize_num == 6:
                bot.send_message(call.message.chat.id, prize_text)
            else:
                code = PRIZE_CODES[prize_num]
                bot.send_message(
                    call.message.chat.id,
                    f"🎉 Поздравляем! Ты выиграл:\n\n{prize_text}\n\nТвой код:\n{code}\n\nЧтобы получить приз отправь это сообщение мне:@BiomXShop_Support"
                )

        threading.Thread(target=_spin_thread, daemon=True).start()
