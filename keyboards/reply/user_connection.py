from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_connection = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Изменить имя')
        ]
    ],
    resize_keyboard=True
)
