from handlers.custom_handlers.user_end_assessment import assessment_end
from keyboards.reply.user_again_assessment import user_again_assessment
from loader import bot
from telebot.types import Message


def assessment_again(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Информация об изменении оценки с какой на какую',
                     reply_markup=user_again_assessment())
    assessment_end(message)
