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
             'orders': [],
             'total_sum': 0})