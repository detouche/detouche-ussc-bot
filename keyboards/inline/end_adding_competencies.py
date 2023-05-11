from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def end_adding_competencies():
    buttons = [
        [
            InlineKeyboardButton(text=f"Завершить добавление",
                                 callback_data='end_adding_competencies'),
            InlineKeyboardButton(text=f"Удалить компетенцию",
                                 callback_data='delete_competencies')
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def end_adding_competencies_error():
    buttons = [
        [
            InlineKeyboardButton(text=f"Завершить добавление",
                                 callback_data='end_adding_competencies'),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def change_profile_end_adding_competencies():
    buttons = [
        [
            InlineKeyboardButton(text=f"Завершить добавление",
                                 callback_data='change_profile_end_adding_competencies'),
            InlineKeyboardButton(text=f"Удалить компетенцию",
                                 callback_data='change_profile_delete_competencies')
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def end_change_profile_end_adding_competencies():
    buttons = [
        [
            InlineKeyboardButton(text=f"Завершить добавление",
                                 callback_data='change_profile_end_adding_competencies'),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
