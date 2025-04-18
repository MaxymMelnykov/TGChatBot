# TGChatBot

Telegram-бот для конфігурації онлайн-замовлень для компанії ТОВ "ЕКО ЛОГІЧНІ СИСТЕМИ"

## Налаштування та запуск проєкту
### Необхідне програмне забезпечення

### Компонент
Python	3.10+

pip	latest

Git	latest

Telegram API key	Отримати у @BotFather

### Налаштування середовища розробки

1. Клонуйте репозиторій:
   ```bash
   git clone https://github.com/ваш-юзернейм/TGChatBot.git
2. Встановіть всі залежності
    ```bash
   pip install -r requirements.txt
3. Налаштування:

У файлі config.py у змінну TOKEN впишіть згенерований токен бота,
а у змінну ADMIN_ID впишіть ID менеджера, якому будуть приходити
повідомлення про нові замовлення.

# Використання
### Запуск бота

#### Режим розробки

```bash
/docs/scripts/run_dev.sh
```
#### Режим production
```bash
/docs/scripts/run_prod.sh
```
Заходимо у бота, до якого Ви прив'язали свій токен, тепер Ви можеет користуватися основними функціями бота такими як:
1. Отримати відповіді на поширені запитання.
2. Отримати контакту інформацію.
3. Перейти на веб-сайт компанії, для перегляду каталогу товарів.
3. Сконфігурувати онлайн-замовлення, як забудовник ЖК, з прорахуванням кількості квартир та площі ЖК.
4. Замовити товар, як приватний покупець.

## Документування коду

Цей проєкт використовує **Google-style docstrings** та генерацію документації за допомогою **Sphinx**.

### Приклад форматування функції:

```python
def calculate_total(price, quantity):
    """
    Обчислює загальну суму.

    Args:
        price (float): Ціна одного товару.
        quantity (int): Кількість товарів.

    Returns:
        float: Загальна сума.
    """
    return price * quantity
```
# Тестування
Тести зберігаються в [tests](tests) тут є як інтеграційні
та юніт тести так і behave тести.
# Ліцензія
Цей проект ліцензовано за MIT License - дивіться файл LICENSE для деталей.
