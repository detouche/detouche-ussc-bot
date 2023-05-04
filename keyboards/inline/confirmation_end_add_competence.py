from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirmation_end_add_competence():
    buttons = [
        [
            InlineKeyboardButton(text=f"Завершить удаление компетенций",
                                 callback_data='end_add_competence_in_profile'),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard