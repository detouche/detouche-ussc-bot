from telebot.types import KeyboardButton
from telebot import types


def user_end_assessment():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Изменить оценку'), KeyboardButton('Завершить проверку'))
    return keyboard
