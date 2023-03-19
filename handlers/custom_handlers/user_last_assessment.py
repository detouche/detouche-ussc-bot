from keyboards.reply.user_last_assessment import user_last_assessment
from loader import bot
from telebot.types import Message


def assessment_last(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Информация об успешной оценке', reply_markup=user_last_assessment())
