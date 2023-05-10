from loader import rt
from aiogram import types, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.reply.admin_delete_competencies import admin_delete_competencies
from keyboards.reply.admin_choosing_actions_competencies import admin_choosing_actions_competencies

from keyboards.inline.confirmation_delete_competence import confirmation_delete_competence

from states.competencies import Competence

from database.connection_db import delete_competence, get_competencies_list, check_competence_id

from handlers.custom_handlers.admin_choosing_actions_competencies import choosing_actions_competencies
from handlers.custom_handlers.admin_choosing_actions_competencies import creating_pdf
from handlers.custom_handlers.role import admin_command


@rt.message(Text('Удалить компетенцию'))
@admin_command
async def delete_competencies(message: types.Message, state: FSMContext, bot: Bot, *args, **kwargs):
    await state.set_state(Competence.delete)
    data_list = get_competencies_list()
    comp_list = '\n'.join(list(map(lambda x: f'ID: {x[0]} Name: {x[1]}', data_list)))
    await message.answer(text=f'Введите ID компетенции, которую необходимо удалить. \n'
                              f'Список всех имеющихся компетенций: \n{comp_list}',
                         reply_markup=admin_delete_competencies)
    await creating_pdf(bot, message)


@rt.message(Competence.delete)
async def delete_competence_handler(message: types.Message, state: FSMContext):
    await state.update_data(delete=message.text)
    if check_competence_id(message.text):
        await message.answer(text=f"Вы уверены что хотите удалить компетенцию с ID:{message.text} ",
                             reply_markup=confirmation_delete_competence())
    else:
        await message.answer(text='Такого ID компетенции не существует!',
                             reply_markup=admin_choosing_actions_competencies)


@rt.callback_query(Text('delete_competence_true'))
@admin_command
async def delete_competence_true(callback: CallbackQuery, state: FSMContext, *args, **kwargs):
    data = await state.get_data()
    delete_comp = data['delete']
    await callback.message.edit_text(text='Компетенция успешно удалена.')
    delete_competence(delete_comp)
    await state.clear()
    await choosing_actions_competencies(callback.message, state)


@rt.callback_query(Text('delete_competence_false'))
@admin_command
async def delete_competence_false(callback: CallbackQuery, state: FSMContext, bot: Bot, *args, **kwargs):
    await delete_competencies(callback.message, state, bot)
