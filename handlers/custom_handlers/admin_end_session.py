from aiogram.types import Message, CallbackQuery
from loader import rt
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram import F

from handlers.custom_handlers.role import admin_command, role

from database.connection_db import delete_session

from states.admin_delete_session import ConfirmationDeleteSession

from keyboards.inline.confirmation_delete_session import get_keyboard_confirmation_del


# @admin_command
@rt.message(Text('Завершить сессию'))
async def end_session(message: Message):
    await message.answer(text=f'Вы уверены?',
                         reply_markup=get_keyboard_confirmation_del())


@rt.callback_query(Text('confirmat_del_session'))
async def confirmat_del_session(callback: CallbackQuery, state: FSMContext, message):
    delete_session(callback.from_user.id)
    await callback.message.answer(text=f'Сессия закончена.')
    print(callback.message)
    await role(message, state)


@rt.callback_query(Text('cancel_del_session'))
async def cancel_del_session(callback: CallbackQuery, state: FSMContext, message):
    await role(message, state)
