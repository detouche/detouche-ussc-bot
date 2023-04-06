from aiogram.fsm.state import StatesGroup, State


class User(StatesGroup):
    name = State()
