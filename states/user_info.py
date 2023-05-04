from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage


class User(StatesGroup):
    name = State()
    rename = State()
    start_session = State()
