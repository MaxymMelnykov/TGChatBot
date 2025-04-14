import re

from numpy import ceil

from config import (
    ADMIN_ID,
    CONFIG_RA_APARTMENTS_MESSAGE,
    START_MESSAGE,
    VALUE_ERROR_MESSAGE,
    bot,
)
from Container import Container
from markups import (
    create_get_ra_name_markup,
    create_main_markup,
    create_main_menu_keyboard,
    create_order_navigation_markup,
)
from user_data import user_data
from utils import calculate_ra_volume_count, clear_user_data, send_photos_with_message


def get_ra_area(message):
    user_id = message.chat.id
    if message.text is not None:
        try:
            area = float(message.text)
            user_data[user_id]["area"] = area
            bot.send_message(user_id, CONFIG_RA_APARTMENTS_MESSAGE)
            bot.register_next_step_handler(message, get_ra_apartments)
        except ValueError:
            bot.send_message(user_id, VALUE_ERROR_MESSAGE)
            bot.register_next_step_handler(message, get_ra_area)
    else:
        bot.send_message(user_id, VALUE_ERROR_MESSAGE)
        bot.register_next_step_handler(message, get_ra_area)


def get_ra_apartments(message):
    message_id = message.chat.id
    if message.text is not None:
        try:
            apartments = int(message.text)
            user_data[message_id]["apartments"] = apartments
            calculate_ra_volume_count(message_id)
            send_photos_with_message(
                message_id,
                [
                    Container.get_photo_by_name("Підземний"),
                    Container.get_photo_by_name("Напівпідземний"),
                ],
                caption=f"Для вашого ЖК потрібно <strong>{ceil(calculate_ra_volume_count(message_id))} м³</strong> об`єму контейнерів.\n"
                f"Виберіть вид контейнера",
                reply_markup=create_get_ra_name_markup(),
            )
        except ValueError:
            bot.send_message(message_id, VALUE_ERROR_MESSAGE)
            bot.register_next_step_handler(message, get_ra_apartments)
    else:
        bot.send_message(message_id, VALUE_ERROR_MESSAGE)
        bot.register_next_step_handler(message, get_ra_apartments)


def get_wall_width(message):
    message_id = message.chat.id
    if message.text is not None:
        try:
            width = int(message.text)
            if width < 2 or width > 5:
                bot.send_message(
                    message_id,
                    "Ви ввели некорректну товщину стінок контейнерів.\n"
                    "✍🏻 Введіть бажану товщину стінок контейнерів:",
                )
                bot.register_next_step_handler(message, get_wall_width)
            else:
                user_data[message_id]["container_width"] = width
                bot.send_message(
                    message_id, "✍🏻 Введіть бажану кількість контейнерів: "
                )
                bot.register_next_step_handler(message, get_quantity)
        except ValueError:
            bot.send_message(message_id, VALUE_ERROR_MESSAGE)
            bot.register_next_step_handler(message, get_wall_width)
    else:
        bot.send_message(message_id, VALUE_ERROR_MESSAGE)
        bot.register_next_step_handler(message, get_wall_width)


