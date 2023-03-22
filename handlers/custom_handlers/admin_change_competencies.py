from loader import bot
from telebot.types import Message

from keyboards.reply.admin_change_competencies import admin_change_competencies

from handlers.custom_handlers.role import admin_command


@admin_command
def change_competencies(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Выбор нужной компетенции',
                     reply_markup=admin_change_competencies())

