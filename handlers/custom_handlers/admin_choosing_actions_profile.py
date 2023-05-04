from aiogram.types import BufferedInputFile
from loader import rt
from aiogram import types, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from jinja2 import Environment, FileSystemLoader
import pdfkit
import io

from database.connection_db import get_profile_list, get_profile_competencies, get_competence_title, \
    get_competencies_list

from keyboards.reply.admin_choosing_actions_profile import admin_choosing_actions_profile
from keyboards.reply.admin_delete_profile import admin_delete_profile

from states.profiles import Profile

WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'


@rt.message(Text('Профили'))
@rt.message(Text('Назад в меню профилей'))
async def choosing_actions_profile(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f'Вы вошли в меню "Профили"',
                         reply_markup=admin_choosing_actions_profile)


@rt.message(Text('Список профилей'))
async def profile_list(message: types.Message, state: FSMContext, bot):
    data_profile_list = get_profile_list()
    data_profile_list = '\n'.join(list(map(lambda x: f'ID: {x[0]} Name: {x[1]}', data_profile_list)))
    await state.set_state(Profile.check_competencies)
    await message.answer(text=f'Введите ID профиля для просмотра входящих компетенций. \n'
                              f'Список всех имеющихся профилей:\n{data_profile_list}',
                         reply_markup=admin_delete_profile)
    await creating_pdf(bot, message)



@rt.message(Profile.check_competencies)
async def get_competencies_in_profile(message: types.Message, state: FSMContext):
    comp_list = get_profile_competencies(message.text.lower())
    comp_list = list(map(get_competence_title, comp_list))
    if comp_list:
        title = '\n'.join(list(map(lambda x: f'Компетенция: {x[0]}', comp_list)))
        await message.answer(text=f'Компетенции входящие в профиль\n'
                                  f'{title}',
                             reply_markup=admin_delete_profile)
    else:
        await message.answer(text='В профиле нет компетенций или он не существует. \n'
                                  'Повторите ввод ID')


async def creating_pdf(bot: Bot, message: types.Message):
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template(r"html/profile-list/index.html")

    data_profile_list = get_profile_list()
    profile_id = (list(map(lambda x: x[0], data_profile_list)))
    profile_competencies = []
    for i in range(len(profile_id)):
        profile_competencies.append(get_profile_competencies(profile_id[i]))
    profile_name = (list(map(lambda x: x[1], data_profile_list)))
    number_repetitions_profile = len(profile_id)

    competencies_list = get_competencies_list()
    pdf_template = template.render(
        {
            'profile_competencies': profile_competencies,
            'competencies_list': dict(competencies_list),
            'number_repetitions_profile': number_repetitions_profile,
            'profile_id': profile_id,
            'profile_name': profile_name,
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
    pdf_file = BufferedInputFile(flike, filename="Список профилей.pdf")
    await bot.send_document(message.chat.id, pdf_file)
