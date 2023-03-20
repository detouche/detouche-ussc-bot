from keyboards.reply.admin_create_profile import admin_create_profile
from keyboards.reply.admin_successful_create_profile import admin_successful_create_profile
from loader import bot
from telebot.types import Message


def add_profile(message: Message) -> None:
    bot.send_message(message.from_user.id, f'1. Ввод названия профиля', reply_markup=admin_create_profile())
    add_profile_successfully(message)


def add_profile_successfully(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Информация про успешное создание компетенции + его название')
    add_profile_competencies(message)


def add_profile_competencies(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Список существующих компетенций')
    add_profile_competencies_successfully(message)


def add_profile_competencies_successfully(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Сообщение об успешном добавлении',
                     reply_markup=admin_successful_create_profile())
