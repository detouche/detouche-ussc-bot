from loader import bot
from telebot.types import Message

from keyboards.reply.admin_create_session import admin_create_session

from handlers.custom_handlers.role import admin_command


@admin_command
def create_session(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f' Ввод информации по кандидату:\n'
                          f'— ФИО\n'
                          f'— Выбор профиля',
                     reply_markup=admin_create_session())
