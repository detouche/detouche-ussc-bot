from loader import bot
from telebot.types import Message
from keyboards.reply.admin_successful_creation import admin_successful_creation


def successful_creation(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Успешное создание \n'
                          f'Код для присоединения к сессии',
                     reply_markup=admin_successful_creation())

