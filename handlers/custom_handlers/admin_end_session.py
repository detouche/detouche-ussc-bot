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
    get_assessments_competencies

from keyboards.inline.confirmation_delete_session import get_keyboard_confirmation_del

WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'


# @admin_command
@rt.message(Text('Завершить сессию'))
async def end_session(message: Message):
    await message.answer(text=f'Вы уверены?',
                         reply_markup=get_keyboard_confirmation_del())


@rt.callback_query(Text('confirmat_del_session'))
async def confirmat_del_session(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()
    await creating_pdf(bot, callback.message)
    delete_session(callback.from_user.id)
    await callback.message.answer(text=f'Сессия закончена.')
    await role(callback.message, state)


@rt.callback_query(Text('cancel_del_session'))
async def cancel_del_session(callback: CallbackQuery, state: FSMContext, bot):
    admin_id = callback.message.chat.id
    session_code = get_session_code_admin(admin_id)
    id_evaluating = get_id_evaluating(session_code)
    print(id_evaluating)
    comp_names = get_comp_names(session_code)
    print(comp_names)
    dicts = []
    for i in comp_names:
        print(i)
        print(i[0])
        assessments_competencies = get_assessments_competencies(i[0], session_code)
        print(assessments_competencies)
        # dicts.append(i[0], assessments_competencies[0])
    await creating_pdf(bot, callback.message)
    await creating_photo(bot, callback.message)
    await callback.message.delete()
    await create_session(callback.message, state)


async def creating_pdf(bot: Bot, message: types.Message):
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template(r"html/PDF-Report/index.html")
    pdf_template = template.render(
        {
            # 'number_repetitions': number_repetitions,
            # 'competencies_id': competencies_id,
            # 'competencies_name': competencies_name,
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


async def creating_photo(bot: Bot, message: types.Message):
    config = imgkit.config(wkhtmltoimage=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe')
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template(r"html/Mini-Report/index.html")
    pdf_template = template.render(
        {
            # 'number_repetitions': number_repetitions,
            # 'competencies_id': competencies_id,
            # 'competencies_name': competencies_name,
        })
    options = {'enable-local-file-access': '',
               }
    flike = io.BytesIO(imgkit.from_string(pdf_template, False, config=config, options=options)).getvalue()
    photo_file = BufferedInputFile(flike, filename="Мини-отчёт.jpg")
    await bot.send_photo(message.chat.id, photo_file)
