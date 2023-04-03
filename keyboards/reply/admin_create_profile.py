from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_create_profile = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад в меню профилей'),
        ]
    ],
    resize_keyboards=True
)

