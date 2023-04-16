from aiogram.filters.callback_data import CallbackData


class AdminAction(CallbackData, prefix="admin"):
    action: str
    user_id: int
    user_name: str
