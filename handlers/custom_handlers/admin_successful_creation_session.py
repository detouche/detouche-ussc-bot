from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile
from aiogram.utils.deep_linking import create_start_link

from loader import rt
from random import randint
import base64
import qrcode
import io

from keyboards.reply.admin_successful_creation import admin_successful_creation

from database.connection_db import get_profile_competencies, get_competence_title, create_session, get_session_info

from states.admin_session import AdminSession


@rt.message(AdminSession.profile_number)
async def successful_creation(message: Message, state: FSMContext, bot: Bot):
    profile_list = get_profile_competencies(message.text.lower())
    profile_list = list(map(get_competence_title, profile_list))
    if profile_list:
        profile_number = message.text.lower()
        connection_code = randint(100000, 999999)
        data = await state.get_data()
        candidate_name = data['candidate_name']
        await state.clear()
        connections_code = get_session_info(3)
        while connection_code in connections_code:
            connection_code = randint(100000, 999999)
        create_session(candidate_name, profile_number, connection_code, message.from_user.id)
        session_link = await create_start_link(bot=bot, payload=str(connection_code))
        qr = qrcode.make(session_link)
        img_byte_arr = io.BytesIO()
        qr.save(img_byte_arr, 'PNG')
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('ascii')
        img_bytes = base64.b64decode(img_base64)
        qr = io.BytesIO(img_bytes)
        pdf_file = BufferedInputFile(qr.getvalue(), filename="QRCode")
        await message.answer(text=f'Сессия успешно создана.\n'
                                  f'Код для присоединения к сессии: {connection_code}.\n'
                                  f'{session_link}',
                             reply_markup=admin_successful_creation)
        await bot.send_photo(message.chat.id, photo=pdf_file)
        await state.clear()
    else:
        await message.answer(text='Такого профиля не существует.\n Выберите, пожалуйста, другой')
