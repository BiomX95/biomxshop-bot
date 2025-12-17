# database/db.py (ОБНОВЛЕННЫЙ ПОЛНЫЙ КОД)
import sqlite3
import time
from typing import List, Tuple, Optional

# Имя файла базы данных
DB_NAME = 'database.db'

# --- СПИСОК АККАУНТОВ ДЛЯ ДОБАВЛЕНИЯ ---
# Добавляйте сюда новые названия. При перезапуске бота они добавятся в базу.
ACCOUNTS_TO_CHECK = [
    "АККАУНТ №1🚹",
    "АККАУНТ №2🚺",
    "АККАУНТ №3🚹",
    "АККАУНТ №4🚹",
    "АККАУНТ №5🚹",
    "АККАУНТ №6🚹",
    "АККАУНТ №7🚹",
    "АККАУНТ №8🚺",
    "АККАУНТ №9🚹",  # <-- Новые аккаунты
    "АККАУНТ №10🚹" 
    "АККАУНТ №11🚹"# <-- Новые аккаунты
]
# ---------------------------------------

def create_tables():
    """Создает необходимые таблицы, если они не существуют."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Таблица аккаунтов для аренды
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rental_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rent_until REAL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def get_rental_accounts() -> List[Tuple[int, str, float]]:
    """Получает все аккаунты для аренды."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, rent_until FROM rental_accounts")
    accounts = cursor.fetchall()
    conn.close()
    return accounts

def get_rental_account(account_id: int) -> Optional[Tuple[int, str, float]]:
    """Получает конкретный аккаунт по ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, rent_until FROM rental_accounts WHERE id = ?", (account_id,))
    account = cursor.fetchone()
    conn.close()
    return account

def set_rent_time(account_id: int, minutes: int):
    """Устанавливает время окончания аренды."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Текущее время + минуты * 60 секунд
    finish_time = time.time() + (minutes * 60)
    
    cursor.execute("UPDATE rental_accounts SET rent_until = ? WHERE id = ?", (finish_time, account_id))
    conn.commit()
    conn.close()

def add_rental_account(name: str):
    """Добавляет новый аккаунт."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rental_accounts (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def setup_initial_accounts():
    """
    Проверяет список ACCOUNTS_TO_CHECK.
    Если аккаунта из списка нет в базе, он добавляется.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print("🔄 Проверка списка аккаунтов...")
    
    for name in ACCOUNTS_TO_CHECK:
        # Проверяем, есть ли уже аккаунт с таким именем
        cursor.execute("SELECT id FROM rental_accounts WHERE name = ?", (name,))
        data = cursor.fetchone()
        
        if data is None:
            # Если нет — добавляем
            cursor.execute("INSERT INTO rental_accounts (name) VALUES (?)", (name,))
            print(f"✅ Добавлен новый аккаунт: {name}")
        
    conn.commit()
    conn.close()

def reset_rental_accounts_table():
    """Очищает и пересоздает таблицу rental_accounts (для сброса ID)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Удаляем таблицу
    cursor.execute("DROP TABLE IF EXISTS rental_accounts")
    
    # Создаем ее заново
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rental_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rent_until REAL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
    print("Таблица rental_accounts сброшена и пересоздана.")

# --- АВТОЗАПУСК ПРИ ИМПОРТЕ ---
# Это гарантирует, что таблицы создадутся и новые аккаунты добавятся при старте бота
create_tables()
setup_initial_accounts()
