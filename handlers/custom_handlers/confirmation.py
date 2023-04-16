from aiogram.types import CallbackQuery
from loader import rt
from aiogram import F

from keyboards.inline.confirmation import get_keyboard_confirmation

from states.confirmation import Confirmation


async def confirmation_accept(callback):
    await callback.message.edit_text(text=f'Вы уверены?',
                                     reply_markup=get_keyboard_confirmation())
    print(callback)


@rt.callback_query(Confirmation.filter(F.action == 'confirmation'))
async def add_admin_call(callback_data: Confirmation, callback: CallbackQuery):
    return callback_data.confirmation_choice
