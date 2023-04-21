from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.user_assessment import user_assessment

from handlers.custom_handlers.role import user_command


@rt.message(Text("Начать оценку"))
@user_command
async def user_assessment_process(message: types.Message):
    await message.answer(text=f'Показ компетенции и ее описание',
                         reply_markup=user_assessment)
