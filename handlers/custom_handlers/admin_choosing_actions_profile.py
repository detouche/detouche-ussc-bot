from loader import bot
from telebot.types import Message

from keyboards.reply.admin_choosing_actions_profile import admin_choosing_actions_profile

from handlers.custom_handlers.role import admin_command


@admin_command
def choosing_actions_profile(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Информация про существующие профили:\n'
                          f'— Названия\n'
                          f'— Компетенции',
                     reply_markup=admin_choosing_actions_profile())
