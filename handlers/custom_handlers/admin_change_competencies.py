from loader import rt, bot
from aiogram import types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.reply.admin_change_competencies import admin_change_competencies
from keyboards.reply.admin_choosing_actions_competencies import admin_choosing_actions_competencies
from keyboards.inline.change_competence import change_competence
from keyboards.inline.confirmation_change_competence import confirmation_change_competence
from keyboards.inline.confirmation_change_competence_desc import confirmation_change_competence_desc

from states.competencies import Competence

from database.connection_db import change_competence_title, get_competencies_list, change_competence_description, \
    check_competence_id


@rt.message(Text('Изменить компетенцию'))
async def change_competencies(message: types.Message, state: FSMContext):
    competencies_list = get_competencies_list()
    competencies_list = '\n'.join(list(map(lambda x: f'ID: {x[0]} Name: {x[1]}', competencies_list)))
    await message.answer(text=f'ВВедите ID компетенции, которую хотите изменить\n'
                              f'Список доступных компетенций:\n{competencies_list}',
                         reply_markup=admin_change_competencies)
    await state.set_state(Competence.changeable_id)


@rt.message(Competence.changeable_id)
async def get_changeable_competence_id(message: types.Message, state: FSMContext):
    if check_competence_id(message.text):
        if await state.get_data():
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 2)
        await state.update_data(changeable_id=message.text)
        await message.answer(text=f'Что хотите изменить в компетенции с ID: {message.text}',
                             reply_markup=change_competence())
    else:
        await message.answer(text=f'Компетенции с таким ID не существует')
        await state.clear()
        await change_competencies(message, state)


@rt.callback_query(Text('change_competence_title'))
async def change_competence_title_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Competence.change_title)
    await callback.message.answer(text='Введите новое название для компетенции')


@rt.message(Competence.change_title)
async def change_competence_title_confirmation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(change_title=message.text.lower())
    competence_id = data['changeable_id']
    await message.answer(text=f'Вы уверены что хотите изменить название компетенции с ID:{competence_id} на '
                              f'{message.text}',
                         reply_markup=confirmation_change_competence())


@rt.callback_query(Text('change_competence_title_true'))
async def change_competence_title_true(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    competence_id = data['changeable_id']
    competence_title = data['change_title']
    if change_competence_title(competence_id, competence_title):
        await callback.message.edit_text(text='Имя компетенции успешно изменено')
        await state.clear()
        await change_competencies(callback.message, state)
    else:
        await callback.message.edit_text(
            text='Компетенция с таким названием уже существует, либо был введен неверный ID')
        await state.clear()
        await change_competencies(callback.message, state)


@rt.callback_query(Text('change_competence_title_false'))
async def change_competence_title_false(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await change_competencies(callback.message, state)


@rt.callback_query(Text('change_competence_description'))
async def change_competence_description_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Competence.change_description)
    await callback.message.answer(text='Введите новое описание для компетенции')


@rt.message(Competence.change_description)
async def change_competence_title_confirmation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(change_description=message.text.lower())
    competence_id = data['changeable_id']
    await message.answer(text=f'Вы уверены что хотите изменить описание компетенции с ID:{competence_id} на '
                              f'{message.text}',
                         reply_markup=confirmation_change_competence_desc())


@rt.callback_query(Text('change_competence_desc_true'))
async def change_competence_title_true(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    competence_id = data['changeable_id']
    competence_desc = data['change_description']
    if change_competence_description(competence_id, competence_desc):
        await callback.message.edit_text(text='Описание компетенции успешно изменено')
        await state.clear()
        await change_competencies(callback.message, state)
    else:
        await callback.message.edit_text(
            text='Был введен неверный ID, повторите ввод>')
        await state.clear()
        await change_competencies(callback.message, state)


@rt.callback_query(Text('change_competence_desc_false'))
async def change_competence_title_false(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await change_competencies(callback.message, state)
