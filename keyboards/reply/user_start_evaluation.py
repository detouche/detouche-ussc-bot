from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_start_evaluation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Начать оценку')
        ]
    ],
    resize_keyboards=True
)
