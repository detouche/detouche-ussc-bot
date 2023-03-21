from loader import bot
from telebot.types import Message

from keyboards.reply.admin_delete_profile import admin_delete_profile
from handlers.custom_handlers.admin_choosing_actions_profile import choosing_actions_profile


def delete_profile(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Список профилей',
                     reply_markup=admin_delete_profile())


def delete_profile_number(message: Message) -> None:
    if message.text == 'Да':
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Успешное удаление')
        choosing_actions_profile(message)
    elif message.text == 'Нет':
        delete_profile(message)
