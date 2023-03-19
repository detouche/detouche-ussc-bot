from telebot.types import KeyboardButton
from telebot import types


def user_last_assessment():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Оценить последнюю компетенцию'))
    return keyboard
