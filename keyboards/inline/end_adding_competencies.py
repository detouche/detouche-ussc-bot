from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def end_adding_competencies():
    buttons = [
        [
            InlineKeyboardButton(text=f"Завершить добавление компетенций в профиль",
                                 callback_data='end_adding_competencies'),
            InlineKeyboardButton(text=f"Удалить компетенцию из профиля",
                                 callback_data='delete_competencies')
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
