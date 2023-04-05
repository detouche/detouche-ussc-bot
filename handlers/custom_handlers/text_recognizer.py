# from loader import bot
# from telebot.types import Message
#
# from handlers.custom_handlers.confirmation import confirmation_accept
#
# from handlers.custom_handlers.user_start_evaluation import user_start_evaluation_info
# from handlers.custom_handlers.user_assessment import user_assessment_process
# from handlers.custom_handlers.user_last_assessment import assessment_last
# from handlers.custom_handlers.user_end_assessment import assessment_end
# from handlers.custom_handlers.user_change_assessment import change_assessment
#
# from handlers.custom_handlers.admin_connection import admin_start
# from handlers.custom_handlers.admin_successful_creation_session import successful_creation
# from handlers.custom_handlers.admin_choosing_actions_competencies import choosing_actions_competencies
# from handlers.custom_handlers.admin_create_competencies import add_competencies
# from handlers.custom_handlers.admin_delete_competencies import delete_competencies
# from handlers.custom_handlers.admin_change_competencies import change_competencies
# from handlers.custom_handlers.admin_change_competencies_name_or_description \
#     import change_competencies_name_or_description
# from handlers.custom_handlers.admin_change_competencies_description import change_competencies_description
# from handlers.custom_handlers.admin_change_competencies_name import change_competencies_name
# from handlers.custom_handlers.admin_choosing_actions_profile import choosing_actions_profile
# from handlers.custom_handlers.admin_create_session import create_session
# from handlers.custom_handlers.admin_change_profile import change_profile
# from handlers.custom_handlers.admin_delete_profile import delete_profile
# from handlers.custom_handlers.admin_change_profile_name_or_competencies import change_profile_name_or_competencies
# from handlers.custom_handlers.admin_change_profile_competencies import change_profile_competencies
# from handlers.custom_handlers.admin_change_profile_name import change_profile_name
# from handlers.custom_handlers.admin_create_profile import add_profile
#
#
# #@bot.message_handler(content_types=['text'])
# def text_recognizer(message: Message) -> None:
#     # user session
#
#     if message.text == "Начать сессию":
#         user_start_evaluation_info(message)
#
#     elif message.text == "Начать оценку":
#         user_assessment_process(message)
#
#     elif message.text == "Оценить компетенцию":
#         assessment_last(message)
#
#     elif message.text == "Оценить последнюю компетенцию":
#         assessment_end(message)
#
#     elif message.text == "Завершить проверку":
#         confirmation_accept(message)
#
#     elif message.text == "Изменить оценку":
#         change_assessment(message)
#
#     elif message.text == "Заново оценить компетенцию":
#         confirmation_accept(message)
#
#     # admin session
#
#     elif message.text == "Создать сессию":
#         create_session(message)
#
#     elif message.text == "Профили на выбор":
#         successful_creation(message)
#
#     elif message.text == "Завершить сессию":
#         confirmation_accept(message)
#
#     # admin competencies
#
#     elif message.text == "Компетенции":
#         choosing_actions_competencies(message)
#
#     # admin create competencies
#
#     elif message.text == "Создать компетенцию":
#         add_competencies(message)
#
#     # admin delete competencies
#
#     elif message.text == "Удалить компетенцию":
#         delete_competencies(message)
#
#     elif message.text == "Выбрать нужную компетенцию":
#         confirmation_accept(message)
#
#     # admin change competencies
#
#     elif message.text == "Изменить компетенцию":
#         change_competencies(message)
#
#     elif message.text == "Выбрать компетенцию":
#         change_competencies_name_or_description(message)
#
#     elif message.text == "Изменить название компетенции":
#         change_competencies_name(message)
#
#     elif message.text == "Изменить описание компетенции":
#         change_competencies_description(message)
#
#     # admin profile
#
#     elif message.text == "Профили":
#         choosing_actions_profile(message)
#
#     # admin create profile
#
#     elif message.text == "Создать профиль":
#         add_profile(message)
#
#     elif message.text == "Завершить добавление компетенций":
#         choosing_actions_profile(message)
#
#     # admin delete profile
#
#     elif message.text == "Удаление профиля":
#         delete_profile(message)
#
#     elif message.text == "Выбрать нужный профиль":
#         confirmation_accept(message)
#
#     # admin change profile
#
#     elif message.text == "Редактировать профили":
#         change_profile(message)
#
#     elif message.text == "Выбрать профиль":
#         change_profile_name_or_competencies(message)
#
#     elif message.text == "Изменить название профиля":
#         change_profile_name(message)
#
#     elif message.text == "Изменить компетенции профиля":
#         change_profile_competencies(message)
#
#     # admin routing menu
#
#     elif message.text == "Назад в главное меню":
#         admin_start(message)
#
#     elif message.text == "Назад в меню компетенций":
#         choosing_actions_competencies(message)
#
#     elif message.text == "Назад в меню профилей":
#         choosing_actions_profile(message)
