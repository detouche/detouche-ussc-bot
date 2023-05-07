from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_end_assessment = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Завершить проверку')
        ]
    ],
    resize_keyboard=True
)