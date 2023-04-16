from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from states.main_admin_add_admin import AdminAction


def get_keyboard_with_users(users_list: list):
    buttons = []
    for i in range(len(users_list)):
        button = [InlineKeyboardButton(text=f"{users_list[i][1]}",
                                       callback_data=AdminAction(action="add",
                                                                 user_id=users_list[i][0],
                                                                 user_name=users_list[i][1]).pack())]
        buttons.append(button)
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
