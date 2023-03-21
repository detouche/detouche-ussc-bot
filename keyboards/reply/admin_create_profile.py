from telebot.types import KeyboardButton
from telebot import types


def admin_create_profile():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Назад в меню профилей'))
    return keyboard

