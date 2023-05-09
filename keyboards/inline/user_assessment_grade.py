from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from states.user_assessment_comp import UserAssessmentGrade


def user_assessment_grade_get_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text=f"Да",
                                 callback_data=UserAssessmentGrade(action="assessment_grade", grade=1).pack()),
            InlineKeyboardButton(text=f"Частично",
                                 callback_data=UserAssessmentGrade(action="assessment_grade", grade=0.5).pack()),
            InlineKeyboardButton(text=f"Нет",
                                 callback_data=UserAssessmentGrade(action="assessment_grade", grade=0).pack())
        ],
        [
            InlineKeyboardButton(text=f"Без оценки",
                                 callback_data=UserAssessmentGrade(action="assessment_grade", grade=-1).pack())
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
