from loader import rt
from aiogram import types

from keyboards.reply.user_connection import user_connection


async def user_start(message: types.Message):
    await message.answer(text=f'Ввод кода сессии',
                         reply_markup=user_connection)
