from telebot.types import KeyboardButton
from telebot import types

# Временная кнопка


def admin_delete_competencies():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Выбрать нужную компетенцию'),
                 KeyboardButton('Назад в меню компетенций'))
    return keyboard
