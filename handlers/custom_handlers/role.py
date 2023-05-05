from aiogram.fsm.context import FSMContext
from loader import rt
from aiogram import types
from aiogram.filters import Command

from handlers.custom_handlers.user_connection import user_start

from handlers.custom_handlers.admin_connection import admin_start

from handlers.custom_handlers.main_admin_connection import main_admin_start

from database.connection_db import get_admins_list

from database.connection_db import get_admins_list

# Никита - 755950556
# Миша - 642205779
# Лёша - 6290014843
# Антон - 476994720
# Игорь - 372233735


MAIN_ADMINS = [642205779, 980964741]


@rt.message(Command("start"))
async def role(message: types.Message, state: FSMContext):
    await message.answer(text=f'Ваш ID: {message.chat.id}')
    customer_id = message.chat.id
    if customer_id in MAIN_ADMINS:
        await admin_start(message)
    elif customer_id in get_admins_list(0):
        await admin_start(message)
    elif customer_id in MAIN_ADMINS:
        await main_admin_start(message)
    else:
        await state.clear()

        if len(message.text.split()) == 1:
            await user_start(message, state)
        else:
            await user_start(message, state, message.text.split()[1])


def admin_command(func):
    async def wrapped(message):
        customer_id = message.chat.id
        if customer_id not in get_admins_list(0) and customer_id not in MAIN_ADMINS:
            await message.answer(text=f'Нет прав',
                                 reply_markup=types.ReplyKeyboardRemove())
            return
        await func(message)

    return wrapped


def user_command(func):
    async def wrapped(message):
        customer_id = message.chat.id
        if customer_id in get_admins_list(0):
            await message.answer(text=f'Нет прав',
                                 reply_markup=types.ReplyKeyboardRemove())
            return
        await func(message)

    return wrapped


def main_admin_command(func):
    async def wrapped(message, state):
        customer_id = message.chat.id
        if customer_id not in MAIN_ADMINS:
            await message.answer(text=f'Нет прав',
                                 reply_markup=types.ReplyKeyboardRemove())
            return
        await func(message, state)

    return wrapped
