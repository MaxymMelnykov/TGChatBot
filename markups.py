from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from Container import *
from config import *
from user_data import *


def create_main_markup():
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton('🛒Конфігуратор замовлень', callback_data='config'),
    )
    markup.row(

        types.InlineKeyboardButton('🌐Переглянути каталог', url='https://els.systems/katalog/'),
        types.InlineKeyboardButton('⁉️Відповіді на питання', callback_data='help')
    )
    return markup


def create_help_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key, (text, _) in QUESTIONS.items():
        markup.add(types.InlineKeyboardButton(text, callback_data=key))
    markup.add(types.InlineKeyboardButton('☎️Зворотній зв`язок', callback_data='contacts'))
    markup.add(types.InlineKeyboardButton('◀️Повернутися', callback_data='start'))
    return markup


def create_get_ra_name_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('Підземний', callback_data='Підземний'))
    markup.add(types.InlineKeyboardButton('Напівпідземний', callback_data='Напівпідземний'))
    return markup


def create_config_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    # Звичайний покупець
    markup.add(types.InlineKeyboardButton('Приватний покупець', callback_data='customer'))
    # ЖК
    markup.add(types.InlineKeyboardButton('Забудовник', callback_data='ra'))
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


def create_sensor_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(types.InlineKeyboardButton('✅ Потрібна', callback_data='true'),
               types.InlineKeyboardButton('❌ Не потрібна', callback_data='false'))
    return markup


def create_contacts_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('🗺Переглянути на мапі',
                                          url='https://www.google.com/maps/place/Boryspilska+St,+9/@50.4296885,30.6636144,18.25z/data=!4m7!3m6!1s0x40d4c5213495e2fd:0x38eb621a82251730!4b1!8m2!3d50.4295865!4d30.6634792!16s%2Fg%2F11fx8hp_71?entry=ttu'))
    markup.add(types.InlineKeyboardButton('◀️Повернутися', callback_data='start'))
    return markup


def create_faq_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('◀️Повернутися', callback_data='help'))
    markup.add(types.InlineKeyboardButton('⏪До головного меню', callback_data='start'))
    return markup


def create_type_markup(container_name):
    if container_name == 'Підземний' or container_name == 'Напівпідземний' or container_name == 'Для небезпечних відходів':
        markup = types.InlineKeyboardMarkup(row_width=3)
    elif container_name == 'Сортувальний':
        markup = types.InlineKeyboardMarkup(row_width=2)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
    container_types = Container.get_types_by_name(container_name)
    buttons = [types.InlineKeyboardButton(text=container_type, callback_data=container_type) for container_type in
               container_types]
    markup.add(*buttons)
    return markup


def create_order_navigation_markup(message_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    if user_data[message_id]['user_type'] == 'customer':
        markup.add(types.InlineKeyboardButton('➕ Доповнити замовлення', callback_data='customer'))
        markup.add(types.InlineKeyboardButton('✔️ Завершити замовлення', callback_data='customer_end'))
    else:
        markup.add(types.InlineKeyboardButton('➕ Доповнити замовлення', callback_data='ar_additional_order'))
        markup.add(types.InlineKeyboardButton('✔️ Завершити замовлення', callback_data='customer_end'))
    return markup


def create_material_markup(container_name):
    markup = types.InlineKeyboardMarkup(row_width=1)
    materials = Container.get_materials_by_name(container_name)
    for material in materials:
        markup.add(types.InlineKeyboardButton(material, callback_data=material))
    return markup

def create_main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton('🚪 До головного меню'))
    return markup

