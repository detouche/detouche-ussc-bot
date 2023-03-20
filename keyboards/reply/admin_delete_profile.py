from telebot.types import KeyboardButton
from telebot import types

# Временная кнопка


def admin_delete_profile():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Выбрать нужный профиль'), KeyboardButton('Назад в меню профилей'))
    return keyboard
