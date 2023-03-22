from loader import bot
from telebot.types import Message

from handlers.custom_handlers.user_end_assessment import assessment_end
from handlers.custom_handlers.user_change_assessment import change_assessment

from handlers.custom_handlers.role import user_command


@user_command
def assessment_again(message: Message) -> None:
    if message.text == 'Да':
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Информация об изменении оценки с какой на какую')
        assessment_end(message)
    elif message.text == 'Нет':
        change_assessment(message)
