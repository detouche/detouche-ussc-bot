from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_change_competencies = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад в меню компетенций')],
    ],
    resize_keyboard=True
)