from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_assessment_again = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Заново оценить компетенцию'),
        ]
    ],
    resize_keyboards=True
)
