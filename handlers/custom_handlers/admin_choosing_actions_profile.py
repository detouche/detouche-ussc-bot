from loader import rt
from aiogram import types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from database.connection_db import get_profile_list, get_profile_competencies, get_competence_title

from keyboards.reply.admin_choosing_actions_profile import admin_choosing_actions_profile
from keyboards.reply.admin_delete_profile import admin_delete_profile

from states.profiles import Profile


@rt.message(Text('Профили'))
@rt.message(Text('Назад в меню профилей'))
async def choosing_actions_profile(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f'Вы вошли в меню "Профили"',
                         reply_markup=admin_choosing_actions_profile)


@rt.message(Text('Список профилей'))
async def profile_list(message: types.Message, state: FSMContext):
    data_profile_list = get_profile_list()
    data_profile_list = '\n'.join(list(map(lambda x: f'ID: {x[0]} Name: {x[1]}', data_profile_list)))
    await state.set_state(Profile.check_competencies)
    await message.answer(text=f'Введите ID профиля для просмотра входящих компетенций. \n'
                              f'Список всех имеющихся профилей:\n{data_profile_list}',
                         reply_markup=admin_delete_profile)


@rt.message(Profile.check_competencies)
async def get_competencies_in_profile(message: types.Message, state: FSMContext):
    comp_list = get_profile_competencies(message.text.lower())
    comp_list = list(map(get_competence_title, comp_list))
    if comp_list:
        title = '\n'.join(list(map(lambda x: f'Компетенция: {x[0]}', comp_list)))
        await message.answer(text=f'Компетенции входящие в профиль\n'
                                  f'{title}',
                             reply_markup=admin_delete_profile)
    else:
        await message.answer(text='В профиле нет компетенций или он не существует. \n'
                                  'Повторите ввод ID')
