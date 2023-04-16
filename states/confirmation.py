from aiogram.filters.callback_data import CallbackData


class Confirmation(CallbackData, prefix="confirmation_choice"):
    action: str
    confirmation_choice: bool
