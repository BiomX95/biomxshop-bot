# handlers/roulette.py
import time
import threading
from datetime import datetime, timedelta
from pymongo import MongoClient
from telebot import types

# Настройки MongoDB: сначала пробуем взять из config (если есть), иначе берем локал-хост
try:
    from config import MONGODB_URI
except Exception:
    MONGODB_URI = None

MONGO_FALLBACK = "mongodb://localhost:27017/biomxshop"
MONGO_URI = MONGODB_URI or MONGO_FALLBACK

# Подключаемся к MongoDB
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client.get_database()  # если URI содержит БД, возьмёт её; иначе default
spins_col = db.get_collection("roulette_spins")

# Параметры рулетки
SECTORS = 6
# Призы (в порядке секторов 0..5)
PRIZES = [
    {
        "title": "Аккаунт с клоуном — 5 часов",
        "description": "Аккаунт с персонажем «Клоун», аренда 5 часов.",
        "meta": {"type": "account", "period_hours": 5}
    },
    {
        "title": "Женский аккаунт — 3 часа",
        "description": "Женский аккаунт для аренды на 3 часа.",
        "meta": {"type": "account", "period_hours": 3}
    },
    {
        "title": "Скидка на аренду 10%",
        "description": "Купон: 10% скидка на следующую аренду.",
        "meta": {"type": "coupon", "value_percent": 10}
    },
    {
        "title": "Скидка на аренду 30%",
        "description": "Купон: 30% скидка на следующую аренду.",
        "meta": {"type": "coupon", "value_percent": 30}
    },
    {
        "title": "Аккаунт с 2 пропуском — 1 час",
        "description": "Аккаунт с 2 пропуском на 1 час.",
        "meta": {"type": "account", "period_hours": 1, "passes": 2}
    },
    {
        "title": "ПРОИГРЫШ — попробуй в следующий раз :)",
        "description": "Упс! Не повезло — попробуйте завтра.",
        "meta": {"type": "lose"}
    }
]

# Визуальные фреймы для "анимации" (перечисляем имена/эмодзи для смены)
ANIMATION_FRAMES = [
    "🔵", "🟣", "🔴", "🟢", "🟡", "⚪️"
]

# Время анимации (сек)
ANIMATION_DURATION = 5.8
ANIMATION_INTERVAL = 0.25  # сек между кадрами

# Время блокировки между спинами (24 часа)
LOCK_SECONDS = 24 * 3600

# Вспомогательные функции
def can_spin_now(user_id):
    """Возвращает (allowed: bool, seconds_left: int)"""
    last = spins_col.find_one({"user_id": str(user_id)}, sort=[("created_at", -1)])
    if not last:
        return True, 0
    last_time = last.get("created_at")
    if not last_time:
        return True, 0
    next_allowed = last_time + timedelta(seconds=LOCK_SECONDS)
    now = datetime.utcnow()
    if now >= next_allowed:
        return True, 0
    return False, int((next_allowed - now).total_seconds())

def record_spin(user_id, prize_index):
    doc = {
        "user_id": str(user_id),
        "prize_index": int(prize_index),
        "prize_title": PRIZES[prize_index]["title"],
        "created_at": datetime.utcnow()
    }
    spins_col.insert_one(doc)

def pick_random_prize():
    # Простейший равновероятный выбор; можно заменить на веса
    import random
    return random.randrange(0, len(PRIZES))

