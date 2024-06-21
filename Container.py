class Container:
    containers = []

    def __init__(self, container_name, name_photo, container_material, container_type,container_type_photo, volume, price):
        self.container_name = container_name
        self.name_photo = name_photo
        self.container_material = container_material
        #self.material_photo = './resources/materials.jpg' # Потом возможно поменять если будут фото других материалов
        self.container_type = container_type
        self.container_type_photo = container_type_photo
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
    @staticmethod
    def get_photo_by_type(container_type):
        photo = ''
        for container in Container.containers:
            if container.container_type == container_type:
                photo = container.container_type_photo
        return photo
    @staticmethod
    def get_all_type_photos_by_name(container_name):
        photoes = []
        types = Container.get_types_by_name(container_name)
        for type in types:
            photoes.append(Container.get_photo_by_type(type))
        return photoes


# Приклад додавання контейнерів
Container('Підземний', './resources/pidzemniy.jpg', 'Профіль настил кольоровий', 'Збільшена (120л)','./resources/pidzemniy_type_big.jpg', 5, 100)
Container('Підземний', './resources/pidzemniy.jpg', 'Сталь нержавіюча перфорована', 'Збільшена (120л)','./resources/pidzemniy_type_big.jpg', 5, 100)
Container('Підземний', './resources/pidzemniy.jpg', 'Деревина різних порід', 'Збільшена (120л)','./resources/pidzemniy_type_big.jpg', 5, 100)
Container('Підземний', './resources/pidzemniy.jpg', 'Профіль настил кольоровий', 'Звичайна (50л)','./resources/pidzemniy_type_normal.jpg', 5, 100)
Container('Підземний', './resources/pidzemniy.jpg', 'Сталь нержавіюча перфорована', 'Звичайна (50л)','./resources/pidzemniy_type_normal.jpg', 5, 100)
Container('Підземний', './resources/pidzemniy.jpg', 'Деревина різних порід', 'Звичайна (50л)','./resources/pidzemniy_type_normal.jpg', 5, 100)
Container('Напівпідземний', './resources/napivpidzemniy.jpg', 'Профіль настил кольоровий', 'Об`єм 2,5 м^3','./resources/napivpidzemniy_type_25.jpg', 2.5, 150)
Container('Напівпідземний', './resources/napivpidzemniy.jpg', 'Профіль настил кольоровий', 'Об`єм 3,8 м^3','./resources/napivpidzemniy_type_38.png', 3.8, 200)
Container('Напівпідземний', './resources/napivpidzemniy.jpg', 'Профіль настил кольоровий', 'Об`єм 5.0 м^3','./resources/napivpidzemniy_type_50.jpg', 5.0, 300)
Container('Напівпідземний', './resources/napivpidzemniy.jpg', 'Сталь нержавіюча перфорована', 'Об`єм 2,5 м^3','./resources/napivpidzemniy_type_25.jpg', 2.5, 200)
Container('Напівпідземний', './resources/napivpidzemniy.jpg', 'Сталь нержавіюча перфорована', 'Об`єм 3,8 м^3','./resources/napivpidzemniy_type_38.png', 3.8, 250)
Container('Напівпідземний', './resources/napivpidzemniy.jpg', 'Сталь нержавіюча перфорована', 'Об`єм 5.0 м^3','./resources/napivpidzemniy_type_50.jpg', 5.0, 350)
Container('Напівпідземний', './resources/napivpidzemniy.jpg', 'Деревина різних порід', 'Об`єм 2,5 м^3','./resources/napivpidzemniy_type_25.jpg', 2.5, 150)
Container('Напівпідземний', './resources/napivpidzemniy.jpg', 'Деревина різних порід', 'Об`єм 3,8 м^3','./resources/napivpidzemniy_type_38.png', 3.8, 250)
Container('Напівпідземний', './resources/napivpidzemniy.jpg', 'Деревина різних порід', 'Об`єм 5.0 м^3','./resources/napivpidzemniy_type_50.jpg', 5.0, 350)
Container('Сортувальний', './resources/sortyvalniy.png', 'Матеріал', '3в1 330 літрів','./resources/sortyvalniy_3v1_330.png', 0, 120)
Container('Сортувальний', './resources/sortyvalniy.png', 'Матеріал', '3в1 540 літрів','./resources/sortyvalniy_3v1_540.png', 0, 120)
Container('Сортувальний', './resources/sortyvalniy.png', 'Матеріал', 'Дзвін','./resources/sortyvalniy_dzvin.png', 0, 120)
Container('Сортувальний', './resources/sortyvalniy.png', 'Матеріал', 'Трапеція','./resources/sortyvalniy_trap.png', 0, 120)
Container('Для небезпечних відходів', './resources/dlya_nebezpech.png', 'Матеріал',  'Звичайний','./resources/dlya_nebezpech_standart.png',0, 120)
Container('Для небезпечних відходів', './resources/dlya_nebezpech.png', 'Матеріал',  'Сіті-Лайт','./resources/dlya_nebezpech_city_light.png',0, 120)
Container('Вулична урна', './resources/vylurna.png', 'Матеріал', 'Для сміття різних фракцій','.resources/vylurn_rizn_frac.png', 0, 120)
Container('Вулична урна', './resources/vylurna.png', 'Матеріал', 'Для сміття з попільничкою','./resources/vylurn_with_popil.png', 0, 120)
Container('Вулична урна', './resources/vylurna.png', 'Матеріал', 'З дерев`яними вставками','./resources/vylurn_with_der.png', 0, 120)
Container('Вулична урна', './resources/vylurna.png', 'Матеріал', 'Для використаних стаканчиків','./resources/vylurn_rizn_frac.png', 0, 120)

print(Container.get_photo_by_name('Сортувальний'))

print("Все контейнеры:")
for container in Container.get_containers():
    print(container)
