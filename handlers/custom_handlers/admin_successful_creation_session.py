from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.admin_successful_creation import admin_successful_creation

from handlers.custom_handlers.role import admin_command


@admin_command
@rt.message(Text('Профили на выбор'))
async def successful_creation(message: types.Message):
    await message.answer(text=f'Успешное создание \n'
                              f'Код для присоединения к сессии',
                         reply_markup=admin_successful_creation)
