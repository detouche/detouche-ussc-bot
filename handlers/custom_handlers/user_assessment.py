from loader import bot
from telebot.types import Message

from keyboards.reply.user_assessment import user_assessment

from handlers.custom_handlers.role import user_command


@user_command
def user_assessment_process(message: Message) -> None:
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Показ компетенции и ее описание',
                     reply_markup=user_assessment())
