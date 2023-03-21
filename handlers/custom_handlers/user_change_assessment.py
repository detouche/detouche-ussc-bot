from loader import bot
from telebot.types import Message

from keyboards.reply.user_change_assessment import user_change_assessment


def change_assessment(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Список компетенций',
                     reply_markup=user_change_assessment())
