from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_successful_create_profile = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Завершить добавление компетенций'),
        ]
    ],
    resize_keyboards=True
)
