from aiogram.types import Message, CallbackQuery
from aiogram.types import BufferedInputFile
from aiogram import types, Bot
from handlers.custom_handlers.admin_create_session import create_session
from loader import rt
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from jinja2 import Environment, FileSystemLoader
import pdfkit
import io
import imgkit

from handlers.custom_handlers.role import admin_command, role

from database.connection_db import delete_session, get_session_code_admin, get_id_evaluating, get_comp_names, \
    get_assessments_competencies, get_candidate_name, get_profile_name_session, get_user_name_for_id, get_user_grades, \
    get_admins_list

from keyboards.inline.confirmation_delete_session import get_keyboard_confirmation_del

WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'


# @admin_command
@rt.message(Text('Завершить сессию'))
async def end_session(message: Message, state: FSMContext):
    if message.chat.id in get_admins_list(0):
        await message.answer(text=f'Вы уверены?',
                             reply_markup=get_keyboard_confirmation_del())
    else:
        await message.answer(text=f'Вы не являетесь администратором')
        await role(message, state)


@rt.callback_query(Text('confirmat_del_session'))
async def confirmat_del_session(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await callback.message.answer(text=f'Сессия закончена.\n Пожалуйста, дождитесь генерации результатов')
    admin_id = callback.message.chat.id
    session_code = get_session_code_admin(admin_id)
    comp_names = list(map(lambda x: x[0], get_comp_names(session_code)))
    grade_dicts = {}
    for i in comp_names:
        assessments_competencies = list(map(lambda x: x[0], get_assessments_competencies(i, session_code)))
        if assessments_competencies.count(-1) == len(assessments_competencies):
            grade = 0
        else:
            grade = float((sum(assessments_competencies) + assessments_competencies.count(-1))
                          / (len(assessments_competencies) - assessments_competencies.count(-1)))
        grade_dicts[i] = int(grade * 100)
    candidate_name = get_candidate_name(session_code)
    profile_name = get_profile_name_session(session_code)
    id_evaluating = list(map(lambda x: x[0], get_id_evaluating(session_code)))
    user_grade_info = {}
    for i in id_evaluating:
        evaluating_name = get_user_name_for_id(i)
        user_grades = get_user_grades(i, session_code)
        user_grade_info[evaluating_name] = {}
        for j in user_grades:
            user_grade_info[evaluating_name][j[0]] = j[1]
    await creating_pdf(bot, callback.message, grade_dicts, candidate_name, profile_name, user_grade_info)
    await creating_photo(bot, callback.message, grade_dicts, candidate_name, profile_name)
    delete_session(callback.from_user.id)
    await role(callback.message, state)


@rt.callback_query(Text('cancel_del_session'))
async def cancel_del_session(callback: CallbackQuery, state: FSMContext, bot):
    await callback.message.delete()
    await create_session(callback.message, state)


def value_converter_text(value):
    if value == -1:
        return "Без оценки"
    elif value == 0:
        return "Нет"
    elif value == 0.5:
        return "Частично"
    elif value == 1:
        return "Да"


async def creating_pdf(bot: Bot, message: types.Message, grade_dicts: dict, candidate_name: str, profile_name: str,
                       user_grade_info: dict):
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template(r"html/PDF-Report/index.html")
    pdf_template = template.render(
        {
            'grade_dicts': grade_dicts,
            'candidate_name': candidate_name,
            'profile_name': profile_name,
            'user_grade_info': user_grade_info,
            'value_converter_text': value_converter_text
        })
    options = {'enable-local-file-access': '',
               'margin-top': '0.3in',
               'margin-right': '0in',
               'margin-bottom': '0in',
               'margin-left': '0in',
               'encoding': 'UTF-8',
               'disable-smart-shrinking': '',
               }
    flike = io.BytesIO(pdfkit.from_string(pdf_template, False, configuration=config, options=options)).getvalue()
    pdf_file = BufferedInputFile(flike, filename="PDF-Отчёт.pdf")
    await bot.send_document(message.chat.id, pdf_file)


async def creating_photo(bot: Bot, message: types.Message, grade_dicts: dict, candidate_name: str, profile_name: str):
    config = imgkit.config(wkhtmltoimage=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe')
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template(r"html/Mini-Report/index.html")
    pdf_template = template.render(
        {
            'grade_dicts': grade_dicts,
            'candidate_name': candidate_name,
            'profile_name': profile_name,
        })
    options = {'enable-local-file-access': '',
               }
    flike = io.BytesIO(imgkit.from_string(pdf_template, False, config=config, options=options)).getvalue()
    photo_file = BufferedInputFile(flike, filename="Мини-отчёт.jpg")
    await bot.send_photo(message.chat.id, photo_file)