def get_quantity(message):
    message_id = message.chat.id
    quantity_text = message.text

    try:
        quantity = int(quantity_text)
        user_data[message_id]["container_quantity"] = quantity

        container_volume_needed_for_ra = user_data[message_id]["container_calc_res_ra"]

        user_type = user_data[message_id]["user_type"]

        container_name = user_data[message_id]["container_name"]

        container_type = user_data[message_id]["container_type"]

        container_volume = Container.get_volume_by_type(container_type)

        container_material = user_data[message_id]["container_material"]

        container_photo_path = Container.get_photo_by_name(container_name)

        container_underground_sensor = user_data[message_id][
            "container_underground_sensor"
        ]

        container_width = user_data[message_id]["container_width"]

        user_data[message_id]["container_volume_of_all_orders"] += (
            quantity * container_volume
        )
        container_volume_of_all_orders = user_data[message_id][
            "container_volume_of_all_orders"
        ]

        if not container_photo_path:
            raise FileNotFoundError("No photo path found for container.")

        with open(container_photo_path, "rb") as container_photo:
            if container_name == "Підземний" or container_name == "Напівпідземний":
                price_per_unit = Container.get_price_of_container_by_all_data(
                    container_name, container_type, container_material
                )
            else:
                price_per_unit = Container.get_price_by_type(container_type)
            if container_name == "Підземний":
                sensor_cost = 335
                if container_underground_sensor:
                    sensor_message = "✅"
                if not container_underground_sensor:
                    sensor_message = "❌"
                    price_per_unit -= sensor_cost

            total_price = quantity * price_per_unit
            container_volume_need_more = ceil(
                container_volume_needed_for_ra - container_volume_of_all_orders
            )
            optional_message = (
                f"❗️<strong>Для вашого ЖК потрібно ще {container_volume_need_more} м³ контейнерів, бажаєте дозамовити?</strong>\n\n"
                if user_type == "ra" and container_volume_need_more > 0
                else ""
            )
            material_message = (
                f"🧱<b>Матеріал:</b> {container_material}\n"
                if container_name in ["Підземний", "Напівпідземний"]
                else ""
            )
            sensor_message_text = (
                f"📡<b>Сенсор:</b> {sensor_message}\n"
                if container_name == "Підземний"
                else ""
            )
            width_message = (
                f"📏<b>Товщина стінки:</b> {container_width}\n"
                if container_width > 0
                else ""
            )

            # Збираємо основний текст
            message_text = (
                f"{optional_message}"
                f"<b>Ви успішно додали товар до вашого замовлення!</b>\n"
                f"<b>Товар:</b>\n"
                f"🗑 <b>Контейнер:</b> {container_name}\n"
                f"🏷 <b>Тип:</b> {container_type}\n"
                f"{material_message}"
                f"{sensor_message_text}"
                f"{width_message}"
                f"1️⃣<b>Вартість одного</b>: {price_per_unit}\n"
                f"🔢 <b>Кількість:</b> {quantity} шт.\n"
                f"💵 <b>Сума:</b> {total_price} $\n\n"
                f"Ви можете ➕ Доповнити ваше замовлення, або ✔️ Завершити його."
            )

            bot.send_photo(
                message_id,
                container_photo,
                message_text,
                reply_markup=create_order_navigation_markup(message_id),
                parse_mode="html",
            )
            user_data[message_id]["total_sum"] += total_price
            user_data[message_id]["orders"].append(
                {
                    "container_name": container_name,
                    "container_type": container_type,
                    "container_material": container_material,
                    "container_underground_sensor": container_underground_sensor,
                    "container_width": container_width,
                    "quantity": quantity,
                    "total_price": total_price,
                    "photo": container_photo_path,
                }
            )
            user_data[message_id]["container_width"] = 0

    except FileNotFoundError as e:
        bot.send_message(message_id, str(e))
    except ValueError:
        bot.send_message(message_id, VALUE_ERROR_MESSAGE)
        bot.register_next_step_handler(message, get_quantity)


def get_all_purchases(message):
    message_id = message.chat.id
    orders = user_data[message_id].get("orders", [])
    if not isinstance(orders, list):
        bot.send_message(message_id, "Немає даних про замовлення.")
        return

    container_names = []
    container_types = []
    container_materials = []
    container_sensors = []
    container_widths = []
    container_photos = []
    container_quantities = []
    total_sum = user_data[message_id]["total_sum"]

    for order in orders:
        container_names.append(order["container_name"])
        container_types.append(order["container_type"])
        container_materials.append(order["container_material"])
        container_sensors.append(order["container_underground_sensor"])
        container_widths.append(order["container_width"])
        container_quantities.append(order["quantity"])
        container_photos.append(order["photo"])

    notify_admin(message, orders)

    message_lines = [
        "<b>🎉Вітаємо, Ви успішно створили нове замовлення!</b>\n"
        "Очікуйте на повідомлення від нашого менеджера\n\n"
        "<b>Ваше замовлення:</b>",
        f"<b>💵 Загальна сума:</b> від {total_sum} $",
        "----------------------------------------",
    ]

    for idx, order in enumerate(orders, start=1):
        if order["container_name"] == "Підземний":
            if order["container_underground_sensor"]:
                sensor_message = "✅"
            else:
                sensor_message = "❌"
            message_lines.append(
                f"№{idx}:\n"
                f"🗑 <b>Контейнер:</b>  {order['container_name']}\n"
                f"🏷 <b>Тип:</b>  {order['container_type']}\n"
                f"🧱 <b>Матеріал:</b>  {order['container_material']}\n"
                f"📡 <b>Сенсор:</b>  {sensor_message}\n"
                f"1️⃣ <b>Ціна за контейнер:</b> від {order['total_price'] / order['quantity']} $\n"
                f"🔢 <b>Кількість:</b>  {order['quantity']} шт.\n"
                f"💵 <b>Сума:</b>  від {order['total_price']} $\n"
                "----------------------------------------"
            )
        elif order["container_name"] == "Напівпідземний":
            message_lines.append(
                f"№{idx}:\n"
                f"🗑 <b>Контейнер:</b>  {order['container_name']}\n"
                f"🏷 <b>Тип:</b>  {order['container_type']}\n"
                f"🧱 <b>Матеріал:</b>  {order['container_material']}\n"
                f"1️⃣ <b>Ціна за контейнер:</b> від {order['total_price'] / order['quantity']} $\n"
                f"🔢 <b>Кількість:</b>  {order['quantity']} шт.\n"
                f"💵 <b>Сума:</b>  від {order['total_price']} $\n"
                "----------------------------------------"
            )
        else:
            container_width_text = (
                f"📏 <b>Товщина стінки:</b> {order['container_width']}\n"
                if order["container_width"] > 0
                else ""
            )

            message_lines.append(
                f"№{idx}:\n"
                f"🗑 <b>Контейнер:</b>  {order['container_name']}\n"
                f"🏷 <b>Тип:</b>  {order['container_type']}\n"
                f"{container_width_text}"
                f"1️⃣ <b>Ціна за контейнер:</b> від {order['total_price'] / order['quantity']} $\n"
                f"🔢 <b>Кількість:</b>  {order['quantity']} шт.\n"
                f"💵 <b>Сума:</b>  від {order['total_price']} $\n"
                "----------------------------------------"
            )

            message_lines.append(
                'Натисніть "🚪 До головного меню", щоб перейти до головного меню.'
            )
    message = "\n".join(message_lines)
    send_photos_with_message(
        message_id, container_photos, message, create_main_menu_keyboard()
    )

    clear_user_data(message_id)


