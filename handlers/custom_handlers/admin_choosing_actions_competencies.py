from loader import rt
from aiogram import types, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from jinja2 import Environment, FileSystemLoader
import pdfkit
import io

from keyboards.reply.admin_choosing_actions_competencies import admin_choosing_actions_competencies
from keyboards.reply.admin_create_competencies import admin_create_competencies

from database.connection_db import get_competencies_list, get_competence_description

from states.competencies import Competence

WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'


@rt.message(Text('Компетенции'))
@rt.message(Text('Назад в меню компетенций'))
async def choosing_actions_competencies(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Вы вошли в меню 'Компетенции'",
                         reply_markup=admin_choosing_actions_competencies)


@rt.message(Text('Список компетенций'))
async def competencies_list(message: types.Message, state: FSMContext, bot: Bot):
    data_list = get_competencies_list()
    comp_list = '\n'.join(list(map(lambda x: f'ID: {x[0]} Name: {x[1]}', data_list)))
    await state.set_state(Competence.check_description)
    await message.answer(text=f'Введите ID компетенции для просмотра ее описания. \n'
                              f'Список всех имеющихся компетенций:\n{comp_list}',
                         reply_markup=admin_create_competencies)
    await creating_pdf(bot, message)


@rt.message(Competence.check_description)
async def check_competence_description(message: types.Message):
    description = get_competence_description(message.text.lower())
    if description:
        desc = ('\n'.join(map(str, description)))
        await message.answer(text=f'{desc}',
                             reply_markup=admin_create_competencies)
    else:
        await message.answer(text='Введите существующий ID')


async def creating_pdf(bot: Bot, message: types.Message):
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template(r"html/competencies-list/index.html")
    data_list = get_competencies_list()
    competencies_id = (list(map(lambda x: x[0], data_list)))
    competencies_name = (list(map(lambda x: x[1], data_list)))
    number_repetitions = len(competencies_name)
    pdf_template = template.render(
        {
            'number_repetitions': number_repetitions,
            'competencies_id': competencies_id,
            'competencies_name': competencies_name,
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
    pdf_file = BufferedInputFile(flike, filename="Список компетенций.pdf")
    await bot.send_document(message.chat.id, pdf_file)
