import logging
import os
from logging.handlers import RotatingFileHandler

from config import ADMIN_ID, bot

LOG_FILE = "bot.log"
LOG_LEVEL = os.getenv("BOT_LOG_LEVEL", "DEBUG").upper()

# Створюємо логер
logger = logging.getLogger("bot_logger")
logger.setLevel(LOG_LEVEL)

# Формат логів
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

# Обробник для запису у файл з ротацією
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=3, encoding="utf-8")
file_handler.setFormatter(formatter)

# Обробник для виводу в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Додаємо обробники до логера
logger.addHandler(file_handler)
logger.addHandler(console_handler)


class TelegramCriticalHandler(logging.Handler):
    def emit(self, record):
        if record.levelno >= logging.CRITICAL:
            log_entry = self.format(record)
            try:
                bot.send_message(ADMIN_ID, f"🚨 КРИТИЧНА ПОМИЛКА 🚨\n{log_entry}")
            except Exception as e:
                print("Не вдалося надіслати критичну помилку:", e)


critical_handler = TelegramCriticalHandler()
critical_handler.setFormatter(formatter)
logger.addHandler(critical_handler)
