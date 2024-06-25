from math import ceil

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
START_MESSAGE = 'Привіт! \n Я бот.....'
HELP_MESSAGE = 'Ось відповіді на часті запитання:'
CONFIG_MESSAGE = 'Оберіть, чи ви звичайний покупець, чи представник ЖК.'

CONFIG_CUSTOMER_MESSAGE = 'Конфігуратор контейнерів для звичайних покупців. Оберіть необхідний контейнер:'
CONTACT_MESSAGE = 'Все ще потрібна допомога? Зв’яжіться з нами!'

AR_CONFIG_SQUARE = 'Введіть площу'
AR_CONFIG_APARTMENTS = 'Введіть кількість квартир'

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
user_data = defaultdict(
    lambda: {'user_type': None,
             'container_calc_res_ra': 0,
             'container_volume_of_all_orders': 0,
             'area': None,
             'apartments': None,
             'container_name': None,
             'container_type': None,
             'container_material': None,
             'container_quantity': 0,
             'container_underground_sensor': False,
             'orders': [],
             'total_sum': 0})


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, START_MESSAGE, reply_markup=MAIN_MARKUP)


@bot.callback_query_handler(func=lambda callback: True)
def callback_function(callback):
    data = callback.data
    message_id = callback.message.chat.id
    this_message_id = callback.message.message_id
    # Різні callback функції
    if data == 'start':
        bot.delete_message(message_id, this_message_id)
        bot.send_message(message_id, START_MESSAGE, reply_markup=MAIN_MARKUP)
    if data == 'help':
        bot.delete_message(message_id,this_message_id)
        bot.send_message(message_id, HELP_MESSAGE, reply_markup=create_help_markup())
    elif data in QUESTIONS:
        _, response = QUESTIONS[data]
        bot.send_message(message_id, response, parse_mode='html')
    elif data == 'contacts':
        bot.send_message(message_id, CONTACTS_MESSAGE, parse_mode='html')
    elif data == 'config':
        bot.send_message(message_id, CONFIG_MESSAGE, reply_markup=create_config_markup())
    elif data == 'customer':
        user_data[message_id]['user_type'] = data
        send_photos_with_message(message_id, Container.get_photoes_containers(), CONFIG_CUSTOMER_MESSAGE,
                                 reply_markup=create_config_customer_markup())
    elif data in Container.get_names_containers():
        user_data[message_id]['container_name'] = data
        if user_data[message_id]['user_type'] == 'customer':
            send_photos_with_message(message_id, Container.get_all_type_photos_by_name(data),
                                     f'Виберіть тип {data.lower()} контейнера', create_type_markup(data))


        elif user_data[message_id]['user_type'] == 'ra':
            calc_res = user_data[message_id]['container_calc_res_ra'] - user_data[message_id][
                'container_volume_of_all_orders']
            if data == 'Підземний':
                calc_res = ceil(calc_res / 5)
                send_photos_with_message(message_id, Container.get_all_type_photos_by_name(data),
                                         f'Вам потрібно :{calc_res} контейнерів {data}, виберіть їх тип',
                                         create_type_markup(data))
            elif data == 'Напівпідземний':
                calc_res_2_5 = ceil(calc_res / 2.5)
                calc_res_3_8 = ceil(calc_res / 3.8)
                calc_res_5_0 = ceil(calc_res / 5.0)
                send_photos_with_message(message_id, Container.get_all_type_photos_by_name(data),
                                         f'Вам потрібно :{calc_res_2_5} контейнерів типу 2.5 або {calc_res_3_8} контейнерів типу 3.8 або {calc_res_5_0} контейнерів типу 5.0 , виберіть їх тип',
                                         create_type_markup(data))


    elif data in Container.get_all_types():
        user_data[message_id]['container_type'] = data
        if user_data[message_id]['container_name'] == 'Підземний':
            photo = open(Container.get_material_photo(), 'rb')
            bot.send_photo(message_id, photo, caption='Виберіть матеріал контейнера ',
                           reply_markup=create_material_markup(data))
        elif user_data[message_id]['container_name'] == 'Напівпідземний':
            photo = open(Container.get_material_photo(), 'rb')
            bot.send_photo(message_id, photo, caption='Виберіть матеріал контейнера ',
                           reply_markup=create_material_markup(data))
        else:
            bot.send_message(message_id, 'Введіть кількість контейнерів:')
            bot.register_next_step_handler(callback.message, get_quantity)

    elif data in Container.get_all_materials():
        user_data[message_id]['container_material'] = data
        if user_data[message_id]['container_name'] != 'Підземний':
            bot.send_message(message_id, 'Введіть кількість контейнерів:')
            bot.register_next_step_handler(callback.message, get_quantity)
        else:
            bot.send_message(message_id,
                             'У підземних контейнерів є опція датчику наповнення, виберіть, чи потрібна вона Вам',
                             reply_markup=create_sensor_markup())

    elif data == 'customer_end':
        get_all_purchases(callback)
    elif data == 'ra':
        user_id = callback.message.chat.id
        user_data[user_id]['user_type'] = data
        bot.send_message(user_id, "Введіть площу:")
        bot.register_next_step_handler(callback.message, get_ra_area)
    elif data == 'true' or data == 'false':
        if data == 'true':
            user_data[message_id]['container_underground_sensor'] = True
        if data == 'false':
            user_data[message_id]['container_underground_sensor'] = False
        bot.send_message(message_id, 'Введіть кількість контейнерів:')
        bot.register_next_step_handler(callback.message, get_quantity)

    elif data == 'ar_additional_order':
        calc_res = user_data[message_id]['container_calc_res_ra']
        user_orders_volume = user_data[message_id]['container_volume_of_all_orders']
        container_volume_need = ceil(calc_res - user_orders_volume)
        send_photos_with_message(message_id, [Container.get_photo_by_name('Підземний'),
                                              Container.get_photo_by_name('Напівпідземний')],
                                 caption=f'Для вашого ЖК потрібно ще {ceil(container_volume_need)} м³ контейнерів. Виберіть назву контейнера',
                                 reply_markup=create_get_ra_name_markup())


