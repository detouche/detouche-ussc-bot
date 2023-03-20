from telebot.types import KeyboardButton
from telebot import types

# Временная кнопка


def admin_change_competencies():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Выбрать компетенцию'), KeyboardButton('Назад в меню компетенций'))
    return keyboard
