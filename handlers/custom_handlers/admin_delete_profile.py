from handlers.custom_handlers.admin_choosing_actions_profile import choosing_actions_profile
from loader import bot
from telebot.types import Message
from keyboards.reply.admin_delete_profile import admin_delete_profile


def delete_profile(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Список профилей', reply_markup=admin_delete_profile())


def delete_profile_number(message: Message) -> None:
    if message.text == 'Да':
        bot.send_message(message.from_user.id, f'Успешное удаление')
        choosing_actions_profile(message)
    elif message.text == 'Нет':
        delete_profile(message)
