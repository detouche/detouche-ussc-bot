from loader import rt
from aiogram import types, F
from aiogram.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters.callback_data import CallbackData

from database.connection_db import get_user_list, main_admin_add_admin


class AdminAction(CallbackData, prefix="admin"):
    action: str
    user_id: int
    user_name: str


@rt.message(Text('Добавить администратора'))
async def add_admin(message: types.Message):
    users_list = get_user_list()
    await message.answer(text=f'{users_list}',
                         reply_markup=get_keyboard(users_list))


def get_keyboard(users_list: list):
    buttons = []
    for i in range(len(users_list)):
        button = [InlineKeyboardButton(text=f"{users_list[i][1]}",
                                       callback_data=AdminAction(action="yes",
                                                                 user_id=users_list[i][0],
                                                                 user_name=users_list[i][1]).pack())]
        buttons.append(button)
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@rt.callback_query(AdminAction.filter(F.action == 'yes'))
async def callbacks_num(callback: CallbackQuery, callback_data: AdminAction):
    user_name = callback_data.user_name
    user_id = callback_data.user_id
    await callback.message.edit_text(text=f"{user_name} теперь администратор c id {user_id}")
    main_admin_add_admin(user_id, user_name)
