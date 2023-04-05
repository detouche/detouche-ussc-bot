from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.admin_change_profile_name_or_competencies import admin_change_profile_name_or_competencies

from handlers.custom_handlers.role import admin_command


@admin_command
@rt.message(Text('Выбрать профиль'))
async def change_profile_name_or_competencies(message: types.Message):
    await message.answer(text=f'Данные о профиле',
                         reply_markup=admin_change_profile_name_or_competencies)