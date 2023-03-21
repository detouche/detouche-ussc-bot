from loader import bot
from telebot.types import Message

from keyboards.reply.user_connection import user_connection


def user_start(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Ввод кода сессии',
                     reply_markup=user_connection())

