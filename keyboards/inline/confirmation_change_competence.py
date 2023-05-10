from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirmation_change_competence():
    buttons = [
        [
            InlineKeyboardButton(text=f"Да",
                                 callback_data='change_competence_title_true'),
            InlineKeyboardButton(text=f"Нет",
                                 callback_data='change_competence_title_false')
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
