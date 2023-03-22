from loader import bot
from telebot.types import Message

from handlers.custom_handlers.admin_choosing_actions_profile import choosing_actions_profile

from handlers.custom_handlers.role import admin_command


@admin_command
def change_profile_competencies(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Сообщение об успешном изменении')
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Профиль, который был изменен')
    choosing_actions_profile(message)

