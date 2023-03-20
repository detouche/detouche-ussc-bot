from keyboards.reply.admin_change_competencies_name_or_description import admin_change_competencies_name_or_description
from loader import bot
from telebot.types import Message


def change_competencies_name_or_description(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Данные о компетенции',
                     reply_markup=admin_change_competencies_name_or_description())
