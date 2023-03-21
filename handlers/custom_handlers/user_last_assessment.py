from loader import bot
from telebot.types import Message

from keyboards.reply.user_last_assessment import user_last_assessment


def assessment_last(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Информация об успешной оценке',
                     reply_markup=user_last_assessment())
