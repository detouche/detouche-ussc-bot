from loader import rt
from aiogram import types
from aiogram.filters import Text

from keyboards.reply.user_start_evaluation import user_start_evaluation

from handlers.custom_handlers.role import user_command


@rt.message(Text('Начать сессию'))
@user_command
async def user_start_evaluation_info(message: types.Message):
    await message.answer(text=f'Информация о кандидате:\n'
                              f'— ФИО\n'
                              f'— Профиль\n'
                              f'— Компетенции\n'
                              f'Методичка по оценкам',
                         reply_markup=user_start_evaluation)
