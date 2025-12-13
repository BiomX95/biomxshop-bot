# handlers/__init__.py

# Импортируем все ваши модули с хендлерами,
# чтобы они зарегистрировались в инстансе бота.

from . import start
from . import menu
from . import callbacks
from . import autopost

# Новые хендлеры, которые мы сейчас добавляем:
from . import rent
from . import donate

# Дополнительные хендлеры, которые у вас уже есть:
# Раскомментируйте те, которые вы используете
# from . import donate 
# from . import errors 
# from . import roulette
# from . import wheel