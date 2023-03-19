from keyboards.reply.role import get_role
from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['role'])
def role(message: Message) -> None:
    bot.send_message(message.from_user.id,
                     f'Привет, {message.from_user.username}. Выбери роль',
                     reply_markup=get_role())

