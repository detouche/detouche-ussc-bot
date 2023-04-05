from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.user_change_assessment import user_change_assessment

from handlers.custom_handlers.role import user_command


@user_command
@rt.message(Text('Изменить оценку'))
async def change_assessment(message: types.Message):
    await message.answer(text=f'Список компетенций',
                         reply_markup=user_change_assessment)
