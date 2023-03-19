from loader import bot
from telebot.types import Message


def finish(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Спасибо, до свидания')
