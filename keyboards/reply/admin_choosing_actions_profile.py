from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_choosing_actions_profile = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Создать профиль'),
            KeyboardButton(text='Редактировать профиль'),
            KeyboardButton(text='Список профилей'),
            KeyboardButton(text='Удалить профиль')],
        [
            KeyboardButton(text='Назад в главное меню')],
    ],
    resize_keyboard=True
)
