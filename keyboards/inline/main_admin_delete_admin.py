from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from database.connection_db import get_admins_list_by_column

from states.main_admin_delete_admin import AdminAction

PAGE_SIZE = 10


async def delete_admin_get_keyboard(message: Message, state: FSMContext, menu_page_shift: int):
    data = await state.get_data()
    admins_name = get_admins_list_by_column(1)
    admins_id = get_admins_list_by_column(0)
    current_page_index = data['current_page_index_delete_admin']
    new_page_index = current_page_index + menu_page_shift
    if new_page_index < 0 or new_page_index >= len(admins_id)/PAGE_SIZE:
        new_page_index = current_page_index
    await state.update_data(current_page_index_delete_admin=new_page_index)
    buttons = []
    index = new_page_index * PAGE_SIZE
    for i in range(len(admins_name[index:index+PAGE_SIZE])):
        button = [InlineKeyboardButton(text=f"{admins_name[i+index]}",
                                       callback_data=AdminAction(action="delete",
                                                                 admin_id=admins_id[i+index]).pack())]
        buttons.append(button)
    switching_button = [InlineKeyboardButton(text='Назад',
                                             callback_data='back_step_delete_admin'),
                        InlineKeyboardButton(text='Далее',
                                             callback_data='next_step_delete_admin')]
    stop_button = [InlineKeyboardButton(text='Закончить удаление',
                                        callback_data='stop_delete_admin')]
    buttons.append(switching_button)
    buttons.append(stop_button)
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    if menu_page_shift == 0:
        await message.answer(text='Вы можете удалить следующих администраторов:',
                             reply_markup=keyboard)
    else:
        try:
            await message.edit_text(text='Вы можете удалить следующих администраторов:',
                                    reply_markup=keyboard)
        except TelegramBadRequest:
            pass
