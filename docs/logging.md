# Логування

## Рівні логування:

- logger.debug()	Пише в лог технічну інформацію (наприклад, значення змінних)
- logger.info()	Пише щось типу: "Користувач натиснув на кнопку"
- logger.warning()	Пише: "Обережно, ця кнопка неактивна, але бот не зламався"
- logger.error()	Пише: "Помилка! Але ми її перехопили"
- logger.exception()	Те саме що error, але ще й з трасуванням (дебаг-інфо про місце)
- logger.critical()	Бот зламався.

#### Всі дії користувача логуються у файл `bot.log`.
#### Для логів реалізовано ротацію з обмеженням на 1MB.
#### Формат: `[дата] - [рівень] - [модуль] - [повідомлення]`

### Команда бота /report_error.
Ця команда запускає інтерактивну форму збору технічного звіту про помилку, яка допомагає користувачам повідомляти про проблеми, що виникають під час використання Telegram-бота.
