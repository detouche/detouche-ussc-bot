from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.main_admin_delete_or_add_admin import main_admin_delete_or_add_admin

from handlers.custom_handlers.role import main_admin_command

from database.connection_db import get_admins_list


@rt.message(Text('Администраторы'))
@main_admin_command
async def delete_or_add_admin(message: types.Message, *args, **kwargs):
    admins_name = ('\n'.join(get_admins_list(1)))
    await message.answer(text=f'Сейчас администраторами являются: \n{admins_name}.',
                         reply_markup=main_admin_delete_or_add_admin)
