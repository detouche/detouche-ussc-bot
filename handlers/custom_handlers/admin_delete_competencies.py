from loader import rt
from aiogram import types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from jinja2 import Environment, FileSystemLoader
import pdfkit
import io

from keyboards.reply.admin_delete_competencies import admin_delete_competencies
from keyboards.reply.admin_choosing_actions_competencies import admin_choosing_actions_competencies

from states.competencies import Competence

from database.connection_db import delete_competence, get_competencies_list

WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'


@rt.message(Text('Удалить компетенцию'))
async def delete_competencies(message: types.Message, state: FSMContext, bot):
    await state.set_state(Competence.delete)
    data_list = get_competencies_list()
    comp_list = '\n'.join(list(map(lambda x: f'ID: {x[0]} Name: {x[1]}', data_list)))
    await message.answer(text=f'Введите ID компетенции, которую необходимо удалить. \n'
                              f'Список всех имеющихся компетенций: \n{comp_list}',
                         reply_markup=admin_delete_competencies)
    await creating_pdf(bot, message)


@rt.message(Competence.delete)
async def delete_competence_handler(message: types.Message, state: FSMContext):
    if delete_competence(message.text):
        await message.answer(text="Компетенция успешно удалена",
                             reply_markup=admin_choosing_actions_competencies)
    else:

        await message.answer(text='Такого ID компетенции не существует!',
                             reply_markup=admin_choosing_actions_competencies)
    await state.clear()


async def creating_pdf(bot, message):
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
               'margin-top': '0in',
               'margin-right': '0in',
               'margin-bottom': '0in',
               'margin-left': '0in',
               'encoding': 'UTF-8',
               'disable-smart-shrinking': '',
               }
    flike = io.BytesIO(pdfkit.from_string(pdf_template, False, configuration=config, options=options)).getvalue()
    pdf_file = BufferedInputFile(flike, filename="Список компетенций.pdf")
    await bot.send_document(message.chat.id, pdf_file)

