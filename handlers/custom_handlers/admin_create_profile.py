from loader import bot
from telebot.types import Message

from keyboards.reply.admin_create_profile import admin_create_profile
from keyboards.reply.admin_successful_create_profile import admin_successful_create_profile

from handlers.custom_handlers.role import admin_command


@admin_command
def add_profile(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'1. Ввод названия профиля',
                     reply_markup=admin_create_profile())
    add_profile_successfully(message)


@admin_command
def add_profile_successfully(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Информация про успешное создание профиля + его название')
    add_profile_competencies(message)


@admin_command
def add_profile_competencies(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Список существующих компетенций')
    add_profile_competencies_successfully(message)


@admin_command
def add_profile_competencies_successfully(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Сообщение об успешном добавлении',
                     reply_markup=admin_successful_create_profile())
