from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from database.connection_db import get_user_list_by_column

from states.main_admin_add_admin import AdminAction

PAGE_SIZE = 10


async def add_admin_get_keyboard(message: Message, state: FSMContext, menu_page_shift: int):
    data = await state.get_data()
    users_name = get_user_list_by_column(1)
    users_id = get_user_list_by_column(0)
    current_page_index = data['current_page_index_add_admin']
    new_page_index = current_page_index + menu_page_shift
    if new_page_index < 0 or new_page_index >= len(users_id)/PAGE_SIZE:
        new_page_index = current_page_index
    await state.update_data(current_page_index_add_admin=new_page_index)
    buttons = []
    index = new_page_index * PAGE_SIZE
    for i in range(len(users_name[index:index+PAGE_SIZE])):
        button = [InlineKeyboardButton(text=f"{users_name[i+index]}",
                                       callback_data=AdminAction(action="add",
                                                                 user_id=users_id[i+index]).pack())]
        buttons.append(button)
    switching_button = [InlineKeyboardButton(text='Назад',
                                             callback_data='back_step_add_admin'),
                        InlineKeyboardButton(text='Далее',
                                             callback_data='next_step_add_admin')]
    buttons.append(switching_button)
    stop_button = [InlineKeyboardButton(text='Закончить добавление',
                                        callback_data='stop_add_admin')]
    buttons.append(stop_button)
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    if menu_page_shift == 0:
        await message.answer(text='Вы можете сделать администратором следующих пользователей:',
                             reply_markup=keyboard)
    else:
        try:
            await message.edit_text(text='Вы можете сделать администратором следующих пользователей:',
                                    reply_markup=keyboard)
        except TelegramBadRequest:
            pass
