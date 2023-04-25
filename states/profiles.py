from aiogram.fsm.state import StatesGroup, State


class Profile(StatesGroup):
    title = State()
    competencies = State()
    delete = State()
    check_competencies = State()
