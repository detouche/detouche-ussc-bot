import os

from loader import rt
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.connection_db import get_admins_list_by_column

# Никита - 755950556
# Миша - 642205779
# Лёша - 6290014843
# Антон - 476994720
# Игорь - 372233735


# MAIN_ADMINS = [980964741]
MAIN_ADMINS = list(map(int, os.getenv("MAIN_ADMINS").split()))


@rt.message(Command("start"))
async def get_role(message: types.Message, state: FSMContext):
    await message.answer(text=f'Ваш ID: {message.chat.id}')
    customer_id = message.chat.id

    from handlers.custom_handlers.admin_connection import admin_start
    from handlers.custom_handlers.user_connection import user_start

    if customer_id in MAIN_ADMINS:
        await admin_start(message, state)
    elif customer_id in get_admins_list_by_column(0):
        await admin_start(message, state)
    else:
        await state.clear()
        if len(message.text.split()) == 2 and "start" in message.text:
            await user_start(message, state, message.text.split()[1])
        else:
            await user_start(message, state)


def admin_command(func):
    async def wrapped(message, *args, **kwargs):
        customer_id = message.chat.id
        if customer_id not in get_admins_list_by_column(0) and customer_id not in MAIN_ADMINS:
            await message.answer(text=f'Нет прав',
                                 reply_markup=types.ReplyKeyboardRemove())
            return
        await func(message, *args, **kwargs)

    return wrapped


def user_command(func):
    async def wrapped(message, *args, **kwargs):
        customer_id = message.chat.id
        if customer_id in get_admins_list_by_column(0) or customer_id in MAIN_ADMINS:
            await message.answer(text=f'Нет прав',
                                 reply_markup=types.ReplyKeyboardRemove())
            return
        await func(message, *args, **kwargs)

    return wrapped


def main_admin_command(func):
    async def wrapped(message, *args, **kwargs):
        customer_id = message.chat.id
        if customer_id not in MAIN_ADMINS:
            await message.answer(text=f'Нет прав',
                                 reply_markup=types.ReplyKeyboardRemove())
            return
        await func(message, *args, **kwargs)

    return wrapped
