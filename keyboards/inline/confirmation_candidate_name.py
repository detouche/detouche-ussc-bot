from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from states.admin_confirmation_candidate_name import ConfirmationCandidateName


def get_keyboard_confirmation():
    buttons = [
        [
            InlineKeyboardButton(text=f"Да",
                                 callback_data=ConfirmationCandidateName(
                                     action="confirmat_cand_name",
                                     confirmation=True).pack())
        ],
        [
            InlineKeyboardButton(text=f"Нет",
                                 callback_data=ConfirmationCandidateName(
                                     action="confirmat_cand_name",
                                     confirmation=False).pack())
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
