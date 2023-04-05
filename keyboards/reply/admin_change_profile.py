from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_change_profile = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Выбрать профиль'),
            KeyboardButton(text='Назад в меню профилей')],
],
    resize_keyboard=True
)
