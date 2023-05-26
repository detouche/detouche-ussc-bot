from loader import rt
from aiogram import types, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from keyboards.reply.admin_create_profile import admin_create_profile
from keyboards.reply.admin_choosing_actions_profile import admin_choosing_actions_profile

from handlers.custom_handlers.role import admin_command
from handlers.custom_handlers.admin_choosing_actions_competencies import creating_pdf

from states.profiles import Profile

from database.connection_db import create_profile_db, get_competencies_list, add_competence_in_profile, get_profile_id,\
    get_competence_title, competence_in_profile


@rt.message(Text('Создать профиль'))
@admin_command
async def create_profile(message: types.Message, state: FSMContext, *args, **kwargs):
    await message.answer(text=f"Введите название профиля",
                         reply_markup=admin_create_profile)
    await state.set_state(Profile.title)


@rt.message(Profile.title)
async def create_profile_title(message: types.Message, state: FSMContext, bot: Bot):
    comp_list = '\n'.join(list(map(lambda x: f'[ID: {x[0]}] {x[1].capitalize()}', get_competencies_list())))
    if create_profile_db(message.text.lower()):
        profile_title = message.text.capitalize()
        await message.answer(text=f"Профиль компетенций {profile_title} успешно создан")
        await state.set_state(Profile.competencies)
        await state.update_data(title=message.text.lower().title())
        await message.answer(text=f'Через запятую введите ID компетенций (только цифры), '
                                  f'которые хотите добавить в профиль {profile_title}\n'
                                  f'Список всех имеющихся компетенций:\n\n{comp_list}\n\n'
                                  f'Рекомендуется не более 5-7 компетенций в профиле\n')
        await creating_pdf(bot=bot, message=message)
    else:
        await message.answer(text=f"Ошибка: Профиль с названием {message.text.capitalize()} уже существует",
                             reply_markup=admin_choosing_actions_profile)


@rt.message(Profile.competencies)
async def add_competencies_in_profile(message: types.Message, state: FSMContext):
    profile_name = await state.get_data()
    profile_id = get_profile_id(profile_name=profile_name['title'])
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
        else "\n".join(
        list(map(lambda x: f"[ID: {x}] {get_competence_title(x)[0].capitalize()}", added_competencies_id)))
    already_competencies_list = '...' if len(already_competencies_id) == 0 \
        else "\n".join(
        list(map(lambda x: f"[ID: {x}] {get_competence_title(x)[0].capitalize()}", already_competencies_id)))
    missing_competencies_list = '...' if len(missing_competencies_id) == 0 \
        else ", ".join(list(map(lambda x: f"[ID: {x}]", missing_competencies_id)))
    profile_title = profile_name['title']
    await state.clear()
    await message.answer(text=f'В профиль "{profile_title}" добавлены компетенции:'
                              f'\n{added_competencies_list}\n\n'
                              f'В профиле "{profile_title}" уже имеются следующие компетенции, поэтому они не добавлены:'
                              f'\n{already_competencies_list}\n\n'
                              f'Введены несуществующие ID компетенций:'
                              f'\n{missing_competencies_list}',
                         reply_markup=admin_choosing_actions_profile)
