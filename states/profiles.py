from aiogram.fsm.state import StatesGroup, State


class Profile(StatesGroup):
    title = State()
    competencies = State()
    delete = State()
    delete_confirmation = State()
    delete_cancel = State()
    check_competencies = State()
    changeable_id = State()
    change_title = State()
    add_competence = State()
    delete_competence = State()
