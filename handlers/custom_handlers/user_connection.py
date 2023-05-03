from aiogram.fsm.context import FSMContext
from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.user_connection import user_connection

from database.connection_db import user_register, auth_validation, user_rename

from states.user_info import User


async def user_start(message: types.Message, state: FSMContext, url_code=None):
    await state.clear()
    current_id = message.from_user.id
    authorized = auth_validation(current_id)
    if authorized:
        if url_code is None:
            await message.answer(text=f'Пожалуйста, введите код сессии',
                                 reply_markup=user_connection)
            await state.set_state(User.start_session)
        else:
            await state.set_state(User.start_session)
            await state.update_data(start_session=url_code)
            from handlers.custom_handlers.user_start_evaluation import user_start_evaluation_info
            await user_start_evaluation_info(message, state)
    else:
        await message.answer("Вижу Вас в первый раз. Введите своё ФИО")
        await state.set_state(User.name)


@rt.message(User.name)
async def user_enter_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_data = await state.get_data()
    current_id = message.from_user.id
    await message.answer(f"Я Вас запомнил, {user_data['name']}")
    await state.clear()
    user_register(current_id, user_data['name'])
    await user_start(message, state)


@rt.message(Text('Изменить имя'))
async def user_want_rename(message: types.Message, state: FSMContext):
    await message.answer("Как Вас перезаписать?")
    await state.set_state(User.rename)


@rt.message(User.rename)
async def user_enter_rename(message: types.Message, state: FSMContext):
    await state.update_data(rename=message.text)
    user_data = await state.get_data()
    current_id = message.from_user.id
    await message.answer(f"Перезаписал Вас, {user_data['rename']}")
    await state.clear()
    user_rename(current_id, user_data['rename'])
    await user_start(message, state)
