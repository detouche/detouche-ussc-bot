from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext


class UserGrading(CallbackData, prefix="assessment"):
    action: str
    competence_id: int


class UserGrade(CallbackData, prefix="assessment_grades"):
    action: str
    grade: float


class CompetenceSessionInfo(FSMContext):
    pass
