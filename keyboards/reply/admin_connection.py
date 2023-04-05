from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_connection = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Компетенции'),
            KeyboardButton(text='Создать сессию'),
            KeyboardButton(text='Профили')
        ]
    ],
    resize_keyboard=True
)
