from handlers.custom_handlers.admin_choosing_actions_competencies import choosing_actions_competencies
from loader import bot
from telebot.types import Message


def change_competencies_description(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Сообщение об успешном изменении')
    bot.send_message(message.from_user.id, f'Компетенция, которая была изменена')
    choosing_actions_competencies(message)
