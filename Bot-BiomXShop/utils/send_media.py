# utils/send_media.py
from telebot.types import InputMediaPhoto

# Добавлен аргумент reply_markup=None для поддержки клавиатуры статуса
def send_two_photos(bot, message, photo1_path, photo2_path, caption, reply_markup=None):
    
    # 1. ОТКРЫТИЕ ФАЙЛОВ (ИСПРАВЛЕНИЕ NameError)
    # Используем with open, чтобы гарантировать закрытие файлов
    with open(photo1_path, 'rb') as photo1_file, \
         open(photo2_path, 'rb') as photo2_file:
        
        # 2. СОЗДАНИЕ МЕДИА-ГРУППЫ
        media = [
            # Теперь photo1_file и photo2_file определены
            InputMediaPhoto(photo1_file, caption=caption),
            InputMediaPhoto(photo2_file)
        ]
        
        # 3. ОТПРАВКА МЕДИА-ГРУППЫ
        bot.send_media_group(
            message.chat.id, 
            media
        ) 
        
    # 4. ОТПРАВКА КЛАВИАТУРЫ СТАТУСА (отдельным сообщением)
    # Клавиатуру нельзя прикрепить к медиа-группе, только к отдельному сообщению
    if reply_markup:
        # Отправляем сообщение только для того, чтобы прикрепить к нему кнопку
        bot.send_message(
            message.chat.id, 
            "⬇️ Нажмите, чтобы проверить статус аккаунта:", 
            reply_markup=reply_markup
        )

# Если у вас есть другие функции в этом файле, они остаются без изменений.