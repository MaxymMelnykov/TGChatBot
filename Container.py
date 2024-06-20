class Container:
    containers = []

    def __init__(self, container_name, name_photo, container_type, price):
        self.container_name = container_name
        self.name_photo = name_photo
        self.container_type = container_type
        self.price = price
        Container.containers.append(self)

    def __str__(self):
        return f"{self.container_name}, {self.container_type}: {self.price} грн"

    @staticmethod
    def get_containers():
        return Container.containers

    @staticmethod
    def get_types_by_name(container_name):
        types = []
        for container in Container.containers:
            if container.container_name == container_name:
                types.append(container.container_type)
        return types

    @staticmethod
    def get_names_containers():
        names = []
        for container in Container.containers:
            names.append(container.container_name)
        return names

    @staticmethod
    def get_price_by_type(container_type):
        for container in Container.containers:
            if container.container_type == container_type:
                return container.price
        return 0

    @staticmethod
    def get_all_types():
        types = []
        for container in Container.containers:
            types.append(container.container_type)
        return types

    @staticmethod
    def get_photoes_containers():
        photoes = []
        for container in Container.containers:
            if container.name_photo not in photoes:
                photoes.append(container.name_photo)
        return photoes

    @staticmethod
    def get_photo_by_name(container_name):
        print(f"Ищем фото для контейнера: {container_name}")  # Добавьте логирование для отладки
        for container in Container.containers:
            if container.container_name == container_name:
                print(f"Найдено фото: {container.name_photo}")  # Логирование найденного фото
                return container.name_photo
        print("Контейнер не найден, возвращаем значение по умолчанию")
        return "фывфв"


# Приклад додавання контейнерів
Container('Підземний', './resources/pidzemniy.png', 'Збільшена', 100)
Container('Підземний', './resources/pidzemniy.png', 'Стандартна', 100)
Container('Напівпідземний', './resources/pivpidzemniy.png', 'Профіль настил кольоровий', 150)
Container('Напівпідземний', './resources/pivpidzemniy.png', 'Сталь нержавіюча перфорована', 150)
Container('Напівпідземний', './resources/pivpidzemniy.png', 'Деревина різних порід', 150)
Container('Сортувальний', './resources/sortyvalniy.png', '3в1 330 літрів', 120)
Container('Сортувальний', './resources/sortyvalniy.png', '3в1 540 літрів', 120)
Container('Сортувальний', './resources/sortyvalniy.png', 'Дзвін', 120)
Container('Сортувальний', './resources/sortyvalniy.png', 'Трапеція', 120)
Container('Для небезпечних відходів', './resources/kontainer for nebezpech.png', 'Звичайний', 120)
Container('Для небезпечних відходів', './resources/kontainer for nebezpech.png', 'Сіті-Лайт', 120)
Container('Вулична урна', './resources/vylurna.png', 'Для сміття різних фракцій', 120)
Container('Вулична урна', './resources/vylurna.png', 'Для сміття з попільничкою', 120)
Container('Вулична урна', './resources/vylurna.png', 'З дерев`яними вставками', 120)
Container('Вулична урна', './resources/vylurna.png', 'Для використаних стаканчиків', 120)

print(Container.get_photo_by_name('Сортувальний'))

print("Все контейнеры:")
for container in Container.get_containers():
    print(container)
