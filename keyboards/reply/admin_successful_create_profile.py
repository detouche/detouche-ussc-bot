from telebot.types import KeyboardButton
from telebot import types


def admin_successful_create_profile():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Завершить добавление компетенций'))
    return keyboard
