from behave import *
from user_data import user_data
from handlers import get_ra_area, get_ra_apartments

use_step_matcher("re")

@given("Користувач почав взаємодію з ботом")
def step_impl(context):
    context.chat_id = "516166196"

# Використовуємо регулярний вираз для захоплення площі
@when(r'Користувач вводить площу "(?P<area>\d+)"')
def step_impl(context, area):
    message_area = type('obj', (object,), {"chat": type('obj', (object,), {"id": context.chat_id}), "text": area})
    get_ra_area(message_area)


@then(r'Площа повинна бути збережена в системі як "(?P<area>\d+)"')
def step_impl(context, area):
    assert user_data[context.chat_id]['area'] == float(area), f"Очікувана площа {area}, але отримано {user_data[context.chat_id]['area']}"


@when(r'Користувач вводить кількість квартир "(?P<apartments>\d+)"')
def step_impl(context, apartments):
    message_apartments = type('obj', (object,), {"chat": type('obj', (object,), {"id": context.chat_id}), "text": apartments})
    get_ra_apartments(message_apartments)


@then(r'Кількість квартир повинна бути збережена в системі як "(?P<apartments>\d+)"')
def step_impl(context, apartments):
    assert user_data[context.chat_id]['apartments'] == int(apartments), f"Очікувана кількість квартир = {apartments}, але отримано {user_data[context.chat_id]['apartments']}"

@then('Кількість контейнерів має бути "(?P<calc_res>.+)"')
def step_impl(context, calc_res):
    assert user_data[context.chat_id]['container_calc_res_ra'] == int(calc_res), f"Очікувана кількість контейнерів для ЖК = {calc_res}, але отримано {user_data[context.chat_id]['container_calc_res_ra']}"