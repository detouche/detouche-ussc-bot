from telebot.types import KeyboardButton
from telebot import types


def admin_choosing_actions_competencies():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Удалить компетенцию'),
                 KeyboardButton('Изменить компетенцию'),
                 KeyboardButton('Создать компетенцию'),
                 KeyboardButton('Назад в главное меню'))
    return keyboard
