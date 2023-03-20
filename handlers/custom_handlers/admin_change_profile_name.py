from handlers.custom_handlers.admin_choosing_actions_profile import choosing_actions_profile
from loader import bot
from telebot.types import Message


def change_profile_name(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Сообщение об успешном изменении')
    bot.send_message(message.from_user.id, f'Профиль, который был изменен')
    choosing_actions_profile(message)
