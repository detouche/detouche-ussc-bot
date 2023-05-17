from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_start_grading = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Приступить к оцениванию')
        ]
    ],
    resize_keyboard=True, one_time_keyboard=True
)
