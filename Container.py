from math import ceil


class Container:
    containers = []

    def __init__(self, container_name, name_photo, container_material, material_photo, container_type,container_type_photo, volume, price):
        self.container_name = container_name
        self.name_photo = name_photo
        self.container_material = container_material
        self.material_photo = material_photo
        self.container_type = container_type
        self.container_type_photo = container_type_photo
        self.volume = volume
        self.price = price
        Container.containers.append(self)

    def __str__(self):
        return f"{self.container_name}, {self.container_type}: {self.price} грн"
    @staticmethod
    def get_material_photos_by_name(container_name):
        material_photoes = []
        for container in Container.containers:
            if container.container_name == container_name:
                if container.material_photo not in material_photoes:
                    material_photoes.append(container.material_photo)
        return material_photoes
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
        photo = ''
        for container in Container.containers:
            if container.container_name == container_name:
                photo = container.name_photo
        return photo

    @staticmethod
    def get_materials_by_name(container_name):
        materials = []
        for container in Container.containers:
            if container.container_name == container_name:
                if container.container_material not in materials:
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

    @staticmethod
    def get_container_need_more_by_type(container_type,calc_res):
        container_need_more = 0
        if container_type == '1️⃣ 120л' or container_type == '2️⃣ 50л' or container_type == '3️⃣ 5,0 м³':
            container_need_more = ceil(calc_res / 5.0)
        elif container_type == '1️⃣ 2,5 м³' or container_type == '4️⃣ 2,5 м³, для сортування':
            container_need_more = ceil(calc_res / 2.5)
        elif container_type == '2️⃣ 3,8 м³':
            container_need_more = ceil(calc_res / 3.8)
        return container_need_more

