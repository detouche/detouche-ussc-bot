from aiogram import types
from aiogram.filters import Text

from database.connection_db import get_admins_list
from loader import rt

from keyboards.reply.admin_connection import admin_connection

from keyboards.reply.main_admin_connection import main_admin_connection

from database.connection_db import get_admins_list


@rt.message(Text('Назад в главное меню'))
async def admin_start(message: types.Message):
    current_id = message.from_user.id
    if current_id in get_admins_list(0):
        await message.answer(text=f'Что выберете?',
                             reply_markup=admin_connection)
    else:
        await message.answer(text=f'Что выберете?',
                             reply_markup=main_admin_connection)
