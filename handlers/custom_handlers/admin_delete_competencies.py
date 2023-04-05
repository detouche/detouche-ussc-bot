from loader import rt
from aiogram import types
from aiogram.filters import Text

from handlers.custom_handlers.admin_choosing_actions_competencies import choosing_actions_competencies
from keyboards.reply.admin_delete_competencies import admin_delete_competencies

from handlers.custom_handlers.role import admin_command


@admin_command
@rt.message(Text('Удалить компетенцию'))
async def delete_competencies(message: types.Message):
    await message.answer(text=f'Компетенция удалена',
                         reply_markup=admin_delete_competencies)
