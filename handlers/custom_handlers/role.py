from loader import bot
from telebot.types import Message
from telebot import types

from handlers.custom_handlers.user_connection import user_start

from handlers.custom_handlers.admin_connection import admin_start

# Никита - 755950556
# Миша - 642205779
# Лёша - 6290014843
# Антон - 476994720
# Игорь - 372233735

ADMINS = [642205779, 6290014843, 755950556, 372233735, 476994720]


@bot.message_handler(commands=['start'])
def role(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Твой ID: {message.from_user.id}')

    customer_id = message.from_user.id
    if customer_id in ADMINS:
        admin_start(message)
    else:
        user_start(message)


def admin_command(func):
    def wrapped(message, *args, **kwargs):
        customer_id = message.from_user.id
        if customer_id not in ADMINS:
            bot.send_message(chat_id=message.from_user.id,
                             text=f'Нет прав',
                             reply_markup=types.ReplyKeyboardRemove())
            return
        return func(message, *args, **kwargs)
    return wrapped


def user_command(func):
    def wrapped(message, *args, **kwargs):
        customer_id = message.from_user.id
        if customer_id in ADMINS:
            bot.send_message(chat_id=message.from_user.id,
                             text=f'Нет прав',
                             reply_markup=types.ReplyKeyboardRemove())
            return
        return func(message, *args, **kwargs)
    return wrapped
