from loader import rt
from aiogram import types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from keyboards.reply.admin_delete_competencies import admin_delete_competencies
from keyboards.reply.admin_choosing_actions_competencies import admin_choosing_actions_competencies

from states.competencies import Competence

from database.connection_db import delete_competence, get_competencies_list

from handlers.custom_handlers.admin_choosing_actions_competencies import creating_pdf


@rt.message(Text('Удалить компетенцию'))
async def delete_competencies(message: types.Message, state: FSMContext, bot):
    await state.set_state(Competence.delete)
    data_list = get_competencies_list()
    comp_list = '\n'.join(list(map(lambda x: f'ID: {x[0]} Name: {x[1]}', data_list)))
    await message.answer(text=f'Введите ID компетенции, которую необходимо удалить. \n'
                              f'Список всех имеющихся компетенций: \n{comp_list}',
                         reply_markup=admin_delete_competencies)
    await creating_pdf(bot, message)


@rt.message(Competence.delete)
async def delete_competence_handler(message: types.Message, state: FSMContext):
    if delete_competence(message.text):
        await message.answer(text="Компетенция успешно удалена",
                             reply_markup=admin_choosing_actions_competencies)
    else:

        await message.answer(text='Такого ID компетенции не существует!',
                             reply_markup=admin_choosing_actions_competencies)
    await state.clear()



