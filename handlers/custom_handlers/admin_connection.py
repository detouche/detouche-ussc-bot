from aiogram import types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from loader import rt

from keyboards.reply.admin_connection import admin_connection
from keyboards.reply.main_admin_connection import main_admin_connection

from handlers.custom_handlers.role import admin_command

from database.connection_db import get_admins_list_by_column


@rt.message(Text('Назад в главное меню'))
@admin_command
async def admin_start(message: types.Message, state: FSMContext, *args, **kwargs):
    await state.clear()
    admin_id = message.chat.id
    if admin_id in get_admins_list_by_column(0):
        await message.answer(text=f'Что выберете?',
                             reply_markup=admin_connection)
    else:
        await message.answer(text=f'Что выберете?',
                             reply_markup=main_admin_connection)
