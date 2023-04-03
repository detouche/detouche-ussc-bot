from loader import bot
from telebot.types import Message

from keyboards.reply.user_end_assessment import user_end_assessment

from handlers.custom_handlers.role import user_command


@user_command
def assessment_end(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Данные кандидата + все проставленные оценки',
                     reply_markup=user_end_assessment())


@rt.message(Text('Начать оценку'))
async def user_start_evaluation_info(message: types.Message):
    await message.answer(text=f'Информация о кандидате:\n'
                              f'— ФИО\n'
                              f'— Профиль\n'
                              f'— Компетенции\n'
                              f'Методичка по оценкам',
                         reply_markup=user_start_evaluation)