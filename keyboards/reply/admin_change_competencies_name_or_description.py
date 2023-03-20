from telebot.types import KeyboardButton
from telebot import types


def admin_change_competencies_name_or_description():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Изменить описание компетенции'),
                 KeyboardButton('Изменить название компетенции'))
    return keyboard
