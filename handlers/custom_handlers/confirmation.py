from keyboards.reply.confirmation import confirmation
from handlers.custom_handlers.user_finish import finish
from handlers.custom_handlers.user_again_assessment import assessment_again
from loader import bot
from telebot.types import Message


def confirmation_accept(message: Message) -> None:
    if message.text == 'Завершить проверку':
        message = bot.send_message(message.from_user.id, f'Вы уверены?', reply_markup=confirmation())
        bot.register_next_step_handler(message, finish)
    elif message.text == 'Заново оценить компетенцию':
        message = bot.send_message(message.from_user.id, f'Вы уверены?', reply_markup=confirmation())
        bot.register_next_step_handler(message, assessment_again)
