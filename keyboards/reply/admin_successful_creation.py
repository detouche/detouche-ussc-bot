from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

admin_successful_creation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Завершить сессию'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


admin_delete_session = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Завершить сессию'),
            KeyboardButton(text='Назад в главное меню')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
