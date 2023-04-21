from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.admin_choosing_actions_profile import admin_choosing_actions_profile

from handlers.custom_handlers.role import admin_command


@rt.message(Text('Профили'))
@rt.message(Text('Назад в меню профилей'))
@admin_command
async def choosing_actions_profile(message: types.Message):
    await message.answer(text=f'Информация про существующие профили:\n'
                              f'— Названия\n'
                              f'— Компетенции',
                         reply_markup=admin_choosing_actions_profile)