def get_telephone_number(message):  # TODO: Поменять на отправку контакта пользователем
    message_id = message.chat.id
    ua_phone_regex = re.compile(r"^\+?380\d{9}$|^0\d{9}$")
    if message.text is not None:
        if ua_phone_regex.match(message.text):
            user_data[message_id]["telephone_number"] = message.text
            get_all_purchases(message)
        else:
            bot.send_message(
                message_id, "Введіть корректний номер телефону, будь ласка."
            )
            bot.register_next_step_handler(message, get_telephone_number)
    else:
        bot.send_message(message_id, "Введіть корректний номер телефону, будь ласка.")
        bot.register_next_step_handler(message, get_telephone_number)


@bot.message_handler(regexp="^🚪 До головного меню$")
def handle_main_menu(message):
    message_id = message.chat.id
    send_main_menu(message_id)


def send_main_menu(user_id):
    bot.send_message(
        user_id, START_MESSAGE, reply_markup=create_main_markup(), parse_mode="HTML"
    )


# Відправлення менеджеру повідомлення про нове замовлення.
def notify_admin(message, orders):
    message_id = message.chat.id

    user_id = message.chat.id
    user_username = message.from_user.username
    user_name = message.from_user.first_name or "Невідоме"
    user_telephone_number = user_data[message_id]["telephone_number"]
    total_sum = user_data[message_id]["total_sum"]
    message_lines = [
        f"<b>🚨 Нове замовлення від клієнта 🚨</b>\n"
        f"<b>🆔 ID користувача: </b> {user_id}\n"
        f"<b>👤 Ім'я користувача: </b> {user_name}\n"
        f"<b>📧 Username користувача: </b> @{user_username}\n"
        f"<b>📱 Моб телефон користувача: </b> {user_telephone_number}\n",
        f"<b>💵 Загальна сума:</b> від {total_sum} $",
        "-----------------------------------------",
    ]

    for idx, order in enumerate(orders, start=1):
        if order["container_name"] == "Підземний":
            if order["container_underground_sensor"]:
                sensor_message = "✅"
            else:
                sensor_message = "❌"
            message_lines.append(
                f"№{idx}:\n"
                f"🗑 Контейнер: {order['container_name']}\n"
                f"🏷 Тип: {order['container_type']}\n"
                f"🧱 Матеріал: {order['container_material']}\n"
                f"📡 Сенсор: {sensor_message}\n"
                f"1️⃣ Ціна за контейнер: від {order['total_price'] / order['quantity']} $\n"
                f"🔢 Кількість: {order['quantity']} шт.\n"
                f"💵 Сума: від {order['total_price']} $\n"
                "-----------------------------------------"
            )
        elif order["container_name"] == "Напівпідземний":
            message_lines.append(
                f"№{idx}:\n"
                f"🗑Контейнер: {order['container_name']}\n"
                f"🏷Тип: {order['container_type']}\n"
                f"🧱Матеріал: {order['container_material']}\n"
                f"1️⃣Ціна за контейнер: від {order['total_price'] / order['quantity']} $\n"
                f"🔢Кількість: {order['quantity']} шт.\n"
                f"💵Сума: від {order['total_price']} $\n"
                "-----------------------------------------"
            )
        else:
            container_width_text = (
                f"📏 <b>Товщина стінки:</b> {order['container_width']}\n"
                if order["container_width"] > 0
                else ""
            )

            message_lines.append(
                f"№{idx}:\n"
                f"🗑 <b>Контейнер:</b>  {order['container_name']}\n"
                f"🏷 <b>Тип:</b>  {order['container_type']}\n"
                f"{container_width_text}"
                f"1️⃣ <b>Ціна за контейнер:</b> від {order['total_price'] / order['quantity']} $\n"
                f"🔢 <b>Кількість:</b>  {order['quantity']} шт.\n"
                f"💵 <b>Сума:</b>  від {order['total_price']} $\n"
                "----------------------------------------"
            )

    message = "\n".join(message_lines)

    bot.send_message(ADMIN_ID, message, parse_mode="HTML")
    # bot.send_message(ADMIN_ID_SECOND, message, parse_mode='HTML')
