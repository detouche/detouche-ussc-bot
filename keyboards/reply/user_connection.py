from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_connection = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Начать сессию'),
        ]
    ],
    resize_keyboard=True
)
