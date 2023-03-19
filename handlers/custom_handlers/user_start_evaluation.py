from keyboards.reply.user_start_evaluation import user_start_evaluation
from loader import bot
from telebot.types import Message


def user_start_evaluation_info(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Информация о кандидате:\n'
                                           f'— ФИО\n'
                                           f'— Профиль\n'
                                           f'— Компетенции\n'
                                           f'Методичка по оценкам', reply_markup=user_start_evaluation())

