from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_delete_profile = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Выбрать нужный профиль'),
            KeyboardButton(text='Назад в меню профилей')
        ]
    ],
    resize_keyboards=True
)
