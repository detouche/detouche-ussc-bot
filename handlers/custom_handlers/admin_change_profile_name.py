from loader import bot
from telebot.types import Message

from handlers.custom_handlers.admin_choosing_actions_profile import choosing_actions_profile


def change_profile_name(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Сообщение об успешном изменении')
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Профиль, который был изменен')
    choosing_actions_profile(message)
