from aiogram.fsm.state import StatesGroup, State


class User(StatesGroup):
    name = State()
    rename = State()
    connection_code = State()
