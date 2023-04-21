from aiogram import types
from aiogram.filters import Text

from database.connection_db import get_admins_list
from loader import rt

from keyboards.reply.admin_connection import admin_connection


@rt.message(Text('Назад в главное меню'))
async def admin_start(message: types.Message):
    await message.answer(text=f'Что выберете?',
                         reply_markup=admin_connection)
