from aiogram.fsm.context import FSMContext
from loader import rt
from aiogram import types
from aiogram.filters import Command

from handlers.custom_handlers.user_connection import user_start

from handlers.custom_handlers.admin_connection import admin_start

from handlers.custom_handlers.main_admin_connection import main_admin_start

from database.connection_db import get_admins_list

# Никита - 755950556
# Миша - 642205779
# Лёша - 6290014843
# Антон - 476994720
# Игорь - 372233735


MAIN_ADMINS = [642205779]


@rt.message(Command("start"))
async def role(message: types.Message, state: FSMContext):
    await message.answer(text=f'Ваш ID: {message.from_user.id}')

    customer_id = message.from_user.id
    if customer_id in get_admins_list(0):
        await admin_start(message)
    elif customer_id in MAIN_ADMINS:
        await main_admin_start(message)
    else:
        await state.clear()
        await user_start(message, state)


async def admin_command(func):
    def wrapped(message, *args, **kwargs):
        customer_id = message.from_user.id
        if customer_id not in get_admins_list(0):
            message.answer(text=f'Нет прав',
                           reply_markup=types.ReplyKeyboardRemove())
            return
        return func(message, *args, **kwargs)
    return wrapped


def user_command(func):
    def wrapped(message, *args, **kwargs):
        customer_id = message.from_user.id
        if customer_id in get_admins_list(0):
            message.answer(text=f'Нет прав',
                           reply_markup=types.ReplyKeyboardRemove())
            return
        return func(message, *args, **kwargs)
    return wrapped


async def main_admin_command(func):
    def wrapped(message, *args, **kwargs):
        customer_id = message.from_user.id
        if customer_id not in MAIN_ADMINS:
            message.answer(text=f'Нет прав',
                           reply_markup=types.ReplyKeyboardRemove())
            return
        return func(message, *args, **kwargs)
    return wrapped
