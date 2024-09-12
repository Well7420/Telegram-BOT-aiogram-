from aiogram.types import BotCommand

private = [
    BotCommand(command='menu', description='Переглянути меню'),
    BotCommand(command='about', description='Адреса піцерії'),
    BotCommand(command='order', description='Створити замовлення'),
    BotCommand(command='status', description='Статус замовлення'),
    BotCommand(command='delivery', description='Варіанти доставки'),
    BotCommand(command='payment', description='Варіанти оплати')
]