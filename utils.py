import os
from math import ceil

from telebot import types

from config import bot
from user_data import user_data


def calculate_volume_count(user_id, volume):
    """
    Обчислює кількість контейнерів на основі результатів розрахунків і об'єму контейнера.

    Args:
        user_id (int): ID користувача.
        volume (float): Об'єм контейнера.

    Returns:
        float: Кількість контейнерів, що можна заповнити заданим об'ємом.
    """
    count = user_data[user_id]["container_calc_res_ra"]
    result = count / volume
    return result


def calculate_ra_volume_count(user_id):
    """
    Обчислює кількість контейнерів для житлового комплексу (ЖК) на основі різних параметрів, таких як площа
    та кількість квартир, а також генерує рекомендації щодо контейнерів для утилізації ПВ.

    Args:
        user_id (int): ID користувача.

    Returns:
        int: Кількість рекомендованих контейнерів для ЖК.
    """
    area = user_data[user_id]["area"]
    apartments = user_data[user_id]["apartments"]

    average_apartment_square = (
        area / apartments
    )  # Середня кількість людей в 1ій квартирі

    one_apartment_people = (
        average_apartment_square - 10.5
    ) / 21  # Скільки людей в одній квартирі

    people_in_ra = ceil(one_apartment_people * apartments)  # Кількість жителів в ЖК

    q = 0.0059  # Добовий  об'єм  утворення  кожного виду ПВ на одного
    k = 1.4  # Добовий  коефіцієнт  нерівномірності  утворення  кожного
    t = 5  # Кількість неробочих днів на рік
    # Максимальний добовий об'єм утворення ТПВ
    qdmax = (q * people_in_ra * 365 / (365 - t)) * k

    period = 1  # Періодичність перевезення кожного виду ПВ, діб,
    repair = 1.05  # Коефіцієнт,  який  враховує  кількість контейнерів, що враховує кількість контейнеів у ремонті

    C = 1  # noqa: N806  # Місткість одного контейнера, куб.м.

    full = 0.9  # коефіцієнт заповнення контейнера.

    # Кількість контейнерів рекомендується визначати за формулою:
    # N = (Qдmax * t * 1, 4 * 1, 05) / (5 * 0, 9)
    N = (qdmax * period * k * repair) / (C * full)  # noqa: N806
    user_data[user_id]["container_calc_res_ra"] = ceil(N)
    return ceil(N)


def send_photos_with_message(chat_id, photo_paths, caption, reply_markup=None):
    """
    Відправляє групу фотографій користувачу з підписом та, за потреби, кнопками.

    Args:
        chat_id (int): ID чату користувача.
        photo_paths (list of str): Список шляхів до фотографій, які потрібно надіслати.
        caption (str): Підпис до фотографій.
        reply_markup (types.ReplyKeyboardMarkup, optional): Клавіатура для відповіді користувача (за замовчуванням None).

    Returns:
        - Повідомлення користувачеві з фотографіями.
    """
    media = []
    open_files = []
    try:
        for photo_path in photo_paths:
            try:
                if not os.path.exists(photo_path) or os.path.getsize(photo_path) == 0:
                    raise FileNotFoundError(
                        f"Файл із зображенням {photo_path} не знайдено або він порожній."
                    )

                photo = open(photo_path, "rb")
                open_files.append(photo)
                media.append(types.InputMediaPhoto(photo))
            except FileNotFoundError as e:
                bot.send_message(chat_id, str(e))
                return

        if media:
            bot.send_media_group(chat_id, media)
            bot.send_message(
                chat_id, caption, reply_markup=reply_markup, parse_mode="html"
            )
    finally:
        for file in open_files:
            file.close()


def clear_user_data(user_id):
    """
    Очищає дані користувача з глобального словника.

    Args:
        user_id (int): ID користувача, чиї дані потрібно очистити.
    """
    if user_id in user_data:
        del user_data[user_id]
