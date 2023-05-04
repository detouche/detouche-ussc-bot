from loader import rt
from aiogram import types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.types import CallbackQuery
from jinja2 import Environment, FileSystemLoader
import pdfkit
import io

from keyboards.reply.admin_delete_competencies import admin_delete_competencies
from keyboards.reply.admin_choosing_actions_competencies import admin_choosing_actions_competencies

from keyboards.inline.confirmation_delete_competence import confirmation_delete_competence

from states.competencies import Competence

from handlers.custom_handlers.admin_choosing_actions_competencies import choosing_actions_competencies

from database.connection_db import delete_competence, get_competencies_list, check_competence_id

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
    await state.update_data(delete=message.text)
    if check_competence_id(message.text):
        await message.answer(text=f"Вы уверены что хотите удалить компетенцию с ID:{message.text} ",
                             reply_markup=confirmation_delete_competence())
    else:

        await message.answer(text='Такого ID компетенции не существует!',
                             reply_markup=admin_choosing_actions_competencies)


@rt.callback_query(Text('delete_competence_true'))
async def delete_competence_true(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    delete_comp = data['delete']
    await callback.message.edit_text(text='Компетенция успешно удалена.')
    delete_competence(delete_comp)
    await state.clear()
    await choosing_actions_competencies(callback.message, state)


@rt.callback_query(Text('delete_competence_false'))
async def delete_competence_false(callback: CallbackQuery, state: FSMContext, bot):
    await delete_competencies(callback.message, state, bot)


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
