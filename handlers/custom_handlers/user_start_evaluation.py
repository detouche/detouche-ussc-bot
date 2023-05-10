from loader import rt
from aiogram import types

from keyboards.reply.user_start_evaluation import user_start_evaluation

from handlers.custom_handlers.user_connection import user_start

from database.connection_db import get_session_info, get_candidate_name, get_profile_name_session, \
    user_session_info, get_user_session_info, user_has_active_session, get_comp_name_session, get_comp_desc_session, \
    get_admins_list

from states.user_info import User

DEFAULT_GRADE = -1


@rt.message(User.start_session)
async def user_start_evaluation_info(message: types.Message, state):
    data = await state.get_data()
    if data:
        start_session = data['start_session']
    else:
        await state.update_data(start_session=message.text)
        start_session = (await state.get_data())['start_session']
    await state.clear()
    connection_codes = get_session_info(3)

    try:
        start_session_code = int(start_session)
    except ValueError:
        if message.chat.id in get_admins_list(0):
            await message.answer(text=f'Хуй')
        else:
            await user_start(message=message, state=state)
        return

    if start_session_code in connection_codes:
        user_id = message.chat.id
        candidate_name = get_candidate_name(start_session)
        profile_name = get_profile_name_session(start_session)
        comp_list_name = get_comp_name_session(start_session)
        comp_list_desc = get_comp_desc_session(start_session)
        if not user_has_active_session(user_id):
            for i in range(len(comp_list_name)):
                user_session_info(candidate_name, profile_name, comp_list_name[i][0], comp_list_desc[i][0],
                                  start_session, user_id, DEFAULT_GRADE)
        title_comp = '\n'.join(list(map(lambda x: f'— {x[0]}', comp_list_name)))
        await message.answer(text=f'Информация о кандидате:\n'
                                  f'— Имя кандидата: {get_user_session_info(1, start_session)[0]}\n'
                                  f'— Профиль: {get_user_session_info(2, start_session)[0]}\n'
                                  f'— Компетенции входящие в профиль:\n'
                                  f'{title_comp}\n'
                                  f'Методичка по оценкам',
                             reply_markup=user_start_evaluation)
    else:
        await message.answer(text=f'Код указан неверно')
        await user_start(message, state)
