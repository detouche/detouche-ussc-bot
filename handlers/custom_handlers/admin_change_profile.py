from loader import rt
from aiogram import types, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.reply.admin_change_profile import admin_change_profile
from keyboards.inline.change_profile import change_profile
from keyboards.inline.confirmation_change_desc_title import confirmation_change_desc_title
from keyboards.inline.end_adding_competencies import change_profile_end_adding_competencies, \
    end_adding_competencies_error, end_change_profile_end_adding_competencies
from keyboards.inline.confirmation_end_adding_competence import confirmation_end_adding_competence

from database.connection_db import get_profile_list, check_profile, change_profile_title, add_competence_in_profile, \
    get_competencies_list, remove_competence_from_profile, competencies_in_profile, get_competence_title, \
    delete_competence_from_profile, get_profile_name, get_profile_competencies, competence_in_profile

from states.profiles import Profile

from handlers.custom_handlers.role import admin_command
from handlers.custom_handlers.admin_choosing_actions_profile import choosing_actions_profile, creating_pdf


@rt.message(Text('Редактировать профиль'))
@admin_command
async def change_profiles(message: types.Message, state: FSMContext, bot: Bot, *args, **kwargs):
    data_profile_list = '\n'.join(list(map(lambda x: f'<b>[ID: {x[0]}]</b> {x[1].capitalize()}', get_profile_list())))
    await message.answer(text=f'Выберите ID профиля, который хотите изменить\n'
                              f'Список доступных профилей:\n\n{data_profile_list}',
                         reply_markup=admin_change_profile)
    await state.set_state(Profile.changeable_id)
    await creating_pdf(bot=bot, message=message)


@rt.message(Profile.changeable_id)
async def get_changeable_description_id(message: types.Message, state: FSMContext, bot: Bot):
    if check_profile(profile_id=message.text):
        await state.update_data(changeable_id=message.text)
        profile_name = get_profile_name(message.text)
        competencies_list = '\n'.join(list(map(lambda x: f'<b>[ID: {x}]</b> {get_competence_title(x)[0].capitalize()}',
                                               get_profile_competencies(message.text))))
        await message.answer(text=f'Что хотите изменить в профиле?\n\n'
                                  f'<b>Название:</b> {profile_name.capitalize()}\n'
                                  f'<b>Компетенции:</b>\n'
                                  f'{competencies_list}',
                             reply_markup=change_profile())
    else:
        await message.answer(text=f'<b>Ошибка:</b> Профиль с <b>[ID: {message.text.lower()}]</b> '
                                  f'не найден, повторите ввод')
        await state.clear()
        await change_profiles(message=message, state=state, bot=bot)


@rt.callback_query(Text('change_desc_title'))
async def change_desc_title_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Profile.change_title)
    await callback.message.answer(text='Введите новое название для профиля')


@rt.message(Profile.change_title)
async def change_desc_title_confirmation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(change_title=message.text.lower())
    profile_id = data['changeable_id']
    profile_name = get_profile_name(profile_id=profile_id)
    await message.answer(text=f'Вы уверены, что хотите изменить название профиля?\n\n'
                              f'<b>Старое название:</b> {profile_name.capitalize()}\n'
                              f'<b>Новое название:</b> {message.text.capitalize()}',
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
            text=f'<b>Ошибка:</b> Профиль с названием <b>{profile_title.capitalize()}</b> уже существует, '
                 f'либо был введен неверный ID')
        await state.clear()
        await change_profiles(message=callback.message, state=state, bot=bot)


