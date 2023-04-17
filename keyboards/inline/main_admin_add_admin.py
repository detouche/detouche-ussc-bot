from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import rt
from aiogram import types
from aiogram.filters import Command, Text
from aiogram.fsm.state import StatesGroup, State

from states.main_admin_add_admin import AdminAction


res = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] # будущие элементы вашей инлайн клавы, не надо их импортировать через global, это просто пример списка чтоб компилятор не ругался
PAGE_SIZE = 3


class Menu(StatesGroup):
    step = State()


def get_keyboard_with_users(users_list: list):
    part = users_list
    size = len(part) - 1
    buttons = []
    for i in range(size + 1):
        button = [InlineKeyboardButton(text=f"{users_list[i][1]}",
                                       callback_data=AdminAction(action="add",
                                                                 user_id=users_list[i][0],
                                                                 user_name=users_list[i][1]).pack())]
        buttons.append(button)
    switching_button = [InlineKeyboardButton(text='Назад',
                                             callback_data='back_step'),
                        InlineKeyboardButton(text='Далее',
                                             callback_data='next_step')]
    buttons.append(switching_button)
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def answer_with_menu(message: types.Message, state: FSMContext, menu_page_shift: int):
    global res
    data = await state.get_data()
    current_page_index = data['res']
    new_page_index = current_page_index + menu_page_shift
    if (new_page_index < 0 or new_page_index > len(res)/PAGE_SIZE):
        new_page_index = current_page_index
    data['res'] = new_page_index

    buttons = []
    index = new_page_index * PAGE_SIZE
    for text in res[index:index + PAGE_SIZE]:
        button = InlineKeyboardButton(text=text, callback_data='the_step')
        buttons.append(button)
    switching_button = [InlineKeyboardButton(text='Назад',
                                             callback_data='back_step'),
                        InlineKeyboardButton(text='Далее',
                                             callback_data='next_step')]
    buttons.append(switching_button)
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer('Меню', reply_markup=keyboard)


@rt.message(Command("test"))
async def enter_test(message: types.Message, state: FSMContext):
    await state.set_state(Menu.step)
    await state.update_data(res=0)
    await answer_with_menu(message, state, 0)


@rt.callback_query(Text(startswith="next_step"))
async def next_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await answer_with_menu(callback.message, state, +1)


@rt.callback_query(Text(startswith='back_step'))
async def back_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await answer_with_menu(callback.message, state, -1)