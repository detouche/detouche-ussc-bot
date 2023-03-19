from keyboards.reply.user_end_assessment import user_end_assessment
from loader import bot
from telebot.types import Message


def assessment_end(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Данные кандидата + все проставленные оценки',
                     reply_markup=user_end_assessment())
