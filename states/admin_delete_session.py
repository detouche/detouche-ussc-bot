from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext


class ConfirmationDeleteSession(CallbackData, prefix="del_session"):
    action: str
    confirmation_del: bool


class DeleteSession(FSMContext):
    pass
