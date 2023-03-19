from telebot.types import KeyboardButton
from telebot import types


def user_connection():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Начать сессию'))
    return keyboard
