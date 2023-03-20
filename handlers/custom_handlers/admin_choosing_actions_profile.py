from keyboards.reply.admin_choosing_actions_profile import admin_choosing_actions_profile
from loader import bot
from telebot.types import Message


def choosing_actions_profile(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Информация про существующие профили:\n'
                                           f'— Названия\n'
                                           f'— Компетенции',
                     reply_markup=admin_choosing_actions_profile())
