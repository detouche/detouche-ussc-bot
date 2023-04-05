from loader import rt
from aiogram import types
from aiogram.filters import Text

from handlers.custom_handlers.admin_choosing_actions_competencies import choosing_actions_competencies
from keyboards.reply.admin_create_competencies import admin_create_competencies

from handlers.custom_handlers.role import admin_command


@admin_command
@rt.message(Text('Создать компетенцию'))
async def create_session(message: types.Message):
    await message.answer(text=f'Введите данные о компетенции',
                         reply_markup=admin_create_competencies)
