from loader import bot
from telebot.types import Message

from handlers.custom_handlers.admin_connection import admin_start
from handlers.custom_handlers.admin_successful_creation_session import successful_creation

from handlers.custom_handlers.role import admin_command


@admin_command
def end_session(message: Message) -> None:
    if message.text == 'Да':
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Успешное завершение \n'
                              f'Информация о кандидате')
        admin_start(message)
    elif message.text == 'Нет':
        successful_creation(message)
