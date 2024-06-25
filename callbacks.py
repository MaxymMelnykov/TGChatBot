from handlers import *
from markups import *
from utils import *


def setup_callbacks(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, START_MESSAGE, reply_markup=create_main_markup())

    @bot.callback_query_handler(func=lambda callback: True)
    def callback_function(callback):
        data = callback.data
        message_id = callback.message.chat.id
        this_message_id = callback.message.message_id
        # Різні callback функції
        if data == 'start':
            bot.delete_message(message_id, this_message_id)
            bot.send_message(message_id, START_MESSAGE, reply_markup=create_main_markup())
        elif data == 'help':
            bot.delete_message(message_id, this_message_id)
            bot.send_message(message_id, HELP_MESSAGE, reply_markup=create_help_markup())
        elif data in QUESTIONS:
            _, response = QUESTIONS[data]
            bot.send_message(message_id, response, parse_mode='html')
        elif data == 'contacts':
            bot.send_message(message_id, CONTACTS_MESSAGE, parse_mode='html')
        elif data == 'config':
            bot.send_message(message_id, CONFIG_MESSAGE, reply_markup=create_main_markup())
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
