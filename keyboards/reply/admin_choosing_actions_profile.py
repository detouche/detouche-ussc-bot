from telebot.types import KeyboardButton
from telebot import types


def admin_choosing_actions_profile():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Удаление профиля'),
                 KeyboardButton('Создать профиль'),
                 KeyboardButton('Редактировать профили'),
                 KeyboardButton('Назад в главное меню'))
    return keyboard
