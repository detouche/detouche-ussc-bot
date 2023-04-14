from loader import rt
from aiogram import types
from aiogram.filters import Text


@rt.message(Text('Удалить администратора'))
async def delete_admin(message: types.Message):
    await message.answer(text=f'Список всех существующих администраторов')