def create_material_markup(container_type):
    markup = types.InlineKeyboardMarkup(row_width=1)
    materials = Container.get_materials_by_type(container_type)
    for material in materials:
        markup.add(types.InlineKeyboardButton(material, callback_data=material))
    return markup


def calculate_volume_count(user_id, volume):
    count = user_data[user_id]['container_calc_res_ra']
    result = count / volume
    return result


def calculate_ra_volume_count(user_id):
    area = user_data[user_id]['area']
    apartments = user_data[user_id]['apartments']

    average_apartment_square = area / apartments  # Середня кількість людей в 1ій квартирі

    one_apartment_people = (average_apartment_square - 10.5) / 21  # Скільки людей в одній квартирі

    people_in_ra = ceil(one_apartment_people * apartments)  # Кількість жителів в ЖК

    q = 0.0059  # Добовий  об'єм  утворення  кожного виду ПВ на одного
    k = 1.4  # Добовий  коефіцієнт  нерівномірності  утворення  кожного
    t = 5  # Кількість неробочих днів на рік
    # Максимальний добовий об'єм утворення ТПВ
    qdmax = (q * people_in_ra * 365 / (365 - t)) * k

    period = 1  # Періодичність перевезення кожного виду ПВ, діб,
    repair = 1.05  # Коефіцієнт,  який  враховує  кількість контейнерів, що враховує кількість контейнеів у ремонті

    C = 1  # Місткість одного контейнера, куб.м.

    full = 0.9  # коефіцієнт заповнення контейнера.

    # Кількість контейнерів рекомендується визначати за формулою:
    # N = (Qдmax * t * 1, 4 * 1, 05) / (5 * 0, 9)
    N = (qdmax * period * k * repair) / (C * full)
    user_data[user_id]['container_calc_res_ra'] = ceil(N)
    return ceil(N)


def get_ra_area(message):
    user_id = message.chat.id
    if message.text is not None:
        try:
            area = float(message.text)
            user_data[user_id]['area'] = area
            bot.send_message(user_id, "Введіть кількість квартир:")
            bot.register_next_step_handler(message, get_ra_apartments)
        except ValueError:
            bot.send_message(user_id, "Будь ласка, введіть числове значення.")
            bot.register_next_step_handler(message, get_ra_area)
    else:
        bot.send_message(user_id, "Будь ласка, введіть числове значення.")
        bot.register_next_step_handler(message, get_ra_area)


def get_ra_apartments(message):
    user_id = message.chat.id
    if message.text is not None:
        try:
            apartments = int(message.text)
            user_data[user_id]['apartments'] = apartments
            calculate_ra_volume_count(user_id)
            send_photos_with_message(user_id, [Container.get_photo_by_name('Підземний'),
                                               Container.get_photo_by_name('Напівпідземний')],
                                     caption=f'Для вашого ЖК потрібно {ceil(calculate_ra_volume_count(user_id))} м^3 контейнерів. Виберіть назву контейнера',
                                     reply_markup=create_get_ra_name_markup())
        except ValueError:
            bot.send_message(user_id, "Будь ласка, введіть числове значення.")
            bot.register_next_step_handler(message, get_ra_apartments)
    else:
        bot.send_message(user_id, "Будь ласка введіть числове значення.")
        bot.register_next_step_handler(message, get_ra_area)


def create_get_ra_name_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('Підземний', callback_data='Підземний'))
    markup.add(types.InlineKeyboardButton('Напівпідземний', callback_data='Напівпідземний'))
    return markup


