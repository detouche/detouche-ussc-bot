from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def change_competence():
    buttons = [
        [
            InlineKeyboardButton(text=f"Изменить название компетенции",
                                 callback_data='change_competence_title'),
            InlineKeyboardButton(text=f"Изменить описание коммпетенции",
                                 callback_data='change_competence_description')
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
