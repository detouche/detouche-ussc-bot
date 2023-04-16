from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from states.main_admin_delete_admin import AdminAction


def get_keyboard_with_admins(admins_id: list, admins_name: list):
    buttons = []
    for i in range(len(admins_id)):
        button = [InlineKeyboardButton(text=f"{admins_name[i]}",
                                       callback_data=AdminAction(action="delete",
                                                                 admin_id=admins_id[i],
                                                                 admin_name=admins_name[i]).pack())]
        buttons.append(button)
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
