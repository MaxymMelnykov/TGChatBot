from Container import *
from config import *
from user_data import *


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


def create_main_markup():
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton('Перейти на сайт', url='https://els.systems'),
        types.InlineKeyboardButton('Відповіді на питання', callback_data='help')
    )
    markup.row(
        types.InlineKeyboardButton('Конфігуратор контейнерів', callback_data='config'),
        types.InlineKeyboardButton('Зв`яжіться з нами', callback_data='contacts')
    )
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


def create_material_markup(container_type):
    markup = types.InlineKeyboardMarkup(row_width=1)
    materials = Container.get_materials_by_type(container_type)
    for material in materials:
        markup.add(types.InlineKeyboardButton(material, callback_data=material))
    return markup
