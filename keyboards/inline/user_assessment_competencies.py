from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from database.connection_db import get_connection_code_session, get_comp_name_session, get_assessment_comp_session, \
    get_id_comp_session

from states.user_assessment_comp import UserAssessment


async def user_assessment_get_keyboard(message: Message):
    current_id = message.chat.id
    connection_code = get_connection_code_session(current_id)[0]
    comp_list_name = get_comp_name_session(connection_code)
    buttons = []
    comp_info = '\n'.join(list(map(lambda x: f'{x[0]}\n'
                                             f'Оценка: {value_converter_text(float(get_assessment_comp_session(str(x[0]), current_id)))}\n',
                                   comp_list_name)))
    await message.answer(text=f'Информация о компетенциях:\n \n{comp_info}')
    for i in range(len(comp_list_name)):
        comp_id = get_id_comp_session(comp_list_name[i][0], current_id)
        button = [InlineKeyboardButton(text=f"{comp_list_name[i][0]}",
                                       callback_data=UserAssessment(action="assessment", comp_id=comp_id).pack())]
        buttons.append(button)
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text='Вы можете оценить следующие компетенции:', reply_markup=keyboard)


def value_converter_text(value):
    if value == -1:
        return "Без оценки"
    elif value == 0:
        return "Нет"
    elif value == 0.5:
        return "Частично"
    elif value == 1:
        return "Да"
