from aiogram.fsm.state import StatesGroup, State


class AdminSession(StatesGroup):
    name = State()
    profile_number = State()
