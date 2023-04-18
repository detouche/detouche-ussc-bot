from aiogram.fsm.state import StatesGroup, State


class MenuAddAdmin(StatesGroup):
    step_add_admin = State()


class MenuDeleteAdmin(StatesGroup):
    step_delete_admin = State()
