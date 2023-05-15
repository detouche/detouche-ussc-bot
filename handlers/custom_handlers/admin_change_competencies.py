from loader import rt
from aiogram import types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.custom_handlers.role import admin_command

from keyboards.reply.admin_change_competence import admin_change_competence

from keyboards.inline.change_competence import change_competence
from keyboards.inline.confirmation_change_competence import confirmation_change_competence
from keyboards.inline.confirmation_change_competence_desc import confirmation_change_competence_desc

from states.competencies import Competence

from database.connection_db import change_competence_title, get_competencies_list, change_competence_description, \
    check_competence_id, get_competence_title, get_competence_description


@rt.message(Text('Изменить компетенцию'))
@admin_command
async def change_competencies(message: types.Message, state: FSMContext, *args, **kwargs):
    competencies_list = '\n'.join(list(map(lambda x: f'[ID: {x[0]}] {x[1].capitalize()}', get_competencies_list())))
    await message.answer(text=f'Введите ID компетенции, которую хотите изменить\n'
                              f'Список всех компетенций:\n\n{competencies_list}',
                         reply_markup=admin_change_competence)
    await state.set_state(Competence.changeable_id)


@rt.message(Competence.changeable_id)
async def get_changeable_competence_id(message: types.Message, state: FSMContext):
    await state.clear()
    if check_competence_id(competence_id=message.text):
        competence_name = get_competence_title(message.text.lower())[0]
        competence_description = get_competence_description(message.text.lower())[0]
        await state.update_data(changeable_id=message.text)
        await message.answer(text=f'Что хотите изменить в компетенции?\n\n'
                                  f'Название: {competence_name.capitalize()}\n'
                                  f'Описание: {competence_description.capitalize()}',
                             reply_markup=change_competence())
    else:
        await message.answer(text=f'Ошибка: Компетенция с ID: {message.text.lower()} не найдена, повторите ввод')
        await change_competencies(message=message, state=state)


@rt.callback_query(Text('change_competence_title'))
async def change_competence_title_start(callback: CallbackQuery, state: FSMContext):
    competence_id = await state.get_data()
    competence_name = get_competence_title(competence_id['changeable_id'])[0]
    await state.set_state(Competence.change_title)
    await callback.message.answer(text=f'Введите новое название для компетенции:\n\n'
                                       f'[ID: {competence_id["changeable_id"]}] {competence_name.capitalize()}')


@rt.message(Competence.change_title)
async def change_competence_title_confirmation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await state.update_data(change_title=message.text.lower())
    await state.update_data(changeable_id=data['changeable_id'])
    competence_id = data['changeable_id']
    competence_name = get_competence_title(competence_id=competence_id)[0]
    await message.answer(text=f'Вы уверены, что хотите изменить название компетенции?\n\n'
                              f'Старое название: {competence_name.capitalize()}\n'
                              f'Новое название: {message.text.capitalize()}',
                         reply_markup=confirmation_change_competence())


@rt.callback_query(Text('change_competence_title_true'))
async def change_competence_title_true(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    competence_id = data['changeable_id']
    competence_title = data['change_title']
    if change_competence_title(competence_id=competence_id, new_competence_name=competence_title):
        await callback.message.edit_text(text='Название компетенции успешно изменено')
        await state.clear()
        await change_competencies(message=callback.message, state=state)
    else:
        await callback.message.edit_text(
            text=f'Ошибка: Компетенция с названием {competence_title.capitalize()} уже существует, '
                 f'либо был введен неверный ID')
        await state.clear()
        await change_competencies(message=callback.message, state=state)


@rt.callback_query(Text('change_competence_title_false'))
async def change_competence_title_false(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await change_competencies(message=callback.message, state=state)


@rt.callback_query(Text('change_competence_description'))
async def change_competence_description_start(callback: CallbackQuery, state: FSMContext):
    competence_id = await state.get_data()
    competence_name = get_competence_title(competence_id['changeable_id'])[0]
    await state.set_state(Competence.change_description)
    await callback.message.answer(text=f'Введите новое описание для компетенции:\n\n'
                                       f'[ID: {competence_id["changeable_id"]}] {competence_name.capitalize()}')


@rt.message(Competence.change_description)
async def change_competence_description_confirmation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await state.update_data(change_description=message.text.lower())
    await state.update_data(changeable_id=data['changeable_id'])
    competence_id = data['changeable_id']
    competence_description = get_competence_description(competence_id=competence_id)[0]
    await message.answer(text=f'Вы уверены, что хотите изменить описание компетенции?\n\n'
                              f'Старое описание: {competence_description.capitalize()}\n'
                              f'Новое описание: {message.text.capitalize()}',
                         reply_markup=confirmation_change_competence_desc())


@rt.callback_query(Text('change_competence_desc_true'))
async def change_competence_description_true(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    competence_id = data['changeable_id']
    competence_desc = data['change_description']
    if change_competence_description(competence_id=competence_id, new_competence_description=competence_desc):
        await callback.message.edit_text(text=f'Описание компетенции успешно изменено')
        await state.clear()
        await change_competencies(message=callback.message, state=state)


@rt.callback_query(Text('change_competence_desc_false'))
async def change_competence_description_false(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await change_competencies(message=callback.message, state=state)


@rt.callback_query(Text('select_any_competence'))
async def change_competence_title_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await change_competencies(callback.message, state)
