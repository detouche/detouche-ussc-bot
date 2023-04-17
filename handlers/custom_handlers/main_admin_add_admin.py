from loader import rt
from aiogram import types, F
from aiogram.filters import Text
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database.connection_db import get_user_list, main_admin_add_admin, get_admins_list

from states.confirmation import Confirmation, UserInfo
from states.main_admin_add_admin import AdminAction

from keyboards.inline.main_admin_add_admin import get_keyboard_with_users
from keyboards.inline.confirmation_add import get_keyboard_confirmation


@rt.message(Text('Добавить администратора'))
async def add_admin(message: types.Message):
    users_list = get_user_list()
    await message.answer(text=f'Вы можете сделать администраторами следующих людей:',
                         reply_markup=get_keyboard_with_users(users_list))


@rt.callback_query(AdminAction.filter(F.action == 'add'))
async def add_admin_callbacks(callback: CallbackQuery, callback_data: AdminAction, state: FSMContext):
    user_name = callback_data.user_name
    user_id = callback_data.user_id
    await callback.message.edit_text(text=f'Вы уверены?',
                                     reply_markup=get_keyboard_confirmation())
    await UserInfo.set_data(state, data={'user_name': user_name, 'user_id': user_id})


@rt.callback_query(Confirmation.filter(F.action == 'confirmation_add'))
async def add_admin_confirmation(callback: CallbackQuery, callback_data: Confirmation, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    user_name = data['user_name']
    user_id = data['user_id']
    admins_id = get_admins_list(0)
    confirmation = callback_data.confirmation_choice
    users_list = get_user_list()
    if confirmation:
        if user_id in admins_id:
            await callback.message.edit_text(text=f"{user_name} уже является администратором")
        else:
            await callback.message.edit_text(text=f"Успешно! {user_name} теперь администратор c id {user_id}")
            main_admin_add_admin(user_id, user_name)
        await callback.message.answer(text=f'Вы можете сделать администраторами следующих людей:',
                                      reply_markup=get_keyboard_with_users(users_list))
    else:
        await callback.message.edit_text(text=f'Вы можете сделать администраторами следующих людей:',
                                         reply_markup=get_keyboard_with_users(users_list))
