from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.main_admin_delete_or_add_admin import main_admin_delete_or_add_admin


@rt.message(Text('Администраторы'))
async def delete_or_add_admin(message: types.Message):
    await message.answer(text=f'Список всех существующих администраторов',
                         reply_markup=main_admin_delete_or_add_admin)
