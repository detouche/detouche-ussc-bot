from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from states.admin_delete_session import ConfirmationDeleteSession


def get_keyboard_confirmation_del():
    buttons = [
        [
            InlineKeyboardButton(text=f"Да",
                                 callback_data='confirmat_del_session')
        ],
        [
            InlineKeyboardButton(text=f"Нет",
                                 callback_data='cancel_del_session')
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
