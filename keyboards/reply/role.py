from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

role = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Я администратор'),
            KeyboardButton(text='Я пользователь')
        ]
    ],
    resize_keyboard=True
)
