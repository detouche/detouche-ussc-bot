from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_last_assessment = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Оценить последнюю компетенцию'),
        ]
    ],
    resize_keyboard=True
)