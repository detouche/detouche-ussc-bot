from telebot.types import KeyboardButton
from telebot import types


def get_role():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Я админстратор'),
                 KeyboardButton('Я пользователь'))
    return keyboard

