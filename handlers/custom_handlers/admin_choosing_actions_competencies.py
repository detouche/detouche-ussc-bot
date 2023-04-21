from loader import rt
from aiogram import types, html
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from keyboards.reply.admin_choosing_actions_competencies import admin_choosing_actions_competencies
from keyboards.reply.admin_create_competencies import admin_create_competencies

from database.connection_db import get_competencies_list, get_competence_description

from states.competencies import Competence

from handlers.custom_handlers.role import admin_command


@rt.message(Text('Компетенции'))
@rt.message(Text('Назад в меню компетенций'))
async def choosing_actions_competencies(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Вы вошли в меню 'Компетенции'",
                         reply_markup=admin_choosing_actions_competencies)


@rt.message(Text('Список компетенций'))
async def competencies_list(message: types.Message, state: FSMContext):
    data_list = get_competencies_list()
    comp_list = '\n'.join(list(map(lambda x: f'ID: {x[0]} Name: {x[1]}', data_list)))
    await state.set_state(Competence.check_description)
    await message.answer(text=f'Введите ID компетенции для просмотра ее описания. \n'
                              f'Список всех имеющихся компетенций:\n{comp_list}',
                         reply_markup=admin_create_competencies)


@rt.message(Competence.check_description)
async def check_competence_description(message: types.Message):
    description = get_competence_description(message.text.lower())
    if description:
        desc = ('\n'.join(map(str, description)))
        await message.answer(text=f'{desc}',
                             reply_markup=admin_create_competencies)
    else:
        await message.answer(text='Введите существующий ID')
