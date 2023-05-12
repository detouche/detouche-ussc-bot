from loader import rt
from aiogram import F
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from database.connection_db import main_admin_add_admin, get_admins_list_by_column, get_user_name_for_id

from handlers.custom_handlers.role import main_admin_command

from states.confirmation import Confirmation, UserInfo
from states.main_admin_add_admin import AdminAction
from states.page_switcher import MenuAddAdmin

from keyboards.inline.main_admin_add_admin import add_admin_get_keyboard
from keyboards.inline.confirmation_add import get_keyboard_confirmation


@rt.message(Text('Добавить администратора'))
@main_admin_command
async def add_admin(message: Message, state: FSMContext, *args, **kwargs):
    await add_admin_keyboard(message, state)


@rt.callback_query(AdminAction.filter(F.action == 'add'))
async def add_admin_callbacks(callback: CallbackQuery, callback_data: AdminAction, state: FSMContext):
    user_id = callback_data.user_id
    user_name = get_user_name_for_id(user_id)
    await callback.message.edit_text(text=f'Вы уверены?',
                                     reply_markup=get_keyboard_confirmation())
    await UserInfo.set_data(state, data={'user_name': user_name, 'user_id': user_id})


@rt.callback_query(Confirmation.filter(F.action == 'confirmation_add'))
async def add_admin_confirmation(callback: CallbackQuery, callback_data: Confirmation, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    user_name = data['user_name']
    user_id = data['user_id']
    admins_id = get_admins_list_by_column(0)
    confirmation = callback_data.confirmation_choice
    if confirmation:
        if user_id in admins_id:
            await callback.message.edit_text(text=f"<b>{user_name.title()}</b> уже является администратором")
        else:
            await callback.message.edit_text(text=f"Успешно! <b>[ID: {user_id}] {user_name.title()}</b> "
                                                  f"теперь администратор")
            main_admin_add_admin(user_id, user_name)
        await add_admin_keyboard(callback.message, state)
    else:
        await callback.message.delete()
        await add_admin_keyboard(callback.message, state)


async def add_admin_keyboard(message: Message, state: FSMContext):
    await state.set_state(MenuAddAdmin.step_add_admin)
    await state.update_data(current_page_index_add_admin=0)
    await add_admin_get_keyboard(message, state, 0)


@rt.callback_query(Text(startswith="next_step_add_admin"), MenuAddAdmin.step_add_admin)
async def add_admin_next_menu(callback: CallbackQuery, state: FSMContext):
    await add_admin_get_keyboard(callback.message, state, 1)


@rt.callback_query(Text(startswith='back_step_add_admin'), MenuAddAdmin.step_add_admin)
async def add_admin_back_menu(callback: CallbackQuery, state: FSMContext):
    await add_admin_get_keyboard(callback.message, state, -1)


@rt.callback_query(Text(startswith='stop_add_admin'), MenuAddAdmin.step_add_admin)
async def add_admin_finish(callback: CallbackQuery, state: FSMContext,):
    await callback.message.delete()
    await callback.message.answer('Добавление администраторов закончено')
    await state.clear()
