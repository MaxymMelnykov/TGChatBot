class Container:
    containers = []

    def __init__(self, container_name, container_type, price):
        self.container_name = container_name
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
        price = 0
        for container in Container.containers:
            if container.container.type == container_type:
                price = container.price
        return price



Container('Підземний', 'Збільшена', 100)
Container('Підземний', 'Стандартна', 100)
Container('Напівпідземний', 'Профіль настил кольоровий', 150)
Container('Напівпідземний', 'Сталь нержавіюча перфорована', 150)
Container('Напівпідземний', 'Деревина різних порід', 150)
Container('Сортувальний', '3в1 330 літрів', 120)
Container('Сортувальний', '3в1 540 літрів', 120)
Container('Сортувальний', 'Дзвін', 120)
Container('Сортувальний', 'Трапеція', 120)
Container('Для небезпечних відходів', 'Звичайний', 120)
Container('Для небезпечних відходів', 'Сіті-Лайт', 120)
Container('Вулична урна', 'Для сміття різних фракцій', 120)
Container('Вулична урна', 'Для сміття з попільничкою', 120)
Container('Вулична урна', 'З дерев`яними вставками', 120)
Container('Вулична урна', 'Для використаних стаканчиків', 120)

print("Все контейнеры:")
for container in Container.get_containers():
    print(container)
