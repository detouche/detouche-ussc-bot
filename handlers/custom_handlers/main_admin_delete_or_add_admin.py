from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.main_admin_delete_or_add_admin import main_admin_delete_or_add_admin

from handlers.custom_handlers.role import main_admin_command

from database.connection_db import get_admins_list_by_column


@rt.message(Text('Администраторы'))
@main_admin_command
async def delete_or_add_admin(message: types.Message, *args, **kwargs):
    admins_name = ('\n'.join(map(lambda x: f'{x[0]}. <b>{x[1].title()}</b>', enumerate(get_admins_list_by_column(1), 1))))
    await message.answer(text=f'Все администраторы чат-бота:\n'
                              f'{admins_name}',
                         reply_markup=main_admin_delete_or_add_admin)
