from handlers.custom_handlers.admin_connection import admin_start
from keyboards.reply.admin_create_session import admin_create_session
from loader import bot
from telebot.types import Message


def create_session(message: Message) -> None:
    bot.send_message(message.from_user.id, f' Ввод информации по кандидату:\n'
                                           f'— ФИО\n'
                                           f'— Выбор профиля', reply_markup=admin_create_session())

