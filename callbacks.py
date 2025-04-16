from numpy import ceil

from config import (
    CONFIG_CUSTOMER_MESSAGE,
    CONFIG_MESSAGE,
    CONFIG_RA_AREA_MESSAGE,
    CONTACTS_MESSAGE,
    HELP_MESSAGE,
    QUESTIONS,
    START_MESSAGE,
)
from Container import Container
from handlers import (
    get_all_purchases,
    get_quantity,
    get_ra_area,
    get_telephone_number,
    get_wall_width,
)
from markups import (
    create_config_customer_markup,
    create_config_markup,
    create_contacts_markup,
    create_faq_markup,
    create_get_ra_name_markup,
    create_help_markup,
    create_main_markup,
    create_material_markup,
    create_sensor_markup,
    create_type_markup,
)
from user_data import user_data
from utils import send_photos_with_message


def setup_callbacks(bot):
    """
    Реєструє всі обробники команд і callback-запитів для Telegram-бота.

    Ця функція налаштовує основну логіку обробки взаємодії з користувачем:

    - Обробляє команду `/start` та виводить стартове меню.
    - Обробляє callback-запити:
      - Перехід по головному меню, допомога, контакти, FAQ.
      - Налаштування користувачів (замовник/ЖК).
      - Вибір типу та матеріалу контейнерів.
      - Опція датчиків наповнення для підземних контейнерів.
      - Підрахунок потрібних контейнерів для ЖК.
      - Запит номера телефону для замовника.

    Працює в парі з іншими модулями проєкту:
    `config`, `handlers`, `Container`, `markups`, `user_data`, `utils`.

    :param bot: Екземпляр TeleBot для взаємодії з Telegram API.
    """
    @bot.message_handler(commands=['start'])
    def start(message):
        message_id = message.chat.id
        this_message_id = message.message_id
        bot.delete_message(message_id, this_message_id)
        bot.send_message(message.chat.id, START_MESSAGE, reply_markup=create_main_markup(), parse_mode='html')

    @bot.callback_query_handler(func=lambda callback: True)
    def callback_function(callback):
        data = callback.data
        message_id = callback.message.chat.id
        this_message_id = callback.message.message_id
        # Різні callback функції
        if data == 'start':
            bot.delete_message(message_id, this_message_id)
            bot.send_message(message_id, START_MESSAGE, reply_markup=create_main_markup(), parse_mode='html')
        elif data == 'help':
            bot.delete_message(message_id, this_message_id)
            bot.send_message(message_id, HELP_MESSAGE, reply_markup=create_help_markup())
        elif data in QUESTIONS:
            _, response = QUESTIONS[data]
            bot.delete_message(message_id, this_message_id)
            bot.send_message(message_id, response, reply_markup=create_faq_markup(), parse_mode='html')
        elif data == 'contacts':
            bot.delete_message(message_id, this_message_id)
            bot.send_message(message_id, CONTACTS_MESSAGE, reply_markup=create_contacts_markup(), parse_mode='html')
        elif data == 'config':
            bot.send_message(message_id, CONFIG_MESSAGE, reply_markup=create_config_markup())
        elif data == 'customer':
            user_data[message_id]['user_type'] = data
            send_photos_with_message(message_id, Container.get_photoes_containers(), CONFIG_CUSTOMER_MESSAGE,
                                     reply_markup=create_config_customer_markup())
        elif data in Container.get_names_containers():
            user_data[message_id]['container_name'] = data
            if user_data[message_id]['user_type'] == 'customer':
                if data == 'Підземний':
                    send_photos_with_message(message_id, Container.get_all_type_photos_by_name(data),
                                             'У підземного контейнера є 2 типи:\n'
                                             '1️⃣ Зі <strong>збільшеною</strong> сміттєприймальною колонкою на <strong>120л</strong>\n'
                                             '2️⃣ Зі <strong>звичайною</strong> сміттєприймальною колонкою на <strong>50л</strong>\n\n'
                                             'Виберіть тип контейнера:',
                                             create_type_markup(data))
                elif data == 'Напівпідземний':
                    send_photos_with_message(message_id, Container.get_all_type_photos_by_name(data),
                                             'У напівпідземного контейнера є 3 типи:\n'
                                             '1️⃣ З об`ємом бака <strong>2,5 м³</strong>\n'
                                             '2️⃣ З об`ємом бака <strong>3,8 м³</strong>\n'
                                             '3️⃣ З об`ємом бака <strong>5,0 м³</strong>\n\n'
                                             'Виберіть тип контейнера:',
                                             create_type_markup(data))
                else:
                    send_photos_with_message(message_id, Container.get_all_type_photos_by_name(data),
                                             'Виберіть тип контейнера', create_type_markup(data))

            elif user_data[message_id]['user_type'] == 'ra':
                calc_res = user_data[message_id]['container_calc_res_ra'] - user_data[message_id][
                    'container_volume_of_all_orders']
                if data == 'Підземний':
                    container_need_more = Container.get_container_need_more_by_type('1️⃣ 120л', calc_res)
                    send_photos_with_message(message_id, Container.get_all_type_photos_by_name(data),
                                             f"{f'❗️<strong>Для вашого ЖК потрібно {container_need_more} підземних контейнерів будь-якого типу.</strong>\n\n' if container_need_more > 0 else ''}"
                                             f'У підземного контейнера є 2 типи:\n'
                                             f'1️⃣ Зі <strong>збільшеною</strong> сміттєприймальною колонкою на <strong>120л</strong>\n'
                                             f'2️⃣ Зі <strong>звичайною</strong> сміттєприймальною колонкою на <strong>50л</strong>\n\n'
                                             f'Виберіть тип контейнера:',
                                             create_type_markup(data))
                elif data == 'Напівпідземний':
                    container_need_more_2_5 = Container.get_container_need_more_by_type('1️⃣ 2,5 м³', calc_res)
                    container_need_more_3_8 = Container.get_container_need_more_by_type('2️⃣ 3,8 м³', calc_res)
                    container_need_more_5_0 = Container.get_container_need_more_by_type('3️⃣ 5,0 м³', calc_res)
                    send_photos_with_message(message_id, Container.get_all_type_photos_by_name(data),
                                             f"{f'❗️Для вашого ЖК потрібно:'
                                                f'\n<strong>{container_need_more_2_5}</strong> напівпідземних контейнерів з об`ємом бака 2.5 м³ '
                                                f'\nабо'
                                                f'\n<strong>{container_need_more_3_8}</strong> напівпідземних контейнерів з об`ємом бака 3.8 м³ '
                                                f'\nабо'
                                                f'\n<strong>{container_need_more_5_0}</strong> напівпідземних контейнерів з об`ємом бака 5.0 м³.\n\n' if container_need_more_3_8 > 0 or container_need_more_3_8 > 0 or container_need_more_5_0 > 0 else ''}"
                                             f'У напівпідземного контейнера є 4 типи:\n'
                                             f'1️⃣ З об`ємом бака <strong>2,5 м³</strong>\n'
                                             f'2️⃣ З об`ємом бака <strong>3,8 м³</strong>\n'
                                             f'3️⃣ З об`ємом бака <strong>5,0 м³</strong>\n\n'
                                             f'4️⃣ З об`ємом бака <strong>2,5 м³</strong>, та сортуванням скло/пластик.\n\n'
                                             f'Виберіть тип контейнера:',
                                             create_type_markup(data))


        elif data in Container.get_all_types():
            user_data[message_id]['container_type'] = data
            container_name = user_data[message_id]['container_name']
            if container_name == 'Підземний' or container_name == 'Напівпідземний':
                photoes = Container.get_material_photos_by_name(container_name)
                send_photos_with_message(message_id, photoes, 'Виберіть матеріал контейнера',
                                         create_material_markup(container_name))
            else:
                if data == 'Для сміття різних фракцій' or data == 'Для сміття з попільничкою' or data == 'З дерев`яними вставками':
                    max_width = 5
                    if data == 'Для сміття різних фракцій':
                        max_width = 3
                    bot.send_message(message_id, f'✍🏻 Введіть бажану товщину стінки контейнера (Від 2мм до {max_width}мм)')
                    bot.register_next_step_handler(callback.message, get_wall_width)
                else:
                    bot.send_message(message_id, '✍🏻 Введіть кількість контейнерів:')
                    bot.register_next_step_handler(callback.message, get_quantity)


        elif data in Container.get_all_materials():
            user_data[message_id]['container_material'] = data
            if user_data[message_id]['container_name'] != 'Підземний':
                container_type = user_data[message_id]['container_type']
                calc_res = user_data[message_id]['container_calc_res_ra'] - user_data[message_id][
                    'container_volume_of_all_orders']
                container_need_more = Container.get_container_need_more_by_type(container_type, calc_res)
                message = (
                    f'❕Нагадую, для вашого ЖК потрібно {container_need_more} контейнерів обраного типу.\n'
                    if container_need_more > 0
                    else ''
                )
                message += '✍🏻 Введіть кількість контейнерів: '
                bot.send_message(message_id, message)
                bot.register_next_step_handler(callback.message, get_quantity)
            else:
                bot.send_message(message_id,
                                 'У підземних контейнерів є опція датчику наповнення\n'
                                 'Виберіть, чи потрібна вона Вам:',
                                 reply_markup=create_sensor_markup())

        elif data == 'customer_end':
            if callback.from_user.username is None:
                bot.send_message(message_id, 'Будь ласка, введіть ваш номер телефону, щоб наш менеджер міг зв`язатись з вами.')
                bot.register_next_step_handler(callback.message, get_telephone_number)
            else:
                get_all_purchases(callback)
        elif data == 'ra':
            user_id = callback.message.chat.id
            user_data[user_id]['user_type'] = data
            bot.send_message(user_id, CONFIG_RA_AREA_MESSAGE)
            bot.register_next_step_handler(callback.message, get_ra_area)
        elif data == 'true' or data == 'false':
            container_type = user_data[message_id]['container_type']
            calc_res = user_data[message_id]['container_calc_res_ra'] - user_data[message_id][
                'container_volume_of_all_orders']
            container_need_more = Container.get_container_need_more_by_type(container_type, calc_res)
            if data == 'true':
                user_data[message_id]['container_underground_sensor'] = True
            if data == 'false':
                user_data[message_id]['container_underground_sensor'] = False
            message = (
                f'❕Нагадую, для вашого ЖК потрібно {container_need_more} контейнерів обраного типу.\n'
                if container_need_more > 0
                else ''
            )
            message += '✍🏻 Введіть кількість контейнерів: '
            bot.send_message(message_id, message)
            bot.register_next_step_handler(callback.message, get_quantity)

        elif data == 'ar_additional_order':
            calc_res = user_data[message_id]['container_calc_res_ra']
            user_orders_volume = user_data[message_id]['container_volume_of_all_orders']
            container_volume_need = ceil(calc_res - user_orders_volume)
            send_photos_with_message(message_id, [Container.get_photo_by_name('Підземний'),
                                                  Container.get_photo_by_name('Напівпідземний')],
                                     caption=f"{f'❗️<strong>Для вашого ЖК потрібно ще {container_volume_need} м³ об`єму контейнерів.</strong>\n\n' if container_volume_need > 0 else ''}"
                                             f'Виберіть вид контейнера',
                                     reply_markup=create_get_ra_name_markup())
