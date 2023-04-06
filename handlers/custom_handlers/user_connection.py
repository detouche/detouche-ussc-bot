from aiogram.fsm.context import FSMContext
from loader import rt
from aiogram import types

from keyboards.reply.user_connection import user_connection

from database.connection_db import user_register, auth_validation

from states.user_info import User


async def user_start(message: types.Message, state: FSMContext):
    current_id = message.from_user.id
    authorized = auth_validation(current_id)
    if authorized:
        await message.answer(text=f'Ввод кода сессии',
                             reply_markup=user_connection)
    else:
        await message.answer("Вижу Вас в первый раз. Ввидите своё ФИО")
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
