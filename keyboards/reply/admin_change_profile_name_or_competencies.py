from telebot.types import KeyboardButton
from telebot import types


def admin_change_profile_name_or_competencies():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Изменить компетенции профиля'),
                 KeyboardButton('Изменить название профиля'))
    return keyboard
