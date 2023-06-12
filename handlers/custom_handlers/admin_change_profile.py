from loader import rt
from aiogram import types, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.reply.admin_change_profile import admin_change_profile
from keyboards.inline.change_profile import change_profile
from keyboards.inline.confirmation_change_desc_title import confirmation_change_desc_title

from database.connection_db import get_profile_list, check_profile, change_profile_title, add_competence_in_profile, \
    get_competencies_list, competencies_in_profile, get_competence_title, \
    delete_competence_from_profile, get_profile_name, get_profile_competencies, competence_in_profile

from states.profiles import Profile

from handlers.custom_handlers.role import admin_command
from handlers.custom_handlers.admin_choosing_actions_profile import creating_pdf
from handlers.custom_handlers.admin_choosing_actions_competencies import creating_pdf as creating_pdf_competencies


@rt.message(Text('Редактировать профиль'))
@admin_command
async def change_profiles(message: types.Message, state: FSMContext, bot: Bot, *args, **kwargs):
    data_profile_list = '\n'.join(list(map(lambda x: f'[ID: {x[0]}] {x[1].capitalize()}', get_profile_list())))
    await message.answer(text=f'Выберите ID профиля, который хотите изменить\n'
                              f'Список доступных профилей:\n\n{data_profile_list}',
                         reply_markup=admin_change_profile)
    await state.set_state(Profile.changeable_id)
    await creating_pdf(bot=bot, message=message)


@rt.message(Profile.changeable_id)
async def get_changeable_description_id(message: types.Message, state: FSMContext, bot: Bot):
    await state.clear()
    if check_profile(profile_id=message.text):
        await state.update_data(changeable_id=message.text)
        profile_name = get_profile_name(message.text)
        competencies_list = '\n'.join(list(map(lambda x: f'[ID: {x}] {get_competence_title(x)[0].capitalize()}',
                                               get_profile_competencies(message.text))))
        await message.answer(text=f'Что хотите изменить в профиле?\n\n'
                                  f'Название: {profile_name.capitalize()}\n'
                                  f'Компетенции:\n'
                                  f'{competencies_list}',
                             reply_markup=change_profile())
    else:
        await message.answer(text=f'Ошибка: Профиль с [ID: {message.text.lower()}] '
                                  f'не найден, повторите ввод')
        await change_profiles(message=message, state=state, bot=bot)


@rt.callback_query(Text('change_desc_title'))
async def change_desc_title_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Profile.change_title)
    data = await state.get_data()
    profile_id = data['changeable_id']
    profile_name = get_profile_name(profile_id).capitalize()
    await callback.message.answer(text=f'Введите новое название для профиля:\n\n'
                                       f'[ID: {profile_id}] {profile_name}')


@rt.message(Profile.change_title)
async def change_desc_title_confirmation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await state.update_data(change_title=message.text.lower())
    await state.update_data(changeable_id=data['changeable_id'])
    profile_id = data['changeable_id']
    profile_name = get_profile_name(profile_id=profile_id)
    await message.answer(text=f'Вы уверены, что хотите изменить название профиля?\n\n'
                              f'Старое название: {profile_name.capitalize()}\n'
                              f'Новое название: {message.text.capitalize()}',
                         reply_markup=confirmation_change_desc_title())


