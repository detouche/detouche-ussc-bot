from loader import bot
from telebot.types import Message

from keyboards.reply.user_start_evaluation import user_start_evaluation

from handlers.custom_handlers.role import user_command


@user_command
def user_start_evaluation_info(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Информация о кандидате:\n'
                          f'— ФИО\n'
                          f'— Профиль\n'
                          f'— Компетенции\n'
                          f'Методичка по оценкам',
                     reply_markup=user_start_evaluation())
