# database/db.py (Полный код)
import sqlite3
import time
from typing import List, Tuple, Optional

# Имя файла базы данных
DB_NAME = 'database.db'

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
    """Создает тестовые аккаунты (до 8), если их нет."""
    accounts = get_rental_accounts()
    if not accounts:
        # Добавляем 8 аккаунтов
        add_rental_account("АККАУНТ №1🚹")
        add_rental_account("АККАУНТ №2🚺")
        add_rental_account("АККАУНТ №3🚹")
        add_rental_account("АККАУНТ №4🚹")
        add_rental_account("АККАУНТ №5🚹")
        add_rental_account("АККАУНТ №6🚹")
        add_rental_account("АККАУНТ №7🚹")
        add_rental_account("АККАУНТ №8🚹")

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