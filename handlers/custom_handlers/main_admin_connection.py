from aiogram import types
from aiogram.filters import Text
from loader import rt

from keyboards.reply.main_admin_connection import main_admin_connection


@rt.message(Text('Назад в главное меню'))
async def main_admin_start(message: types.Message):
    await message.answer(text=f'Что выберете?',
                         reply_markup=main_admin_connection)
