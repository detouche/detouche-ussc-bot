from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.main_admin_delete_or_add_admin import main_admin_delete_or_add_admin

from database.connection_db import get_admins_list


@rt.message(Text('Администраторы'))
async def delete_or_add_admin(message: types.Message):
    admins_name = ('\n'.join(get_admins_list(1)))
    await message.answer(text=f'Сейчас администраторами являются: \n{admins_name}.',
                         reply_markup=main_admin_delete_or_add_admin)
