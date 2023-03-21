from telebot.types import KeyboardButton
from telebot import types


def admin_connection():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Компетенции'),
                 KeyboardButton('Создать сессию'),
                 KeyboardButton('Профили'))
    return keyboard