# Приклад додавання контейнерів
Container('Підземний', './resources/name_photo/pidzemniy.jpg', 'Сталь нержавіюча','./resources/material_photo/stal_nerzha.jpg', '1️⃣ 120л','./resources/type_photo/pidzemniy_type_big.jpg', 5, 7000)
Container('Підземний', './resources/name_photo/pidzemniy.jpg', 'Сталь оцинкована','./resources/material_photo/stal_ocink.jpg', '1️⃣ 120л','./resources/type_photo/pidzemniy_type_big.jpg', 5, 7000)
Container('Підземний', './resources/name_photo/pidzemniy.jpg', 'Сталь нержавіюча','./resources/material_photo/stal_nerzha.jpg', '2️⃣ 50л','./resources/type_photo/pidzemniy_type_normal.jpg', 5, 7200)
Container('Підземний', './resources/name_photo/pidzemniy.jpg', 'Сталь оцинкована','./resources/material_photo/stal_ocink.jpg', '2️⃣ 50л','./resources/type_photo/pidzemniy_type_normal.jpg', 5, 7200)
Container('Напівпідземний', './resources/name_photo/napivpidzemniy.jpg', 'Сталь нержавіюча перфорована','./resources/material_photo/stal_nerzha_perf.jpg', '1️⃣ 2,5 м³','./resources/type_photo/napivpidzemniy_type_25.jpg', 2.5, 2800)
Container('Напівпідземний', './resources/name_photo/napivpidzemniy.jpg', 'Сталь нержавіюча перфорована','./resources/material_photo/stal_nerzha_perf.jpg', '2️⃣ 3,8 м³','./resources/type_photo/napivpidzemniy_type_38.jpg', 3.8, 3800)
Container('Напівпідземний', './resources/name_photo/napivpidzemniy.jpg', 'Сталь нержавіюча перфорована','./resources/material_photo/stal_nerzha_perf.jpg', '3️⃣ 5,0 м³','./resources/type_photo/napivpidzemniy_type_50.jpg', 5.0, 4550)
Container('Напівпідземний', './resources/name_photo/napivpidzemniy.jpg', 'Сталь нержавіюча перфорована','./resources/material_photo/stal_nerzha_perf.jpg', '4️⃣ 2,5 м³, для сортування','./resources/type_photo/napivpidzemniy_type_sort.jpg', 2.5, 3200)
Container('Напівпідземний', './resources/name_photo/napivpidzemniy.jpg', 'Профіль настил кольоровий','./resources/material_photo/profnastyl.jpg', '1️⃣ 2,5 м³','./resources/type_photo/napivpidzemniy_type_25.jpg', 2.5, 2800)
Container('Напівпідземний', './resources/name_photo/napivpidzemniy.jpg', 'Профіль настил кольоровий','./resources/material_photo/profnastyl.jpg', '2️⃣ 3,8 м³','./resources/type_photo/napivpidzemniy_type_38.jpg', 3.8, 3800)
Container('Напівпідземний', './resources/name_photo/napivpidzemniy.jpg', 'Профіль настил кольоровий','./resources/material_photo/profnastyl.jpg', '3️⃣ 5,0 м³','./resources/type_photo/napivpidzemniy_type_50.jpg', 5.0, 4550)
Container('Напівпідземний', './resources/name_photo/napivpidzemniy.jpg', 'Профіль настил кольоровий','./resources/material_photo/profnastyl.jpg', '4️⃣ 2,5 м³, для сортування','./resources/type_photo/napivpidzemniy_type_sort.jpg', 2.5, 3200)
Container('Напівпідземний', './resources/name_photo/napivpidzemniy.jpg', 'Деревина різних порід','./resources/material_photo/derevyna_rizn_porid.jpg', '1️⃣ 2,5 м³','./resources/type_photo/napivpidzemniy_type_25.jpg', 2.5, 2800)
Container('Напівпідземний', './resources/name_photo/napivpidzemniy.jpg', 'Деревина різних порід','./resources/material_photo/derevyna_rizn_porid.jpg', '2️⃣ 3,8 м³','./resources/type_photo/napivpidzemniy_type_38.jpg', 3.8, 3800)
Container('Напівпідземний', './resources/name_photo/napivpidzemniy.jpg', 'Деревина різних порід','./resources/material_photo/derevyna_rizn_porid.jpg', '3️⃣ 5,0 м³','./resources/type_photo/napivpidzemniy_type_50.jpg', 5.0, 4550)
Container('Напівпідземний', './resources/name_photo/napivpidzemniy.jpg', 'Деревина різних порід','./resources/material_photo/derevyna_rizn_porid.jpg', '4️⃣ 2,5 м³, для сортування','./resources/type_photo/napivpidzemniy_type_sort.jpg', 2.5, 3200)
Container('Сортувальний', './resources/name_photo/sortyvalniy.jpg', 'Матеріал','', '3в1 330 літрів','./resources/type_photo/sortyvalniy_3v1_330.jpg', 0, 860)
Container('Сортувальний', './resources/name_photo/sortyvalniy.jpg', 'Матеріал','', '3в1 540 літрів','./resources/type_photo/sortyvalniy_3v1_540.jpg', 0, 950)
Container('Сортувальний', './resources/name_photo/sortyvalniy.jpg', 'Матеріал','', 'Дзвін','./resources/type_photo/sortyvalniy_dzvin.jpg', 0, 690)
Container('Сортувальний', './resources/name_photo/sortyvalniy.jpg', 'Матеріал','', 'Трапеція','./resources/type_photo/sortyvalniy_trap.jpg', 0, 660)
Container('Для небезпечних відходів', './resources/name_photo/dlya_nebezpech.jpg', 'Матеріал','',  'Звичайний','./resources/type_photo/dlya_nebezpech_standart.jpg',0, 370)
Container('Для небезпечних відходів', './resources/name_photo/dlya_nebezpech.jpg', 'Матеріал','',  'Сіті-Лайт','./resources/type_photo/dlya_nebezpech_city_light.jpg',0, 1810)
Container('Вулична урна', './resources/name_photo/vylurna.jpg', 'Матеріал','', 'Для сміття різних фракцій','./resources/type_photo/vylurn_rizn_frac.jpg', 0, 215)
Container('Вулична урна', './resources/name_photo/vylurna.jpg', 'Матеріал','', 'Для сміття з попільничкою','./resources/type_photo/vylurn_with_popil.jpg', 0, 260)
Container('Вулична урна', './resources/name_photo/vylurna.jpg', 'Матеріал','', 'З дерев`яними вставками','./resources/type_photo/vylurn_with_der.jpg', 0, 250)
Container('Вулична урна', './resources/name_photo/vylurna.jpg', 'Матеріал','','Для використаних стаканчиків','./resources/type_photo/vylurn_for_stakan.jpg', 0, 75)
