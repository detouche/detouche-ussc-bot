from loader import bot
from telebot.types import Message

from keyboards.reply.admin_change_profile import admin_change_profile


def change_profile(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Выбор нужного профиля',
                     reply_markup=admin_change_profile())

