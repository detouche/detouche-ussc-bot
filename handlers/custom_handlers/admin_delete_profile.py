from loader import rt
from aiogram import types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from keyboards.reply.admin_choosing_actions_profile import admin_choosing_actions_profile
from keyboards.reply.admin_delete_profile import admin_delete_profile

from database.connection_db import delete_profile, get_profile_list

from states.profiles import Profile


@rt.message(Text('Удалить профиль'))
async def delete_profile_start(message: types.Message, state: FSMContext):
    await state.set_state(Profile.delete)
    data_profile_list = get_profile_list()
    data_profile_list = '\n'.join(list(map(lambda x: f'ID: {x[0]} Name: {x[1]}', data_profile_list)))
    await message.answer(text=f'Введите ID профиля, который необходимо удалить.\n'
                              f'Список существующих профилей:\n{data_profile_list}',
                         reply_markup=admin_delete_profile)


@rt.message(Profile.delete)
async def delete_profile_end(message: types.Message, state: FSMContext):
    if delete_profile(message.text):
        await message.answer(text='Профиль успешно удален.',
                             reply_markup=admin_choosing_actions_profile)
    else:
        await message.answer(text='Такого профиля не существует, либо вы не корректно ввели ID. \n'
                                  'Повторите ввод.')
    await state.clear()
