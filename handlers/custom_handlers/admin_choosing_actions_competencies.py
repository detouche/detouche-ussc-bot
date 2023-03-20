from keyboards.reply.admin_choosing_actions_competencies import admin_choosing_actions_competencies
from loader import bot
from telebot.types import Message


def choosing_actions_competencies(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Список всех имеющихся компетенций',
                     reply_markup=admin_choosing_actions_competencies())
