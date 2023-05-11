from aiogram.filters.callback_data import CallbackData


class AdminAction(CallbackData, prefix="add_admin"):
    action: str
    user_id: int
