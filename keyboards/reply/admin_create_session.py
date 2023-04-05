from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_create_session = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Профили на выбор'),
            KeyboardButton(text='Назад в главное меню')
        ]
    ],
    resize_keyboard=True
)

