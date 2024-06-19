import telebot
from telebot import types
from collections import defaultdict
from Container import Container

TOKEN = '7367025283:AAFahZ2L7v-YugDOLAedTkxOqQ02MbHW8jg'
bot = telebot.TeleBot(TOKEN)

# Повідомлення
START_MESSAGE = 'Привіт! \n Я бот....'
HELP_MESSAGE = 'Питання'
CONFIG_MESSAGE = 'Конфігуратор контейнерів...Оберіть...'
CONTACT_MESSAGE = 'Все ще потрібна допомога? Зв`яжіться з нами!......'
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
                      'Усі залізні деталі конструкції виготовленні за технологією гарячого цинкування, що вважається '
                      'одним з найнадійніших методів захисту заліза і сталі від корозії. За даними American Galvanizer '
                      'Association гаряче цинкування забезпечує захист від корозії до 85 років у міському середовищі. '
                      'Тому контейнери можна очищувати за допомогою води з використанням хімічних засобів.'),

    'secondQuestion': ('Як дізнатися чи заповнений контейнер?',
                       '<strong>Як дізнатися чи заповнений контейнер?</strong>\n'
                       'Контейнер оснащений лазерним датчиком заповнення сміттям та GPRS-модемом для диспетчеризації '
                       'логістики. Автоматизація процесів дозволяє вчасно реагувати на наповненість контейнерів та '
                       'оптимізувати логістику вивозу сміття.'),

    'thirdQuestion': ('Чи є в контейнерах захист від пожежі?',
                      '<strong>Чи є в контейнерах захист від пожежі? - Так, є</strong>\n'
                      'Контейнер обладнаний автономною системою пожежогасіння. Спрацьовує при підвищенні температури '
                      'повітря у контейнері вище 68°С. Об’єм захисту такої системи – 12 м³, у той час, як максимальний '
                      'об’єм контейнеру 5 м³. Це запобігає самозайманню і горінню сміття у місті.'),

    'fourthQuestion': ('Чи є контейнери для небезпечних відходів?',
                       '<strong>Чи є контейнери для небезпечних відходів? - Так, є</strong>\n'
                       'Контейнер для небезпечних відходів - металевий призначений для збору використаних ламп, '
                       'батарейок, акумуляторів та термометрів. У такому сміттєвому баку вони підлягають безпечному '
                       'зберіганню та транспортуванню, гарантовано не зможуть завдати шкоди природі і здоров`ю людини.')
}

# Словарь для разметки основного меню
MAIN_MARKUP = types.InlineKeyboardMarkup()
MAIN_MARKUP.row(
    types.InlineKeyboardButton('Перейти на сайт', url='https://els.systems/about-company/'),
    types.InlineKeyboardButton('Відповіді на питання', callback_data='help')
)
MAIN_MARKUP.row(
    types.InlineKeyboardButton('Конфігуратор контейнерів', callback_data='config'),
    types.InlineKeyboardButton('Зв`яжіться з нами', callback_data='contacts')
)

# Контактная информация
CONTACTS_MESSAGE = ('<strong>Адреса компанії:</strong>\n'
                    'м. Київ, вул. Бориспільська, 9 корпус, 94\n'
                    '<strong>Телефон:</strong>\n'
                    '+38 (068) 207-07-15\n'
                    '<strong>Графік роботи:</strong>\n'
                    'Пн.-Пт. 08:00-17:00\n'
                    '<strong>Пишіть, ми на зв`язку:</strong>\n'
                    'sf_els@ukr.net , elsinfo@ukr.net')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, START_MESSAGE, reply_markup=MAIN_MARKUP)


@bot.callback_query_handler(func=lambda callback: True)
def callback_function(callback):
    data = callback.data
    message_id = callback.message.chat.id

    if data == 'help':
        bot.send_message(message_id, HELP_MESSAGE, reply_markup=create_help_markup())
    elif data == 'config':
        bot.send_message(message_id, CONFIG_MESSAGE, reply_markup=create_config_markup())
    elif data == 'contacts':
        bot.send_message(message_id, CONTACTS_MESSAGE, parse_mode='html')
    elif data in QUESTIONS:
        _, response = QUESTIONS[data]
        bot.send_message(message_id, response, parse_mode='html')
    elif data in Container.get_names_containers():
        bot.send_message(message_id, f'Виберіть тип {data.lower()} контейнера:',
                         reply_markup=create_type_markup(data))

@bot.callback_query_handlers(callback_function = Container.containers.container_type)
def callback_function(callback):
    message_id = callback.message.chat.id
    bot.send_message(message_id, 'Введіть, кількість конейнерів')
    bot.register_next_step_handler(callback, calc)

def calc(callback):
    quant = 0
    quant = callback.text
def create_help_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key, (text, _) in QUESTIONS.items():
        markup.add(types.InlineKeyboardButton(text, callback_data=key))
    return markup


def create_config_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    names = set()
    containers = Container.get_containers()
    for container in containers:
        if container.container_name not in names:
            names.add(container.container_name)
            markup.add(types.InlineKeyboardButton(container.container_name, callback_data=container.container_name))
    return markup


def create_type_markup(container_name):
    markup = types.InlineKeyboardMarkup()
    container_types = Container.get_types_by_name(container_name)
    for container_type in container_types:
        markup.add(types.InlineKeyboardButton(container_type, callback_data=container_type))
    return markup

def

# Запуск бота
bot.polling(none_stop=True, interval=0)
