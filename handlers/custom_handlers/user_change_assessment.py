from keyboards.reply.user_change_assessment import user_change_assessment
from loader import bot
from telebot.types import Message


def change_assessment(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Список компетенций', reply_markup=user_change_assessment())
