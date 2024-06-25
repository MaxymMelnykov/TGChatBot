from markups import *
from utils import *


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
