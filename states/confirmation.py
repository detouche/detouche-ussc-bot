from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext


class Confirmation(CallbackData, prefix="confirmation_choice"):
    action: str
    confirmation_choice: bool


class UserInfo(FSMContext):
    pass


class AdminInfo(FSMContext):
    pass
