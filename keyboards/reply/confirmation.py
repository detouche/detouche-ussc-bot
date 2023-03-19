from telebot.types import KeyboardButton
from telebot import types


def confirmation():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Да'),
                 KeyboardButton('Нет'))
    return keyboard

