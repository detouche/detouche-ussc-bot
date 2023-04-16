from loader import rt
from aiogram import types, F
from aiogram.filters import Text
from aiogram.types import CallbackQuery

from database.connection_db import get_user_list, main_admin_add_admin, get_admins_list

from states.main_admin_add_admin import AdminAction
from keyboards.inline.main_admin_add_admin import get_keyboard_with_users

from handlers.custom_handlers.confirmation import confirmation_accept


@rt.message(Text('Добавить администратора'))
async def add_admin(message: types.Message):
    users_list = get_user_list()
    await message.answer(text=f'Вы можете сделать администраторами следующих людей:',
                         reply_markup=get_keyboard_with_users(users_list))


@rt.callback_query(AdminAction.filter(F.action == 'add'))
async def add_admin_callbacks(callback: CallbackQuery, callback_data: AdminAction):
    user_name = callback_data.user_name
    user_id = callback_data.user_id
    admins_id = get_admins_list(0)
    confirmation = await confirmation_accept(callback)
    print(confirmation)
    if confirmation:
        if user_id in admins_id:
            await callback.message.edit_text(text=f"{user_name} уже является администратором")
        else:
            await callback.message.edit_text(text=f"Успешно! {user_name} теперь администратор c id {user_id}")
            main_admin_add_admin(user_id, user_name)
