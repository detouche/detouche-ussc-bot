from telebot.types import KeyboardButton
from telebot import types


def admin_successful_creation():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Завершить сессию'))
    return keyboard
