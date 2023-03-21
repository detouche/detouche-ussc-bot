from loader import bot
from telebot.types import Message

from keyboards.reply.admin_choosing_actions_competencies import admin_choosing_actions_competencies


def choosing_actions_competencies(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Список всех имеющихся компетенций',
                     reply_markup=admin_choosing_actions_competencies())
