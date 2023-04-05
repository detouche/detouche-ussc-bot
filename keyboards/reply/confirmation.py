from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

confirmation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Да'),
            KeyboardButton(text='Нет')
        ]
    ],
    resize_keyboard=True
)

