from loader import bot
from telebot.types import Message
import sqlite3

from handlers.custom_handlers.admin_choosing_actions_competencies import choosing_actions_competencies
from keyboards.reply.admin_create_competencies import admin_create_competencies

from handlers.custom_handlers.role import admin_command

conn = sqlite3.connect('database/database.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(competencies_id: int, competencies_name: str, competencies_text: str):
    cursor.execute('INSERT INTO competencies (competencies_id, competencies_name, competencies_text) VALUES (?, ?, ?)',
                   (competencies_id, competencies_name, competencies_text))
    conn.commit()


@admin_command
def add_competencies(message: Message):
    msg = bot.send_message(chat_id=message.from_user.id,
                           text=f'1. Ввод названия компетенции',
                           reply_markup=admin_create_competencies())
    bot.register_next_step_handler(msg, add_competencies_description)


def add_competencies_description(message: Message):
    global competencies_name
    competencies_name = message.text
    msg = bot.send_message(chat_id=message.from_user.id,
                           text=f'2. Ввод ее описания')
    bot.register_next_step_handler(msg, add_competencies_successfully)


def add_competencies_successfully(message: Message):
    db_table_val(message.id, competencies_name, message.text)
    bot.send_message(chat_id=message.from_user.id,
                     text=f'Информация про успешное создание компетенции')
    choosing_actions_competencies(message)
