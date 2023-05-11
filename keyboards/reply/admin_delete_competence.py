from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_delete_competence = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад в меню компетенций')
        ]
    ],
    resize_keyboard=True
)
