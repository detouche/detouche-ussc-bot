from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.admin_create_session import admin_create_session

from handlers.custom_handlers.role import admin_command


@admin_command
@rt.message(Text('Создать сессию'))
async def create_session(message: types.Message):
    await message.answer(text=f' Ввод информации по кандидату:\n'
                              f'— ФИО\n'
                              f'— Выбор профиля',
                         reply_markup=admin_create_session)
