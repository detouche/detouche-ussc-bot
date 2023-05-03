from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.user_start_evaluation import user_start_evaluation

# from handlers.custom_handlers.role import user_command
from handlers.custom_handlers.user_connection import user_start

from database.connection_db import get_session_info

from states.user_info import User


@rt.message(User.start_session)
# @user_command
async def user_start_evaluation_info(message: types.Message, state):
    print(await state.get_data())
    await state.update_data(start_session=message.text)
    print(await state.get_data())
    data = await state.get_data()
    start_session = data['start_session']
    await state.clear()
    connection_codes = get_session_info(3)
    if int(start_session) in connection_codes:
        await message.answer(text=f'Информация о кандидате:\n'
                                  f'— ФИО\n'
                                  f'— Профиль\n'
                                  f'— Компетенции\n'
                                  f'Методичка по оценкам',
                             reply_markup=user_start_evaluation)
    else:
        await message.answer(text=f'Код указан неверно')
        await user_start(message, state)
