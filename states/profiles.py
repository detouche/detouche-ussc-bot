from aiogram.fsm.state import StatesGroup, State


class Profile(StatesGroup):
    title = State()
    competencies = State()
    delete = State()
    delete_confirmation = State()
    delete_cancel = State()
    check_competencies = State()
