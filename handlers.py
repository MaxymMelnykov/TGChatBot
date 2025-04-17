from datetime import datetime

from numpy import ceil

from config import (
    ADMIN_ID,
    CONFIG_RA_APARTMENTS_MESSAGE,
    START_MESSAGE,
    TYPE_ERROR_MESSAGE,
    VALUE_ERROR_MESSAGE,
    bot,
)
from Container import Container
from logger import logger
from markups import (
    create_get_ra_name_markup,
    create_main_markup,
    create_main_menu_keyboard,
    create_order_navigation_markup,
)
from user_data import user_data
from utils import calculate_ra_volume_count, clear_user_data, send_photos_with_message


def get_ra_area(message):
    """
    Отримує площу приміщення від користувача та переходить до наступного кроку для введення кількості квартир.

    Args:
        message (Message): Повідомлення від користувача, яке містить площу приміщення.

    Returns:
        - Якщо введено коректну площу, переходимо до наступного етапу.
        - Якщо значення некоректне, з'являється повідомлення про помилку.
    """
    user_id = message.chat.id
    try:
        area = float(message.text)
        user_data[user_id]["area"] = area
        bot.send_message(user_id, CONFIG_RA_APARTMENTS_MESSAGE)
        bot.register_next_step_handler(message, get_ra_apartments)
        logger.info(f"[{user_id}] Введена площа: {area}")
    except ValueError:
        bot.send_message(user_id, VALUE_ERROR_MESSAGE)
        bot.register_next_step_handler(message, get_ra_area)
        logger.exception(f"[{user_id}] Некоректне значення площі: {message.text}")
    except TypeError:
        bot.send_message(user_id, TYPE_ERROR_MESSAGE)
        bot.register_next_step_handler(message, get_ra_area)
        logger.exception(f"[{user_id}] TypeError при введенні площі: {message.text}")


def get_ra_apartments(message):
    """
    Отримує кількість квартир від користувача та обчислює обсяг контейнерів, необхідних для ЖК.

    Args:
        message (Message): Повідомлення від користувача, яке містить кількість квартир.

    Returns:
        - Якщо введено коректну кількість квартир, переходимо до наступного етапу.
        - Якщо значення некоректне, з'являється повідомлення про помилку.
    """
    message_id = message.chat.id
    try:
        apartments = int(message.text)
        user_data[message_id]["apartments"] = apartments
        logger.info(f"[{message_id}] Введена кількість квартир: {apartments}")

        volume = calculate_ra_volume_count(message_id)
        logger.info(f"[{message_id}] Обчислений об'єм контейнерів для ЖК: {volume} м³")
        send_photos_with_message(
            message_id,
            [
                Container.get_photo_by_name("Підземний"),
                Container.get_photo_by_name("Напівпідземний"),
            ],
            caption=f"Для вашого ЖК потрібно <strong>{ceil(volume)} м³</strong> об`єму контейнерів.\n"
                    f"Виберіть вид контейнера",
            reply_markup=create_get_ra_name_markup(),
        )
    except ValueError:
        bot.send_message(message_id, VALUE_ERROR_MESSAGE)
        bot.register_next_step_handler(message, get_ra_apartments)
        logger.exception(f"[{message_id}] Некоректна кількість квартир: {message.text}")
    except TypeError:
        bot.send_message(message_id, TYPE_ERROR_MESSAGE)
        bot.register_next_step_handler(message, get_ra_apartments)
        logger.exeption(f"[{message_id}] Некоректна кількість квартир: {message.text}")


def get_wall_width(message):
    """
    Отримує товщину стінок контейнерів від користувача, перевіряє правильність введених даних.

    Args:
        message (Message): Повідомлення від користувача, яке містить товщину стінок контейнера.

    Returns:
        - Якщо введена некоректна товщина стінок, система просить ввести значення знову.
        - Якщо значення коректне, переходимо до введення кількості контейнерів.
    """
    message_id = message.chat.id
    try:
        width = int(message.text)
        if width < 2 or width > 5:
            bot.send_message(
                message_id,
                "Ви ввели некорректну товщину стінок контейнерів.\n"
                "✍🏻 Введіть бажану товщину стінок контейнерів:",
            )
            bot.register_next_step_handler(message, get_wall_width)
            logger.warning(f"[{message_id}] Некоректна товщина стінки: {width}")
        else:
            user_data[message_id]["container_width"] = width
            logger.info(f"[{message_id}] Введена товщина стінки: {width}")
            bot.send_message(
                message_id, "✍🏻 Введіть бажану кількість контейнерів: "
            )
            bot.register_next_step_handler(message, get_quantity)
    except ValueError:
        bot.send_message(message_id, VALUE_ERROR_MESSAGE)
        bot.register_next_step_handler(message, get_wall_width)
        logger.exception(f"[{message_id}] Некоректна товщина стінки {message.text}")
    except TypeError:
        bot.send_message(message_id, TYPE_ERROR_MESSAGE)
        bot.register_next_step_handler(message, get_wall_width)
        logger.exception(f"[{message_id}] Некоректна товщина стінки {message.text}")


