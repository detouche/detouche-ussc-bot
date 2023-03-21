from loader import bot
from telebot.types import Message

from keyboards.reply.admin_change_profile_name_or_competencies import admin_change_profile_name_or_competencies


def change_profile_name_or_competencies(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Данные о профиле',
                     reply_markup=admin_change_profile_name_or_competencies())
