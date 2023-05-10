from loader import rt
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from keyboards.reply.admin_create_profile import admin_create_profile
from keyboards.reply.admin_choosing_actions_profile import admin_choosing_actions_profile

from keyboards.inline.end_adding_competencies import end_adding_competencies

from handlers.custom_handlers.role import admin_command

from states.profiles import Profile

from database.connection_db import create_profile_db, get_competencies_list, add_competence_in_profile, get_profile_id, \
    remove_competence_from_profile


@rt.message(Text('Создать профиль'))
@admin_command
async def create_profile(message: types.Message, state: FSMContext, *args, **kwargs):
    await message.answer(text=f"Введите название профиля, который хотите создать.",
                         reply_markup=admin_create_profile)
    await state.set_state(Profile.title)


@rt.message(Profile.title)
async def create_profile_title(message: types.Message, state: FSMContext):
    comp_list = '\n'.join(list(map(lambda x: f'ID: {x[0]} Name: {x[1]}', get_competencies_list())))
    if create_profile_db(message.text.lower()):
        await message.answer(text="Профиль компетенций успешно создан.")
        await state.set_state(Profile.competencies)
        await state.update_data(title=message.text.lower().title())
        await message.answer(text=f"Введите ID компетенций, которые хотите добавить в профиль\n"
                                  f"Список всех имеющихся компетенций:\n{comp_list}")
    else:
        await message.answer(text="Такой профиль уже существует.",
                             reply_markup=admin_choosing_actions_profile)


@rt.message(Profile.competencies)
async def add_competencies_in_profile(message: types.Message, state: FSMContext):
    profile_name = await state.get_data()
    profile_id = get_profile_id(profile_name=profile_name['title'])
    await state.update_data(competencies=message.text)
    if add_competence_in_profile(competence_id=message.text, profile_id=profile_id):
        await message.answer(text=f"Компетенция c ID: {message.text} успешно добавлена. \n "
                                  f"Введите ID Следующей компетенции, которую хотите добавить",
                             reply_markup=end_adding_competencies())
    else:
        await message.answer(text="Такого ID компетенции не существует или он уже добавлен. \n"
                                  "Повторите ввод.")


@rt.callback_query(Text('end_adding_competencies'))
async def end_add_competencies_profile(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text='Компетенции успешно добавлены в профиль!',
                                  reply_markup=admin_choosing_actions_profile)


@rt.callback_query(Text('delete_competencies'))
async def delete_competence_in_profile(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    profile_id = get_profile_id(data['title'])
    competence_id = data['competencies']
    remove_competence_from_profile(competence_id=competence_id, profile_id=profile_id)
    await callback.message.delete()
    await callback.message.answer(text='Компетенция удалена из профиля. Продолжайте ввод.')
