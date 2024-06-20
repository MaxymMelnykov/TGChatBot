import telebot
import os
from telebot import types
from collections import defaultdict
from Container import Container

# Токен бота
TOKEN = '7367025283:AAFahZ2L7v-YugDOLAedTkxOqQ02MbHW8jg'
bot = telebot.TeleBot(TOKEN)

# ID адміністратора
ADMIN_ID = 516166196

# Повідомлення
START_MESSAGE = 'Привіт! \n Я бот для конфігурації контейнерів.'
HELP_MESSAGE = 'Ось відповіді на часті запитання:'
CONFIG_MESSAGE = 'Оберіть, чи ви звичайний покупець, чи представник ЖК.'

CONFIG_CUSTOMER_MESSAGE = 'Конфігуратор контейнерів для звичайних покупців. Оберіть необхідний контейнер:'
CONTACT_MESSAGE = 'Все ще потрібна допомога? Зв’яжіться з нами!'

# Контакти
CONTACTS = ('<strong>Адреса компанії:</strong>\n'
            'м. Київ, вул. Бориспільська, 9 корпус, 94\n'
            '<strong>Телефон:</strong>\n'
            '+38 (068) 207-07-15\n'
            '<strong>Графік роботи:</strong>\n'
            'Пн.-Пт. 08:00-17:00\n'
            '<strong>Пишіть, ми на зв`язку:</strong>\n'
            'sf_els@ukr.net , elsinfo@ukr.net')

# Питання
QUESTIONS = {
    'firstQuestion': ('Чи піддаються контейнери корозії?',
                      '<strong>Чи піддаються контейнери корозії? - Ні.</strong>\n'
                      'Усі залізні деталі конструкції виготовленні за технологією гарячого цинкування...'),

    'secondQuestion': ('Як дізнатися чи заповнений контейнер?',
                       '<strong>Як дізнатися чи заповнений контейнер?</strong>\n'
                       'Контейнер оснащений лазерним датчиком заповнення сміттям та GPRS-модемом...'),

    'thirdQuestion': ('Чи є в контейнерах захист від пожежі?',
                      '<strong>Чи є в контейнерах захист від пожежі? - Так, є</strong>\n'
                      'Контейнер обладнаний автономною системою пожежогасіння...'),

    'fourthQuestion': ('Чи є контейнери для небезпечних відходів?',
                       '<strong>Чи є контейнери для небезпечних відходів? - Так, є</strong>\n'
                       'Контейнер для небезпечних відходів - металевий...')
}

# Словник для розмітки основного меню
MAIN_MARKUP = types.InlineKeyboardMarkup()
MAIN_MARKUP.row(
    types.InlineKeyboardButton('Перейти на сайт', url='https://els.systems'),
    types.InlineKeyboardButton('Відповіді на питання', callback_data='help')
)
MAIN_MARKUP.row(
    types.InlineKeyboardButton('Конфігуратор контейнерів', callback_data='config'),
    types.InlineKeyboardButton('Зв`яжіться з нами', callback_data='contacts')
)

# Контактна інформація
CONTACTS_MESSAGE = ('<strong>Адреса компанії:</strong>\n'
                    'м. Київ, вул. Бориспільська, 9 корпус, 94\n'
                    '<strong>Телефон:</strong>\n'
                    '+38 (068) 207-07-15\n'
                    '<strong>Графік роботи:</strong>\n'
                    'Пн.-Пт. 08:00-17:00\n'
                    '<strong>Пишіть, ми на зв`язку:</strong>\n'
                    'sf_els@ukr.net , elsinfo@ukr.net')

# Словник для зберігання даних користувачів
user_data = defaultdict(lambda: {'orders': [], 'total_sum': 0})


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, START_MESSAGE, reply_markup=MAIN_MARKUP)


@bot.callback_query_handler(func=lambda callback: True)
def callback_function(callback):
    data = callback.data
    message_id = callback.message.chat.id
    # Різні callback функції
    if data == 'help':
        bot.send_message(message_id, HELP_MESSAGE, reply_markup=create_help_markup())
    elif data in QUESTIONS:
        _, response = QUESTIONS[data]
        bot.send_message(message_id, response, parse_mode='html')
    elif data == 'contacts':
        bot.send_message(message_id, CONTACTS_MESSAGE, parse_mode='html')
    elif data == 'config':
        bot.send_message(message_id, CONFIG_MESSAGE, reply_markup=create_config_markup())
    elif data == 'customer':
        send_photos_with_message(message_id, Container.get_photoes_containers(), CONFIG_CUSTOMER_MESSAGE,
                                 reply_markup=create_config_customer_markup())
    elif data in Container.get_names_containers():
        user_data[message_id]['container_name'] = data
        bot.send_message(message_id, f'Виберіть тип {data.lower()} контейнера:', reply_markup=create_type_markup(data))
    elif data in Container.get_all_types():
        user_data[message_id]['container_type'] = data
        bot.send_message(message_id, 'Введіть кількість контейнерів:')
        bot.register_next_step_handler(callback.message, get_quantity)
    elif data == 'customer_end':
        get_all_purchares(callback)


