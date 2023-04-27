from loader import rt
from aiogram import types
from aiogram.filters import Text

from handlers.custom_handlers.admin_choosing_actions_profile import choosing_actions_profile

from handlers.custom_handlers.role import admin_command


@rt.message(Text('Изменить компетенции профиля'))
@admin_command
async def change_profile_name(message: types.Message):
    await message.answer(text=f'Сообщение об успещшном изминении')
    await message.answer(text=f'Профиль, который был изменен')
