from loader import bot
from telebot.types import Message

from handlers.custom_handlers.admin_choosing_actions_competencies import choosing_actions_competencies


def change_competencies_name(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Сообщение об успешном изменении')
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Компетенция, которая была изменена')
    choosing_actions_competencies(message)
