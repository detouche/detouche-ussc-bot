from loader import bot
from telebot.types import Message

from handlers.custom_handlers.admin_choosing_actions_competencies import choosing_actions_competencies

from handlers.custom_handlers.role import admin_command


@admin_command
def change_competencies_description(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Сообщение об успешном изменении')
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Компетенция, которая была изменена')
    choosing_actions_competencies(message)
