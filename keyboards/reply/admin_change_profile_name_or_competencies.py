from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_change_profile_name_or_competencies = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Изменить компетенции профиля'),
            KeyboardButton(text='Изменить название профиля')],
],
    resize_keyboard=True
)