from loader import rt
from aiogram import types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from keyboards.reply.admin_create_competencies import admin_create_competencies
from keyboards.reply.admin_choosing_actions_competencies import admin_choosing_actions_competencies

from handlers.custom_handlers.role import admin_command

from states.competencies import Competence

from database.connection_db import add_competence, check_competence


@rt.message(Text('Создать компетенцию'))
@admin_command
async def create_competence(message: types.Message, state: FSMContext, *args, **kwargs):
    await message.answer(text=f'Введите название компетенции',
                         reply_markup=admin_create_competencies)
    await state.set_state(Competence.title)


@rt.message(Competence.title)
async def create_competence_title(message: types.Message, state: FSMContext):
    if check_competence(message.text):
        await state.update_data(title=message.text.lower())
        await message.answer(text=f'Введите описание компетенции')
        await state.set_state(Competence.description)
    else:
        await message.answer(text="Такая компетения уже существует.",
                             reply_markup=admin_choosing_actions_competencies)


@rt.message(Competence.description)
async def create_competence_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    competence_data = await state.get_data()
    await state.clear()
    add_competence(competence_data['title'], competence_data['description'])
    await message.answer(text=f'Компетенция {competence_data["title"]} успешно создана.\n'
                              f'Ее описание: {competence_data["description"]}',
                         reply_markup=admin_choosing_actions_competencies)