def create_sensor_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('З датчиком', callback_data='true'))
    markup.add(types.InlineKeyboardButton('Без датчику', callback_data='false'))
    return markup


def get_quantity(message):
    message_id = message.chat.id
    quantity_text = message.text

    try:
        quantity = int(quantity_text)
        user_data[message_id]['container_quantity'] = quantity

        container_volume_needed_for_ra = user_data[message_id]['container_calc_res_ra']

        user_type = user_data[message_id]['user_type']

        container_name = user_data[message_id]['container_name']

        container_type = user_data[message_id]['container_type']

        container_volume = Container.get_volume_by_type(container_type)

        container_material = user_data[message_id]['container_material']

        container_photo_path = Container.get_photo_by_type(container_type)

        container_underground_sensor = user_data[message_id]['container_underground_sensor']

        user_data[message_id]['container_volume_of_all_orders'] += quantity * container_volume
        container_volume_of_all_orders = user_data[message_id]['container_volume_of_all_orders']

        if not container_photo_path:
            raise FileNotFoundError("No photo path found for container.")

        with open(container_photo_path, 'rb') as container_photo:
            if container_name == 'Підземний' or container_name == 'Напівпідземний':
                price_per_unit = Container.get_price_of_container_by_all_data(container_name, container_type,
                                                                              container_material)
            else:
                price_per_unit = Container.get_price_by_type(container_type)

            sensor_cost = 200
            if container_underground_sensor:
                price_per_unit += sensor_cost
            sensor_message = '✅'
            if not container_underground_sensor:
                sensor_message = '❌'

            total_price = quantity * price_per_unit
            container_volume_need_more = ceil(container_volume_needed_for_ra - container_volume_of_all_orders)
            message_text = (
                f"{f'❗️<strong>Для вашого ЖК потрібно ще {container_volume_need_more} м³ контейнерів, бажаєте дозамовити?</strong>\n' if user_type == 'ra' and container_volume_need_more > 0 else ''}"
                f"<b>Ваше замовлення:</b>\n"
                f"🗑 <b>Контейнер:</b> {container_name}\n"
                f"🏷 <b>Тип:</b> {container_type}\n"
                f"{f'🧱<b>Матеріал:</b> {container_material}\n' if container_name in ['Підземний', 'Напівпідземний'] else ''}"
                f"{f'📡<b>Сенсор:</b> {sensor_message}\n' if container_name == 'Підземний' else ''}"
                f"1️⃣<b>Вартість одного</b>: {price_per_unit}\n"
                f"🔢 <b>Кількість:</b> {quantity} шт.\n"
                f"💵 <b>Сума:</b> {total_price} грн\n"
            )

            bot.send_photo(message_id, container_photo, message_text,
                           reply_markup=create_order_navigation_markup(message_id), parse_mode='html')
            user_data[message_id]['total_sum'] += total_price
            user_data[message_id]['orders'].append({
                'container_name': container_name,
                'container_type': container_type,
                'container_material': container_material,
                'container_underground_sensor': container_underground_sensor,
                'quantity': quantity,
                'total_price': total_price,
                'photo': container_photo_path,
            })


    except FileNotFoundError as e:
        bot.send_message(message_id, str(e))
    except ValueError:
        bot.send_message(message_id, 'Будь ласка, введіть числове значення.')
        bot.register_next_step_handler(message, get_quantity)


