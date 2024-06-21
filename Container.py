class Container:
    containers = []

    def __init__(self, container_name, name_photo, container_material, container_type, volume, price):
        self.container_name = container_name
        self.name_photo = name_photo
        self.container_material = container_material
        #self.material_photo = './resources/materials.jpg' # Потом возможно поменять если будут фото других материалов
        self.container_type = container_type
        self.volume = volume
        self.price = price
        Container.containers.append(self)

    def __str__(self):
        return f"{self.container_name}, {self.container_type}: {self.price} грн"
    @staticmethod
    def get_material_photo():
        return './resources/materials.jpg' # Потом возможно поменять если будут фото других материалов
    @staticmethod
    def get_containers():
        return Container.containers

    @staticmethod
    def get_types_by_name(container_name):
        types = []
        for container in Container.containers:
            if container.container_name == container_name:
                if container.container_type not in types:
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
    def get_all_materials():
        materials = []
        for container in Container.containers:
            materials.append(container.container_material)
        return materials

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

    @staticmethod
    def get_materials_by_type(container_type):
        materials = []
        for container in Container.containers:
            if container.container_type == container_type:
                materials.append(container.container_material)
        return materials

    @staticmethod
    def get_price_of_container_by_all_data(container_name, container_type, container_material):
        price_of_container = 0
        for container in Container.containers:
            if container.container_name == container_name:
                if container.container_type == container_type:
                    if container.container_material == container_material:
                        price_of_container = container.price
        return price_of_container
    @staticmethod
    def get_volume_by_type(container_type):
        volume = 0
        for container in Container.containers:
            if container.container_type == container_type:
                volume = container.volume
        return volume


# Приклад додавання контейнерів
Container('Підземний', './resources/pidzemniy.png', 'Профіль настил кольоровий', 'Збільшена (120л)', 5, 100)
Container('Підземний', './resources/pidzemniy.png', 'Сталь нержавіюча перфорована', 'Збільшена (120л)', 5, 100)
Container('Підземний', './resources/pidzemniy.png', 'Деревина різних порід', 'Збільшена (120л)', 5, 100)
Container('Підземний', './resources/pidzemniy.png', 'Профіль настил кольоровий', 'Звичайна (50л)', 5, 100)
Container('Підземний', './resources/pidzemniy.png', 'Сталь нержавіюча перфорована', 'Звичайна (50л)', 5, 100)
Container('Підземний', './resources/pidzemniy.png', 'Деревина різних порід', 'Звичайна (50л)', 5, 100)
Container('Напівпідземний', './resources/pivpidzemniy.png', 'Профіль настил кольоровий', 'Об`єм 2,5 м^3', 2.5, 150)
Container('Напівпідземний', './resources/pivpidzemniy.png', 'Профіль настил кольоровий', 'Об`єм 3,8 м^3', 3.8, 200)
Container('Напівпідземний', './resources/pivpidzemniy.png', 'Профіль настил кольоровий', 'Об`єм 5.0 м^3', 5.0, 300)
Container('Напівпідземний', './resources/pivpidzemniy.png', 'Сталь нержавіюча перфорована', 'Об`єм 2,5 м^3', 2.5, 200)
Container('Напівпідземний', './resources/pivpidzemniy.png', 'Сталь нержавіюча перфорована', 'Об`єм 3,8 м^3', 3.8, 250)
Container('Напівпідземний', './resources/pivpidzemniy.png', 'Сталь нержавіюча перфорована', 'Об`єм 5.0 м^3', 5.0, 350)
Container('Напівпідземний', './resources/pivpidzemniy.png', 'Деревина різних порід', 'Об`єм 2,5 м^3', 2.5, 150)
Container('Напівпідземний', './resources/pivpidzemniy.png', 'Деревина різних порід', 'Об`єм 3,8 м^3', 3.8, 250)
Container('Напівпідземний', './resources/pivpidzemniy.png', 'Деревина різних порід', 'Об`єм 5.0 м^3', 5.0, 350)
Container('Сортувальний', './resources/sortyvalniy.png', 'Матеріал', '3в1 330 літрів', 0, 120)
Container('Сортувальний', './resources/sortyvalniy.png', 'Матеріал', '3в1 540 літрів', 0, 120)
Container('Сортувальний', './resources/sortyvalniy.png', 'Матеріал', 'Дзвін', 0, 120)
Container('Сортувальний', './resources/sortyvalniy.png', 'Матеріал', 'Трапеція', 0, 120)
Container('Для небезпечних відходів', './resources/kontainer for nebezpech.png', 'Матеріал', 0, 'Звичайний', 120)
Container('Для небезпечних відходів', './resources/kontainer for nebezpech.png', 'Матеріал', 0, 'Сіті-Лайт', 120)
Container('Вулична урна', './resources/vylurna.png', 'Матеріал', 'Для сміття різних фракцій', 0, 120)
Container('Вулична урна', './resources/vylurna.png', 'Матеріал', 'Для сміття з попільничкою', 0, 120)
Container('Вулична урна', './resources/vylurna.png', 'Матеріал', 'З дерев`яними вставками', 0, 120)
Container('Вулична урна', './resources/vylurna.png', 'Матеріал', 'Для використаних стаканчиків', 0, 120)

print(Container.get_photo_by_name('Сортувальний'))

print("Все контейнеры:")
for container in Container.get_containers():
    print(container)
