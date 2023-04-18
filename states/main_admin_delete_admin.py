from aiogram.filters.callback_data import CallbackData


class AdminAction(CallbackData, prefix="admin_delete"):
    action: str
    admin_id: int
