from telebot.types import KeyboardButton
from telebot import types


def user_start_evaluation():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Начать оценку'))
    return keyboard
