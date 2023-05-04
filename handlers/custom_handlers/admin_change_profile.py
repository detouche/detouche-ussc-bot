from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.admin_change_profile import admin_change_profile

from handlers.custom_handlers.role import admin_command


@rt.message(Text('Редактировать профиль'))
@admin_command
async def change_competencies_name_or_description(message: types.Message):
    await message.answer(text=f'Выберите профиль, который хотите изменить \n'
                              f'Список доступных профилей',
                         reply_markup=admin_change_profile)