@rt.callback_query(Text('change_desc_title_true'))
async def change_desc_title_true(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    profile_id = data['changeable_id']
    profile_title = data['change_title']
    if change_profile_title(profile_id=profile_id, new_profile_name=profile_title):
        await callback.message.edit_text(text='Название профиля успешно изменено')
        await state.clear()
        await change_profiles(message=callback.message, state=state, bot=bot)
    else:
        await callback.message.edit_text(
            text=f'Ошибка: Профиль с названием {profile_title.capitalize()} уже существует, '
                 f'либо был введен неверный ID')
        await state.clear()
        await change_profiles(message=callback.message, state=state, bot=bot)


@rt.callback_query(Text('change_desc_title_false'))
async def change_desc_title_false(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await callback.message.delete()
    await change_profiles(message=callback.message, state=state, bot=bot)


@rt.callback_query(Text('add_comp_from_desc'))
async def add_competence_from_profile(callback: CallbackQuery, state: FSMContext, bot: Bot):
    comp_list = '\n'.join(list(map(lambda x: f'[ID: {x[0]}] {x[1].capitalize()}', get_competencies_list())))
    data = await state.get_data()
    profile_id = data['changeable_id']
    profile_title = get_profile_name(profile_id).capitalize()
    await callback.message.answer(text=f'Через запятую введите ID компетенций (только цифры), '
                                       f'которые хотите добавить в профиль "{profile_title}"\n'
                                       f'Список компетенций:\n\n'
                                       f'{comp_list}\n\n'
                                       f'Рекомендуется не более 5-7 компетенций в профиле\n')
    await state.set_state(Profile.add_competence)
    await creating_pdf_competencies(bot=bot, message=callback.message)


@rt.message(Profile.add_competence)
async def add_competence_from_profile_start(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    profile_id = data['changeable_id']
    competencies_id = [int(competence_id) for competence_id in message.text.split(',') if competence_id.isdigit()]
    added_competencies_id = []
    already_competencies_id = []
    missing_competencies_id = []
    for competence_id in competencies_id:
        if add_competence_in_profile(competence_id=competence_id, profile_id=profile_id):
            added_competencies_id.append(competence_id)
        elif competence_in_profile(competence_id=competence_id, profile_id=profile_id):
            already_competencies_id.append(competence_id)
        else:
            missing_competencies_id.append(competence_id)
    added_competencies_list = '...' if len(added_competencies_id) == 0 \
        else "\n".join(list(map(lambda x: f"[ID: {x}] {get_competence_title(x)[0].capitalize()}", added_competencies_id)))
    already_competencies_list = '...' if len(already_competencies_id) == 0 \
        else "\n".join(list(map(lambda x: f"[ID: {x}] {get_competence_title(x)[0].capitalize()}", already_competencies_id)))
    missing_competencies_list = '...' if len(missing_competencies_id) == 0 \
        else ", ".join(list(map(lambda x: f"[ID: {x}]", missing_competencies_id)))
    profile_title = get_profile_name(profile_id).capitalize()
    await message.answer(text=f'В профиль "{profile_title}" добавлены компетенции:'
                              f'\n{added_competencies_list}\n\n'
                              f'В профиле "{profile_title}" уже имеются следующие компетенции, поэтому они не добавлены:'
                              f'\n{already_competencies_list}\n\n'
                              f'Введены несуществующие ID компетенций:'
                              f'\n{missing_competencies_list}')
    await state.clear()
    await change_profiles(message=message, state=state, bot=bot)


@rt.callback_query(Text('delete_comp_from_desc'))
async def delete_competence_from_profile_start(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    profile_id = data['changeable_id']
    data_list = competencies_in_profile(profile_id)
    title_list = list(map(lambda x: get_competence_title(x), data_list))
    competence_list = '\n'.join(list(map(lambda x, y: f'[ID: {y}] {x[0].capitalize()}', title_list, data_list)))
    await callback.message.answer(text=f'Через запятую введите ID компетенций (только цифры), '
                                       f'которые хотите удалить из профиля '
                                       f'"{get_profile_name(profile_id).capitalize()}"\n'
                                       f'Список компетенций в профиле:\n\n'
                                       f'{competence_list}')
    await state.set_state(Profile.delete_competence)


@rt.message(Profile.delete_competence)
async def delete_competence_from_profile_end(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    profile_id = data['changeable_id']
    competencies_id = [int(competence_id) for competence_id in message.text.split(',') if competence_id.isdigit()]
    delete_competencies_id = []
    missing_competencies_id = []
    for competence_id in competencies_id:
        if delete_competence_from_profile(competence_id=competence_id, profile_id=profile_id):
            delete_competencies_id.append(competence_id)
        else:
            missing_competencies_id.append(competence_id)

    delete_competencies_list = '...' if len(delete_competencies_id) == 0 \
        else "\n".join(
        list(map(lambda x: f"[ID: {x}] {get_competence_title(x)[0].capitalize()}", delete_competencies_id)))
    missing_competencies_list = '...' if len(missing_competencies_id) == 0 \
        else ", ".join(list(map(lambda x: f"[ID: {x}]", missing_competencies_id)))
    profile_title = get_profile_name(profile_id).capitalize()
    await state.update_data(competencies_list=delete_competencies_list)
    await message.answer(text=f'Из профилья "{profile_title}" удалены компетенции:'
                              f'\n{delete_competencies_list}\n\n'
                              f'Введены несуществующие ID компетенций:'
                              f'\n{missing_competencies_list}')
    await state.clear()
    await change_profiles(message=message, state=state, bot=bot)


@rt.callback_query(Text('select_any_profile'))
async def change_competence_title_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await callback.message.delete()
    await change_profiles(message=callback.message, state=state, bot=bot)
