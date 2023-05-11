from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from states.user_grading_competence import UserGrade


def user_grade_get_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text=f"Да",
                                 callback_data=UserGrade(action="assessment_grade", grade=1).pack()),
            InlineKeyboardButton(text=f"Частично",
                                 callback_data=UserGrade(action="assessment_grade", grade=0.5).pack()),
            InlineKeyboardButton(text=f"Нет",
                                 callback_data=UserGrade(action="assessment_grade", grade=0).pack())
        ],
        [
            InlineKeyboardButton(text=f"Без оценки",
                                 callback_data=UserGrade(action="assessment_grade", grade=-1).pack())
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