def get_quantity(message):
    message_id = message.chat.id
    quantity_text = message.text

    try:
        quantity = int(quantity_text)
        user_data[message_id]['quantity'] = quantity

        container_name = user_data[message_id].get('container_name')
        container_photo_path = Container.get_photo_by_name(container_name)

        if not container_photo_path:
            raise FileNotFoundError("No photo path found for container.")

        with open(container_photo_path, 'rb') as container_photo:
            container_type = user_data[message_id].get('container_type')
            price_per_unit = Container.get_price_by_type(container_type)

            total_price = quantity * price_per_unit
            user_data[message_id]['total_sum'] += total_price
            user_data[message_id]['orders'].append({
                'container_name': container_name,
                'container_type': container_type,
                'quantity': quantity,
                'total_price': total_price,
                'photo': container_photo_path,
            })

            bot.send_photo(message_id, container_photo,
                           caption=f'Ваше замовлення: {container_name} типу {container_type} в кількості {quantity}.\n'
                                   f'Сума замовлення: {total_price} грн\n',
                           reply_markup=create_order_navigation_markup())
    except FileNotFoundError as e:
        bot.send_message(message_id, str(e))
    except ValueError:
        bot.send_message(message_id, 'Будь ласка, введіть числове значення.')
        bot.register_next_step_handler(message, get_quantity)


def get_all_purchares(callback):
    message_id = callback.message.chat.id
    orders = user_data[message_id].get('orders', [])

    if not isinstance(orders, list):
        bot.send_message(message_id, "Invalid order data.")
        return

    container_names = []
    container_types = []
    container_photos = []
    container_quantities = []
    total_sum = user_data[message_id]['total_sum']

    for order in orders:
        container_names.append(order['container_name'])
        container_types.append(order['container_type'])
        container_photos.append(order['photo'])
        container_quantities.append(order['quantity'])

    user_username = callback.from_user.username
    user_name = callback.from_user.first_name or 'Невідоме'

    notify_admin(message_id, user_username, user_name, container_names, container_quantities, container_types,
                 total_sum)

    send_photos_with_message(message_id, container_photos,
                             f'Ваше замовлення:\nКонтейнери {container_names}, типів {container_types}, в кількостях {container_quantities}\n'
                             f'Загальна сума замовлення: {total_sum}')

    clear_user_data(message_id)

# Відправлення менеджеру повідомлення про нове замовлення.
def notify_admin(user_id, user_username, user_name, container_names, container_quantities, container_types,
                 total_price):
    user_info = (f"Користувач ID: {user_id},\n"
                 f"Юзернейм користувача: @{user_username},\n"
                 f"Ім'я користувача: {user_name},\n")

    details = (f"{user_info}\n"
               f"Назва контейнера: {', '.join(container_names)}\n"
               f"Тип контейнера: {', '.join(container_types)}\n"
               f"Кількість: {', '.join(map(str, container_quantities))}\n"
               f"Загальна вартість: {total_price} грн")

    bot.send_message(ADMIN_ID, details)

def clear_user_data(user_id):
    if user_id in user_data:
        del user_data[user_id]

# Відправлення повідомлення із зображеннями
def send_photos_with_message(chat_id, photo_paths, caption, reply_markup=None):
    media = []
    open_files = []
    try:
        for photo_path in photo_paths:
            try:
                if not os.path.exists(photo_path) or os.path.getsize(photo_path) == 0:
                    raise FileNotFoundError(f"Файл із зображенням {photo_path} не знайдено або він порожній.")

                photo = open(photo_path, 'rb')
                open_files.append(photo)
                media.append(types.InputMediaPhoto(photo))
            except FileNotFoundError as e:
                bot.send_message(chat_id, str(e))
                return

        if media:
            bot.send_media_group(chat_id, media)
            bot.send_message(chat_id, caption, reply_markup=reply_markup)
    finally:
        for file in open_files:
            file.close()


def create_help_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key, (text, _) in QUESTIONS.items():
        markup.add(types.InlineKeyboardButton(text, callback_data=key))
    return markup


def create_config_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    # Звичайний покупець
    markup.add(types.InlineKeyboardButton('Покупець', callback_data='customer'))
    # ЖК
    markup.add(types.InlineKeyboardButton('ЖК', callback_data='ra'))
    return markup


def create_config_customer_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    names = set()
    containers = Container.get_containers()
    for container in containers:
        if container.container_name not in names:
            names.add(container.container_name)
            markup.add(types.InlineKeyboardButton(container.container_name, callback_data=container.container_name))
    return markup


def create_type_markup(container_name):
    markup = types.InlineKeyboardMarkup(row_width=1)
    container_types = Container.get_types_by_name(container_name)
    for container_type in container_types:
        markup.add(types.InlineKeyboardButton(container_type, callback_data=container_type))
    return markup


def create_order_navigation_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('Доповнити замовлення', callback_data='customer'))
    markup.add(types.InlineKeyboardButton('Завершити замовлення', callback_data='customer_end'))
    return markup



# Запуск бота
bot.polling(none_stop=True, interval=0)
