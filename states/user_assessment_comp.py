from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext


class UserAssessment(CallbackData, prefix="assessment"):
    action: str
    comp_id: int


class UserAssessmentGrade(CallbackData, prefix="assessment_grades"):
    action: str
    grade: float


class CompSessionInfo(FSMContext):
    pass
