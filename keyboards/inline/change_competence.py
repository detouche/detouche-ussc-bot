from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def change_competence():
    buttons = [
        [
            InlineKeyboardButton(text=f"Изменить название",
                                 callback_data='change_competence_title'),
            InlineKeyboardButton(text=f"Изменить описание",
                                 callback_data='change_competence_description')
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
