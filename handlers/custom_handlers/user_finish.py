from telebot import types
from loader import bot
from telebot.types import Message
from handlers.custom_handlers.user_end_assessment import assessment_end


def finish(message: Message) -> None:
    if message.text == 'Да':
        bot.send_message(message.from_user.id, f'Спасибо, до свидания', reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'Нет':
        assessment_end(message)
