from handlers.custom_handlers.admin_choosing_actions_competencies import choosing_actions_competencies
from loader import bot
from telebot.types import Message
from keyboards.reply.admin_delete_competencies import admin_delete_competencies


def delete_competencies(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Выбор нужной компетенции', reply_markup=admin_delete_competencies())


def delete_competencies_number(message: Message) -> None:
    if message.text == 'Да':
        bot.send_message(message.from_user.id, f'Успешное удаление')
        choosing_actions_competencies(message)
    elif message.text == 'Нет':
        delete_competencies(message)
