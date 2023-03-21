from loader import bot
from telebot.types import Message

from keyboards.reply.admin_connection import admin_connection


def admin_start(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Что выберете?',
                     reply_markup=admin_connection())
