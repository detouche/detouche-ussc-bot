from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirmation_change_desc_title():
    buttons = [
        [
            InlineKeyboardButton(text=f"Да",
                                 callback_data='change_desc_title_true'),
            InlineKeyboardButton(text=f"Нет",
                                 callback_data='change_desc_title_false')
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
