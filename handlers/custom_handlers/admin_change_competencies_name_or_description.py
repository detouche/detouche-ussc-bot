from loader import bot
from telebot.types import Message

from keyboards.reply.admin_change_competencies_name_or_description import admin_change_competencies_name_or_description

from handlers.custom_handlers.role import admin_command


@admin_command
def change_competencies_name_or_description(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Данные о компетенции',
                     reply_markup=admin_change_competencies_name_or_description())
