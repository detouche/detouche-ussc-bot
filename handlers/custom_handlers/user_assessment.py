from keyboards.reply.user_assessment import user_assessment
from loader import bot
from telebot.types import Message


def user_assessment_process(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Показ компетенции и ее описание', reply_markup=user_assessment())

