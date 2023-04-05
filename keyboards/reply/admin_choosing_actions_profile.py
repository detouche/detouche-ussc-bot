from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_choosing_actions_profile = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Удалить профиль'),
            KeyboardButton(text='Создать профиль'),
            KeyboardButton(text='Назад в главное меню'),
            KeyboardButton(text='Редактировать профиль')],
],
    resize_keyboard=True
)
