from loader import rt
from aiogram import types
from aiogram.filters import Text

from handlers.custom_handlers.admin_choosing_actions_competencies import choosing_actions_competencies

from handlers.custom_handlers.role import admin_command


@admin_command
@rt.message(Text('Изменить описание компетенции'))
async def change_competencies_description(message: types.Message):
    await message.answer(text=f'Сообщение об успещшном изминении описания')
    await message.answer(text=f'Описание компетенции, которая была изменена')
