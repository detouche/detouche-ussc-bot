from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_admin_connection = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Компетенции'),
            KeyboardButton(text='Создать сессию'),
            KeyboardButton(text='Профили'),
            KeyboardButton(text='Администраторы')
        ]
    ],
    resize_keyboard=True
)
