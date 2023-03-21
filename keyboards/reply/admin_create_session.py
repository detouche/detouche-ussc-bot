from telebot.types import KeyboardButton
from telebot import types


def admin_create_session():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Профили на выбор'),
                 KeyboardButton('Назад в главное меню'))
    return keyboard

