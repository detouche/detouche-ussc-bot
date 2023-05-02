from aiogram.fsm.state import StatesGroup, State


class Competence(StatesGroup):
    title = State()
    description = State()
    delete = State()
    check_description = State()
    changeable_id = State()
    change_title = State()
    change_description = State()
