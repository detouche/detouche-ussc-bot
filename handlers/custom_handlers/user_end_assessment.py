from loader import bot
from telebot.types import Message

from keyboards.reply.user_end_assessment import user_end_assessment


def assessment_end(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Данные кандидата + все проставленные оценки',
                     reply_markup=user_end_assessment())
