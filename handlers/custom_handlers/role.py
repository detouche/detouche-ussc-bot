from loader import bot
from telebot.types import Message

from keyboards.reply.role import get_role


@bot.message_handler(commands=['role'])
def role(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Привет, {message.from_user.username}. Выбери роль',
                     reply_markup=get_role())
