from handlers.custom_handlers.admin_delete_competencies import delete_competencies_number
from handlers.custom_handlers.admin_delete_profile import delete_profile_number
from handlers.custom_handlers.admin_end_session import end_session
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
    elif message.text == 'Завершить сессию':
        message = bot.send_message(message.from_user.id, f'Вы уверены?', reply_markup=confirmation())
        bot.register_next_step_handler(message, end_session)
    elif message.text == 'Выбрать нужную компетенцию':
        message = bot.send_message(message.from_user.id, f'Вы уверены?', reply_markup=confirmation())
        bot.register_next_step_handler(message, delete_competencies_number)
    elif message.text == 'Выбрать нужный профиль':
        message = bot.send_message(message.from_user.id, f'Вы уверены?', reply_markup=confirmation())
        bot.register_next_step_handler(message, delete_profile_number)
