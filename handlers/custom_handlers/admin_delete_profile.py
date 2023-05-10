from loader import rt
from aiogram import types, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.reply.admin_delete_profile import admin_delete_profile
from keyboards.inline.confirmation_delete_profile import confirmation_delete_profile

from database.connection_db import delete_profile, get_profile_list, check_profile

from states.profiles import Profile

from handlers.custom_handlers.admin_choosing_actions_profile import creating_pdf
from handlers.custom_handlers.admin_choosing_actions_profile import choosing_actions_profile
from handlers.custom_handlers.role import admin_command


@rt.message(Text('Удалить профиль'))
@admin_command
async def delete_profile_start(message: types.Message, state: FSMContext, bot: Bot, *args, **kwargs):
    await state.set_state(Profile.delete)
    data_profile_list = get_profile_list()
    data_profile_list = '\n'.join(list(map(lambda x: f'ID: {x[0]} Name: {x[1]}', data_profile_list)))
    await message.answer(text=f'Введите ID профиля, который необходимо удалить.\n'
                              f'Список существующих профилей:\n{data_profile_list}',
                         reply_markup=admin_delete_profile)
    await creating_pdf(bot, message)


@rt.message(Profile.delete)
async def delete_profile_end(message: types.Message, state: FSMContext):
    if check_profile(message.text):
        await state.update_data(delete=message.text)
        await message.answer(text=f'Вы уверены, что хотите удалить профиль c ID: {message.text}?',
                             reply_markup=confirmation_delete_profile())
    else:
        await message.answer(text='Такого профиля не существует, либо вы не корректно ввели ID. \n'
                                  'Повторите ввод.')


@rt.callback_query(Text('confirm_delete_profile'))
@admin_command
async def confirmation_delete(callback: CallbackQuery, state: FSMContext, *args, **kwargs):
    data = await state.get_data()
    delete_profile(data['delete'])
    await callback.message.answer(text='Профиль успешно удален.')
    await choosing_actions_profile(callback.message, state)
    await state.clear()


@rt.callback_query(Text('cancel_delete_profile'))
@admin_command
async def cancel_delete(callback: CallbackQuery, state: FSMContext, *args, **kwargs):
    await delete_profile_start(callback.message, state)
