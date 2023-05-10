from loader import rt
from aiogram import Bot
from aiogram.types import Message
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from states.user_info import User

from database.connection_db import get_session_code

from handlers.custom_handlers.role import user_command


@rt.message(Text("Завершить проверку"))
@user_command
async def user_grading_process(message: Message, bot: Bot, state: FSMContext, *args, **kwargs):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await message.answer(text=f'Проверка кандидата завершена.\n'
                              f'Вы можете изменить поставленные оценки, нажав "Начать оценку"')
    user_id = message.chat.id
    start_session = get_session_code(user_id)
    await state.set_state(User.start_session)
    await state.update_data(start_session=start_session)
    from handlers.custom_handlers.user_start_grading import user_start_grading_info
    await user_start_grading_info(message, state)
