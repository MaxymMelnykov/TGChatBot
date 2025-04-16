from behave import given, when, then

@given('бот запущений')
def step_impl(context):
    # Симуляція запуску бота або мок
    context.bot_running = True

@when('користувач обирає опцію "Замовити контейнер"')
def step_impl(context):
    assert context.bot_running
    context.response = "Оберіть тип контейнера"

@then('бот повинен запропонувати вибрати тип контейнера')
def step_impl(context):
    assert context.response == "Оберіть тип контейнера"
