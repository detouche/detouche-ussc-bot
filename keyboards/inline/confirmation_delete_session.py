from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_confirmation_delete():
    buttons = [
        [
            InlineKeyboardButton(text=f"Да",
                                 callback_data='confirmation_delete_session')
        ],
        [
            InlineKeyboardButton(text=f"Нет",
                                 callback_data='cancel_delete_session')
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
