from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_create_session = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад в главное меню'),
        ]
    ],
    resize_keyboard=True
)

admin_choice_profile = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Профили на выбор')
        ]
    ],
    resize_keyboard=True
)
