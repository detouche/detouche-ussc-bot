from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands


@bot.message_handler(commands=['start'])
def say_hy(message):
    bot.send_message(message.from_user.id, "Привет! Я твой бот-помощник!")


if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
