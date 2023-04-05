from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_change_competencies_name_or_description = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Изменить описание компетенции'),
            KeyboardButton(text='Изменить название компетенции')],
],
    resize_keyboard=True
)