from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirmation_change_competence_desc():
    buttons = [
        [
            InlineKeyboardButton(text=f"Да",
                                 callback_data='change_competence_desc_true'),
            InlineKeyboardButton(text=f"Нет",
                                 callback_data='change_competence_desc_false')
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
