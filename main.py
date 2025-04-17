"""
Основна точка запуску для Telegram-бота. Ініціалізує та запускає бота.

При запуску:
- Виводиться повідомлення про запуск бота в консолі.
- Налаштовуються зворотні виклики для обробки повідомлень та команд.
- Запускається процес polling для бота, що дозволяє йому працювати без зупинок.

Викликається функція `setup_callbacks` для налаштування обробників.
Потім запускається метод `polling` для безперервної роботи бота.
"""

from callbacks import setup_callbacks
from config import bot
from logger import logger

if __name__ == '__main__':
    logger.info('Запуск Telegram-бота...')
    print('Бота запущено!')

    try:
        setup_callbacks(bot)
        logger.debug('Зворотні виклики успішно налаштовано.')
        bot.polling(none_stop=True)
    except Exception:
        logger.critical('Помилка під час запуску бота')
