from keyboards.reply.admin_successful_creation import admin_successful_creation
from loader import bot
from telebot.types import Message


def successful_creation(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Успешное создание \n'
                                           f'Код для присоединения к сессии',
                     reply_markup=admin_successful_creation())

