from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.user_last_assessment import user_last_assessment

from handlers.custom_handlers.role import user_command


@rt.message(Text("Оценить компетенцию"))
@user_command
async def assessment_last(message: types.Message):
    await message.answer(text=f'Информация об успешной оценке',
                         reply_markup=user_last_assessment)
