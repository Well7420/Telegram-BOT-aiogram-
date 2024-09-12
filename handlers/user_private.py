from aiogram import F, types, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards import reply

UP_Router = Router()

class Order(StatesGroup): # клас для створення замовлення
    name = State()
    pizza = State()
    number = State()


@UP_Router.message(F.text.lower() == 'привіт') # Початок спілкування з ботом
@UP_Router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привіт, я віртуальний помічник!\nЧим я можу Вам допомогти?😊', 
                                                                    reply_markup=reply.start_kb)


@UP_Router.message(F.text.lower().contains('меню')) # Функція виклику меню закладу
@UP_Router.message(Command('menu'))
async def menu_cmd(message: types.Message):
    await message.answer_photo(photo='https://ibb.co/qJh6Pcd', caption='Ось наше меню👀')


@UP_Router.message(F.text.lower().contains('адрес')) # Функція виклику інформації щодо адреси закладу
@UP_Router.message(Command('about'))
async def about_cmd(message: types.Message):
    await message.answer('З радістю підкажу інформацію щодо закладів🤗')
    await message.answer('📍Адреса: проспект Степана Бандери 7\n\n⌚Графік роботи: працюємо кожного дня з 08:00 до 23:00\n\n📲Контактний номер телефону: 0445103070')


@UP_Router.message(F.text.lower().contains('оплат')) # Функція виклику інформації щодо варіантів оплати
@UP_Router.message(Command('payment'))
async def payment_cmd(message: types.Message):
    await message.answer('Варіанти оплати: ')


@UP_Router.message(F.text.lower().contains('доставк')) # Функція виклику інформації щодо варіантів доставки
@UP_Router.message(Command('delivery'))
async def delivery_cmd(message: types.Message):
    await message.answer('Варіанти доставки: ')


@UP_Router.message(F.text.lower().contains('статус')) # Функція виклику інформації щодо статусу замовлення
@UP_Router.message(Command('status'))
async def status_cmd(message: types.Message):
    await message.answer('Статус замовлення')


@UP_Router.callback_query(F.data == 'yes') # Функція підтвердження замовлення
async def yes(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Дякуємо за Ваше замовлення!😊🍕', reply_markup=reply.start_kb)


@UP_Router.callback_query(F.data == 'no') # Функція скасування замовлення
async def no(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Будь ласка, створіть замовлення повторно.', 
                                                                    reply_markup=reply.start_kb)


@UP_Router.message(F.text.lower().contains('створити замовлення')) # Функція створення замовлення
@UP_Router.message(Command('order'))
async def order_cmd(message: Message, state: FSMContext):
    await state.set_state(Order.name)
    await message.answer('Введіть, будь ласка, Ваше ім\'я')


@UP_Router.message(Order.name)
async def order_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Order.pizza)
    await message.answer('Яку піцу обрали?😋🍕')


@UP_Router.message(Order.pizza)
async def order_pizza(message: Message, state: FSMContext):
    await state.update_data(pizza=message.text)
    await state.set_state(Order.number)
    await message.answer('Введіть, будь ласка, Ваш контактний номер телефона', 
                                                                    reply_markup=reply.get_number)


@UP_Router.message(Order.number, F.contact)
async def order_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f'🪪Ваше ім\'я: {data["name"]}\n🍕Обрана піца: {data["pizza"]}\n📲Контактний номер телефону: {data["number"]}\n\nЗамовлення сформовано вірно?',
                                                                    reply_markup=reply.order_kb)
    await state.clear()