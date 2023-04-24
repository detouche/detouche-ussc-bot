from loader import rt
from aiogram import types, F
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, BufferedInputFile
from jinja2 import Environment, FileSystemLoader
import pdfkit
import io

from keyboards.reply.admin_delete_competencies import admin_delete_competencies
from keyboards.reply.admin_choosing_actions_competencies import admin_choosing_actions_competencies

from handlers.custom_handlers.role import admin_command

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
    await start7(bot, message)


@rt.message(Competence.delete)
async def delete_competence_handler(message: types.Message, state: FSMContext):
    if delete_competence(message.text):
        await message.answer(text="Компетенция успешно удалена",
                             reply_markup=admin_choosing_actions_competencies)
    else:

        await message.answer(text='Такого ID компетенции не существует!',
                             reply_markup=admin_choosing_actions_competencies)
    await state.clear()


async def start7(bot, message):
    c = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template(r"html/competencies-list/index.html")
    data_list = get_competencies_list()
    competencies_id = (list(map(lambda x: x[0], data_list)))

    competencies_name = (list(map(lambda x: x[1], data_list)))
    pdf_template = template.render(
        {'competencies_id': f'{competencies_id}',
         'competencies_name': f'{competencies_name}',
         })
    options = {"enable-local-file-access": ""}
    print(pdf_template)
    flike = io.BytesIO(pdfkit.from_string(pdf_template, False, configuration=c, options=options))
    test = BufferedInputFile(flike, filename="file.html")
    # text = FSInputFile(path=pdf_template, filename='ky')
    # test = FSInputFile(path=r"C:\Users\10\PycharmProjects\detouche-ussc-bot\html\competencies-list\index.html",
    #                    filename="123.html")

    await bot.send_document(message.chat.id, ('card.pdf', flike))
