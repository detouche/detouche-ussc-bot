from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_admin_delete_or_add_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Добавить администратора'),
            KeyboardButton(text='Удалить администратора'),
        ],
        [
            KeyboardButton(text='Назад в главное меню')
        ]
    ],
    resize_keyboard=True
)
