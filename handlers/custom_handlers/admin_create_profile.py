from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.admin_create_profile import admin_create_profile

from handlers.custom_handlers.role import admin_command


@rt.message(Text('Создать профиль'))
@admin_command
async def add_profile(message: types.Message):
    await message.answer(text=f'Профиль успешно создан',
                         reply_markup=admin_create_profile)
