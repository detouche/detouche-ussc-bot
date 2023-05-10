from loader import rt
from aiogram import types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.reply.admin_change_profile import admin_change_profile
from keyboards.inline.change_profile import change_profile
from keyboards.inline.confirmation_change_desc_title import confirmation_change_desc_title
from keyboards.inline.end_add_competencies import end_add_competencies
from keyboards.inline.confirmation_end_add_competence import confirmation_end_add_competence

from database.connection_db import get_profile_list, check_profile, change_profile_title, add_competence_in_profile, \
    get_competencies_list, remove_competence_from_profile, competencies_in_profile, get_competence_title, \
    delete_competence_from_profile

from states.profiles import Profile

from handlers.custom_handlers.role import admin_command
from handlers.custom_handlers.admin_choosing_actions_profile import choosing_actions_profile


@rt.message(Text('Редактировать профиль'))
@admin_command
async def change_profiles(message: types.Message, state: FSMContext, *args, **kwargs):
    data_profile_list = get_profile_list()
    data_profile_list = '\n'.join(list(map(lambda x: f'ID: {x[0]} Name: {x[1]}', data_profile_list)))
    await message.answer(text=f'Выберите профиль, который хотите изменить\n'
                              f'Список доступных профилей:\n{data_profile_list}',
                         reply_markup=admin_change_profile)
    await state.set_state(Profile.changeable_id)


@rt.message(Profile.changeable_id)
async def get_changeable_description_id(message: types.Message, state: FSMContext):
    if check_profile(message.text):
        await state.update_data(changeable_id=message.text)
        await message.answer(text=f'Что хотите изменить в профиле с ID: {message.text}',
                             reply_markup=change_profile())
    else:
        await message.answer(text=f'Профиля с таким ID не существует')
        await state.clear()
        await change_profiles(message, state)


@rt.callback_query(Text('change_desc_title'))
@admin_command
async def change_desc_title_start(callback: CallbackQuery, state: FSMContext, *args, **kwargs):
    await state.set_state(Profile.change_title)
    await callback.message.answer(text='Введите новое название для профиля')


@rt.message(Profile.change_title)
async def change_desc_title_confirmation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(change_title=message.text.lower())
    competence_id = data['changeable_id']
    await message.answer(text=f'Вы уверены что хотите изменить название профиля с ID:{competence_id} на '
                              f'{message.text}',
                         reply_markup=confirmation_change_desc_title())


@rt.callback_query(Text('change_desc_title_true'))
@admin_command
async def change_desc_title_true(callback: CallbackQuery, state: FSMContext, *args, **kwargs):
    data = await state.get_data()
    profile_id = data['changeable_id']
    profile_title = data['change_title']
    if change_profile_title(profile_id, profile_title):
        await callback.message.edit_text(text='Имя профиля успешно изменено')
        await state.clear()
        await change_profiles(callback.message, state)
    else:
        await callback.message.edit_text(
            text='Профиль с таким названием уже существует, либо был введен неверный ID')
        await state.clear()
        await change_profiles(callback.message, state)


@rt.callback_query(Text('change_desc_title_false'))
@admin_command
async def change_desc_title_false(callback: CallbackQuery, state: FSMContext, *args, **kwargs):
    await state.clear()
    await callback.message.delete()
    await change_profiles(callback.message, state)


@rt.callback_query(Text('add_comp_from_desc'))
@admin_command
async def add_competence_from_profile(callback: CallbackQuery, state: FSMContext, *args, **kwargs):
    data_list = get_competencies_list()
    comp_list = '\n'.join(list(map(lambda x: f'ID: {x[0]} Name: {x[1]}', data_list)))
    await callback.message.answer(text=f'Список доступных компетенций: \n'
                                       f'{comp_list}'
                                       f'Введите ID компетенции, которую хотите добавить в профиль.')
    await state.set_state(Profile.add_competence)


@rt.message(Profile.add_competence)
async def add_competence_from_profile_start(message: types.Message, state: FSMContext):
    profile_id = await state.get_data()
    profile_id = profile_id['changeable_id']
    if add_competence_in_profile(message.text, profile_id):
        await state.update_data(add_competence=message.text)
        await message.answer(text=f"Компетенция c ID: {message.text} успешно добавлена. \n "
                                  f"Введите ID Следующей компетенции, которую хотите добавить",
                             reply_markup=end_add_competencies())
    else:
        await message.answer(text="Такого ID компетенции не существует или он уже добавлен. \n"
                                  "Повторите ввод.")


@rt.callback_query(Text('end_add_competencies'))
@admin_command
async def end_add_competencies_profile(callback: CallbackQuery, state: FSMContext, *args, **kwargs):
    await state.clear()
    await callback.message.delete()
    await change_profiles(callback.message, state)
    await callback.message.answer(text='Компетенции успешно добавлены в профиль!')


@rt.callback_query(Text('delete_competencies'))
@admin_command
async def delete_competence_profile(callback: CallbackQuery, state: FSMContext, *args, **kwargs):
    data = await state.get_data()
    profile_id = data['changeable_id']
    competence_id = data['add_competence']
    remove_competence_from_profile(competence_id, profile_id)
    await callback.message.delete()
    await callback.message.answer(text='Компетенция удалена из профиля.  Продолжайте ввод.')


@rt.callback_query(Text('delete_comp_from_desc'))
@admin_command
async def delete_competence_from_profile_start(callback: CallbackQuery, state: FSMContext, *args, **kwargs):
    data = await state.get_data()
    profile_id = data['changeable_id']
    data_list = competencies_in_profile(profile_id)
    title_list = list(map(lambda x: get_competence_title(x), data_list))
    comp_list = '\n'.join(list(map(lambda x, y: f'ID: {y} Name: {x[0]}', title_list, data_list)))
    await callback.message.answer(text=f'Список компетенций в профиле: \n'
                                       f'{comp_list} \n'
                                       f'Введите ID компетенции, которую хотите удалить из профиля.')
    await state.set_state(Profile.delete_competence)


@rt.message(Profile.delete_competence)
async def delete_competence_from_profile_end(message: types.Message, state: FSMContext):
    data = await state.get_data()
    profile_id = data['changeable_id']
    if delete_competence_from_profile(message.text, profile_id):
        await message.answer(text='Компетенция успешно удалена из профиля. Продолжайте ввод.',
                             reply_markup=confirmation_end_add_competence())
    else:
        await message.answer(text='Такой компетенции нет в профиле, либо был введен неверный ID. Повторите ввод.')


@rt.callback_query(Text('end_add_competence_in_profile'))
@admin_command
async def end_add_comp_in_profile(callback: CallbackQuery, state: FSMContext, *args, **kwargs):
    await state.clear()
    await choosing_actions_profile(callback.message, state)
    await change_profiles(callback.message, state)