def get_quantity(message):
    """
    Отримує кількість контейнерів від користувача, обчислює загальну вартість замовлення.

    Args:
        message (Message): Повідомлення від користувача, яке містить кількість контейнерів.

    Returns:
        - Якщо введено коректну кількість контейнерів, система розраховує загальну вартість замовлення.
        - Якщо кількість некоректна, з'являється повідомлення про помилку.
    """
    message_id = message.chat.id
    quantity_text = message.text
    try:
        quantity = int(quantity_text)
        logger.info(f"[{message_id} введена кількість контейнерів: {message.text}]")
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
            logger.critical(f"[{message_id} Не знайдено фото для контейнерів]")
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
        logger.critical(f"[{message_id} файл не знайдено {str(e)}]")
    except ValueError:
        bot.send_message(message_id, VALUE_ERROR_MESSAGE)
        bot.register_next_step_handler(message, get_quantity)
        logger.exception(f"[{message_id} Неккоректна кількість контейнерів {message.text}]")
    except TypeError:
        bot.send_message(message_id, TYPE_ERROR_MESSAGE)
        bot.register_next_step_handler(message, get_quantity)
        logger.exception(f"[{message_id} Неккоректна кількість контейнерів {message.text}]")


def get_all_purchases(message):
    """
    Виводить всі покупки користувача та відправляє повідомлення менеджеру про нове замовлення.

    Args:
        message (Message): Повідомлення від користувача.

    Returns:
        - Якщо все нормально - виводить всі замовлення користувача та передає повідомлення менеджеру через notify_admin.
        - Якщо щось пішло не так - виводить повідомлення про помилку.
    """
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


@bot.message_handler(regexp="^🚪 До головного меню$")
def handle_main_menu(message):
    """
    Обробляє запит користувача на повернення до головного меню.

    Args:
        message (Message): Повідомлення від користувача.

    Returns:
        - Повертає користувача до головного меню(через функцію send_main_menu).
    """
    message_id = message.chat.id
    send_main_menu(message_id)


def send_main_menu(user_id):
    """
    Відправляє користувачеві головне меню.

    Args:
        user_id (int): ID користувача, якому потрібно відправити головне меню.

    Returns:
        - Повертає користувача до головного меню
    """
    bot.send_message(
        user_id, START_MESSAGE, reply_markup=create_main_markup(), parse_mode="HTML"
    )


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    phone_number = message.contact.phone_number
    user_name = message.contact.first_name

    user_data[message.chat.id]["telephone_number"] = phone_number
    user_data[message.chat.id]["name"] = user_name

    get_all_purchases(message)


def collect_error_steps(message):
    user_data[message.chat.id] = {'steps': message.text}
    msg = bot.send_message(message.chat.id, "Яку ОС / пристрій ви використовуєте?")
    bot.register_next_step_handler(msg, collect_error_system)


def collect_error_system(message):
    if message.chat.id not in user_data:
        user_data[message.chat.id] = {}
    user_data[message.chat.id]['system'] = message.text
    msg = bot.send_message(message.chat.id, "Прикріпіть скріншот або напищіть будь-що.")
    bot.register_next_step_handler(msg, collect_error_screenshot)


def collect_error_screenshot(message):
    error = user_data.get(message.chat.id, {
        'steps': 'невідомо',
        'system': 'невідомо',
    })

    try:
        if message.content_type == 'photo':
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            screenshot_path = f"resources/errors/{message.chat.id}_{datetime.now().isoformat().replace(':', '-')}.jpg"

            with open(screenshot_path, 'wb') as f:
                f.write(downloaded_file)

            error['screenshot'] = screenshot_path
        else:
            error['screenshot'] = 'не надано'

        log_msg = (
            f"[USER ERROR REPORT] ID: {message.chat.id}\n"
            f"Steps: {error.get('steps')}\n"
            f"System: {error.get('system')}\n"
            f"Screenshot: {error.get('screenshot')}"
        )
        logger.error(log_msg)
        bot.send_message(message.chat.id, "✅ Дякуємо! Повідомлення збережено та передано адміністрації.")
        bot.send_message(ADMIN_ID, log_msg)

    except Exception:
        logger.exception(f"[ERROR REPORT FAIL] Не вдалося обробити скаргу від {message.chat.id}")
        bot.send_message(message.chat.id,
                         "⚠️ Виникла помилка під час обробки. Спробуйте ще раз або зверніться до підтримки.")


def notify_admin(message, orders):
    """
    Відправляє менеджеру повідомлення про нове замовлення від користувача.

    Args:
        message (Message): Повідомлення від користувача, яке містить дані замовлення.
        orders (list): Список замовлених товарів, що включає дані про контейнери та їх кількість.

    Returns:
        - Відправляє повідомлення менеджеру з замовленням користувача, та його контактними даними.
    """
    message_id = message.chat.id

    user_id = message.chat.id
    user_name = user_data[message.chat.id]["name"]
    user_telephone_number = user_data[message_id]["telephone_number"]
    total_sum = user_data[message_id]["total_sum"]
    message_lines = [
        f"<b>🚨 Нове замовлення від клієнта 🚨</b>\n"
        f"<b>🆔 ID користувача: </b> {user_id}\n"
        f"<b>👤 Ім'я користувача: </b> {user_name}\n"
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
    logger.info(f'[{message_id} Менеджеру відправлено повідомлення {message}]')
    # bot.send_message(ADMIN_ID_SECOND, message, parse_mode='HTML')
