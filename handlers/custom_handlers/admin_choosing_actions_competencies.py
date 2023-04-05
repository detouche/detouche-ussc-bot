from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.admin_choosing_actions_competencies import admin_choosing_actions_competencies

from handlers.custom_handlers.role import admin_command


@admin_command
@rt.message(Text(['Компетенции']))
@rt.message(Text(['Назад в меню компетенций']))
async def choosing_actions_competencies(message: types.Message):
    await message.answer(text=f'Список всех имеющихся компетенций',
                         reply_markup=admin_choosing_actions_competencies)