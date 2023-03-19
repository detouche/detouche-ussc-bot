from keyboards.reply.admin_connection import admin_connection
from loader import bot
from telebot.types import Message


def admin_start(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Что выбирите?', reply_markup=admin_connection())
