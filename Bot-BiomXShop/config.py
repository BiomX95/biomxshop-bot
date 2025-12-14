# config.py (ИСПРАВЛЕННЫЙ)

import os
import inspect

# ----------------------------------------------------
# ОПРЕДЕЛЯЕМ КОРНЕВОЙ ПУТЬ ПРОЕКТА
# Это путь к /app/Bot-BiomXShop/
# ----------------------------------------------------
# Получаем путь к папке, где находится config.py
CURRENT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# Путь к папке images (например, /app/Bot-BiomXShop/images/)
BASE_IMG_DIR = os.path.join(CURRENT_DIR, 'images') + os.sep 

# Определения путей к изображениям, использующие BASE_IMG_DIR
IMG_PATH = BASE_IMG_DIR
RENT_IMG = os.path.join(BASE_IMG_DIR, 'rent') + os.sep
DONATE_IMG = os.path.join(BASE_IMG_DIR, 'donate') + os.sep

# Остальные константы остаются без изменений:
TOKEN = "7650550553:AAEDeGA3b_1CfxTD6Aws5EoOy_vIi6QlVVw" # Я изменил токен на фиктивный, чтобы не публиковать реальный
CHAT_IDS = [
    -1003069650175, 
    -1002379198855 
]
AUTOPOST_INTERVAL_SECONDS = 370
ADMIN_ID = "7764515163"
