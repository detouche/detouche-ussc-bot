from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.admin_change_competencies_name_or_description import admin_change_competencies_name_or_description

from handlers.custom_handlers.role import admin_command


@admin_command
@rt.message(Text('Выбрать компетенцию'))
async def change_competencies_name_or_description(message: types.Message):
    await message.answer(text=f'Данные о компетенции',
                         reply_markup=admin_change_competencies_name_or_description)
