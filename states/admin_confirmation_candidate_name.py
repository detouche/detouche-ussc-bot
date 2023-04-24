from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext


class ConfirmationCandidateName(CallbackData, prefix="admin"):
    action: str
    confirmation: bool


class CandidateName(FSMContext):
    pass
