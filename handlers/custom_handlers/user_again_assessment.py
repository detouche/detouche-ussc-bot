from handlers.custom_handlers.user_end_assessment import assessment_end
from handlers.custom_handlers.user_change_assessment import change_assessment
from loader import bot
from telebot.types import Message


def assessment_again(message: Message) -> None:
    if message.text == 'Да':
        bot.send_message(message.from_user.id, f'Информация об изменении оценки с какой на какую')
        assessment_end(message)
    elif message.text == 'Нет':
        change_assessment(message)
