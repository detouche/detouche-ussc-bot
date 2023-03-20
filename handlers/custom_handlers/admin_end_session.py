from handlers.custom_handlers.admin_connection import admin_start
from handlers.custom_handlers.admin_successful_creation_session import successful_creation
from loader import bot
from telebot.types import Message


def end_session(message: Message) -> None:
    if message.text == 'Да':
        bot.send_message(message.from_user.id, f'Успешное завершение \n'
                                               f'Информация о кандидате')
        admin_start(message)
    elif message.text == 'Нет':
        successful_creation(message)
