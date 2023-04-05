from loader import rt
from aiogram import types
from aiogram.filters import Text

from handlers.custom_handlers.admin_choosing_actions_profile import admin_choosing_actions_profile
from keyboards.reply.admin_delete_profile import admin_delete_profile

from handlers.custom_handlers.role import admin_command


@admin_command
@rt.message(Text('Удалить профиль'))
async def delete_profile(message: types.Message):
    await message.answer(text=f'Список профилей. Профиль успешно удален',
                         reply_markup=admin_delete_profile)
