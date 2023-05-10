from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def change_profile():
    buttons = [
        [
            InlineKeyboardButton(text=f"Изменить название профиля",
                                 callback_data='change_desc_title'),
        ],
        [
            InlineKeyboardButton(text=f"Добавить компетенции в профиль",
                                 callback_data='add_comp_from_desc'),
            InlineKeyboardButton(text=f"Удалить компетенции из профиля",
                                 callback_data='delete_comp_from_desc')
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
