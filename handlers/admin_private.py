from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply import get_keyboard


AP_Router = Router()
AP_Router.message.filter(ChatTypeFilter(['private']), IsAdmin())


ADMIN_KB = get_keyboard(
    'Додати товар',
    'Змінити товар',
    'Видалити товар',
    'Перевірка товарів',
    placeholder='Оберіть дію',
    sizes=(2, 1, 1),
)


@AP_Router.message(Command('admin'))
async def admin_features(message: types.Message):
    await message.answer('Що бажаєте зробити?👀', reply_markup=ADMIN_KB)


@AP_Router.message(F.text == 'Перевірка товарів')
async def starring_at_product(message: types.Message):
    await message.answer('ОК, ось список товарів')


@AP_Router.message(F.text == 'Змінити товар')
async def change_product(message: types.Message):
    await message.answer('Який товар бажаєте змінити?😊')


@AP_Router.message(F.text == 'Удалить товар')
async def delete_product(message: types.Message):
    await message.answer('Оберіть, будь ласка, товар(и) для видалення')


#Код нижче для машини стану (FSM)

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'AddProduct:name': 'Введіть назву повторно:',
        'AddProduct:description': 'Введіть опис повторно:',
        'AddProduct:price': 'Введіть вартість знову:',
        'AddProduct:image': 'Цей стан останній, тому...',
    }

#Стаємо в стан очікування введення name
@AP_Router.message(StateFilter(None), F.text == 'Додати товар')
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        'Введіть назву товара', reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


#Хендлер скасування та скидання стану має бути тут завжди,
#після того, як стали в стан номер 1 (елементарне чергування фільтрів)
@AP_Router.message(StateFilter('*'), Command('отмена'))
@AP_Router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer('Усі дії скасовано', reply_markup=ADMIN_KB)

#Повернутися на крок назад (в минулий стан)
@AP_Router.message(StateFilter('*'), Command('назад'))
@AP_Router.message(StateFilter('*'), F.text.casefold() == 'назад')
async def back_step_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer('Попереднього кроку немає, введіть назву товару або напишіть "Скасувати"')
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f'Ок, Ви повернули до попереднього кроку \n 
                                 {AddProduct.texts[previous.state]}')
            return
        previous = step


#Ловим данные для состояние name и потом меняем состояние на description
@AP_Router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    # Здесь можно сделать какую либо дополнительную проверку
    #и выйти из хендлера не меняя состояние с отправкой соответствующего сообщения
    #например:
    if len(message.text) >= 100:
        await message.answer('Назва товару не повинна перевищувати 100 символів. \n Введіть, будь ласка, повторно')
        return
    
    await state.update_data(name=message.text)
    await message.answer('Введіть, будь ласка, опис товару')
    await state.set_state(AddProduct.description)

#Хендлер для отлова некорректных вводов для состояния name
@AP_Router.message(AddProduct.name)
async def add_name2(message: types.Message, state: FSMContext):
    await message.answer('Ви ввели недопустимі дані, введіть текст назви товару')



#Ловим данные для состояние description и потом меняем состояние на price
@AP_Router.message(AddProduct.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Введіть, будь ласка, вартість товару')
    await state.set_state(AddProduct.price)

#Хендлер для отлова некорректных вводов для состояния description
@AP_Router.message(AddProduct.description)
async def add_description2(message: types.Message, state: FSMContext):
    await message.answer('Ви ввели недопустимі дані, введіть текст назви товару')



#Ловим данные для состояние price и потом меняем состояние на image
@AP_Router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    try:
        float(message.text)
    except ValueError:
        await message.answer('Введіть коректне значення ціни')
        return
    
    await state.update_data(price=message.text)
    await message.answer('Завантажте зображення товару')
    await state.set_state(AddProduct.image)

#Хендлер для отлова некорректных ввода для состояния price
@AP_Router.message(AddProduct.price)
async def add_price2(message: types.Message, state: FSMContext):
    await message.answer('Ви ввели недопустимі дані, введіть текст назви товару')



#Ловим данные для состояние image и потом выходим из состояний
@AP_Router.message(AddProduct.image, F.photo)
async def add_image(message: types.Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer('Товар успішно додано', reply_markup=ADMIN_KB)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()

@AP_Router.message(AddProduct.image)
async def add_image2(message: types.Message, state: FSMContext):
    await message.answer('Надішліть фото їжі')