from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from states.confirmation import Confirmation


def get_keyboard_confirmation():
    buttons = [
        [
            InlineKeyboardButton(text=f"Да",
                                 callback_data=Confirmation(
                                     action="confirmation_add",
                                     confirmation_choice=True).pack())
        ],
        [
            InlineKeyboardButton(text=f"Нет",
                                 callback_data=Confirmation(
                                     action="confirmation_add",
                                     confirmation_choice=False).pack())
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