def get_all_purchases(callback):
    message_id = callback.message.chat.id
    orders = user_data[message_id].get('orders', [])

    if not isinstance(orders, list):
        bot.send_message(message_id, "Немає даних про замовлення.")
        return

    container_names = []
    container_types = []
    container_materials = []
    container_sensors = []
    container_photos = []
    container_quantities = []
    total_sum = user_data[message_id]['total_sum']

    for order in orders:
        container_names.append(order['container_name'])
        container_types.append(order['container_type'])
        container_materials.append(order['container_material'])
        container_sensors.append(order['container_underground_sensor'])
        container_quantities.append(order['quantity'])
        container_photos.append(order['photo'])

    user_username = callback.from_user.username
    user_name = callback.from_user.first_name or 'Невідоме'

    notify_admin(callback, orders)

    message_lines = [
        f"<b>Ваше замовлення:</b>",
        f"<b>Загальна сума:</b> {total_sum} грн",
        "-----------------------------------------------"
    ]

    for idx, order in enumerate(orders, start=1):
        if order['container_name'] == 'Підземний':
            if order['container_underground_sensor']:
                sensor_message = '✅'
            else:
                sensor_message = '❌'
            message_lines.append(
                f"№{idx}:\n"
                f"🗑Контейнер:  {order['container_name']}\n"
                f"🏷Тип:  {order['container_type']}\n"
                f"🧱Матеріал:  {order['container_material']}\n"
                f"📡Сенсор:  {sensor_message}\n"
                f"1️⃣Ціна за контейнер: {order['total_price'] / order['quantity']} грн\n"
                f"🔢Кількість:  {order['quantity']} шт.\n"
                f"💵Сума:  {order['total_price']} грн\n"
                '-----------------------------------------------'
            )
        elif order['container_name'] == 'Напівпідземний':
            message_lines.append(
                f"№{idx}:\n"
                f"🗑Контейнер:  {order['container_name']}\n"
                f"🏷Тип:  {order['container_type']}\n"
                f"🧱Матеріал:  {order['container_material']}\n"
                f"1️⃣Ціна за контейнер:  {order['total_price'] / order['quantity']} грн\n"
                f"🔢Кількість:  {order['quantity']} шт.\n"
                f"💵Сума:  {order['total_price']} грн\n"
                '-----------------------------------------------'
            )
        else:
            message_lines.append(
                f"№{idx}:\n"
                f"🗑Контейнер:  {order['container_name']}\n"
                f"🏷Тип:  {order['container_type']}\n"
                f"1️⃣Ціна за контейнер:  {order['total_price'] / order['quantity']} грн\n"
                f"🔢Кількість:  {order['quantity']} шт.\n"
                f"💵Сума:  {order['total_price']} грн\n"
                '-----------------------------------------------')

    message = "\n".join(message_lines)
    bot.send_message(message_id, message, parse_mode='html')

    clear_user_data(message_id)


# Відправлення менеджеру повідомлення про нове замовлення.
def notify_admin(callback, orders):
    message_id = callback.message.chat.id

    user_id = callback.message.chat.id
    user_username = callback.from_user.username
    user_name = callback.from_user.first_name or 'Невідоме'

    total_sum = user_data[message_id]['total_sum']
    message_lines = [
        f"<b>🚨 Нове замовлення від клієнта 🚨</b>\n"
        f"<b>🆔ID користувача: </b> {user_id}\n"
        f"<b>👤Ім'я користувача: </b> {user_name}\n"
        f"<b>📧Username користувача: </b> @{user_username}\n",
        f"<b>💵Загальна сума:</b> {total_sum} грн",
        "-----------------------------------------------"
    ]

    for idx, order in enumerate(orders, start=1):
        if order['container_name'] == 'Підземний':
            if order['container_underground_sensor']:
                sensor_message = '✅'
            else:
                sensor_message = '❌'
            message_lines.append(
                f"№{idx}:\n"
                f"🗑Контейнер: {order['container_name']}\n"
                f"🏷Тип: {order['container_type']}\n"
                f"🧱Матеріал: {order['container_material']}\n"
                f"📡Сенсор: {sensor_message}\n"
                f"1️⃣Ціна за контейнер: {order['total_price'] / order['quantity']} грн\n"
                f"🔢Кількість: {order['quantity']} шт.\n"
                f"💵Сума: {order['total_price']} грн\n"
                '-----------------------------------------------'
            )
        elif order['container_name'] == 'Напівпідземний':
            message_lines.append(
                f"№{idx}:\n"
                f"🗑Контейнер: {order['container_name']}\n"
                f"🏷Тип: {order['container_type']}\n"
                f"🧱Матеріал: {order['container_material']}\n"
                f"1️⃣Ціна за контейнер: {order['total_price'] / order['quantity']} грн\n"
                f"🔢Кількість: {order['quantity']} шт.\n"
                f"💵Сума: {order['total_price']} грн\n"
                '-----------------------------------------------'
            )
        else:
            message_lines.append(
                f"№{idx}:\n"
                f"🗑Контейнер: {order['container_name']}\n"
                f"🏷Тип: {order['container_type']}\n"
                f"1️⃣Ціна за контейнер: {order['total_price'] / order['quantity']} грн\n"
                f"🔢Кількість: {order['quantity']} шт.\n"
                f"💵Сума: {order['total_price']} грн\n"
                '-----------------------------------------------')

    message = "\n".join(message_lines)

    bot.send_message(ADMIN_ID, message, parse_mode='HTML')

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
    markup.add(types.InlineKeyboardButton('Повернутися', callback_data='start'))
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


def create_order_navigation_markup(message_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    if user_data[message_id]['user_type'] == 'customer':
        markup.add(types.InlineKeyboardButton('Доповнити замовлення', callback_data='customer'))
        markup.add(types.InlineKeyboardButton('Завершити замовлення', callback_data='customer_end'))
    else:
        markup.add(types.InlineKeyboardButton('Доповнити замовлення', callback_data='ar_additional_order'))
        markup.add(types.InlineKeyboardButton('Завершити замовлення', callback_data='customer_end'))
    return markup


# Запуск бота
bot.polling(none_stop=True, interval=0)
