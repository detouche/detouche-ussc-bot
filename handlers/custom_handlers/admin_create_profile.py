from loader import rt
from aiogram import types, Bot
from aiogram.types import CallbackQuery
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from keyboards.reply.admin_create_profile import admin_create_profile
from keyboards.reply.admin_choosing_actions_profile import admin_choosing_actions_profile

from keyboards.inline.end_adding_competencies import end_adding_competencies, end_adding_competencies_error

from handlers.custom_handlers.role import admin_command

from states.profiles import Profile

from database.connection_db import create_profile_db, get_competencies_list, add_competence_in_profile, get_profile_id, \
    remove_competence_from_profile, get_competence_title, get_profile_competencies, competence_in_profile


@rt.message(Text('Создать профиль'))
@admin_command
async def create_profile(message: types.Message, state: FSMContext, *args, **kwargs):
    await message.answer(text=f"Введите название профиля",
                         reply_markup=admin_create_profile)
    await state.set_state(Profile.title)


@rt.message(Profile.title)
async def create_profile_title(message: types.Message, state: FSMContext):
    comp_list = '\n'.join(list(map(lambda x: f'<b>[ID: {x[0]}]</b> {x[1].capitalize()}', get_competencies_list())))
    if create_profile_db(message.text.lower()):
        await message.answer(text=f"Профиль компетенций <b>{message.text.capitalize()}</b> успешно создан")
        await state.set_state(Profile.competencies)
        await state.update_data(title=message.text.lower().title())
        await message.answer(text=f"Введите ID компетенций, которые хотите добавить в профиль\n"
                                  f"Список всех имеющихся компетенций:\n\n{comp_list}")
    else:
        await message.answer(text=f"<b>Ошибка:</b> Профиль с названием <b>{message.text.capitalize()}</b> уже существует",
                             reply_markup=admin_choosing_actions_profile)


@rt.message(Profile.competencies)
async def add_competencies_in_profile(message: types.Message, state: FSMContext, bot: Bot):
    profile_name = await state.get_data()
    profile_id = get_profile_id(profile_name=profile_name['title'])
    try:
        if profile_name['competencies']:
            await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                                message_id=message.message_id - 1,
                                                reply_markup=None)
    except KeyError:
        pass

    await state.update_data(competencies=message.text)
    if add_competence_in_profile(competence_id=message.text, profile_id=profile_id):
        competence_name = get_competence_title(message.text)[0]
        await message.answer(text=f"Компетенция <b>[ID: {message.text}] {competence_name.capitalize()}</b> "
                                  f"успешно добавлена.\n"
                                  f"Введите ID следующей компетенции, которую хотите добавить",
                             reply_markup=end_adding_competencies())
    elif competence_in_profile(profile_id=profile_id, competence_id=message.text):
        await message.answer(text=f'<b>Ошибка:</b> Компетенция с <b>[ID: {message.text.lower()}]</b> '
                                  f'уже добавлена, удалите ее или продолжите ввод',
                             reply_markup=end_adding_competencies())
    else:
        await message.answer(text=f'<b>Ошибка:</b> Компетенция с <b>[ID: {message.text.lower()}]</b> '
                                  f'не найдена, повторите ввод',
                             reply_markup=end_adding_competencies_error())


@rt.callback_query(Text('end_adding_competencies'))
async def end_add_competencies_profile(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    profile_id = get_profile_id(data['title'])
    competencies_list = get_profile_competencies(profile_id=profile_id)
    comp_list = '\n'.join(list(map(lambda x: f'<b>[ID: {x}]</b> {get_competence_title(x)[0].capitalize()}',
                                   competencies_list)))
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text=f'Компетенции успешно добавлены в профиль:\n\n'
                                       f'{comp_list}',
                                  reply_markup=admin_choosing_actions_profile)


@rt.callback_query(Text('delete_competencies'))
async def delete_competence_in_profile(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    profile_id = get_profile_id(data['title'])
    competence_id = data['competencies']
    remove_competence_from_profile(competence_id=competence_id, profile_id=profile_id)
    await callback.message.delete()
    await callback.message.answer(text='Компетенция удалена из профиля. Продолжайте ввод.',
                                  reply_markup=end_adding_competencies_error())
