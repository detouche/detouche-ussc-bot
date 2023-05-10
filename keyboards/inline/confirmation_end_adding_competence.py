from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirmation_end_adding_competence():
    buttons = [
        [
            InlineKeyboardButton(text=f"Завершить удаление компетенций",
                                 callback_data='end_add_competence_in_profile'),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
