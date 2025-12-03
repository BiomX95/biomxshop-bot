# handlers/wheel.py
import json, os, random, time
from telebot import types

FILE_PATH = "wheel_data.json"

PRIZE_CODES = {
    1: "CODE-CLOWN-XXX",
    2: "CODE-GIRL-XXX",
    3: "CODE-DISC10-XXX",
    4: "CODE-DISC30-XXX",
    5: "CODE-PROPUSK1H-XXX"
}

PRIZES = {
    1: "🎭 Аккаунт с клоуном (5 часов)",
    2: "👩 Аккаунт женский (3 часа)",
    3: "💸 Скидка на аренду 10%",
    4: "💎 Скидка на аренду 30%",
    5: "🔥 Аккаунт с 2 пропуском (1 час)",
    6: "❌ Проигрыш! Попробуй в следующий раз."
}

def load_data():
    if not os.path.exists(FILE_PATH):
        return {}
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def can_spin(user_id):
    data = load_data()
    if str(user_id) not in data:
        return True, 0
    last_spin = data[str(user_id)]
    now = time.time()
    diff = now - last_spin
    if diff >= 86400:
        return True, 0
    else:
        return False, int(86400 - diff)

def start_wheel(bot, message):
    can, wait_time = can_spin(message.from_user.id)
    if not can:
        hours = wait_time // 3600
        minutes = (wait_time % 3600) // 60
        bot.send_message(message.chat.id, f"Ты уже крутил рулетку! Следующая попытка через {hours} ч {minutes} мин.")
        return

    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🎰 Крутить рулетку", callback_data="spin_wheel")
    markup.add(btn)
    bot.send_message(message.chat.id, "Готов? Жми кнопку и крути рулетку!", reply_markup=markup)

def register_callbacks(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "spin_wheel")
    def spin(call):
        user_id = call.from_user.id
        prize_num = random.randint(1, 6)
        prize_text = PRIZES[prize_num]

        data = load_data()
        data[str(user_id)] = time.time()
        save_data(data)

        bot.answer_callback_query(call.id)
        bot.edit_message_text("🎡 Крутится...", call.message.chat.id, call.message.message_id)
        time.sleep(2)

        if prize_num == 6:
            bot.send_message(call.message.chat.id, prize_text)
        else:
            code = PRIZE_CODES[prize_num]
            bot.send_message(call.message.chat.id, f"Поздравляем! Ты выиграл:\n\n{prize_text}\n\nТвой код:\n{code}")

