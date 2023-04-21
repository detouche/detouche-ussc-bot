from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.admin_change_competencies import admin_change_competencies

from handlers.custom_handlers.role import admin_command


@rt.message(Text('Изменить компетенцию'))
@admin_command
async def change_competencies(message: types.Message):
    await message.answer(text=f'Введите данные о компетенции',
                         reply_markup=admin_change_competencies)
