from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_change_assessment = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Заново оценить компетенцию'),
        ]
    ],
    resize_keyboards=True
)
