from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.user_start_evaluation import user_start_evaluation

# from handlers.custom_handlers.role import user_command
from handlers.custom_handlers.user_connection import user_start

from database.connection_db import get_session_info, get_candidate_name, get_profile_number, get_profile_name, \
    get_competencies_id, get_profile_competencies, get_competence_title

from states.user_info import User


@rt.message(User.start_session)
# @user_command
async def user_start_evaluation_info(message: types.Message, state):
    data = await state.get_data()
    if data:
        start_session = data['start_session']
    else:
        await state.update_data(start_session=message.text)
        start_session = (await state.get_data())['start_session']
    await state.clear()
    connection_codes = get_session_info(3)
    candidate_name = get_candidate_name(start_session)
    profile_number = get_profile_number(start_session)
    profile_name = get_profile_name(profile_number)
    comp_list = get_profile_competencies(profile_number)
    comp_list = list(map(get_competence_title, comp_list))
    title_comp = '\n'.join(list(map(lambda x: f'— {x[0]}', comp_list)))
    if int(start_session) in connection_codes:
        await message.answer(text=f'Информация о кандидате:\n'
                                  f'— Имя кандидата: {candidate_name}\n'
                                  f'— Профиль: {profile_name}\n'
                                  f'— Компетенции входящие в профиль:\n'
                                  f'{title_comp}\n'
                                  f'Методичка по оценкам',
                             reply_markup=user_start_evaluation)
    else:
        await message.answer(text=f'Код указан неверно')
        await user_start(message, state)
