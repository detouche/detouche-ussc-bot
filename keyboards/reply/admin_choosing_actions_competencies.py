from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_choosing_actions_competencies = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Удалить компетенцию'),
            KeyboardButton(text='Изменить компетенцию'),
            KeyboardButton(text='Назад в главное меню'),
            KeyboardButton(text='Создать компетенцию')],
],
    resize_keyboard=True
)
