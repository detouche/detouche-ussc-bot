from loader import rt
from aiogram import F
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from database.connection_db import main_admin_delete_admin, get_admins_name_for_id

from handlers.custom_handlers.role import main_admin_command

from states.main_admin_delete_admin import AdminAction
from states.confirmation import Confirmation, AdminInfo
from states.page_switcher import MenuDeleteAdmin

from keyboards.inline.main_admin_delete_admin import delete_admin_get_keyboard
from keyboards.inline.confirmation_delele import get_keyboard_confirmation


@rt.message(Text('Удалить администратора'))
@main_admin_command
async def delete_admin(message: Message, state: FSMContext, *args, **kwargs):
    await delete_admin_keyboard(message, state)


@rt.callback_query(AdminAction.filter(F.action == 'delete'))
async def delete_admin_callbacks(callback: CallbackQuery, callback_data: AdminAction, state: FSMContext):
    admin_id = callback_data.admin_id
    admin_name = get_admins_name_for_id(admin_id)
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
        await delete_admin_keyboard(callback.message, state)
    else:
        await callback.message.delete()
        await delete_admin_keyboard(callback.message, state)


async def delete_admin_keyboard(message: Message, state: FSMContext):
    await state.set_state(MenuDeleteAdmin.step_delete_admin)
    await state.update_data(current_page_index_delete_admin=0)
    await delete_admin_get_keyboard(message, state, 0)


@rt.callback_query(Text(startswith="next_step_delete_admin"), MenuDeleteAdmin.step_delete_admin)
async def delete_admin_next_menu(callback: CallbackQuery, state: FSMContext):
    await delete_admin_get_keyboard(callback.message, state, 1)


@rt.callback_query(Text(startswith='back_step_delete_admin'), MenuDeleteAdmin.step_delete_admin)
async def delete_admin_back_menu(callback: CallbackQuery, state: FSMContext):
    await delete_admin_get_keyboard(callback.message, state, -1)


@rt.callback_query(Text(startswith='stop_delete_admin'), MenuDeleteAdmin.step_delete_admin)
async def delete_admin_finish(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Удаление администраторов закончено')
    await state.clear()
