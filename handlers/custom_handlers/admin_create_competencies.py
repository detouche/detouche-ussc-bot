from loader import bot
from telebot.types import Message

from handlers.custom_handlers.admin_choosing_actions_competencies import choosing_actions_competencies
from keyboards.reply.admin_create_competencies import admin_create_competencies


def add_competencies(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'1. Ввод названия компетенции',
                     reply_markup=admin_create_competencies())
    add_competencies_description(message)


def add_competencies_description(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'2. Ввод ее описания')
    add_competencies_successfully(message)


def add_competencies_successfully(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Информация про успешное создание компетенции')
    choosing_actions_competencies(message)
