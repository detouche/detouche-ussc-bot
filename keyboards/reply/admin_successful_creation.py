from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_successful_creation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Завершить сессию'),
        ]
    ],
    resize_keyboards=True
)
