from loader import rt
from aiogram import types, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.reply.admin_delete_profile import admin_delete_profile
from keyboards.inline.confirmation_delete_profile import confirmation_delete_profile

from database.connection_db import delete_profile, get_profile_list, check_profile, get_profile_name

from states.profiles import Profile

from handlers.custom_handlers.admin_choosing_actions_profile import creating_pdf
from handlers.custom_handlers.admin_choosing_actions_profile import choosing_actions_profile
from handlers.custom_handlers.role import admin_command


@rt.message(Text('Удалить профиль'))
@admin_command
async def delete_profile_start(message: types.Message, state: FSMContext, bot: Bot, *args, **kwargs):
    await state.set_state(Profile.delete)
    data_profile_list = '\n'.join(list(map(lambda x: f'[ID: {x[0]}] {x[1].capitalize()}', get_profile_list())))
    await message.answer(text=f'Введите ID профиля, который необходимо удалить\n'
                              f'Список всех профилей:\n\n{data_profile_list}',
                         reply_markup=admin_delete_profile)
    await creating_pdf(bot=bot, message=message)


@rt.message(Profile.delete)
async def delete_profile_end(message: types.Message, state: FSMContext):
    await state.clear()
    if check_profile(message.text):
        profile_name = get_profile_name(message.text)
        await state.update_data(delete=message.text)
        await message.answer(text=f'Вы уверены, что хотите удалить профиль [ID: {message.text}] '
                                  f'{profile_name.capitalize()}?',
                             reply_markup=confirmation_delete_profile())
    else:
        await message.answer(text=f'Ошибка: Профиля с ID: {message.text.lower()} не существует, повторите ввод')
        await state.set_state(Profile.delete)


@rt.callback_query(Text('confirm_delete_profile'))
async def confirmation_delete(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    profile_name = get_profile_name(data['delete'])
    delete_profile(profile_id=data['delete'])
    await callback.message.answer(text=f'Профиль [ID: {data["delete"]}] '
                                       f'{profile_name.capitalize()} успешно удален')
    await choosing_actions_profile(message=callback.message, state=state)
    await state.clear()


@rt.callback_query(Text('cancel_delete_profile'))
async def cancel_delete(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await delete_profile_start(message=callback.message, state=state, bot=bot)
