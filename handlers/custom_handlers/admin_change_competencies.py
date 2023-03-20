from loader import bot
from telebot.types import Message
from keyboards.reply.admin_change_competencies import admin_change_competencies


def change_competencies(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Выбор нужной компетенции', reply_markup=admin_change_competencies())

