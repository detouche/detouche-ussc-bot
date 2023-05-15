from loader import rt
from aiogram import types
from aiogram.fsm.context import FSMContext

from keyboards.reply.user_start_grading import user_start_grading

from handlers.custom_handlers.user_connection import user_start

from database.connection_db import get_session_info, get_candidate_name, get_profile_name_session, \
    user_session_info, get_user_session_info, user_has_active_session, get_comp_name_session, get_comp_desc_session, \
    get_admins_list_by_column, get_competence_id

from states.user_info import User

DEFAULT_GRADE = -1


@rt.message(User.connection_code)
async def user_start_grading_info(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data:
        connection_code = data['connection_code']
    else:
        await state.update_data(connection_code=message.text)
        connection_code = (await state.get_data())['connection_code']
    await state.clear()

    try:
        connection_code_int = int(connection_code)
    except ValueError:
        if message.chat.id not in get_admins_list_by_column(0):
            await message.answer(text=f'Ошибка: Вы ввели неправильный код сессии')
            await user_start(message=message, state=state)
        return

    if connection_code_int in get_session_info(3):
        user_id = message.chat.id
        candidate_name = get_candidate_name(connection_code)
        profile_name = get_profile_name_session(connection_code)
        competencies_list_name = get_comp_name_session(connection_code)
        competencies_list_desc = get_comp_desc_session(connection_code)
        if not user_has_active_session(user_id):
            for i in range(len(competencies_list_name)):
                user_session_info(candidate_name=candidate_name,
                                  profile_name=profile_name,
                                  competence_name=competencies_list_name[i][0],
                                  competence_description=competencies_list_desc[i][0],
                                  connection_code=connection_code,
                                  user_id=user_id,
                                  grade=DEFAULT_GRADE)

        competence_title = '\n'.join(list(map(lambda x: f'— [ID: {get_competence_id(x[0])[0]}] {x[0].capitalize()}', competencies_list_name)))
        await message.answer(text=f'Информация о кандидате:\n\n'
                                  f'Имя кандидата: {get_user_session_info(1, connection_code)[0].title()}\n'
                                  f'Профиль: {get_user_session_info(2, connection_code)[0].capitalize()}\n'
                                  f'Компетенции входящие в профиль:\n'
                                  f'{competence_title}\n',
                             reply_markup=user_start_grading)
    else:
        await message.answer(text=f'Код указан неверно')
        await user_start(message, state)
