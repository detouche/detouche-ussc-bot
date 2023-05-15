from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def change_profile():
    buttons = [
        [
            InlineKeyboardButton(text=f"Изменить название профиля",
                                 callback_data='change_desc_title'),
        ],
        [
            InlineKeyboardButton(text=f"Добавить компетенции",
                                 callback_data='add_comp_from_desc'),
            InlineKeyboardButton(text=f"Удалить компетенции",
                                 callback_data='delete_comp_from_desc')
        ],
        [
            InlineKeyboardButton(text=f"Выбрать другой профиль",
                                 callback_data='select_any_profile'),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
