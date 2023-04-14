from aiogram.fsm.context import FSMContext
from loader import rt
from aiogram import types
from aiogram.filters import Command

from handlers.custom_handlers.user_connection import user_start

from handlers.custom_handlers.admin_connection import admin_start

from handlers.custom_handlers.main_admin_connection import main_admin_start

# Никита - 755950556
# Миша - 642205779
# Лёша - 6290014843
# Антон - 476994720
# Игорь - 372233735

ADMINS = [6290014843, 755950556, 372233735, 476994720]

MAIN_ADMINS = [642205779]


@rt.message(Command("start"))
async def role(message: types.Message, state: FSMContext):
    await message.answer(text=f'Твой ID: {message.from_user.id}')

    customer_id = message.from_user.id
    if customer_id in ADMINS:
        await admin_start(message)
    elif customer_id in MAIN_ADMINS:
        await main_admin_start(message)
    else:
        await state.clear()
        await user_start(message, state)


async def admin_command(func):
    def wrapped(message, *args, **kwargs):
        customer_id = message.from_user.id
        if customer_id not in ADMINS:
            message.answer(text=f'Нет прав',
                           reply_markup=types.ReplyKeyboardRemove())
            return
        return func(message, *args, **kwargs)
    return wrapped


def user_command(func):
    def wrapped(message, *args, **kwargs):
        customer_id = message.from_user.id
        if customer_id in ADMINS:
            message.answer(text=f'Нет прав',
                           reply_markup=types.ReplyKeyboardRemove())
            return
        return func(message, *args, **kwargs)
    return wrapped
