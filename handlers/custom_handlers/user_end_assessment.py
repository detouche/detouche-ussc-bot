from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.user_end_assessment import user_end_assessment

from handlers.custom_handlers.role import user_command


@user_command
@rt.message(Text('Оценить последнюю компетенцию'))
async def assessment_end(message: types.Message):
    await message.answer(text=f'Данные кандидата + все проставленные оценки',
                         reply_markup=user_end_assessment)
