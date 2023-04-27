from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirmation_delete_profile():
    buttons = [
        [
            InlineKeyboardButton(text=f"Да",
                                 callback_data='confirm_delete_profile'),
            InlineKeyboardButton(text=f"Нет",
                                 callback_data='cancel_delete_profile')
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
