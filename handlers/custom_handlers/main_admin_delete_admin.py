from loader import rt
from aiogram import types, F
from aiogram.filters import Text
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database.connection_db import get_admins_list, main_admin_delete_admin

from states.main_admin_delete_admin import AdminAction
from states.confirmation import Confirmation, AdminInfo

from keyboards.inline.main_admin_delete_admin import get_keyboard_with_admins
from keyboards.inline.confirmation_delele import get_keyboard_confirmation


@rt.message(Text('Удалить администратора'))
async def delete_admin(message: types.Message):
    admins_id = get_admins_list(0)
    admins_name = get_admins_list(1)
    await message.answer(text=f'Вы можете удалить следующих администраторов:',
                         reply_markup=get_keyboard_with_admins(admins_id, admins_name))


@rt.callback_query(AdminAction.filter(F.action == 'delete'))
async def delete_admin_callbacks(callback: CallbackQuery, callback_data: AdminAction, state: FSMContext):
    admin_name = callback_data.admin_name
    admin_id = callback_data.admin_id
    await callback.message.edit_text(text=f'Вы уверены?',
                                     reply_markup=get_keyboard_confirmation())
    await AdminInfo.set_data(state, data={'admin_name': admin_name, 'admin_id': admin_id})


@rt.callback_query(Confirmation.filter(F.action == 'confirmation_delete'))
async def delete_admin_confirmation(callback: CallbackQuery, callback_data: Confirmation, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    admin_name = data['admin_name']
    admin_id = data['admin_id']
    confirmation = callback_data.confirmation_choice
    if confirmation:
        await callback.message.edit_text(text=f"Успешно! {admin_name} теперь перестал быть администратором")
        main_admin_delete_admin(admin_id)
    else:
        admins_id = get_admins_list(0)
        admins_name = get_admins_list(1)
        await callback.message.edit_text(text=f'Вы можете удалить следующих администраторов:',
                                         reply_markup=get_keyboard_with_admins(admins_id, admins_name))