@rt.callback_query(Text('change_desc_title_false'))
async def change_desc_title_false(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await callback.message.delete()
    await change_profiles(message=callback.message, state=state, bot=bot)


@rt.callback_query(Text('add_comp_from_desc'))
async def add_competence_from_profile(callback: CallbackQuery, state: FSMContext):
    comp_list = '\n'.join(list(map(lambda x: f'<b>[ID: {x[0]}]</b> {x[1].capitalize()}', get_competencies_list())))
    await callback.message.answer(text=f'Введите ID компетенции, которую хотите добавить в профиль\n'
                                       f'Список компетенций:\n\n'
                                       f'{comp_list}')
    await state.set_state(Profile.add_competence)


@rt.message(Profile.add_competence)
async def add_competence_from_profile_start(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    profile_id = data['changeable_id']

    try:
        if data['add_competence']:
            await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                                message_id=message.message_id - 1,
                                                reply_markup=None)
    except KeyError:
        pass

    await state.update_data(add_competence=message.text)
    if add_competence_in_profile(competence_id=message.text, profile_id=profile_id):
        await message.answer(text=f"Компетенция c ID: {message.text} успешно добавлена. \n"
                                  f"Введите ID Следующей компетенции, которую хотите добавить",
                             reply_markup=change_profile_end_adding_competencies())
    elif competence_in_profile(profile_id=profile_id, competence_id=message.text):
        await message.answer(text=f'<b>Ошибка:</b> Компетенция с <b>[ID: {message.text.lower()}]</b> '
                                  f'уже добавлена, удалите ее или продолжите ввод',
                             reply_markup=change_profile_end_adding_competencies())
    else:
        await message.answer(text=f"<b>Ошибка:</b> Компетенция с <b>[ID: {message.text.lower()}]</b> "
                                  f"не найдена, повторите ввод",
                             reply_markup=end_change_profile_end_adding_competencies())


@rt.callback_query(Text('change_profile_end_adding_competencies'))
async def end_add_competencies_profile(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await callback.message.delete()
    await change_profiles(message=callback.message, state=state, bot=bot)
    await callback.message.answer(text='Компетенции успешно добавлены в профиль')


@rt.callback_query(Text('change_profile_delete_competencies'))
async def delete_competence_profile(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    profile_id = data['changeable_id']
    competence_id = data['add_competence']
    remove_competence_from_profile(competence_id=competence_id, profile_id=profile_id)
    await callback.message.delete()
    await callback.message.answer(text=f'Компетенция <b>[ID: {competence_id}] {get_competence_title(competence_id)[0].capitalize()}</b> '
                                       f'удалена из профиля, продолжайте ввод',
                                  reply_markup=end_change_profile_end_adding_competencies())


@rt.callback_query(Text('delete_comp_from_desc'))
async def delete_competence_from_profile_start(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    profile_id = data['changeable_id']
    data_list = competencies_in_profile(profile_id)
    title_list = list(map(lambda x: get_competence_title(x), data_list))
    competence_list = '\n'.join(list(map(lambda x, y: f'<b>[ID: {y}]</b> {x[0].capitalize()}', title_list, data_list)))
    await callback.message.answer(text=f'Введите ID компетенции, которую хотите удалить из профиля '
                                       f'<b>{get_profile_name(profile_id).capitalize()}</b>\n'
                                       f'Список компетенций в профиле:\n\n'
                                       f'{competence_list}')
    await state.set_state(Profile.delete_competence)


@rt.message(Profile.delete_competence)
async def delete_competence_from_profile_end(message: types.Message, state: FSMContext):
    data = await state.get_data()
    profile_id = data['changeable_id']
    if delete_competence_from_profile(competence_id=message.text, profile_id=profile_id):
        await message.answer(text=f'Компетенция <b>[ID: {message.text}] {get_competence_title(message.text)[0].capitalize()}</b> '
                                  f'успешно удалена из профиля, продолжайте ввод',
                             reply_markup=confirmation_end_adding_competence())
    else:
        await message.answer(text=f'<b>Ошибка:</b> Компетенции с <b>[ID: {message.text.lower()}]</b> '
                                  f'нет в профиле, либо был введен неверный ID, повторите ввод')


@rt.callback_query(Text('end_add_competence_in_profile'))
async def end_add_comp_in_profile(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await choosing_actions_profile(message=callback.message, state=state)
    await change_profiles(message=callback.message, state=state, bot=bot)
