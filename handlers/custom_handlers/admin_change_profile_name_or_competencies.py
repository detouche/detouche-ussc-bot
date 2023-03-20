from keyboards.reply.admin_change_profile_name_or_competencies import admin_change_profile_name_or_competencies
from loader import bot
from telebot.types import Message


def change_profile_name_or_competencies(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Данные о профиле',
                     reply_markup=admin_change_profile_name_or_competencies())
