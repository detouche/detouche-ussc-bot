from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_start_grading = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Начать оценку')
        ]
    ],
    resize_keyboard=True
)
