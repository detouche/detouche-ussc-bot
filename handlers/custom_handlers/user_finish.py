from telebot import types
from loader import bot
from telebot.types import Message

from handlers.custom_handlers.user_end_assessment import assessment_end

from handlers.custom_handlers.role import user_command


@user_command
def finish(message: Message) -> None:
    if message.text == 'Да':
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Спасибо, до свидания',
                         reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'Нет':
        assessment_end(message)
