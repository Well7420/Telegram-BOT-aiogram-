from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder



start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Меню'),
            KeyboardButton(text='Адреса піцерії'),
        ],
        {
            KeyboardButton(text='Варіанти доставки'),
            KeyboardButton(text='Варіанти оплати'),
        },
        {
            KeyboardButton(text='Статус замовлення')
        }
    ],
    resize_keyboard=True,
    input_field_placeholder='Що вас цікавить?'
)

del_keyboard = ReplyKeyboardRemove()

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Надіслати свій номер', request_contact=True)]], resize_keyboard=True)

order_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Так', callback_data='yes'), InlineKeyboardButton(text='Ні', callback_data='no')]
])