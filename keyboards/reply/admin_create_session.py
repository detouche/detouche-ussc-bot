from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_create_session = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад в главное меню'),
        ]
    ],
    resize_keyboard=True
)