# Основная регистрация
def register_handlers(bot, is_private=False):
    """
    register_handlers(bot, is_private=False)
    Подключается к боту. is_private необязателен, мы вручную проверяем message.chat.type.
    """

    # Кнопка меню "Игры" — открывает клавиатуру с рулеткой
    @bot.message_handler(func=lambda m: m.chat.type == "private" and m.text == "🎮Игры")
    def games_menu(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton("🎰Рулетка")
        markup.add(btn)
        bot.send_message(message.chat.id, "Выберите игру:", reply_markup=markup)

    # Команда /roulette и кнопка "🎰Рулетка"
    @bot.message_handler(func=lambda m: m.chat.type == "private" and (m.text == "/roulette" or m.text == "🎰Рулетка"))
    def roulette_start(message):
        user_id = message.from_user.id

        allowed, seconds_left = can_spin_now(user_id)
        if not allowed:
            # Покажем таймер
            hours = seconds_left // 3600
            minutes = (seconds_left % 3600) // 60
            seconds = seconds_left % 60
            bot.send_message(message.chat.id, f"⏳ Подождите {hours}ч {minutes}м {seconds}с до следующего прокрута.")
            return

        # Создаём сообщение-ломтик которое будем редактировать для анимации
        sent = bot.send_message(message.chat.id, "🎰 Подготовка рулетки...")

        # Запускаем анимацию в отдельном потоке, чтобы не блокировать обработчики
        def _animate_and_spin():
            start = time.time()
            elapsed = 0.0
            frame_index = 0

            # Скорость смены кадров (можно постепенно замедлять, оставлено простым)
            while elapsed < ANIMATION_DURATION:
                frame = ANIMATION_FRAMES[frame_index % len(ANIMATION_FRAMES)]
                # Формируем визуализацию сектора: прокручиваем названия призов по кругу
                display = []
                for i in range(SECTORS):
                    idx = (frame_index + i) % SECTORS
                    title = PRIZES[idx]["title"]
                    # усечь длинные заголовки ради компактности
                    short = title if len(title) <= 20 else title[:18] + "…"
                    display.append(f"{frame} {short}")
                text = "🎰 Кручение...\n\n" + "\n".join(display)
                try:
                    bot.edit_message_text(text, message.chat.id, sent.message_id)
                except Exception:
                    # игнорируем ошибки редактирования (например, timeout)
                    pass

                time.sleep(ANIMATION_INTERVAL)
                frame_index += 1
                elapsed = time.time() - start

            # После анимации — выбираем приз
            prize_idx = pick_random_prize()
            prize = PRIZES[prize_idx]

            # Регистрируем спин в БД
            try:
                record_spin(user_id, prize_idx)
            except Exception as e:
                # логируем, но не мешаем пользователю
                print("Ошибка записи спина:", e)

            # Финальное сообщение с результатом
            final_text = f"🏆 <b>Выпало:</b> {prize['title']}\n\n{prize['description']}"
            try:
                bot.edit_message_text(final_text, message.chat.id, sent.message_id, parse_mode="HTML")
            except Exception:
                # если не удалось редактировать — отправим новое сообщение
                bot.send_message(message.chat.id, final_text, parse_mode="HTML")

            # Дополнительно: можно отправить приватные данные (логин/пароль) через отдельное сообщение
            # если prize.meta содержит account info, отправим его приватно
            meta = prize.get("meta", {})
            if meta.get("type") == "account":
                # пример: отправка заметки с meta (если есть)
                info_lines = []
                if meta.get("period_hours"):
                    info_lines.append(f"⏱ Срок аренды: {meta['period_hours']} часов")
                if meta.get("passes"):
                    info_lines.append(f"🎫 Пропусков: {meta['passes']}")
                # Если ты хочешь хранить реальные логин/пароль, положи их в meta и отправь здесь
                # e.g. meta['login'], meta['password']
                if meta.get("login"):
                    info_lines.append(f"Логин: {meta['login']}")
                if meta.get("password"):
                    info_lines.append(f"Пароль: {meta['password']}")

                if info_lines:
                    bot.send_message(message.chat.id, "🔐 Данные приза:\n" + "\n".join(info_lines))

        threading.Thread(target=_animate_and_spin, daemon=True).start()

    # Админ: посмотреть историю последних спинов пользователя (команда /my_spins)
    @bot.message_handler(func=lambda m: m.chat.type == "private" and m.text == "/my_spins")
    def my_spins(message):
        user_id = str(message.from_user.id)
        docs = spins_col.find({"user_id": user_id}).sort("created_at", -1).limit(20)
        out = []
        for d in docs:
            t = d.get("created_at")
            title = d.get("prize_title", "—")
            out.append(f"{t.strftime('%Y-%m-%d %H:%M:%S')} — {title}")
        if not out:
            bot.send_message(message.chat.id, "История спинов пуста.")
        else:
            bot.send_message(message.chat.id, "История спинов:\n" + "\n".join(out))


