from loader import bot
from telebot.types import Message
from handlers.custom_handlers.user_connection import user_start
from handlers.custom_handlers.admin_connection import admin_start
from handlers.custom_handlers.user_start_evaluation import user_start_evaluation_info
from handlers.custom_handlers.user_assessment import user_assessment_process
from handlers.custom_handlers.user_last_assessment import assessment_last
from handlers.custom_handlers.user_end_assessment import assessment_end
from handlers.custom_handlers.user_finish import finish
from handlers.custom_handlers.user_change_assessment import change_assessment
from handlers.custom_handlers.user_again_assessment import assessment_again


@bot.message_handler(content_types=['text'])
def text_recognizer(message: Message) -> None:
    if message.text == "Я пользователь":
        user_start(message)
    elif message.text == "Я админстратор":
        admin_start(message)
    elif message.text == "Начать сессию":
        user_start_evaluation_info(message)
    elif message.text == "Начать оценку":
        user_assessment_process(message)
    elif message.text == "Оценить компетенцию":
        assessment_last(message)
    elif message.text == "Оценить последнюю компетенцию":
        assessment_end(message)
    elif message.text == "Завершить проверку":
        finish(message)
    elif message.text == "Изменить оценку":
        change_assessment(message)
    elif message.text == "Заново оценить компетенцию":
        assessment_again(message)
