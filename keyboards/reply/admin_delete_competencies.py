from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_delete_competencies = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Выбрать нужную компетенцию'),
            KeyboardButton(text='Назад в меню компетенций')
        ]
    ],
    resize_keyboards=True
)
