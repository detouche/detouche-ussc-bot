from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_assessment = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Оценить компетенцию'),
        ]
    ],
    resize_keyboards=True
)
