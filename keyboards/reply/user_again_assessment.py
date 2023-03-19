from telebot.types import KeyboardButton
from telebot import types


def user_again_assessment():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Заново оценить компетенцию'))
    return keyboard
