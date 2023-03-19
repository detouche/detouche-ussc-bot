from keyboards.reply.user_connection import user_connection
from loader import bot
from telebot.types import Message


def user_start(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Ввод кода сессии', reply_markup=user_connection())

