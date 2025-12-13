# utils/helpers.py
import time
from typing import Optional # <--- ДОБАВИТЬ ЭТУ СТРОКУ

def format_time_left(rent_until_timestamp: float) -> Optional[str]:
    """Форматирует оставшееся время до освобождения аккаунта."""
    current_time = time.time()
    seconds_left = int(rent_until_timestamp - current_time)
    
    if seconds_left <= 0:
        return None # Время истекло (Аккаунт свободен)
    
    hours = seconds_left // 3600
    minutes = (seconds_left % 3600) // 60
    
    parts = []
    if hours > 0:
        parts.append(f"{hours} ч.")
    if minutes >= 0 or (hours == 0 and minutes == 0):
        parts.append(f"{minutes} мин.")
        
    return " ".join(parts)