from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_choosing_actions_competencies = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Создать компетенцию'),
            KeyboardButton(text='Изменить компетенцию'),
            KeyboardButton(text='Список компетенций'),
            KeyboardButton(text='Удалить компетенцию')],
        [
            KeyboardButton(text='Назад в главное меню')],
    ],
    resize_keyboard=True
)
