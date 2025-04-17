from collections import defaultdict

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
             'container_width': 0,  # Товщина стінки контейнера
             'telephone_number': None,
             'username': None,
             'name': None,
             'orders': [],
             'total_sum': 0})
"""
Словник за замовчуванням для зберігання даних користувачів.

Використовує `defaultdict` з лямбда-функцією, яка ініціалізує кожного користувача з набором значень за замовчуванням.

Attributes:
    user_type (str or None): Тип користувача, наприклад, 'замовник' або 'представник ЖК'.
    container_calc_res_ra (int): Результат розрахунку для контейнера.
    container_volume_of_all_orders (int): Загальний об'єм всіх замовлених контейнерів.
    area (str or None): Площа, яку обслуговує користувач.
    apartments (str or None): Кількість квартир, пов'язаних з користувачем.
    container_name (str or None): Назва контейнера.
    container_type (str or None): Тип контейнера.
    container_material (str or None): Матеріал контейнера.
    container_quantity (int): Кількість контейнерів.
    container_underground_sensor (bool): Наявність сенсора у підземного контейнера.
    container_width (int): Товщина стінки контейнера.
    telephone_number (str or None): Номер телефону користувача.
    orders (list): Список замовлень користувача.
    total_sum (float): Загальна сума всіх замовлень користувача.

Returns:
    defaultdict: Об'єкт `defaultdict`, який автоматично ініціалізує нові записи з вказаними значеннями за замовчуванням.
"""
