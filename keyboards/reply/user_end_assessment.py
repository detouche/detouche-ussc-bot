from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_end_assessment = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Изменить оценку'),
            KeyboardButton(text='Завершить проверку')
        ]
    ],
    resize_keyboards=True
)